import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# ============================================================
# Configuration
# ============================================================

GRAPHQL_URL = "https://leetcode.com/graphql/"

SOLUTIONS_DIR = Path("solutions")
STATE_FILE = Path("sync_state.json")

LEETCODE_SESSION = os.getenv(
    "LEETCODE_SESSION",
    "",
).strip()

LEETCODE_CSRF_TOKEN = os.getenv(
    "LEETCODE_CSRF_TOKEN",
    "",
).strip()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "",
).strip()


# Historical backfill controls.
# These limits are persisted in sync_state.json, so a workflow that runs
# every 15 minutes still processes only a small daily batch.
MAX_HISTORICAL_PROBLEMS_PER_DAY = 5
MAX_GEMINI_REQUESTS_PER_DAY = 8

# Gemini HTTP 429 can mean a short-term rate/token limit or a daily quota
# exhaustion. Retry transient failures without consuming the daily budget.
GEMINI_MAX_RETRIES = 3
GEMINI_BACKOFF_SECONDS = (5, 15, 30)


# Bump this whenever the historical-backfill algorithm changes in a way
# that requires previously processed problems to be reconciled again.
HISTORICAL_BACKFILL_VERSION = 6

# Keep LeetCode requests gentle rather than hammering the GraphQL endpoint.
LEETCODE_REQUEST_DELAY_SECONDS = 0.35

# Number of submission-history rows requested per page.
SUBMISSION_PAGE_SIZE = 40

# Large fallback window used only when the authenticated solved-problem
# progress endpoint is unavailable.
RECENT_AC_FALLBACK_LIMIT = 2000


class GeminiBackfillPaused(RuntimeError):
    """Raised when historical backfill must wait for a later run/day."""


GEMINI_RUNTIME = {
    "requests_used": 0,
    "blocked": False,
    "last_failure": "",
}


# ============================================================
# Validation
# ============================================================

if not LEETCODE_SESSION or not LEETCODE_CSRF_TOKEN:
    print(
        "❌ Missing LeetCode credentials."
    )
    sys.exit(1)


# ============================================================
# LeetCode HTTP client
# ============================================================

leetcode = requests.Session()

leetcode.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "application/json, text/plain, */*"
        ),
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": "https://leetcode.com/",
        "X-CSRFToken": LEETCODE_CSRF_TOKEN,
    }
)

leetcode.cookies.set(
    "LEETCODE_SESSION",
    LEETCODE_SESSION,
    domain="leetcode.com",
)

leetcode.cookies.set(
    "csrftoken",
    LEETCODE_CSRF_TOKEN,
    domain="leetcode.com",
)


# ============================================================
# GraphQL helper
# ============================================================

def graphql(
    query,
    variables=None,
    operation_name=None,
):
    payload = {
        "query": query,
        "variables": variables or {},
    }

    if operation_name:
        payload["operationName"] = operation_name

    response = leetcode.post(
        GRAPHQL_URL,
        json=payload,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"LeetCode GraphQL HTTP "
            f"{response.status_code}: "
            f"{response.text[:500]}"
        )

    body = response.json()

    if body.get("errors"):
        raise RuntimeError(
            json.dumps(
                body["errors"],
                ensure_ascii=False,
            )
        )

    return body.get("data") or {}


# ============================================================
# LeetCode queries
# ============================================================

USER_STATUS_QUERY = """
query globalData {
    userStatus {
        username
        isSignedIn
    }
}
"""


RECENT_ACCEPTED_QUERY = """
query recentAcSubmissions(
    $username: String!,
    $limit: Int!
) {
    recentAcSubmissionList(
        username: $username,
        limit: $limit
    ) {
        id
        title
        titleSlug
        timestamp
    }
}
"""


USER_PROGRESS_QUESTIONS_QUERY = """
query userProgressQuestionList(
    $filters: UserProgressQuestionListInput
) {
    userProgressQuestionList(
        filters: $filters
    ) {
        totalNum
        questions {
            frontendId
            title
            titleSlug
            difficulty
            lastSubmittedAt
            topicTags {
                name
                slug
            }
        }
    }
}
"""


QUESTION_SUBMISSION_LIST_QUERY = """
query questionSubmissionList(
    $offset: Int!,
    $limit: Int!,
    $lastKey: String,
    $questionSlug: String!,
    $status: Int,
    $lang: Int
) {
    questionSubmissionList(
        offset: $offset,
        limit: $limit,
        lastKey: $lastKey,
        questionSlug: $questionSlug,
        status: $status,
        lang: $lang
    ) {
        lastKey
        hasNext
        submissions {
            id
            titleSlug
            status
            statusDisplay
            lang
            runtime
            timestamp
            memory
            isPending
        }
    }
}
"""


SUBMISSION_DETAILS_QUERY = """
query submissionDetails(
    $submissionId: Int!
) {
    submissionDetails(
        submissionId: $submissionId
    ) {
        code
        lang {
            name
        }
        runtime
        runtimeDisplay
        memory
        memoryDisplay
        statusDisplay
    }
}
"""


QUESTION_QUERY = """
query questionData(
    $titleSlug: String!
) {
    question(
        titleSlug: $titleSlug
    ) {
        questionFrontendId
        questionId
        title
        titleSlug
        content
        difficulty
        topicTags {
            name
            slug
        }
    }
}
"""


# ============================================================
# State
# ============================================================

def default_historical_state():
    return {
        "version": HISTORICAL_BACKFILL_VERSION,
        "complete": False,
        "problems": [],
        "problem_index": 0,
        "processed_submission_ids": [],
        "day": "",
        "problems_completed_today": 0,
        "gemini_requests_used_today": 0,
        "gemini_blocked_today": False,
        # Problems with accepted submissions detected after their historical
        # pass. They are reconciled as whole problems later, not imported
        # one submission at a time, so semantic deduplication stays correct.
        "pending_new_problems": [],
    }


def load_state():
    """Load state while remaining compatible with the previous format."""
    default = {
        "processed_submission_ids": [],
        "historical_backfill": default_historical_state(),
    }

    if not STATE_FILE.exists():
        return default

    try:
        data = json.loads(
            STATE_FILE.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):
            return default

        processed_ids = data.get(
            "processed_submission_ids",
            [],
        )
        if not isinstance(processed_ids, list):
            processed_ids = []

        historical = data.get(
            "historical_backfill",
            {},
        )
        if not isinstance(historical, dict):
            historical = {}

        merged_historical = default_historical_state()
        merged_historical.update(historical)

        if not isinstance(
            merged_historical.get("problems"),
            list,
        ):
            merged_historical["problems"] = []

        if not isinstance(
            merged_historical.get("processed_submission_ids"),
            list,
        ):
            merged_historical["processed_submission_ids"] = []

        merged_historical["processed_submission_ids"] = [
            str(x)
            for x in merged_historical["processed_submission_ids"]
        ]

        return {
            "processed_submission_ids": [
                str(x)
                for x in processed_ids
            ],
            "historical_backfill": merged_historical,
        }

    except Exception:
        return default


def save_state(state):
    STATE_FILE.write_text(
        json.dumps(
            state,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def reset_daily_historical_budgets(state):
    """
    Reset daily counters using Google's Gemini quota calendar day.

    Gemini documents Requests Per Day (RPD) resets at midnight Pacific Time,
    not UTC. Persisting the Pacific date keeps the local safety budget aligned
    with the API's actual daily quota window.
    """
    historical = state["historical_backfill"]

    try:
        from datetime import datetime
        from zoneinfo import ZoneInfo

        day_key = datetime.now(
            ZoneInfo("America/Los_Angeles")
        ).strftime("%Y-%m-%d")
    except Exception:
        day_key = time.strftime(
            "%Y-%m-%d",
            time.gmtime(),
        )

    if historical.get("day") != day_key:
        historical["day"] = day_key
        historical["problems_completed_today"] = 0
        historical["gemini_requests_used_today"] = 0
        historical["gemini_blocked_today"] = False

    GEMINI_RUNTIME["requests_used"] = int(
        historical.get(
            "gemini_requests_used_today",
            0,
        )
        or 0
    )

    GEMINI_RUNTIME["blocked"] = bool(
        historical.get(
            "gemini_blocked_today",
            False,
        )
    )

    GEMINI_RUNTIME["last_failure"] = ""


def sync_runtime_to_state(state):
    """Persist Gemini's daily counters in sync_state.json."""
    state["historical_backfill"][
        "gemini_requests_used_today"
    ] = GEMINI_RUNTIME["requests_used"]

    state["historical_backfill"][
        "gemini_blocked_today"
    ] = GEMINI_RUNTIME["blocked"]

# ============================================================
# LeetCode API functions
# ============================================================

def get_username():
    data = graphql(
        USER_STATUS_QUERY,
        operation_name="globalData",
    )

    user = data.get(
        "userStatus"
    ) or {}

    if not user.get(
        "isSignedIn"
    ):
        raise RuntimeError(
            "LeetCode authentication failed. "
            "Your session may have expired."
        )

    username = user.get(
        "username"
    )

    if not username:
        raise RuntimeError(
            "Could not determine LeetCode username."
        )

    return username


def get_recent_accepted(
    username,
    limit=RECENT_AC_FALLBACK_LIMIT,
):
    data = graphql(
        RECENT_ACCEPTED_QUERY,
        {
            "username": username,
            "limit": limit,
        },
        operation_name="recentAcSubmissions",
    )

    return (
        data.get(
            "recentAcSubmissionList"
        )
        or []
    )


def get_all_solved_problems():
    """
    Discover every solved problem available from the authenticated
    LeetCode progress endpoint.
    """
    all_questions = []
    skip = 0
    page_size = 1000

    while True:
        data = graphql(
            USER_PROGRESS_QUESTIONS_QUERY,
            {
                "filters": {
                    "questionStatus": "SOLVED",
                    "skip": skip,
                    "limit": page_size,
                }
            },
            operation_name="userProgressQuestionList",
        )

        result = data.get(
            "userProgressQuestionList"
        ) or {}

        questions = result.get(
            "questions"
        ) or []

        all_questions.extend(
            questions
        )

        total = int(
            result.get(
                "totalNum",
                len(all_questions),
            )
            or len(all_questions)
        )

        if (
            not questions
            or len(all_questions) >= total
        ):
            break

        skip += len(questions)

        if len(questions) < page_size:
            break

        time.sleep(
            LEETCODE_REQUEST_DELAY_SECONDS
        )

    by_slug = {}

    for question in all_questions:
        slug = str(
            question.get(
                "titleSlug",
                "",
            )
        ).strip()

        if slug:
            by_slug[slug] = question

    questions = list(
        by_slug.values()
    )

    # Oldest last-touched problem first gives a stable backfill order.
    questions.sort(
        key=lambda question: (
            str(
                question.get(
                    "lastSubmittedAt",
                    "",
                )
            ),
            int(
                question.get(
                    "frontendId",
                    0,
                )
                or 0
            ),
            str(
                question.get(
                    "titleSlug",
                    "",
                )
            ),
        )
    )

    return questions


def discover_solved_problems(username):
    """
    Prefer the authenticated solved-problem list. Fall back to recent AC
    submissions if that endpoint is unavailable.
    """
    try:
        questions = get_all_solved_problems()

        if questions:
            print(
                f"📚 Discovered {len(questions)} solved problem(s) "
                "from LeetCode progress."
            )
            return questions

    except Exception as exc:
        print(
            "⚠️ Could not use LeetCode's solved-problem progress endpoint: "
            f"{exc}"
        )

    recent = get_recent_accepted(
        username,
        limit=RECENT_AC_FALLBACK_LIMIT,
    )

    by_slug = {}

    for submission in recent:
        slug = str(
            submission.get(
                "titleSlug",
                "",
            )
        ).strip()

        if not slug:
            continue

        by_slug[slug] = {
            "frontendId": "",
            "title": submission.get(
                "title",
                slug,
            ),
            "titleSlug": slug,
            "difficulty": "Unknown",
            "lastSubmittedAt": submission.get(
                "timestamp",
                "",
            ),
            "topicTags": [],
        }

    questions = list(
        by_slug.values()
    )

    questions.sort(
        key=lambda question: (
            str(
                question.get(
                    "lastSubmittedAt",
                    "",
                )
            ),
            str(
                question.get(
                    "titleSlug",
                    "",
                )
            ),
        )
    )

    print(
        f"📚 Fallback discovered {len(questions)} problem(s) "
        "from the recent accepted-submission window."
    )
    print(
        "   ⚠️ This fallback may miss problems outside that window."
    )

    return questions


def _fetch_submission_history_page(
    query,
    operation_name,
    variables,
):
    """Fetch one authenticated submission-history page."""
    data = graphql(
        query,
        variables,
        operation_name=operation_name,
    )

    if operation_name == "questionSubmissionList":
        result = data.get("questionSubmissionList") or {}
    else:
        result = data.get("submissionList") or {}

    return result


def get_all_accepted_submissions_for_problem(
    title_slug,
):
    """
    Fetch the complete accepted-submission history for one problem.

    LeetCode currently exposes submission history through more than one
    GraphQL operation. We use the authenticated questionSubmissionList with
    the explicit Accepted status filter first, then fall back to the older
    submissionList operation if the first operation returns no rows or is
    rejected by the current schema.
    """
    queries = [
        (
            QUESTION_SUBMISSION_LIST_QUERY,
            "questionSubmissionList",
        ),
        (
            """
            query submissionList(
                $offset: Int!,
                $limit: Int!,
                $lastKey: String,
                $questionSlug: String!,
                $status: Int,
                $lang: Int
            ) {
                submissionList(
                    offset: $offset,
                    limit: $limit,
                    lastKey: $lastKey,
                    questionSlug: $questionSlug,
                    status: $status,
                    lang: $lang
                ) {
                    lastKey
                    hasNext
                    submissions {
                        id
                        titleSlug
                        status
                        statusDisplay
                        lang
                        runtime
                        timestamp
                        memory
                        isPending
                    }
                }
            }
            """,
            "submissionList",
        ),
    ]

    all_accepted = []

    for query, operation_name in queries:
        try:
            accepted, success = _walk_submission_history(
                query,
                operation_name,
                title_slug,
            )

            if success:
                return accepted

        except Exception as exc:
            print(
                f"   ⚠️ {operation_name} history lookup failed: {exc}"
            )

    raise RuntimeError(
        f"LeetCode returned no usable submission history for {title_slug}. "
        "The problem was NOT marked complete."
    )


def _walk_submission_history(
    query,
    operation_name,
    title_slug,
):
    """
    Walk every page of a submission-history endpoint.

    The explicit status=10 filter asks LeetCode for Accepted submissions,
    reducing unnecessary rows and making the historical backfill much more
    reliable for solved problems.
    """
    all_accepted = []
    seen_ids = set()

    offset = 0
    last_key = None
    page_number = 0
    saw_usable_response = False

    while True:
        page_number += 1

        result = _fetch_submission_history_page(
            query,
            operation_name,
            {
                "offset": offset,
                "limit": SUBMISSION_PAGE_SIZE,
                "lastKey": last_key,
                "questionSlug": title_slug,
                "status": 10,
                "lang": None,
            },
        )

        if not result:
            return [], False

        saw_usable_response = True

        submissions = result.get("submissions") or []

        if page_number == 1:
            print(
                f"   🔍 {operation_name}: returned "
                f"{len(submissions)} history row(s) on page 1."
            )

            for sample in submissions[:3]:
                print(
                    "   🧪 History sample: "
                    f"id={sample.get('id')} "
                    f"status={sample.get('status')!r} "
                    f"statusDisplay={sample.get('statusDisplay')!r} "
                    f"isPending={sample.get('isPending')!r}"
                )

        new_rows = 0

        for submission in submissions:
            submission_id = str(
                submission.get("id", "")
            ).strip()

            if (
                not submission_id
                or submission_id in seen_ids
            ):
                continue

            seen_ids.add(submission_id)
            new_rows += 1

            status_display = str(
                submission.get("statusDisplay", "")
            ).strip().lower()

            # LeetCode has returned the numeric status as either an int or
            # a string in different GraphQL responses. Normalize it before
            # checking so an Accepted row is not accidentally discarded.
            status_code = str(
                submission.get("status", "")
            ).strip().lower()

            is_accepted = (
                status_display in {"accepted", "ac"}
                or status_code in {"10", "accepted", "ac"}
            )

            is_pending = submission.get("isPending", False)
            if isinstance(is_pending, str):
                is_pending = is_pending.strip().lower() == "true"

            if is_accepted and not is_pending:
                all_accepted.append(submission)

        has_next = bool(
            result.get("hasNext", False)
        )

        next_last_key = result.get("lastKey")

        if (
            not has_next
            or not submissions
            or new_rows == 0
        ):
            break

        offset += len(submissions)
        last_key = next_last_key

        time.sleep(
            LEETCODE_REQUEST_DELAY_SECONDS
        )

        if page_number > 1000:
            raise RuntimeError(
                f"Submission history pagination exceeded 1000 pages "
                f"for {title_slug}."
            )

    all_accepted.sort(
        key=lambda submission: (
            int(
                submission.get("timestamp", 0)
                or 0
            ),
            int(
                submission.get("id", 0)
                or 0
            ),
        )
    )

    if not saw_usable_response:
        return [], False

    return all_accepted, True


def get_submission_details(
    submission_id
):
    data = graphql(
        SUBMISSION_DETAILS_QUERY,
        {
            "submissionId": int(
                submission_id
            )
        },
        operation_name="submissionDetails",
    )

    details = data.get(
        "submissionDetails"
    )

    if not details:
        raise RuntimeError(
            f"No submission details returned "
            f"for {submission_id}."
        )

    if details.get(
        "statusDisplay"
    ) != "Accepted":
        raise RuntimeError(
            f"Submission {submission_id} "
            "is not accepted."
        )

    return details


def get_question(title_slug):
    data = graphql(
        QUESTION_QUERY,
        {
            "titleSlug": title_slug
        },
        operation_name="questionData",
    )

    question = data.get(
        "question"
    )

    if not question:
        raise RuntimeError(
            f"Could not fetch question "
            f"{title_slug}."
        )

    return question


# ============================================================
# Formatting helpers
# ============================================================

def safe_slug(text):
    text = str(text or "").lower()

    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text,
    )

    return text.strip("-")


def difficulty_badge(
    difficulty
):
    return {
        "Easy": "🟢 Easy",
        "Medium": "🟡 Medium",
        "Hard": "🔴 Hard",
    }.get(
        difficulty,
        difficulty or "Unknown",
    )


def language_name(
    language
):
    if isinstance(
        language,
        dict,
    ):
        language = language.get(
            "name",
            "",
        )

    language = str(
        language or ""
    ).strip().lower()

    if language in {
        "", "unknown", "none", "null", "n/a", "na", "not specified",
    }:
        return "Unknown"

    names = {
        "python": "Python",
        "python3": "Python",
        "py": "Python",
        "java": "Java",
        "java8": "Java",
        "java 8": "Java",
        "java11": "Java",
        "java 11": "Java",
        "java17": "Java",
        "java 17": "Java",
        "java21": "Java",
        "java 21": "Java",
        "cpp": "C++",
        "c++": "C++",
        "c-plus-plus": "C++",
        "c": "C",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "typescript": "TypeScript",
        "ts": "TypeScript",
        "csharp": "C#",
        "c#": "C#",
        "cs": "C#",
        "go": "Go",
        "golang": "Go",
        "rust": "Rust",
        "rs": "Rust",
        "kotlin": "Kotlin",
        "kt": "Kotlin",
        "swift": "Swift",
        "php": "PHP",
        "ruby": "Ruby",
        "rb": "Ruby",
        "scala": "Scala",
        "mysql": "SQL",
        "mssql": "SQL",
        "oracle": "SQL",
        "sql": "SQL",
    }

    return names.get(
        language,
        language or "Unknown",
    )


def language_from_filename(filename):
    """Infer a display language from a stored source filename."""
    suffix = Path(str(filename or "")).suffix.lower().lstrip(".")
    return language_name(suffix) if suffix else "Unknown"


def best_known_language(value=None, filename=None, fallback=None):
    """Resolve a language deterministically, never using Gemini as the source of truth."""
    for candidate in (value, fallback):
        resolved = language_name(candidate)
        if resolved != "Unknown":
            return resolved

    inferred = language_from_filename(filename)
    if inferred != "Unknown":
        return inferred

    return "Unknown"


def file_extension(
    language
):
    if isinstance(
        language,
        dict,
    ):
        language = language.get(
            "name",
            "",
        )

    language = str(
        language or ""
    ).lower()

    extensions = {
        "python": "py",
        "python3": "py",
        "java": "java",
        "cpp": "cpp",
        "c++": "cpp",
        "c": "c",
        "javascript": "js",
        "typescript": "ts",
        "csharp": "cs",
        "c#": "cs",
        "go": "go",
        "golang": "go",
        "rust": "rs",
        "kotlin": "kt",
        "swift": "swift",
        "php": "php",
        "ruby": "rb",
        "scala": "scala",
        "mysql": "sql",
        "mssql": "sql",
        "oracle": "sql",
    }

    return extensions.get(
        language,
        "txt",
    )


def html_to_text(
    content
):
    soup = BeautifulSoup(
        content or "",
        "html.parser",
    )

    for br in soup.find_all("br"):
        br.replace_with("\n")

    text = soup.get_text(
        "\n"
    )

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# ============================================================
# Fallback algorithm detector
# ============================================================

def fallback_analysis(
    code,
    tags,
    question=None,
):
    code_lower = (
        code or ""
    ).lower()

    tag_text = " ".join(
        tags or []
    ).lower()

    title = str((question or {}).get("title", "")).strip()

    # Strong code-based fallbacks for common problems. These are used only
    # when Gemini is unavailable, so the explanation remains useful offline.
    if title == "Two Sum":
        if re.search(r"for\s*\([^)]*\).*for\s*\([^)]*\)", code or "", re.DOTALL):
            return {
                "pattern": "🔎 Brute Force / Nested Loops",
                "problem_summary": (
                    "Find two different indices whose values add up to the given target. "
                    "Return the indices of that pair."
                ),
                "intuition": (
                    "Check each possible pair until the two values add up to the target. "
                    "Because the solution uses nested loops, every unique pair is examined."
                ),
                "approach": [
                    "Initialize an array to store the two answer indices.",
                    "Use an outer loop to choose the first index.",
                    "Use an inner loop starting after it to choose the second index.",
                    "Check whether the two selected values sum to target.",
                    "Store the matching indices and return them.",
                ],
                "why_it_works": (
                    "The nested loops enumerate every unique pair with the second index "
                    "greater than the first. Since the problem guarantees a solution, "
                    "the matching pair will be found."
                ),
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)",
                "key_takeaway": (
                    "Brute force is simple and reliable, but checking every pair costs "
                    "quadratic time; a hash map can reduce the time to O(n)."
                ),
            }

    if title == "Palindrome Number" and re.search(r"%\s*10|/=\s*10|/\s*10", code or ""):
        return {
            "pattern": "🔢 Digit Manipulation",
            "problem_summary": (
                "Determine whether an integer reads the same forward and backward."
            ),
            "intuition": (
                "The solution works directly with the digits. It repeatedly takes the "
                "last digit and uses it to build the number in reverse, then compares "
                "the result with the original value."
            ),
            "approach": [
                "Keep the original value available for the final comparison.",
                "Extract the last digit using modulo 10.",
                "Append that digit to the reversed number.",
                "Remove the processed digit using integer division by 10.",
                "Compare the reversed number with the original value.",
            ],
            "why_it_works": (
                "Reversing all digits produces exactly the number obtained by reading "
                "the input from right to left. The two values are equal exactly when "
                "the input is a palindrome."
            ),
            "time_complexity": "O(log n)",
            "space_complexity": "O(1)",
            "key_takeaway": (
                "Modulo and integer division are enough to inspect and reverse digits "
                "without converting the number to a string."
            ),
        }

    if title == "Power of Two":
        code_text = code or ""
        if re.search(r"&\s*\(?[a-zA-Z_][\w]*\s*-\s*1\)?", code_text):
            return {
                "pattern": "⚡ Bit Manipulation",
                "problem_summary": "Determine whether an integer is a power of two.",
                "intuition": (
                    "A positive power of two has exactly one set bit in binary. The "
                    "submitted bitwise check tests that property directly."
                ),
                "approach": [
                    "Reject non-positive values.",
                    "Apply the bitwise power-of-two condition to the number.",
                    "Return true when the condition holds.",
                    "Otherwise return false.",
                ],
                "why_it_works": (
                    "For a positive power of two, subtracting one changes its single "
                    "set bit to zero and turns lower bits on, so the number and n - 1 "
                    "share no set bits. Other positive integers do not satisfy this condition."
                ),
                "time_complexity": "O(1)",
                "space_complexity": "O(1)",
                "key_takeaway": (
                    "Binary representation can turn a seemingly iterative power check "
                    "into a constant-time bit manipulation test."
                ),
            }

        if re.search(r"/\s*=\s*2|/\s*2|\bpow(?!\w)|Math\.pow|recursive", code_text, re.I):
            return {
                "pattern": "🔁 Repeated Division / Recursion",
                "problem_summary": "Determine whether an integer is a power of two.",
                "intuition": (
                    "Powers of two can be reduced by dividing by two repeatedly. A valid "
                    "power reaches 1 without leaving a remainder at any step."
                ),
                "approach": [
                    "Reject values that are not positive.",
                    "Repeatedly reduce the value according to the submitted implementation.",
                    "Check that each required division is valid.",
                    "Accept the number when the process reaches the valid base case.",
                ],
                "why_it_works": (
                    "Every positive power of two can be reduced to 1 by repeatedly dividing "
                    "by two exactly, while any other positive integer eventually leaves a "
                    "remainder or fails the base condition."
                ),
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
                "key_takeaway": (
                    "Repeated division works because the exponent determines how many "
                    "times the value can be divided by two before reaching 1."
                ),
            }

    if title == "Missing Number":
        code_text = code or ""
        if "^" in code_text:
            return {
                "pattern": "🔀 XOR",
                "problem_summary": (
                    "Find the one missing value from an array containing distinct numbers "
                    "chosen from the range 0 through n."
                ),
                "intuition": (
                    "XOR cancels equal values. Combine the expected range with the values "
                    "in the array so every present number cancels itself, leaving only "
                    "the missing number."
                ),
                "approach": [
                    "Initialize the XOR accumulator with the required range state.",
                    "Traverse the array and XOR each present value into the accumulator.",
                    "Also XOR the corresponding range values.",
                    "Let equal values cancel each other through XOR.",
                    "Return the value left in the accumulator.",
                ],
                "why_it_works": (
                    "Because x ^ x = 0 and x ^ 0 = x, every value that exists in both the "
                    "range and the array cancels. The only value without a matching partner "
                    "is the missing number."
                ),
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "key_takeaway": "XOR is a useful way to find one missing value without extra storage.",
            }

        if re.search(r"Arrays\.sort|Collections\.sort|\bsort\s*\(", code_text):
            return {
                "pattern": "📊 Sorting",
                "problem_summary": (
                    "Find the one missing value from the complete range 0 through n."
                ),
                "intuition": (
                    "Sorting places the values in order, making the first position where "
                    "the expected value is absent reveal the missing number."
                ),
                "approach": [
                    "Sort the array.",
                    "Scan the values in increasing order.",
                    "Compare each value with the position or expected value.",
                    "Return the first missing value; otherwise return n when all prior values match.",
                ],
                "why_it_works": (
                    "After sorting, every present value appears in increasing order. The first "
                    "place where the expected sequence is broken identifies the missing value."
                ),
                "time_complexity": "O(n log n)",
                "space_complexity": "O(1)",
                "key_takeaway": "Sorting can simplify missing-value detection, at the cost of O(n log n) time.",
            }

        if re.search(r"n\s*\*\s*\(\s*n\s*\+\s*1\s*\)\s*/\s*2|sum", code_text, re.I):
            return {
                "pattern": "➕ Arithmetic Sum",
                "problem_summary": (
                    "Find the one missing value from the range 0 through n."
                ),
                "intuition": (
                    "The complete range has a known arithmetic sum. Subtracting the actual "
                    "array sum from that expected sum leaves the missing value."
                ),
                "approach": [
                    "Compute the expected sum of values from 0 through n.",
                    "Compute the sum of the values present in the array.",
                    "Subtract the actual sum from the expected sum.",
                    "Return the difference.",
                ],
                "why_it_works": (
                    "Only one value is missing, so the difference between the complete range "
                    "sum and the array sum is exactly that missing value."
                ),
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "key_takeaway": "A known total can expose a single missing value in one pass.",
            }

    # Important: more specific patterns
    # are checked before generic patterns.

    if (
        "% 10" in code_lower
        and "/ 10" in code_lower
    ):
        return {
            "pattern": "🔢 Digit Manipulation",
            "intuition": (
                "The solution processes the number digit by digit "
                "instead of converting it into another representation."
            ),
            "approach": [
                "Process the relevant digits from the input.",
                "Extract or update the current digit/state.",
                "Build the required result while traversing the input.",
                "Return the result after all relevant digits are processed.",
            ],
            "why": (
                "Each iteration handles one digit, so the algorithm "
                "does not need to repeatedly inspect the whole number."
            ),
            "time": "O(log n)",
            "space": "O(1)",
        }

    if (
        "hash map" in tag_text
        or "hashmap" in code_lower
        or "unordered_map" in code_lower
        or "hashmap" in tag_text
        or "dict<" in code_lower
    ):
        return {
            "pattern": "🗺️ Hash Map",
            "intuition": (
                "Previously processed values are stored so the "
                "information needed for later decisions can be "
                "looked up efficiently."
            ),
            "approach": [
                "Create a hash map for previously processed values.",
                "Traverse the input once.",
                "Check the map for the value/state required by the problem.",
                "Update the map and return when the condition is satisfied.",
            ],
            "why": (
                "Hash-map lookups are O(1) on average, avoiding "
                "repeated linear searches."
            ),
            "time": "O(n)",
            "space": "O(n)",
        }

    if (
        "binary search" in tag_text
        or (
            "mid" in code_lower
            and "left" in code_lower
            and "right" in code_lower
        )
    ):
        return {
            "pattern": "🔍 Binary Search",
            "intuition": (
                "The search space is ordered, so each comparison "
                "can eliminate roughly half of the remaining candidates."
            ),
            "approach": [
                "Define the current search boundaries.",
                "Inspect the middle position.",
                "Determine which half can still contain the answer.",
                "Discard the other half and continue.",
            ],
            "why": (
                "Every iteration removes about half of the remaining "
                "search space."
            ),
            "time": "O(log n)",
            "space": "O(1)",
        }

    if (
        "sliding window" in tag_text
    ):
        return {
            "pattern": "🪟 Sliding Window",
            "intuition": (
                "A moving window keeps track of the currently relevant "
                "portion of the input."
            ),
            "approach": [
                "Initialize the window boundaries.",
                "Expand the right side as new elements are processed.",
                "Move the left side whenever the window becomes invalid.",
                "Track the required result.",
            ],
            "why": (
                "Each element enters and leaves the window a limited "
                "number of times."
            ),
            "time": "O(n)",
            "space": "Depends on the maintained window state",
        }

    if (
        "two pointers" in tag_text
        or (
            "left" in code_lower
            and "right" in code_lower
            and "while" in code_lower
        )
    ):
        return {
            "pattern": "👉 Two Pointers",
            "intuition": (
                "Two positions are maintained so the algorithm can "
                "eliminate unnecessary comparisons while scanning the input."
            ),
            "approach": [
                "Initialize the two pointers.",
                "Compare the values at the current positions.",
                "Move the appropriate pointer according to the problem condition.",
                "Continue until the search space is exhausted or the answer is found.",
            ],
            "why": (
                "The pointers move through the input without repeatedly "
                "revisiting eliminated candidates."
            ),
            "time": "O(n)",
            "space": "O(1)",
        }

    if (
        "dynamic programming" in tag_text
        or "lru_cache" in code_lower
        or "memo" in code_lower
        or re.search(
            r"\bdp\b",
            code_lower,
        )
    ):
        return {
            "pattern": "🧠 Dynamic Programming",
            "intuition": (
                "The problem contains overlapping subproblems, so "
                "previously computed results can be reused."
            ),
            "approach": [
                "Define the state representing a smaller subproblem.",
                "Initialize the base cases.",
                "Compute or memoize each state.",
                "Use previously calculated states to derive the final answer.",
            ],
            "why": (
                "Memoization or tabulation prevents the same subproblem "
                "from being solved repeatedly."
            ),
            "time": "Depends on the state space",
            "space": "Depends on the state space",
        }

    if (
        "heap" in tag_text
        or "priority queue" in tag_text
        or "heapq" in code_lower
        or "priorityqueue" in code_lower
    ):
        return {
            "pattern": "🏔️ Heap / Priority Queue",
            "intuition": (
                "A priority queue keeps the most important candidate "
                "available without repeatedly scanning every candidate."
            ),
            "approach": [
                "Insert the relevant candidates into the heap.",
                "Extract the highest-priority candidate when needed.",
                "Add newly relevant candidates.",
                "Continue until the required result is obtained.",
            ],
            "why": (
                "The heap maintains the next best candidate efficiently."
            ),
            "time": "Typically O(n log n)",
            "space": "O(n)",
        }

    if (
        "backtracking" in tag_text
        or "backtrack" in code_lower
    ):
        return {
            "pattern": "🌳 Backtracking",
            "intuition": (
                "The algorithm explores possible choices and undoes "
                "a choice when that path cannot produce a valid result."
            ),
            "approach": [
                "Choose the next available option.",
                "Explore the resulting state recursively.",
                "Undo the choice when returning.",
                "Continue until all required possibilities are considered.",
            ],
            "why": (
                "Invalid branches can be discarded without affecting "
                "other unexplored choices."
            ),
            "time": "Depends on the search space",
            "space": "Depends on recursion depth",
        }

    if (
        "stack" in tag_text
        or (
            "push(" in code_lower
            and "pop(" in code_lower
        )
    ):
        return {
            "pattern": "📚 Stack",
            "intuition": (
                "A stack is useful when the most recently unresolved "
                "element should be processed first."
            ),
            "approach": [
                "Initialize the stack.",
                "Traverse the input.",
                "Push unresolved elements.",
                "Pop elements when the current value resolves them.",
            ],
            "why": (
                "Each element can be pushed and popped while preserving "
                "the required last-in-first-out ordering."
            ),
            "time": "O(n)",
            "space": "O(n)",
        }

    if (
        "breadth-first search" in tag_text
        or "bfs" in tag_text
        or "queue" in tag_text
        or "deque" in code_lower
    ):
        return {
            "pattern": "🌐 Breadth-First Search",
            "intuition": (
                "The structure is explored level by level using a queue."
            ),
            "approach": [
                "Initialize a queue with the starting state.",
                "Process states in FIFO order.",
                "Generate the next valid states.",
                "Continue until the target is found or traversal is complete.",
            ],
            "why": (
                "FIFO processing guarantees that shallower states "
                "are processed before deeper states."
            ),
            "time": "O(V + E)",
            "space": "O(V)",
        }

    if (
        "depth-first search" in tag_text
        or "dfs" in tag_text
    ):
        return {
            "pattern": "🌲 Depth-First Search",
            "intuition": (
                "The algorithm explores one branch deeply before "
                "moving to another branch."
            ),
            "approach": [
                "Start at the relevant node or state.",
                "Visit an unprocessed neighbor recursively.",
                "Track visited state when required.",
                "Backtrack when a branch is exhausted.",
            ],
            "why": (
                "DFS systematically reaches every relevant node "
                "reachable from the starting state."
            ),
            "time": "O(V + E)",
            "space": "O(V)",
        }

    if (
        "sort(" in code_lower
        or "sorted(" in code_lower
        or "sorting" in tag_text
    ):
        return {
            "pattern": "📊 Sorting",
            "intuition": (
                "Ordering the input exposes relationships that are "
                "harder to use in arbitrary order."
            ),
            "approach": [
                "Sort the input.",
                "Traverse the ordered values.",
                "Use the ordering to simplify comparisons or grouping.",
                "Construct the final result.",
            ],
            "why": (
                "The sorted order eliminates many comparisons that "
                "would otherwise be necessary."
            ),
            "time": "O(n log n)",
            "space": "Depends on sorting implementation",
        }

    if (
        "greedy" in tag_text
    ):
        return {
            "pattern": "⚡ Greedy",
            "intuition": (
                "At each step the solution chooses the locally best "
                "option according to the problem's structure."
            ),
            "approach": [
                "Evaluate the available choices.",
                "Select the locally optimal choice.",
                "Update the state.",
                "Continue until the complete result is built.",
            ],
            "why": (
                "The problem's structure guarantees that the chosen "
                "local decisions lead to the required global result."
            ),
            "time": "Depends on implementation",
            "space": "Depends on implementation",
        }

    # General fallback: stay useful even when Gemini is unavailable.
    # Derive as much as possible from the actual code and LeetCode metadata
    # instead of emitting a meaningless template.
    if "hashmap" in code_lower or "hash map" in tag_text or "hash table" in tag_text or "dict" in code_lower:
        fallback = {
            "pattern": "🗺️ Hash Map",
            "intuition": (
                "The implementation stores previously seen values so that a related "
                "value can be checked quickly instead of searching the earlier elements "
                "again. This trades extra memory for faster lookups."
            ),
            "approach": [
                "Create the map used by the submitted implementation.",
                "Traverse the input from the beginning.",
                "Check the map for the value or state required by the current element.",
                "Use the stored information when the required condition is met.",
                "Otherwise store the current value or state and continue.",
            ],
            "why": (
                "Each lookup uses the information collected from earlier elements. "
                "Because the map represents exactly the relevant values already seen, "
                "a successful lookup identifies the condition required by the algorithm."
            ),
            "time": "O(n)",
            "space": "O(n)",
        }
        return fallback

    if "while" in code_lower and ("/ 10" in code_lower or "% 10" in code_lower):
        return {
            "pattern": "🔢 Digit Manipulation",
            "intuition": (
                "The implementation works directly with the decimal digits instead of "
                "converting the number to a string. Modulo 10 exposes the last digit, "
                "while integer division by 10 removes that digit from the working value."
            ),
            "approach": [
                "Keep the original value available when the final result requires a comparison.",
                "Repeatedly extract the last digit with modulo 10.",
                "Use that digit to update the result or required state.",
                "Remove the processed digit with integer division by 10.",
                "Finish when all digits have been processed and return the required result.",
            ],
            "why": (
                "Every iteration processes exactly one decimal digit. The sequence of "
                "extracted digits therefore captures the input from right to left, and "
                "the maintained result contains exactly the information required by the code."
            ),
            "time": "O(log n)",
            "space": "O(1)",
        }

    if "sort(" in code_lower or "sorted(" in code_lower or "sorting" in tag_text:
        return {
            "pattern": "📊 Sorting",
            "intuition": (
                "The implementation first puts the relevant values into a predictable "
                "order. Once the values are ordered, comparisons that would be difficult "
                "in arbitrary order become straightforward while scanning from left to right."
            ),
            "approach": [
                "Sort the input using the operation present in the submitted code.",
                "Traverse the sorted values in order.",
                "Use the ordering to detect the required relationship or boundary.",
                "Return or construct the answer once the condition is identified.",
            ],
            "why": (
                "Sorting establishes the ordering assumed by the subsequent comparisons. "
                "The scan can therefore use that order to eliminate unnecessary cases and "
                "identify the required result."
            ),
            "time": "O(n log n)",
            "space": "O(1)",
        }

    return {
        "pattern": "🔎 Direct Algorithm",
        "intuition": (
            "The submitted code follows a direct procedure tailored to the condition "
            "being checked by the problem. Each operation transforms or evaluates the "
            "current state until the return condition is reached."
        ),
        "approach": [
            "Initialize the variables used by the submitted implementation.",
            "Process the input according to the code's control flow.",
            "Evaluate the condition that determines the next state or answer.",
            "Update the relevant variables and continue until the stopping condition is reached.",
            "Return the value produced by the final state.",
        ],
        "why": (
            "The algorithm preserves the information needed for each decision as it moves "
            "through the input. Because the final return condition is based on that maintained "
            "state, the resulting value follows directly from the operations performed by the code."
        ),
        "time": "O(n)",
        "space": "O(1)",
    }


def normalize_fallback_analysis(analysis, question):
    """Normalize deterministic fallback output to the README schema."""
    result = dict(analysis or {})
    result["why_it_works"] = result.get(
        "why_it_works",
        result.get(
            "why",
            "The submitted algorithm maintains the information needed to determine the result."
        ),
    )
    result["time_complexity"] = result.get(
        "time_complexity",
        result.get("time", "O(n)"),
    )
    result["space_complexity"] = result.get(
        "space_complexity",
        result.get("space", "O(1)"),
    )

    pattern = str(result.get("pattern", "Algorithmic Approach"))
    time_complexity = str(result["time_complexity"]).strip()
    space_complexity = str(result["space_complexity"]).strip()

    if "time_explanation" not in result:
        if "Digit Manipulation" in pattern and "log" in time_complexity:
            result["time_explanation"] = (
                "The loop processes one decimal digit per iteration, and a base-10 integer "
                "contains a number of digits proportional to log₁₀(x)."
            )
        elif "Hash Map" in pattern and time_complexity == "O(n)":
            result["time_explanation"] = (
                "The implementation makes one pass through the input, with average O(1) hash-map "
                "lookups and updates for each element."
            )
        elif "Sorting" in pattern and "n log n" in time_complexity:
            result["time_explanation"] = (
                "The dominant cost is sorting the input, which takes O(n log n), followed by a linear scan."
            )
        elif time_complexity == "O(1)":
            result["time_explanation"] = (
                "The amount of work does not grow with the size of the input."
            )
        elif time_complexity == "O(log n)":
            result["time_explanation"] = (
                "Each iteration reduces the remaining search or value range by a constant factor."
            )
        elif time_complexity == "O(n^2)":
            result["time_explanation"] = (
                "The implementation contains two input-dependent passes that together examine a quadratic number of combinations."
            )
        else:
            result["time_explanation"] = (
                "The running time follows the number of input-dependent operations performed by the submitted implementation."
            )

    if "space_explanation" not in result:
        if space_complexity == "O(1)":
            result["space_explanation"] = (
                "The solution uses only a fixed number of variables and does not allocate memory that grows with the input size."
            )
        elif space_complexity == "O(n)":
            result["space_explanation"] = (
                "The additional data structure grows with the number of input elements."
            )
        elif "log n" in space_complexity:
            result["space_explanation"] = (
                "The additional memory grows with the depth of the logarithmic process."
            )
        else:
            result["space_explanation"] = (
                "The additional memory is determined by the data structures or recursion used by the implementation."
            )

    if "problem_summary" not in result:
        title = str((question or {}).get("title", "this problem"))
        content = html_to_text((question or {}).get("content", ""))
        summary = ""
        for sentence in re.split(r"(?<=[.!?])\s+", content):
            sentence = re.sub(r"\s+", " ", sentence).strip()
            if sentence and len(sentence) >= 25:
                summary = sentence
                break
        if summary:
            result["problem_summary"] = summary[:350]
        else:
            result["problem_summary"] = (
                f"Determine the required result for {title} using the submitted implementation."
            )
    if "key_takeaway" not in result:
        result["key_takeaway"] = (
            f"The main idea is to recognize the {result.get('pattern', 'algorithmic')} "
            "pattern and understand how the submitted implementation applies it to this problem."
        )
    result.pop("why", None)
    result.pop("time", None)
    result.pop("space", None)
    return result


# ============================================================
# Gemini request / retry helpers
# ============================================================

def classify_gemini_429(response):
    """
    Distinguish daily quota exhaustion from short-term rate limiting.
    """
    try:
        body = response.json()
    except Exception:
        body = {}

    error = body.get("error", {}) if isinstance(body, dict) else {}
    status = str(error.get("status", "")).lower()
    message = str(error.get("message", "")).lower()
    details = error.get("details", [])
    detail_text = json.dumps(
        details,
        ensure_ascii=False,
    ).lower()

    combined = " ".join(
        [status, message, detail_text]
    )

    if any(
        token in combined
        for token in (
            "quota_exceeded",
            "generate_content_free_tier_requests",
            "requestsperday",
            "perday",
            "daily quota",
            "quota exceeded",
        )
    ):
        return "daily"

    if any(
        token in combined
        for token in (
            "rate_limit_exceeded",
            "too_many_requests",
            "requestsperminute",
            "tokensperminute",
            "perminute",
            "rate limit",
        )
    ):
        return "rate"

    return "unknown"


def _gemini_post_with_retry(
    *,
    prompt,
    timeout,
):
    """
    Call Gemini with bounded retries for transient failures.

    A successful call is returned. Transient 429/5xx failures are retried,
    while a confirmed daily-quota 429 blocks the backfill until the next
    Pacific-time quota day. Failed attempts never consume the local budget.
    """
    for attempt in range(
        GEMINI_MAX_RETRIES + 1
    ):
        try:
            response = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/interactions",
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": GEMINI_API_KEY,
                },
                json={
                    "model": "gemini-3.6-flash",
                    "input": prompt,
                },
                timeout=timeout,
            )
        except requests.RequestException as exc:
            GEMINI_RUNTIME["last_failure"] = (
                f"Gemini network error: {exc}"
            )

            if attempt < GEMINI_MAX_RETRIES:
                wait_seconds = GEMINI_BACKOFF_SECONDS[
                    min(
                        attempt,
                        len(GEMINI_BACKOFF_SECONDS) - 1,
                    )
                ]
                print(
                    f"⚠️ Gemini network error. "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)
                continue

            print(
                f"⏸️ Gemini network error after retries: {exc}"
            )
            return None

        if response.status_code == 200:
            return response

        if response.status_code == 429:
            kind = classify_gemini_429(response)

            if kind == "daily":
                GEMINI_RUNTIME["blocked"] = True
                GEMINI_RUNTIME["last_failure"] = (
                    "Gemini daily quota exceeded."
                )
                print(
                    "⏸️ Gemini daily quota exceeded. "
                    "Historical backfill will resume after the quota reset."
                )
                print(response.text[:1000])
                return None

            if attempt < GEMINI_MAX_RETRIES:
                wait_seconds = GEMINI_BACKOFF_SECONDS[
                    min(
                        attempt,
                        len(GEMINI_BACKOFF_SECONDS) - 1,
                    )
                ]
                print(
                    f"⚠️ Gemini HTTP 429 ({kind}). "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)
                continue

            GEMINI_RUNTIME["last_failure"] = (
                f"Gemini HTTP 429 ({kind}) persisted after retries."
            )
            print(
                "⏸️ Gemini HTTP 429 persisted after retries. "
                "Historical backfill will retry on a later run."
            )
            print(response.text[:1000])
            return None

        if response.status_code in {
            500,
            502,
            503,
            504,
        }:
            if attempt < GEMINI_MAX_RETRIES:
                wait_seconds = GEMINI_BACKOFF_SECONDS[
                    min(
                        attempt,
                        len(GEMINI_BACKOFF_SECONDS) - 1,
                    )
                ]
                print(
                    f"⚠️ Gemini temporarily unavailable "
                    f"(HTTP {response.status_code}). "
                    f"Retrying in {wait_seconds}s..."
                )
                time.sleep(wait_seconds)
                continue

            GEMINI_RUNTIME["last_failure"] = (
                "Temporary Gemini service error "
                f"HTTP {response.status_code} after retries."
            )
            print(GEMINI_RUNTIME["last_failure"])
            return None

        GEMINI_RUNTIME["last_failure"] = (
            f"Gemini request failed with HTTP "
            f"{response.status_code}."
        )
        print(GEMINI_RUNTIME["last_failure"])
        print(response.text[:1000])
        return None

    return None


# ============================================================
# AI explanation
# ============================================================

def ai_analysis(
    question,
    code,
    tags,
):
    """
    Generate a problem-specific explanation using Gemini.

    The model receives:
        - the LeetCode problem
        - the LeetCode topics
        - the user's actual accepted solution

    The explanation is based on the implementation that was
    actually submitted.
    """

    if not GEMINI_API_KEY:
        print(
            "❌ GEMINI_API_KEY is not configured."
        )
        GEMINI_RUNTIME["blocked"] = True
        GEMINI_RUNTIME["last_failure"] = (
            "GEMINI_API_KEY is not configured."
        )
        return None

    if GEMINI_RUNTIME["blocked"]:
        print(
            "⏸️ Gemini is already blocked for today."
        )
        return None

    if (
        GEMINI_RUNTIME["requests_used"]
        >= MAX_GEMINI_REQUESTS_PER_DAY
    ):
        GEMINI_RUNTIME["blocked"] = True
        GEMINI_RUNTIME["last_failure"] = (
            "Daily Gemini request budget reached."
        )
        print(
            "⏸️ Gemini daily request budget reached."
        )
        return None

    problem_text = html_to_text(
        question.get("content", "")
    )

    if len(problem_text) > 14000:
        problem_text = problem_text[:14000]

    prompt = f"""
You are an expert algorithms educator.

Analyze the following LeetCode problem and the user's accepted
solution code.

Your explanation MUST describe the submitted implementation accurately.

Write the explanation in the same style and quality as a strong human-written
LeetCode solution note: specific to this problem, concrete, beginner-friendly,
and informative. Avoid generic phrases such as "process the input",
"maintain the required state", or "solve the problem using the submitted
implementation" when the code/problem gives enough information to be more
specific.

====================
PROBLEM
====================
{problem_text}

====================
TOPICS
====================
{", ".join(tags)}

====================
ACCEPTED CODE
====================
{code}

====================
TASK
====================

Return ONLY valid JSON with these exact keys:

pattern
problem_summary
intuition
approach
why_it_works
time_complexity
space_complexity
key_takeaway
time_explanation
space_explanation

RULES:

1. Explain the ACTUAL submitted implementation.
2. Do not replace it with a different algorithm.
3. Do not invent a data structure or optimization that is not present.
4. problem_summary must be a concise paraphrase of the actual problem and
   should mention the key input/output condition.
5. intuition must be one useful paragraph explaining the central observation
   behind the submitted algorithm, including important edge cases when relevant.
   It should feel like the explanation in a high-quality LeetCode editorial,
   not a generic template.
6. approach must contain 4 to 8 concrete ordered steps that follow the code
   in execution order. Name important variables, operations, data structures,
   or conditions when they help the reader understand the implementation.
7. why_it_works must be one clear paragraph proving why THIS implementation
   produces the required result. Explain the key invariant or mathematical
   property rather than merely restating the steps.
8. time_complexity must contain ONLY the Big-O expression.
   Examples: O(1), O(n), O(log n), O(n log n), O(n^2).
   Do NOT include explanations, punctuation, or extra text.
9. space_complexity must contain ONLY the Big-O expression.
   Examples: O(1), O(n), O(log n).
   Do NOT include explanations, punctuation, or extra text.
10. time_explanation must be one concise sentence explaining why the stated time complexity applies to THIS code.
11. space_explanation must be one concise sentence explaining why the stated space complexity applies to THIS code.
10. Account for sorting cost when sorting is used.
11. Account for recursion depth when recursion is used.
12. For hash maps and hash sets, use average-case complexity.
13. Explain numeric techniques such as digit extraction when they are used.
16. Keep the writing concise, clear and educational.
17. Do not copy the complete problem statement.
18. Return JSON only.
19. If the submitted code is brute force, explicitly say that it is brute force.
20. If a more optimal solution exists, do not replace the submitted approach
    with it. You may mention the limitation briefly, but document the
    submitted implementation exactly.
21. If the algorithm cannot be confidently inferred from the code, say so
    instead of inventing an explanation.
22. Prefer correctness over sounding sophisticated.
23. Make intuition, approach, why_it_works, and key_takeaway specific to the
    actual problem and code. Never use placeholder/template language when the
    problem statement and code provide enough information.
24. For mathematical or bit-manipulation solutions, explain the underlying
    property in plain language. For data-structure solutions, explain what is
    stored and why. For brute force, explicitly describe what combinations are
    examined.
25. key_takeaway should capture the reusable idea or pattern learned from this
    particular problem in one or two sentences.
"""

    try:
        response = _gemini_post_with_retry(
            prompt=prompt,
            timeout=90,
        )

        if response is None:
            return None

        body = response.json()

        output_text = body.get(
            "output_text"
        )

        if not output_text:
            for step in body.get(
                "steps",
                [],
            ):
                if step.get(
                    "type"
                ) == "model_output":

                    content = step.get(
                        "content",
                        [],
                    )

                    for item in content:
                        if item.get(
                            "type"
                        ) == "text":

                            output_text = item.get(
                                "text",
                                "",
                            )
                            break

                if output_text:
                    break

        if not output_text:
            print(
                "⚠️ Gemini returned no text output."
            )
            return None

        output_text = output_text.strip()

        if output_text.startswith("```"):
            output_text = re.sub(
                r"^```(?:json)?\s*",
                "",
                output_text,
            )

            output_text = re.sub(
                r"\s*```$",
                "",
                output_text,
            )

        result = json.loads(
            output_text
        )

        required_keys = {
            "pattern",
            "problem_summary",
            "intuition",
            "approach",
            "why_it_works",
            "time_complexity",
            "space_complexity",
            "key_takeaway",
            "time_explanation",
            "space_explanation",
        }

        if not required_keys.issubset(
            result.keys()
        ):
            print(
                "⚠️ Gemini response is missing "
                "required fields."
            )
            return None

        if not isinstance(
            result["approach"],
            list,
        ):
            print(
                "⚠️ Gemini returned an invalid "
                "approach format."
            )
            return None

        complexity_pattern = re.compile(
            r"^O\(.+\)$"
        )

        time_complexity = str(
            result.get(
                "time_complexity",
                "",
            )
        ).strip()

        space_complexity = str(
            result.get(
                "space_complexity",
                "",
            )
        ).strip()

        if not complexity_pattern.match(
            time_complexity
        ):
            print(
                "⚠️ Invalid time complexity "
                "returned by Gemini."
            )
            return None

        if not complexity_pattern.match(
            space_complexity
        ):
            print(
                "⚠️ Invalid space complexity "
                "returned by Gemini."
            )
            return None

        result["time_complexity"] = (
            time_complexity
        )

        result["space_complexity"] = (
            space_complexity
        )

        result.setdefault(
            "time_explanation",
            "The stated running time follows the number of input-dependent operations performed by the submitted implementation.",
        )
        result.setdefault(
            "space_explanation",
            "The stated space usage follows the extra variables, data structures, and recursion used by the submitted implementation.",
        )

        # Count only a successful, fully validated Gemini response.
        GEMINI_RUNTIME["requests_used"] += 1
        GEMINI_RUNTIME["last_failure"] = ""
        return result

    except requests.RequestException as exc:
        print(
            f"⚠️ Gemini network error: {exc}"
        )
        return None

    except json.JSONDecodeError as exc:
        print(
            f"⚠️ Gemini returned invalid JSON: {exc}"
        )
        return None

    except Exception as exc:
        print(
            f"⚠️ Gemini analysis failed: {exc}"
        )
        return None

# ============================================================
# Semantic historical clustering
# ============================================================

AI_ANALYSIS_KEYS = {
    "pattern",
    "problem_summary",
    "intuition",
    "approach",
    "why_it_works",
    "time_complexity",
    "space_complexity",
    "key_takeaway",
    "time_explanation",
    "space_explanation",
}


def _parse_gemini_text(body):
    """Extract text from the Gemini Interactions response."""
    output_text = body.get("output_text")

    if not output_text:
        for step in body.get("steps", []):
            if step.get("type") != "model_output":
                continue
            for item in step.get("content", []):
                if item.get("type") == "text":
                    output_text = item.get("text", "")
                    break
            if output_text:
                break

    if not output_text:
        return ""

    output_text = str(output_text).strip()

    if output_text.startswith("```"):
        output_text = re.sub(r"^```(?:json)?\s*", "", output_text)
        output_text = re.sub(r"\s*```$", "", output_text)

    return output_text.strip()


def _validate_analysis(result):
    """Validate one Gemini solution explanation."""
    if not isinstance(result, dict):
        return False

    if not AI_ANALYSIS_KEYS.issubset(result.keys()):
        return False

    if not isinstance(result.get("approach"), list):
        return False

    if not (4 <= len(result["approach"]) <= 8):
        return False

    complexity_pattern = re.compile(r"^O\(.+\)$")
    if not complexity_pattern.match(str(result.get("time_complexity", "")).strip()):
        return False
    if not complexity_pattern.match(str(result.get("space_complexity", "")).strip()):
        return False

    return True


def _normalize_semantic_label(value):
    """Normalize an approach label for conservative post-clustering checks."""
    value = str(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    stop_words = {
        "solution", "approach", "algorithm", "method", "using",
        "with", "the", "a", "an", "of", "for", "and", "plus",
    }
    words = [word for word in value.split() if word not in stop_words]
    return " ".join(words).strip()


def _cluster_has_weak_separation(clusters, candidates):
    """
    Detect likely over-segmentation before accepting Gemini's answer.

    This is intentionally conservative: when several one-item clusters all
    describe the same broad pattern, we ask Gemini to perform a second,
    stricter merge review rather than trusting the first answer blindly.
    """
    if not clusters or len(candidates) <= 1:
        return False

    if len(clusters) < len(candidates):
        return False

    # Every candidate becoming its own cluster is the strongest over-splitting
    # signal we can observe without understanding the code ourselves.
    singleton_only = all(
        len(cluster.get("submission_ids", [])) == 1
        for cluster in clusters
    )

    if not singleton_only:
        return False

    patterns = {
        _normalize_semantic_label(
            cluster.get("analysis", {}).get("pattern", "")
        )
        for cluster in clusters
    }
    names = {
        _normalize_semantic_label(cluster.get("approach_name", ""))
        for cluster in clusters
    }
    keys = {
        _normalize_semantic_label(cluster.get("approach_key", ""))
        for cluster in clusters
    }

    if len(patterns) == 1 and patterns != {""}:
        return True
    if len(names) == 1 and names != {""}:
        return True
    if len(keys) == 1 and keys != {""}:
        return True

    return False


def _coerce_cluster_response(clusters, candidates):
    """Fill harmless presentation omissions while keeping submission assignment strict."""
    if not isinstance(clusters, list):
        return None

    candidate_map = {str(item["submission_id"]): item for item in candidates}
    normalized = []

    for raw_cluster in clusters:
        if not isinstance(raw_cluster, dict):
            return None

        cluster = dict(raw_cluster)
        ids = [str(x) for x in cluster.get("submission_ids", [])]
        representative_id = str(cluster.get("representative_submission_id", ""))
        if not ids or not representative_id or representative_id not in candidate_map:
            return None

        cluster["submission_ids"] = ids
        cluster["representative_submission_id"] = representative_id

        representative = candidate_map[representative_id]
        cluster["language"] = best_known_language(
            cluster.get("language"),
            None,
            representative.get("language"),
        )

        analysis = cluster.get("analysis")
        if isinstance(analysis, dict):
            analysis = dict(analysis)
            if not analysis.get("pattern"):
                analysis["pattern"] = cluster.get("approach_name") or "Algorithmic Approach"
            if not analysis.get("key_takeaway"):
                analysis["key_takeaway"] = (
                    "The reusable idea is captured by the algorithmic pattern used in the submitted implementation."
                )
            cluster["analysis"] = analysis

        approach_name = str(cluster.get("approach_name", "")).strip()
        if not approach_name:
            approach_name = str((analysis or {}).get("pattern", "Algorithmic Approach")).strip()
        cluster["approach_name"] = approach_name or "Algorithmic Approach"

        approach_key = str(cluster.get("approach_key", "")).strip()
        cluster["approach_key"] = (
            approach_key
            or _normalize_semantic_label(cluster["approach_name"])
            or "algorithmic-approach"
        )

        reason = str(cluster.get("cluster_reason", "")).strip()
        cluster["cluster_reason"] = reason or (
            f"These submissions use the same {cluster['approach_name']} strategy."
        )

        normalized.append(cluster)

    return normalized


def _validate_clusters(clusters, candidates):
    """Validate a Gemini cluster list against every candidate submission."""
    if not isinstance(clusters, list) or not clusters:
        return False

    candidate_map = {
        str(item["submission_id"]): item
        for item in candidates
    }
    expected_ids = set(candidate_map)
    assigned_ids = []

    for cluster in clusters:
        if not isinstance(cluster, dict):
            return False

        cluster_ids = [
            str(x)
            for x in cluster.get("submission_ids", [])
        ]
        representative_id = str(
            cluster.get("representative_submission_id", "")
        )
        language = str(
            cluster.get("language", "")
        ).strip()
        approach_key = str(
            cluster.get("approach_key", "")
        ).strip()
        approach_name = str(
            cluster.get("approach_name", "")
        ).strip()
        cluster_reason = str(
            cluster.get("cluster_reason", "")
        ).strip()
        analysis = cluster.get("analysis")

        if not cluster_ids:
            return False
        if representative_id not in cluster_ids:
            return False
        if any(item_id not in expected_ids for item_id in cluster_ids):
            return False
        if not language or not approach_key or not approach_name or not cluster_reason:
            return False
        if not _validate_analysis(analysis):
            return False

        representative = candidate_map[representative_id]
        if language != representative["language"]:
            return False

        assigned_ids.extend(cluster_ids)

    if len(assigned_ids) != len(set(assigned_ids)):
        return False

    return set(assigned_ids) == expected_ids


def _gemini_post_cluster_review(question, candidates, clusters):
    """
    Second-pass review used only when Gemini appears to have over-split a
    problem. It is deliberately stricter: merge unless a concrete algorithmic
    difference can be demonstrated from the code.
    """
    if not candidates or not clusters:
        return clusters

    if GEMINI_RUNTIME["blocked"]:
        return None

    if GEMINI_RUNTIME["requests_used"] >= MAX_GEMINI_REQUESTS_PER_DAY:
        GEMINI_RUNTIME["last_failure"] = (
            "No Gemini request budget remains for the clustering audit."
        )
        return None

    problem_text = html_to_text(question.get("content", ""))
    if len(problem_text) > 8000:
        problem_text = problem_text[:8000]

    candidate_map = {
        str(item["submission_id"]): item
        for item in candidates
    }

    sections = []
    for index, cluster in enumerate(clusters, start=1):
        representative_id = str(
            cluster["representative_submission_id"]
        )
        representative = candidate_map[representative_id]
        code = representative.get("code", "")
        if len(code) > 9000:
            code = code[:9000]

        sections.append(
            "\n".join(
                [
                    f"INITIAL CLUSTER {index}",
                    f"approach_key: {cluster.get('approach_key', '')}",
                    f"approach_name: {cluster.get('approach_name', '')}",
                    f"language: {cluster.get('language', '')}",
                    f"submission_ids: {cluster.get('submission_ids', [])}",
                    f"cluster_reason: {cluster.get('cluster_reason', '')}",
                    f"representative_submission_id: {representative_id}",
                    "representative_code:",
                    code,
                ]
            )
        )

    prompt = f"""
You are the final semantic auditor for a LeetCode solution archive.

We have accepted-submission candidates for ONE problem and an initial Gemini
clustering. The initial clustering may be OVER-SPLIT. Re-review the actual
representative code and merge clusters whenever they use the same core
algorithmic idea.

This archive is meant to store genuinely different approaches, NOT every
source-code variation.

CONSERVATIVE RULE:
If two implementations could be explained by the same algorithmic idea,
same main data structure, same mathematical trick, and same asymptotic method,
MERGE them. When uncertain, MERGE rather than split.

Do NOT treat these as different approaches:
- variable names
- formatting/comments
- changing for-loop syntax to while-loop syntax
- helper methods or small refactors
- different but equivalent expressions
- changing the order of harmless operations

Treat these as different only when there is a concrete difference such as:
- brute force versus hashing
- sorting + two pointers versus hashing
- binary search versus linear scan
- XOR versus arithmetic sum
- recursion versus iterative state when that changes the algorithmic method
- a materially different data structure or mathematical property
- different programming languages

For every retained cluster, provide a concrete cluster_reason grounded in the
representative code. Do not preserve separate clusters just to reflect that
there were separate submissions.

PROBLEM
=======
{problem_text}

INITIAL CLUSTERS
================
{"\n\n".join(sections)}

RETURN ONLY VALID JSON in exactly this form:
{{
  "solutions": [
    {{
      "approach_key": "stable-short-semantic-key",
      "approach_name": "Human-readable algorithmic approach",
      "language": "Java",
      "submission_ids": ["..."],
      "representative_submission_id": "...",
      "cluster_reason": "Concrete reason this cluster is one approach.",
      "analysis": {{
        "pattern": "...",
        "problem_summary": "...",
        "intuition": "...",
        "approach": ["step 1", "step 2", "step 3", "step 4"],
        "why_it_works": "...",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "key_takeaway": "...",
        "time_explanation": "...",
        "space_explanation": "..."
      }}
    }}
  ]
}}

Every candidate submission_id must appear exactly once across the final
clusters. The representative must belong to its cluster, and language must
match the representative candidate exactly.
"""

    try:
        response = _gemini_post_with_retry(
            prompt=prompt,
            timeout=120,
        )

        if response is None:
            return None

        result = json.loads(_parse_gemini_text(response.json()))
        reviewed = _coerce_cluster_response(
            result.get("solutions"),
            candidates,
        )

        if not _validate_clusters(reviewed, candidates):
            GEMINI_RUNTIME["last_failure"] = (
                "Gemini clustering audit returned an invalid or incomplete cluster set."
            )
            print(
                "⚠️ Gemini clustering audit returned an invalid cluster set."
            )
            return None

        GEMINI_RUNTIME["requests_used"] += 1
        GEMINI_RUNTIME["last_failure"] = ""
        return reviewed

    except (requests.RequestException, json.JSONDecodeError) as exc:
        GEMINI_RUNTIME["last_failure"] = (
            f"Gemini clustering audit error: {exc}"
        )
        print(f"⚠️ Gemini clustering audit error: {exc}")
        return None
    except Exception as exc:
        GEMINI_RUNTIME["last_failure"] = (
            f"Gemini clustering audit error: {exc}"
        )
        print(f"⚠️ Gemini clustering audit error: {exc}")
        return None


def _merge_identical_semantic_keys(clusters):
    """Merge clusters that Gemini itself labeled with the same semantic key."""
    merged = []
    positions = {}

    for cluster in clusters:
        language = _normalize_semantic_label(cluster.get("language", ""))
        key = _normalize_semantic_label(
            cluster.get("approach_key", "")
        )
        name = _normalize_semantic_label(
            cluster.get("approach_name", "")
        )
        merge_key = (language, key, name)

        if key and name and merge_key in positions:
            target = merged[positions[merge_key]]
            target["submission_ids"] = list(
                dict.fromkeys(
                    target.get("submission_ids", [])
                    + cluster.get("submission_ids", [])
                )
            )
            target["cluster_reason"] = (
                target.get("cluster_reason", "").rstrip()
                + " "
                + cluster.get("cluster_reason", "").strip()
            ).strip()
        else:
            positions[merge_key] = len(merged)
            merged.append(cluster)

    return merged


def gemini_cluster_problem(question, candidates):
    """
    Ask Gemini to identify genuinely different algorithmic approaches for one
    problem. Equivalent code variants should be merged. A suspiciously
    over-split result receives a second, stricter audit before it can affect
    GitHub.
    """
    if not candidates:
        return []

    if not GEMINI_API_KEY:
        GEMINI_RUNTIME["blocked"] = True
        GEMINI_RUNTIME["last_failure"] = "GEMINI_API_KEY is not configured."
        return None

    if GEMINI_RUNTIME["blocked"]:
        return None

    if GEMINI_RUNTIME["requests_used"] >= MAX_GEMINI_REQUESTS_PER_DAY:
        GEMINI_RUNTIME["blocked"] = True
        GEMINI_RUNTIME["last_failure"] = "Daily Gemini request budget reached."
        return None

    problem_text = html_to_text(question.get("content", ""))
    if len(problem_text) > 10000:
        problem_text = problem_text[:10000]

    candidate_sections = []
    for index, candidate in enumerate(candidates, start=1):
        code = candidate.get("code", "")
        truncated = False
        if len(code) > 12000:
            code = code[:12000]
            truncated = True

        candidate_sections.append(
            "\n".join(
                [
                    f"CANDIDATE {index}",
                    f"submission_id: {candidate['submission_id']}",
                    f"language: {candidate['language']}",
                    f"timestamp: {candidate.get('timestamp', '')}",
                    f"code_truncated: {truncated}",
                    "code:",
                    code,
                ]
            )
        )

    prompt = f"""
You are an expert algorithms educator and code reviewer.

We are rebuilding the user's GitHub archive from ALL accepted submissions
for ONE LeetCode problem. Identify genuinely different ALGORITHMIC APPROACHES,
not merely different source-code versions.

ARCHIVE POLICY — BE CONSERVATIVE:
- Store one approach per core algorithmic idea.
- Different variable names, formatting, comments, loop syntax, helper methods,
  harmless refactors, or equivalent expressions are NOT new approaches.
- Equivalent implementations using the same main data structure and same core
  reasoning are ONE approach.
- Create a new approach ONLY when there is a concrete change in the core
  strategy, data structure, mathematical property, traversal/search method,
  or asymptotic technique.
- When uncertain, MERGE rather than split.
- Different programming languages remain separate approaches.

Examples for Two Sum:
- nested loops / brute force = one approach
- hash map complement lookup = one approach
- sorting + two pointers = one approach
- Five small variations of hash-map code MUST remain ONE hash-map approach.

Do not try to make the number of clusters equal to the number of candidates.
The expected result is usually much smaller than the number of submissions.

PROBLEM
=======
{problem_text}

TOPICS
======
{", ".join(tag.get("name", "") for tag in question.get("topicTags", []) if tag.get("name"))}

ACCEPTED SUBMISSION CANDIDATES
==============================
{"\n\n".join(candidate_sections)}

TASK
====
1. Cluster every candidate into exactly one semantic approach.
2. Merge implementation variants of the same approach.
3. Use the representative submission that best demonstrates each approach;
   prefer the earliest accepted candidate when there is no meaningful reason
   to choose another.
4. For every cluster, include ALL submission IDs that belong to it.
5. Give a concrete cluster_reason explaining why the submissions share one
   algorithmic idea.
6. Generate the high-quality explanation for the REPRESENTATIVE CODE ONLY.
7. Before producing JSON, internally audit the clustering for over-splitting.

RETURN ONLY VALID JSON using the same structure as requested below.

{{
  "solutions": [
    {{
      "approach_key": "stable-short-semantic-key",
      "approach_name": "Human-readable algorithmic approach",
      "language": "Java",
      "submission_ids": ["..."],
      "representative_submission_id": "...",
      "cluster_reason": "Concrete reason these submissions are one approach.",
      "analysis": {{
        "pattern": "...",
        "problem_summary": "...",
        "intuition": "...",
        "approach": ["step 1", "step 2", "step 3", "step 4"],
        "why_it_works": "...",
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "key_takeaway": "...",
        "time_explanation": "...",
        "space_explanation": "..."
      }}
    }}
  ]
}}

VALIDATION RULES:
- Every candidate submission_id appears exactly once.
- representative_submission_id belongs to its own cluster.
- language exactly matches the representative candidate.
- Never split a core algorithm merely because code text differs.
- Never merge different languages.
- Never invent an optimization or data structure.
- Prefer merging when the distinction is only implementation style.
"""

    try:
        response = _gemini_post_with_retry(
            prompt=prompt,
            timeout=120,
        )

        if response is None:
            return None

        body = response.json()
        output_text = _parse_gemini_text(body)
        if not output_text:
            GEMINI_RUNTIME["last_failure"] = "Gemini returned no text output."
            return None

        result = json.loads(output_text)
        clusters = _coerce_cluster_response(
            result.get("solutions"),
            candidates,
        )

        if not _validate_clusters(clusters, candidates):
            GEMINI_RUNTIME["last_failure"] = (
                "Gemini returned an invalid or incomplete semantic clustering."
            )
            print(
                "⚠️ Gemini returned an invalid or incomplete semantic clustering."
            )
            return None

        # Gemini successfully completed the primary clustering request.
        GEMINI_RUNTIME["requests_used"] += 1
        GEMINI_RUNTIME["last_failure"] = ""

        clusters = _merge_identical_semantic_keys(clusters)

        if _cluster_has_weak_separation(clusters, candidates):
            print(
                "   ⚠️ Primary clustering looks over-split; requesting a strict "
                "semantic merge audit..."
            )

            reviewed = _gemini_post_cluster_review(
                question,
                candidates,
                clusters,
            )

            if reviewed is None:
                return None

            clusters = _merge_identical_semantic_keys(reviewed)

            if _cluster_has_weak_separation(clusters, candidates):
                GEMINI_RUNTIME["last_failure"] = (
                    "Gemini still returned an over-split clustering after the strict audit."
                )
                print(
                    "⚠️ Clustering remains ambiguous after the audit; "
                    "historical problem will be retried instead of being written incorrectly."
                )
                return None

        return clusters

    except (requests.RequestException, json.JSONDecodeError) as exc:
        GEMINI_RUNTIME["last_failure"] = f"Gemini clustering error: {exc}"
        print(f"⚠️ Gemini clustering error: {exc}")
        return None
    except Exception as exc:
        GEMINI_RUNTIME["last_failure"] = f"Gemini clustering error: {exc}"
        print(f"⚠️ Gemini clustering error: {exc}")
        return None


def load_existing_solution_catalog(folder):
    """Load stored solution files, language, and any prior analysis."""
    catalog = []
    if not folder.exists():
        return catalog

    metadata = read_metadata(folder)
    metadata_solutions = metadata.get("solutions", [])
    by_filename = {
        item.get("filename"): item
        for item in metadata_solutions
        if isinstance(item, dict) and item.get("filename")
    } if isinstance(metadata_solutions, list) else {}

    for path in solution_files_in_folder(folder):
        try:
            code = path.read_text(encoding="utf-8")
        except Exception:
            continue

        item = by_filename.get(path.name, {})
        language = best_known_language(
            item.get("language"),
            path.name,
            metadata.get("language"),
        )
        catalog.append({
            "filename": path.name,
            "language": language,
            "fingerprint": solution_fingerprint(code, language),
            "code": code,
            "analysis": item.get("analysis") if isinstance(item, dict) else None,
        })

    return catalog


def rebuild_problem_from_clusters(question, candidates, clusters):
    """Reconcile one problem while preserving existing explanations whenever possible."""
    number = int(question["questionFrontendId"])
    folder_name = f"{number:04d}-{safe_slug(question['title'])}"
    folder = SOLUTIONS_DIR / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    readme_path = folder / "README.md"
    metadata_path = folder / "metadata.json"

    candidate_map = {str(item["submission_id"]): item for item in candidates}
    existing_catalog = load_existing_solution_catalog(folder)
    old_metadata = read_metadata(folder)
    try:
        old_readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    except Exception:
        old_readme_text = ""

    existing_blocks = extract_existing_solution_blocks(old_readme_text)
    old_analysis_by_filename = {}
    old_solutions = old_metadata.get("solutions", [])
    if isinstance(old_solutions, list):
        for item in old_solutions:
            if isinstance(item, dict) and item.get("filename") and item.get("analysis"):
                old_analysis_by_filename[item["filename"]] = item["analysis"]

    existing_order = [item["filename"] for item in existing_catalog]
    selected = []
    used_existing_files = set()

    for index, cluster in enumerate(clusters, start=1):
        cluster_ids = [str(x) for x in cluster.get("submission_ids", [])]
        representative_id = str(cluster["representative_submission_id"])
        cluster_candidates = [candidate_map[item_id] for item_id in cluster_ids if item_id in candidate_map]

        reuse = None
        for existing in existing_catalog:
            if existing["filename"] in used_existing_files:
                continue
            if any(existing["fingerprint"] == candidate["exact_fingerprint"] for candidate in cluster_candidates):
                reuse = existing
                break

        if reuse:
            code_filename = reuse["filename"]
            used_existing_files.add(code_filename)
            matched_candidate = next(
                candidate for candidate in cluster_candidates
                if candidate["exact_fingerprint"] == reuse["fingerprint"]
            )
            stored_code = reuse["code"]
            analysis = reuse.get("analysis") or old_analysis_by_filename.get(code_filename) or cluster.get("analysis")
            preserved_block = existing_blocks.get(code_filename)
        else:
            representative = candidate_map[representative_id]
            extension = file_extension(representative["language"])
            code_filename = f"solution.{extension}" if index == 1 else f"solution-{index}.{extension}"
            stored_code = representative["code"]
            matched_candidate = representative
            analysis = cluster.get("analysis")
            preserved_block = None

        language = best_known_language(matched_candidate.get("language"), code_filename)
        (folder / code_filename).write_text(stored_code, encoding="utf-8")

        selected.append({
            "analysis": analysis,
            "submission": {
                "lang": language,
                "runtime": matched_candidate.get("runtime"),
                "runtimeDisplay": matched_candidate.get("runtimeDisplay"),
                "memory": matched_candidate.get("memory"),
                "memoryDisplay": matched_candidate.get("memoryDisplay"),
            },
            "code_filename": code_filename,
            "approach_key": cluster.get("approach_key", ""),
            "approach_name": cluster.get("approach_name", ""),
            "submission_ids": cluster_ids,
            "representative_submission_id": representative_id,
            "solution_hash": matched_candidate["exact_fingerprint"],
            "preserved_readme_block": preserved_block,
        })

    all_existing_reused = (
        bool(existing_catalog)
        and len(existing_catalog) == len(selected)
        and set(used_existing_files) == {item["filename"] for item in existing_catalog}
    )

    if all_existing_reused:
        # Preserve the established solution-file order even if Gemini returns
        # clusters in a different order on another run.
        by_filename = {item["code_filename"]: item for item in selected}
        selected = [by_filename[name] for name in existing_order if name in by_filename]

    keep_names = {item["code_filename"] for item in selected}
    for path in solution_files_in_folder(folder):
        if path.name not in keep_names:
            path.unlink()

    metadata_solutions = []
    for index, item in enumerate(selected, start=1):
        submission = item["submission"]
        language = best_known_language(submission.get("lang"), item["code_filename"])
        metadata_solutions.append({
            "number": index,
            "filename": item["code_filename"],
            "language": language,
            "submission_id": item["representative_submission_id"],
            "submission_ids": item["submission_ids"],
            "solution_hash": item["solution_hash"],
            "approach_key": item["approach_key"],
            "approach_name": item["approach_name"],
            "runtime": submission.get("runtime"),
            "runtime_display": submission.get("runtimeDisplay"),
            "memory": submission.get("memory"),
            "memory_display": submission.get("memoryDisplay"),
            "analysis": item["analysis"],
        })

    languages = list(dict.fromkeys(
        item["language"] for item in metadata_solutions
        if item.get("language") and item["language"] != "Unknown"
    ))
    language_display = " · ".join(languages) or "Unknown"

    metadata = {
        "number": number,
        "title": question["title"],
        "difficulty": question["difficulty"],
        "language": language_display,
        "languages": languages,
        "folder": folder_name,
        "slug": question["titleSlug"],
        "submission_id": selected[0]["representative_submission_id"] if selected else None,
        "runtime": selected[0]["submission"].get("runtime") if selected else None,
        "runtime_display": selected[0]["submission"].get("runtimeDisplay") if selected else None,
        "memory": selected[0]["submission"].get("memory") if selected else None,
        "memory_display": selected[0]["submission"].get("memoryDisplay") if selected else None,
        "solution_count": len(selected),
        "solutions": metadata_solutions,
        "historical_backfill_version": HISTORICAL_BACKFILL_VERSION,
    }

    preserve_full_readme = bool(old_readme_text) and all_existing_reused

    if preserve_full_readme:
        readme_path.write_text(old_readme_text.rstrip() + "\n", encoding="utf-8")
        print("   🛡️ Existing README preserved; only factual metadata labels may be repaired.")
    else:
        readme_path.write_text(create_problem_readme(question, solutions=selected), encoding="utf-8")

    patch_readme_language_fields(readme_path, metadata)
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "folder": folder,
        "selected": selected,
        "exact_candidates": len(candidates),
        "semantic_clusters": len(clusters),
        "new_approaches": sum(1 for item in selected if item["code_filename"] not in existing_order),
        "preserved_existing_readme": preserve_full_readme,
    }


# ============================================================
# README generation
# ============================================================

def format_runtime_memory(submission):
    """Return clean LeetCode runtime and memory display values."""
    runtime_raw = (
        submission.get("runtimeDisplay")
        or submission.get("runtime")
        or "N/A"
    )

    memory_raw = (
        submission.get("memoryDisplay")
        or submission.get("memory")
        or "N/A"
    )

    runtime = str(runtime_raw).strip()
    memory = str(memory_raw).strip()

    if runtime != "N/A" and re.fullmatch(
        r"\d+(?:\.\d+)?",
        runtime,
    ):
        runtime = f"{runtime} ms"

    if memory != "N/A" and re.fullmatch(
        r"\d+(?:\.\d+)?",
        memory,
    ):
        memory_number = float(memory)
        memory = f"{memory_number / 1_000_000:.2f} MB"
        memory = re.sub(r"\.00 MB$", " MB", memory)
        memory = re.sub(r"(\.\d)0 MB$", r"\1 MB", memory)

    return runtime, memory


def _patch_solution_block_language(block, language, code_filename=None):
    """Preserve an existing solution explanation while repairing language/link metadata."""
    if not block:
        return ""

    block = block.rstrip()
    language = language or "Unknown"

    language_re = re.compile(r"^> \*\*Language:\*\*.*$", re.MULTILINE)
    languages_re = re.compile(r"^> \*\*Languages:\*\*.*$", re.MULTILINE)

    if language_re.search(block):
        block = language_re.sub(f"> **Language:** {language}", block, count=1)
    elif languages_re.search(block):
        block = languages_re.sub(f"> **Languages:** {language}", block, count=1)
    else:
        lines = block.splitlines()
        insert_at = 1 if lines and lines[0].startswith("### ") else 0
        lines[insert_at:insert_at] = [f"> **Language:** {language}", ""]
        block = "\n".join(lines)

    if code_filename:
        block = re.sub(
            r"(\]\(\./)[^)]+(\))",
            lambda match: match.group(1) + code_filename + match.group(2),
            block,
        )

    return block.rstrip()


def extract_existing_solution_blocks(readme_text):
    """Extract multi-solution README sections keyed by their linked source filename."""
    blocks = {}
    if not readme_text:
        return blocks

    headings = list(re.finditer(r"(?m)^### .*?Solution \d+.*$", readme_text))
    for index, heading in enumerate(headings):
        start = heading.start()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(readme_text)
        block = readme_text[start:end].strip()
        block = re.split(r"(?m)^## ", block, maxsplit=1)[0].rstrip()
        for filename in re.findall(r"\]\(\./([^)]+)\)", block):
            if filename.startswith("solution"):
                blocks[filename] = block
                break

    return blocks


def patch_readme_language_fields(readme_path, metadata):
    """Repair problem/solution language labels from actual stored source files."""
    if not readme_path.exists():
        return False

    try:
        text = readme_path.read_text(encoding="utf-8")
    except Exception:
        return False

    solutions = metadata.get("solutions", [])
    source_files = solution_files_in_folder(readme_path.parent)
    language_by_filename = {path.name: language_from_filename(path.name) for path in source_files}

    if isinstance(solutions, list):
        for item in solutions:
            if not isinstance(item, dict):
                continue
            filename = str(item.get("filename", "")).strip()
            if not filename:
                continue
            language_by_filename[filename] = best_known_language(
                item.get("language"), filename, metadata.get("language")
            )

    languages = list(dict.fromkeys(lang for lang in language_by_filename.values() if lang != "Unknown"))
    if not languages:
        return False

    display = " · ".join(languages)
    label = "Language" if len(languages) == 1 else "Languages"
    changed = False

    root_patterns = [
        re.compile(r"^(?:>\s*)?\*\*(?:Language|Languages):\*\*.*$", re.MULTILINE),
        re.compile(r"^(?:>\s*)?(?:Language|Languages):\s*.*$", re.MULTILINE),
    ]

    for pattern in root_patterns:
        match = pattern.search(text)
        if match:
            replacement = f"> **{label}:** {display}"
            updated = text[:match.start()] + replacement + text[match.end():]
            if updated != text:
                text = updated
                changed = True
            break
    else:
        lines = text.splitlines()
        heading_index = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
        if heading_index is not None:
            lines[heading_index + 1:heading_index + 1] = ["", f"> **{label}:** {display}", ""]
            text = "\n".join(lines)
            changed = True

    blocks = extract_existing_solution_blocks(text)
    for filename, lang in language_by_filename.items():
        if lang == "Unknown":
            continue
        block = blocks.get(filename)
        if not block:
            continue
        patched = _patch_solution_block_language(block, lang, filename)
        if patched != block:
            text = text.replace(block, patched, 1)
            changed = True

    if changed:
        readme_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return changed


def _solution_block(question, solution, index):
    preserved = solution.get("preserved_readme_block")
    if preserved:
        language = best_known_language(
            solution.get("submission", {}).get("lang"),
            solution.get("code_filename"),
        )
        preserved = _patch_solution_block_language(
            preserved,
            language,
            solution.get("code_filename"),
        )
        preserved = re.sub(
            r"(?m)^### (.*?Solution )\d+(.*)$",
            lambda match: f"### {match.group(1)}{index}{match.group(2)}",
            preserved,
            count=1,
        )
        return preserved

    analysis = solution["analysis"]
    submission = solution["submission"]
    code_filename = solution["code_filename"]
    runtime, memory = format_runtime_memory(submission)
    language = best_known_language(submission.get("lang"), code_filename)

    approach_steps = "\n".join(
        f"{step_index}. {step}"
        for step_index, step in enumerate(
            analysis["approach"],
            start=1,
        )
    )

    label = analysis.get("pattern", f"Solution {index}")

    return f"""### 🧠 Solution {index} — {label}

> **Language:** {language}  
> **Runtime:** `{runtime}`  
> **Memory:** `{memory}`

#### 💡 Intuition

{analysis["intuition"]}

#### 🧠 Algorithmic Pattern

> **{label}**

#### 🚀 Approach

{approach_steps}

#### ✅ Why This Works

{analysis["why_it_works"]}

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **{analysis["time_complexity"]} — {analysis["time_explanation"]}** |
| Space | **{analysis["space_complexity"]} — {analysis["space_explanation"]}** |

#### 💻 Solution

[View the complete {language} solution →](./{code_filename})

#### 🎯 Key Takeaway

{analysis["key_takeaway"]}
"""


def create_problem_readme(
    question,
    submission=None,
    analysis=None,
    code_filename=None,
    solutions=None,
):
    number = question.get(
        "questionFrontendId",
        "",
    )

    title = question.get(
        "title",
        "LeetCode Problem",
    )

    slug = question.get(
        "titleSlug",
        "",
    )

    difficulty = question.get(
        "difficulty",
        "Unknown",
    )

    tags = [
        tag.get("name", "")
        for tag in question.get("topicTags", [])
        if tag.get("name")
    ]

    tags_display = (
        " · ".join(tags)
        if tags
        else "Not specified"
    )

    if solutions is None:
        solutions = [
            {
                "analysis": analysis,
                "submission": submission or {},
                "code_filename": code_filename or "solution.txt",
            }
        ]

    leetcode_url = (
        "https://leetcode.com/problems/"
        f"{slug}/"
    )

    first_analysis = solutions[0]["analysis"]
    problem_summary = first_analysis["problem_summary"]

    if len(solutions) == 1:
        solution = solutions[0]
        analysis = solution["analysis"]
        submission_data = solution["submission"]
        code_filename = solution["code_filename"]
        language = language_name(submission_data.get("lang"))
        runtime, memory = format_runtime_memory(submission_data)

        approach_steps = "\n".join(
            f"{step_index}. {step}"
            for step_index, step in enumerate(
                analysis["approach"],
                start=1,
            )
        )

        return f"""# 🧩 {number}. {title}

> **Difficulty:** {difficulty_badge(difficulty)}  
> **Topics:** {tags_display}  
> **Language:** {language}

[🔗 View Problem on LeetCode]({leetcode_url})

---

## 📝 Problem

{problem_summary}

---

## 💡 Intuition

{analysis["intuition"]}

---

## 🧠 Algorithmic Pattern

> **{analysis["pattern"]}**

---

## 🚀 Approach

{approach_steps}

---

## ✅ Why This Works

{analysis["why_it_works"]}

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **{analysis["time_complexity"]} — {analysis["time_explanation"]}** |
| Space | **{analysis["space_complexity"]} — {analysis["space_explanation"]}** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `{runtime}` |
| Memory | `{memory}` |

---

## 💻 Solution

[View the complete {language} solution →](./{code_filename})

---

## 🎯 Key Takeaway

{analysis["key_takeaway"]}

---

## 🔗 Useful Links

- [LeetCode Problem]({leetcode_url})
- [My Solution](./{code_filename})

---

⭐ Automatically synchronized from an accepted LeetCode submission.
"""

    solution_sections = "\n---\n\n".join(
        _solution_block(question, solution, index)
        for index, solution in enumerate(
            solutions,
            start=1,
        )
    )

    languages = sorted(
        {
            language_name(solution["submission"].get("lang"))
            for solution in solutions
        }
    )
    language_display = " · ".join(languages)

    takeaway = first_analysis["key_takeaway"]

    if len(solutions) > 1:
        takeaway = (
            f"This repository currently contains {len(solutions)} unique approaches for this problem. "
            "Comparing them makes the trade-off between their time, space, and implementation ideas easier to see."
        )

    return f"""# 🧩 {number}. {title}

> **Difficulty:** {difficulty_badge(difficulty)}  
> **Topics:** {tags_display}  
> **Solutions:** {len(solutions)} unique approach(es)  
> **Languages:** {language_display}

[🔗 View Problem on LeetCode]({leetcode_url})

---

## 📝 Problem

{problem_summary}

---

## 🛠️ Solutions

This folder contains **{len(solutions)} unique accepted implementation(s)** for the same problem. Repeated submissions of identical code are ignored automatically.

{solution_sections}

---

## 🎯 Key Takeaway

{takeaway}

---

## 🔗 Useful Links

- [LeetCode Problem]({leetcode_url})
- [Solutions in this folder](.)

---

⭐ Automatically synchronized from accepted LeetCode submissions.
"""


# ============================================================
# Historical backfill
# ============================================================

def merge_discovered_problems(
    historical,
    discovered_questions,
):
    """Add newly discovered solved problems to the persisted backfill queue."""
    existing = {
        str(
            item.get(
                "titleSlug",
                "",
            )
        ): item
        for item in historical.get(
            "problems",
            []
        )
        if isinstance(item, dict)
        and item.get("titleSlug")
    }

    for question in discovered_questions:
        slug = str(
            question.get(
                "titleSlug",
                "",
            )
        ).strip()

        if not slug:
            continue

        if slug not in existing:
            entry = {
                "titleSlug": slug,
                "title": question.get(
                    "title",
                    slug,
                ),
                "frontendId": question.get(
                    "frontendId",
                    "",
                ),
                "difficulty": question.get(
                    "difficulty",
                    "Unknown",
                ),
                "lastSubmittedAt": question.get(
                    "lastSubmittedAt",
                    "",
                ),
            }

            historical["problems"].append(
                entry
            )
            existing[slug] = entry


def monitor_new_accepted_submissions(
    state,
    username,
):
    """
    Watch recent accepted submissions without importing them individually.

    During historical backfill, only problems that have ALREADY been fully
    scanned are eligible for the live queue. Submissions for future historical
    problems are intentionally left for their normal full-history scan.

    When the historical pass is complete, every unseen accepted submission can
    be queued because the archive has already scanned all prior history.
    """
    historical = state["historical_backfill"]

    try:
        recent = get_recent_accepted(
            username,
            limit=RECENT_AC_FALLBACK_LIMIT,
        )
    except Exception as exc:
        print(f"   ⚠️ Could not monitor recent accepted submissions: {exc}")
        return 0

    all_processed = {
        str(x)
        for x in state.get("processed_submission_ids", [])
    }
    all_processed.update(
        str(x)
        for x in historical.get("processed_submission_ids", [])
    )

    problems = historical.get("problems", [])
    problem_index = int(historical.get("problem_index", 0) or 0)

    if historical.get("complete", False):
        # Once the historical archive is complete, an accepted submission can
        # belong to a brand-new solved problem that was not present when the
        # historical list was built. Those should also enter the safe queue.
        eligible_slugs = None
    else:
        eligible_slugs = {
            str(item.get("titleSlug", "")).strip()
            for item in problems[:problem_index]
            if isinstance(item, dict) and item.get("titleSlug")
        }

    pending = historical.get("pending_new_problems", [])
    if not isinstance(pending, list):
        pending = []

    by_slug = {}
    for item in pending:
        if not isinstance(item, dict):
            continue
        slug = str(item.get("titleSlug", "")).strip()
        if not slug:
            continue
        ids = item.get("submission_ids", [])
        if not isinstance(ids, list):
            ids = []
        by_slug[slug] = {
            "titleSlug": slug,
            "title": item.get("title", slug),
            "submission_ids": [str(x) for x in ids],
        }

    queued = 0
    for submission in recent:
        submission_id = str(submission.get("id", "")).strip()
        slug = str(submission.get("titleSlug", "")).strip()
        if not submission_id or not slug:
            continue
        if submission_id in all_processed:
            continue
        if eligible_slugs is not None and slug not in eligible_slugs:
            continue

        entry = by_slug.setdefault(
            slug,
            {
                "titleSlug": slug,
                "title": submission.get("title", slug),
                "submission_ids": [],
            },
        )

        if submission_id not in entry["submission_ids"]:
            entry["submission_ids"].append(submission_id)
            queued += 1

    historical["pending_new_problems"] = list(by_slug.values())

    print(
        f"📡 Checked {len(recent)} recent accepted submission(s); "
        f"{queued} new submission(s) queued for safe problem-level reconciliation."
    )

    return queued


def reconcile_problem_history(question_stub):
    """
    Reconcile one problem from its COMPLETE accepted-submission history.

    This is the single safe path used both by historical backfill and by the
    live queue. It fetches every accepted submission, removes exact duplicates,
    semantically clusters the remaining implementations, and rebuilds the
    problem folder without unnecessarily replacing existing explanations.
    """
    slug = str(question_stub.get("titleSlug", "")).strip()
    title = question_stub.get("title", slug)
    if not slug:
        raise RuntimeError("Cannot reconcile a problem without titleSlug.")

    full_question = get_question(slug)
    submissions = get_all_accepted_submissions_for_problem(slug)
    print(f"   📥 Found {len(submissions)} accepted submission(s) for this problem.")

    candidate_by_fingerprint = {}
    submission_ids_for_problem = []
    exact_duplicates = 0

    for submission in submissions:
        submission_id = str(submission.get("id", "")).strip()
        if not submission_id:
            continue

        submission_ids_for_problem.append(submission_id)
        details = get_submission_details(submission_id)
        code = details.get("code") or ""
        if not code:
            raise RuntimeError(
                f"Submission {submission_id} returned no source code."
            )

        language = language_name(details.get("lang"))
        fingerprint = solution_fingerprint(code, language)

        if fingerprint in candidate_by_fingerprint:
            exact_duplicates += 1
            continue

        candidate_by_fingerprint[fingerprint] = {
            "submission_id": submission_id,
            "language": language,
            "code": code,
            "timestamp": submission.get("timestamp", ""),
            "runtime": details.get("runtime"),
            "runtimeDisplay": details.get("runtimeDisplay"),
            "memory": details.get("memory"),
            "memoryDisplay": details.get("memoryDisplay"),
            "exact_fingerprint": fingerprint,
        }

    candidates = list(candidate_by_fingerprint.values())

    print(f"   🧹 Exact-code unique candidates: {len(candidates)}")
    print(f"   ♻️ Exact duplicates removed in this problem: {exact_duplicates}")

    if not candidates:
        clusters = []
        problem_result = rebuild_problem_from_clusters(
            full_question,
            [],
            [],
        )
    elif len(candidates) == 1:
        folder_for_candidate = (
            SOLUTIONS_DIR
            / f"{int(full_question['questionFrontendId']):04d}-"
            f"{safe_slug(full_question['title'])}"
        )
        existing_catalog = load_existing_solution_catalog(folder_for_candidate)
        existing_match = next(
            (
                item
                for item in existing_catalog
                if item.get("fingerprint") == candidates[0]["exact_fingerprint"]
            ),
            None,
        )

        if existing_match and existing_match.get("analysis"):
            print(
                "   🛡️ Existing single solution found; reusing its "
                "explanation without a Gemini call."
            )
            analysis = existing_match["analysis"]
        elif existing_match:
            print(
                "   🛡️ Existing single solution found; using deterministic "
                "analysis without a Gemini call."
            )
            analysis = normalize_fallback_analysis(
                fallback_analysis(
                    candidates[0]["code"],
                    [
                        tag.get("name", "")
                        for tag in full_question.get("topicTags", [])
                        if tag.get("name")
                    ],
                    full_question,
                ),
                full_question,
            )
        else:
            print(
                "   🧠 One candidate only; generating the normal Gemini "
                "explanation directly..."
            )
            analysis = ai_analysis(
                full_question,
                candidates[0]["code"],
                [
                    tag.get("name", "")
                    for tag in full_question.get("topicTags", [])
                    if tag.get("name")
                ],
            )
            if analysis is None:
                raise GeminiBackfillPaused(
                    GEMINI_RUNTIME.get("last_failure")
                    or "Gemini did not return a valid explanation."
                )

        clusters = [{
            "approach_key": (
                _normalize_semantic_label(
                    analysis.get("pattern", "single-approach")
                )
                or "single-approach"
            ),
            "approach_name": analysis.get("pattern", "Single Approach"),
            "language": candidates[0]["language"],
            "submission_ids": [candidates[0]["submission_id"]],
            "representative_submission_id": candidates[0]["submission_id"],
            "cluster_reason": (
                "Only one exact-code-unique accepted implementation was "
                "found for this problem."
            ),
            "analysis": analysis,
        }]

        problem_result = rebuild_problem_from_clusters(
            full_question,
            candidates,
            clusters,
        )
    else:
        print(
            f"   🧠 Asking Gemini to cluster {len(candidates)} candidate "
            "implementation(s) into genuinely different approaches..."
        )
        clusters = gemini_cluster_problem(
            full_question,
            candidates,
        )

        if clusters is None:
            raise GeminiBackfillPaused(
                GEMINI_RUNTIME.get("last_failure")
                or "Gemini did not return a valid semantic clustering."
            )

        print(f"   🧠 Semantic approaches found: {len(clusters)}")
        print(
            "   ✅ These are algorithmically distinct approaches; minor code "
            "variations are intentionally merged."
        )

        problem_result = rebuild_problem_from_clusters(
            full_question,
            candidates,
            clusters,
        )

    return {
        "title": title,
        "slug": slug,
        "question": full_question,
        "submissions": submissions,
        "submission_ids": submission_ids_for_problem,
        "clusters": clusters,
        "problem_result": problem_result,
        "exact_duplicates": exact_duplicates,
        "semantic_merged": max(0, len(candidates) - len(clusters)),
        "solutions_stored": len(clusters),
    }


def process_pending_problem_reconciliations(
    state,
    username,
):
    """Safely reconcile queued live submissions one whole problem at a time."""
    historical = state["historical_backfill"]
    pending = historical.get("pending_new_problems", [])
    if not isinstance(pending, list) or not pending:
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "failed": 0,
            "paused": False,
            "processed_problems": 0,
        }

    # One live problem per workflow run keeps Gemini usage predictable and
    # prevents a burst of submissions from competing with the historical job.
    item = pending[0]
    if not isinstance(item, dict):
        historical["pending_new_problems"] = pending[1:]
        save_state(state)
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "failed": 0,
            "paused": False,
            "processed_problems": 0,
        }

    slug = str(item.get("titleSlug", "")).strip()
    title = item.get("title", slug)
    if not slug:
        historical["pending_new_problems"] = pending[1:]
        save_state(state)
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "failed": 0,
            "paused": False,
            "processed_problems": 0,
        }

    print("\n" + "=" * 68)
    print(f"📡 Live reconciliation: {title}")
    print("=" * 68)

    try:
        result = reconcile_problem_history({
            "titleSlug": slug,
            "title": title,
        })

        normal_processed = {
            str(x) for x in state.get("processed_submission_ids", [])
        }
        normal_processed.update(result["submission_ids"])
        state["processed_submission_ids"] = sorted(normal_processed)

        historical_processed = {
            str(x)
            for x in historical.get("processed_submission_ids", [])
        }
        historical_processed.update(result["submission_ids"])
        historical["processed_submission_ids"] = sorted(historical_processed)

        historical["pending_new_problems"] = [
            entry
            for entry in pending
            if str(entry.get("titleSlug", "")).strip() != slug
        ]

        save_state(state)

        print(
            f"   ✅ Live problem reconciled: {title} — "
            f"{result['solutions_stored']} genuinely different approach(es) stored."
        )

        return {
            "imported": result["problem_result"].get("new_approaches", 0),
            "duplicate": result["exact_duplicates"],
            "semantic_merged": result["semantic_merged"],
            "failed": 0,
            "paused": False,
            "processed_problems": 1,
        }

    except GeminiBackfillPaused as exc:
        print(f"   ⏸️ Live reconciliation paused: {exc}")
        sync_runtime_to_state(state)
        save_state(state)
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "failed": 0,
            "paused": True,
            "processed_problems": 0,
        }

    except Exception as exc:
        print(f"   ❌ Live reconciliation failed for {title}: {exc}")
        save_state(state)
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "failed": 1,
            "paused": False,
            "processed_problems": 0,
        }


def historical_backfill(
    state,
    username,
):
    """
    Full historical migration.

    For each problem we:
      1. fetch every accepted submission;
      2. remove exact duplicate source code locally;
      3. send the remaining candidates to Gemini ONCE for semantic clustering;
      4. save one representative solution per genuinely different approach.

    This is deliberately problem-oriented: five code variations of the same
    HashMap approach become one stored solution instead of five.
    """
    historical = state["historical_backfill"]

    # The semantic-clustering migration is different from the old hash-only
    # migration. Force a one-time full rescan so bad historical counts are
    # repaired automatically without asking the user to manually delete state.
    if int(historical.get("version", 0) or 0) != HISTORICAL_BACKFILL_VERSION:
        print(
            "\n🔄 Historical backfill algorithm changed. "
            "Resetting historical progress for one full reconciliation pass."
        )
        historical["version"] = HISTORICAL_BACKFILL_VERSION
        historical["complete"] = False
        historical["problem_index"] = 0
        historical["problems_completed_today"] = 0
        historical["processed_submission_ids"] = []

    if historical.get("complete", False):
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "skipped": 0,
            "failed": 0,
            "paused": False,
            "completed_problems": 0,
        }

    discovered = discover_solved_problems(username)
    merge_discovered_problems(historical, discovered)
    problems = historical.get("problems", [])

    problem_index = int(historical.get("problem_index", 0) or 0)
    if problem_index >= len(problems):
        historical["complete"] = True
        print("🎉 Historical backfill is complete.")
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "skipped": 0,
            "failed": 0,
            "paused": False,
            "completed_problems": 0,
        }

    today_completed = int(historical.get("problems_completed_today", 0) or 0)
    if today_completed >= MAX_HISTORICAL_PROBLEMS_PER_DAY:
        print(
            "⏸️ Daily historical problem budget reached "
            f"({MAX_HISTORICAL_PROBLEMS_PER_DAY})."
        )
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "skipped": 0,
            "failed": 0,
            "paused": True,
            "completed_problems": 0,
        }

    if GEMINI_RUNTIME["blocked"] or GEMINI_RUNTIME["requests_used"] >= MAX_GEMINI_REQUESTS_PER_DAY:
        print("⏸️ Daily Gemini explanation budget is exhausted or Gemini is blocked for today.")
        return {
            "imported": 0,
            "duplicate": 0,
            "semantic_merged": 0,
            "skipped": 0,
            "failed": 0,
            "paused": True,
            "completed_problems": 0,
        }

    imported = 0
    reconciled = 0
    duplicate = 0
    semantic_merged = 0
    skipped = 0
    failed = 0
    completed_problems = 0

    while problem_index < len(problems) and today_completed < MAX_HISTORICAL_PROBLEMS_PER_DAY:
        problem = problems[problem_index]
        slug = str(problem.get("titleSlug", "")).strip()
        title = problem.get("title", slug)

        print("\n" + "=" * 68)
        print(f"📚 Historical problem {problem_index + 1}/{len(problems)}: {title}")
        print("=" * 68)

        try:
            result = reconcile_problem_history(problem)

            # The complete problem reconciliation succeeded, so every accepted
            # submission seen in its history can safely be marked processed.
            normal_processed = set(
                str(x)
                for x in state.get("processed_submission_ids", [])
            )
            normal_processed.update(result["submission_ids"])
            state["processed_submission_ids"] = sorted(normal_processed)

            historical_processed = set(
                str(x)
                for x in historical.get("processed_submission_ids", [])
            )
            historical_processed.update(result["submission_ids"])
            historical["processed_submission_ids"] = sorted(historical_processed)

            # A queued submission for this problem is no longer pending because
            # the full accepted history has now been reconciled.
            historical["pending_new_problems"] = [
                entry
                for entry in historical.get("pending_new_problems", [])
                if str(entry.get("titleSlug", "")).strip() != slug
            ]

            imported += result["problem_result"].get("new_approaches", 0)
            duplicate += result["exact_duplicates"]
            semantic_merged += result["semantic_merged"]

            today_completed += 1
            completed_problems += 1
            historical["problems_completed_today"] = today_completed
            problem_index += 1
            historical["problem_index"] = problem_index

            sync_runtime_to_state(state)
            save_state(state)

            print(
                f"   ✅ Historical problem reconciled: {title} — "
                f"{result['solutions_stored']} genuinely different approach(es) stored."
            )

        except GeminiBackfillPaused as exc:
            print(f"   ⏸️ Pausing historical backfill: {exc}")
            sync_runtime_to_state(state)
            save_state(state)
            break
        except Exception as exc:
            failed += 1
            print(f"   ❌ Failed historical problem {title}: {exc}")
            save_state(state)
            break

    if problem_index >= len(problems):
        historical["complete"] = True
        print("\n🎉 All discovered historical problems have been semantically reconciled.")

    sync_runtime_to_state(state)
    save_state(state)

    return {
        "imported": imported,
        "duplicate": duplicate,
        "semantic_merged": semantic_merged,
        "skipped": skipped,
        "failed": failed,
        "paused": (
            not historical.get("complete", False)
            and (
                today_completed >= MAX_HISTORICAL_PROBLEMS_PER_DAY
                or GEMINI_RUNTIME["requests_used"] >= MAX_GEMINI_REQUESTS_PER_DAY
                or GEMINI_RUNTIME["blocked"]
            )
        ),
        "completed_problems": completed_problems,
    }


# ============================================================
# Incremental synchronization
# ============================================================

def incremental_sync(
    state,
    username,
):
    """Normal post-backfill mode: inspect only unseen recent submissions."""
    processed_ids = set(
        str(x)
        for x in state.get(
            "processed_submission_ids",
            []
        )
    )

    submissions = get_recent_accepted(
        username,
        limit=RECENT_AC_FALLBACK_LIMIT,
    )

    print(
        f"📥 Found {len(submissions)} "
        "accepted submissions in the sync window."
    )

    imported = 0
    duplicate = 0
    semantic_merged = 0
    skipped = 0
    failed = 0

    new_submissions = []

    for submission in submissions:
        submission_id = str(
            submission.get(
                "id",
                "",
            )
        ).strip()

        if not submission_id:
            continue

        if submission_id in processed_ids:
            skipped += 1
            continue

        new_submissions.append(
            submission
        )

    print(
        f"🆕 New accepted submissions to process: "
        f"{len(new_submissions)}"
    )

    for submission in reversed(
        new_submissions
    ):
        submission_id = str(
            submission.get(
                "id",
                "",
            )
        ).strip()

        try:
            result = import_submission(
                submission
            )

            processed_ids.add(
                submission_id
            )

            if result == "duplicate":
                duplicate += 1
            else:
                imported += 1

        except Exception as exc:
            failed += 1

            print(
                f"   ❌ Failed: "
                f"{submission.get('title', 'Unknown')}"
            )
            print(
                f"      {exc}"
            )

    state["processed_submission_ids"] = sorted(
        processed_ids
    )

    save_state(
        state
    )

    return {
        "imported": imported,
        "duplicate": duplicate,
        "skipped": skipped,
        "failed": failed,
        "paused": False,
        "completed_problems": 0,
    }


# ============================================================
# Main README
# ============================================================

def update_main_readme():
    SOLUTIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = []

    for folder in SOLUTIONS_DIR.iterdir():
        if not folder.is_dir():
            continue

        metadata_file = (
            folder / "metadata.json"
        )

        if not metadata_file.exists():
            continue

        try:
            metadata = json.loads(
                metadata_file.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(
                metadata,
                dict,
            ):
                records.append(
                    metadata
                )

        except Exception:
            continue

    records.sort(
        key=lambda item: (
            int(
                item.get(
                    "number",
                    999999,
                )
            )
            if str(
                item.get(
                    "number",
                    "",
                )
            ).isdigit()
            else 999999
        )
    )

    easy = sum(
        1
        for item in records
        if item.get(
            "difficulty"
        ) == "Easy"
    )

    medium = sum(
        1
        for item in records
        if item.get(
            "difficulty"
        ) == "Medium"
    )

    hard = sum(
        1
        for item in records
        if item.get(
            "difficulty"
        ) == "Hard"
    )

    rows = []

    for item in records:
        rows.append(
            "| "
            f"{item.get('number', '—')} | "
            f"[{item.get('title', 'Unknown')}]"
            f"(solutions/{item.get('folder', '')}/) | "
            f"{difficulty_badge(item.get('difficulty'))} | "
            f"{best_known_language(item.get('language'), None, ' · '.join(item.get('languages', [])))} | "
            f"{item.get('solution_count', 1)} |"
        )

    if not rows:
        rows.append(
            "| — | No solutions yet | — | — |"
        )

    table = "\n".join(
        rows
    )

    readme = f"""# 🧠 LeetCode Solutions

> My automatically synchronized collection of LeetCode solutions,
> algorithmic insights, and problem-solving notes.

## 📊 Progress

| Metric | Count |
|---|---:|
| 🧩 Total Solved | **{len(records)}** |
| 🟢 Easy | **{easy}** |
| 🟡 Medium | **{medium}** |
| 🔴 Hard | **{hard}** |

---

## 📚 Problem Archive

| # | Problem | Difficulty | Languages | Approaches |
|---:|---|---|---|---:|
{table}

---

## 🤖 Automatic Synchronization

This repository is connected to my LeetCode account through GitHub Actions.

After an accepted submission is detected, the workflow automatically:

1. Retrieves the submitted code.
2. Retrieves the problem metadata.
3. Analyzes the actual implementation.
4. Generates a concise problem explanation.
5. Generates intuition and step-by-step approach.
6. Explains why the solution works.
7. Determines the algorithmic pattern.
8. Documents time and space complexity.
9. Creates or updates the solution folder, keeping only unique implementations.
10. Updates this archive.

### Workflow

**Solve → Submit → Accepted ✅ → GitHub updates automatically**

---

## 🎯 Purpose

This repository is intended to be useful for both myself and visitors.

The goal is not simply to collect code, but to document the ideas,
patterns, and reasoning behind each solution.

⭐ One problem at a time. One concept at a time.
"""

    Path(
        "README.md"
    ).write_text(
        readme,
        encoding="utf-8",
    )


# ============================================================
# Import a submission
# ============================================================

def read_metadata(
    folder
):
    path = folder / "metadata.json"

    if not path.exists():
        return {}

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        return {}


def canonicalize_code(code):
    """Normalize harmless formatting differences for duplicate detection."""
    normalized = (code or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [
        line.rstrip()
        for line in normalized.split("\n")
        if line.strip()
    ]
    return "\n".join(lines).strip()


def solution_fingerprint(code, language):
    """Create a stable fingerprint for a submitted implementation."""
    payload = (
        str(language_name(language)).strip()
        + "\0"
        + canonicalize_code(code)
    )
    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


def solution_files_in_folder(folder):
    """Return source files that belong to stored solutions."""
    files = []
    for path in folder.iterdir():
        if not path.is_file():
            continue
        if path.name in {"README.md", "metadata.json"}:
            continue
        if path.name.startswith("solution"):
            files.append(path)
    return sorted(files)


def existing_solution_fingerprints(folder):
    """Hash every stored solution using its recorded language."""
    fingerprints = {}
    if not folder.exists():
        return fingerprints

    metadata = read_metadata(folder)
    solution_languages = {}

    for item in metadata.get("solutions", []) if isinstance(metadata.get("solutions"), list) else []:
        if isinstance(item, dict) and item.get("filename"):
            solution_languages[item["filename"]] = item.get("language", "Unknown")

    default_language = metadata.get("language", "Unknown")

    for path in solution_files_in_folder(folder):
        try:
            code = path.read_text(encoding="utf-8")
        except Exception:
            continue

        language = solution_languages.get(
            path.name,
            default_language,
        )

        if not language or language == "Unknown":
            language = path.suffix.lstrip(".") or "Unknown"

        fingerprints[path.name] = solution_fingerprint(
            code,
            language,
        )

    return fingerprints


def next_solution_filename(folder, extension):
    """Use solution.ext for the first solution, then solution-2.ext, solution-3.ext, etc."""
    first = folder / f"solution.{extension}"
    if not first.exists():
        return first.name

    index = 2
    while True:
        candidate = folder / f"solution-{index}.{extension}"
        if not candidate.exists():
            return candidate.name
        index += 1


def migrate_solution_metadata(
    folder,
    question,
):
    """Convert old single-solution metadata into the new solutions list."""
    metadata = read_metadata(folder)
    if not metadata:
        return {
            "number": int(question["questionFrontendId"]),
            "title": question["title"],
            "difficulty": question["difficulty"],
            "language": "Unknown",
            "folder": folder.name,
            "slug": question["titleSlug"],
            "solutions": [],
        }

    if isinstance(metadata.get("solutions"), list):
        return metadata

    solutions = []
    source_files = solution_files_in_folder(folder)

    if source_files:
        path = source_files[0]
        try:
            code = path.read_text(encoding="utf-8")
        except Exception:
            code = ""

        old_language = metadata.get("language") or "Unknown"
        solutions.append(
            {
                "number": 1,
                "filename": path.name,
                "language": old_language,
                "submission_id": metadata.get("submission_id"),
                "solution_hash": solution_fingerprint(
                    code,
                    old_language,
                ),
                "runtime": metadata.get("runtime"),
                "runtime_display": metadata.get("runtime_display"),
                "memory": metadata.get("memory"),
                "memory_display": metadata.get("memory_display"),
            }
        )

    metadata["solutions"] = solutions
    metadata["solution_count"] = len(solutions)
    return metadata


def build_solution_record(
    details,
    filename,
    submission_id,
    fingerprint,
    number,
):
    return {
        "number": number,
        "filename": filename,
        "language": language_name(details.get("lang")),
        "submission_id": submission_id,
        "solution_hash": fingerprint,
        "runtime": details.get("runtime"),
        "runtime_display": details.get("runtimeDisplay"),
        "memory": details.get("memory"),
        "memory_display": details.get("memoryDisplay"),
    }


def analyze_submission(
    question,
    details,
    require_gemini=False,
):
    code = details.get("code")
    if not code:
        raise RuntimeError("LeetCode returned no source code.")

    tags = [
        tag.get("name", "")
        for tag in question.get("topicTags", [])
        if tag.get("name")
    ]

    analysis = ai_analysis(
        question,
        code,
        tags,
    )

    if analysis:
        print("   🧠 Explanation: AI-assisted analysis")
        return analysis

    if require_gemini:
        reason = (
            GEMINI_RUNTIME.get(
                "last_failure"
            )
            or "Gemini did not return a usable explanation."
        )
        raise GeminiBackfillPaused(reason)

    analysis = normalize_fallback_analysis(
        fallback_analysis(
            code,
            tags,
            question,
        ),
        question,
    )

    print("   🧠 Explanation: deterministic fallback analysis")
    return analysis


def solution_readme_block(
    solution,
    index,
    heading_prefix="###",
):
    """Build one additional solution section without rewriting earlier README content."""
    analysis = solution["analysis"]
    submission = solution["submission"]
    code_filename = solution["code_filename"]
    runtime, memory = format_runtime_memory(submission)
    language = language_name(submission.get("lang"))
    pattern = analysis.get("pattern", f"Solution {index}")

    approach_steps = "\n".join(
        f"{step_index}. {step}"
        for step_index, step in enumerate(
            analysis["approach"],
            start=1,
        )
    )

    return f"""{heading_prefix} 🔀 Solution {index} — {pattern}

> **Language:** {language}  
> **Runtime:** `{runtime}`  
> **Memory:** `{memory}`

#### 💡 Intuition

{analysis["intuition"]}

#### 🧠 Algorithmic Pattern

> **{pattern}**

#### 🚀 Approach

{approach_steps}

#### ✅ Why This Works

{analysis["why_it_works"]}

#### ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **{analysis["time_complexity"]} — {analysis["time_explanation"]}** |
| Space | **{analysis["space_complexity"]} — {analysis["space_explanation"]}** |

#### 💻 Solution

[View the complete {language} solution →](./{code_filename})
"""


def append_solution_to_readme(
    readme_path,
    solution,
    index,
):
    """Append an additional unique solution while preserving the existing README."""
    existing = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    block = solution_readme_block(
        solution,
        index,
    )

    # Keep Useful Links and the synchronization footer at the bottom.
    marker = "\n## 🔗 Useful Links\n"
    if marker in existing:
        updated = (
            existing.split(marker, 1)[0].rstrip()
            + "\n\n---\n"
            + block.lstrip().rstrip()
            + "\n"
            + marker
            + existing.split(marker, 1)[1]
        )
    else:
        updated = existing.rstrip() + "\n\n---\n" + block.lstrip().rstrip() + "\n"

    readme_path.write_text(
        updated,
        encoding="utf-8",
    )

def import_submission(
    submission,
    require_gemini=False,
):
    submission_id = str(submission.get("id"))
    title = submission.get("title", "Unknown")
    slug = submission.get("titleSlug", "")

    print(f"\n🔎 Processing: {title}")

    question = get_question(slug)
    details = get_submission_details(submission_id)
    code = details.get("code")

    if not code:
        raise RuntimeError("LeetCode returned no source code.")

    number = int(question["questionFrontendId"])
    folder_name = (
        f"{number:04d}-"
        f"{safe_slug(question['title'])}"
    )
    folder = SOLUTIONS_DIR / folder_name
    folder.mkdir(parents=True, exist_ok=True)

    fingerprint = solution_fingerprint(
        code,
        details.get("lang"),
    )

    existing = existing_solution_fingerprints(folder)
    if fingerprint in set(existing.values()):
        duplicate_file = next(
            name
            for name, value in existing.items()
            if value == fingerprint
        )
        print(
            f"   ⏭️ Duplicate solution detected; "
            f"matches {duplicate_file}. Skipping."
        )
        return "duplicate"

    analysis = analyze_submission(
        question,
        details,
        require_gemini=require_gemini,
    )

    extension = file_extension(details.get("lang"))
    code_filename = next_solution_filename(
        folder,
        extension,
    )
    code_path = folder / code_filename
    code_path.write_text(
        code,
        encoding="utf-8",
    )

    metadata = migrate_solution_metadata(
        folder,
        question,
    )

    previous_count = len(metadata.get("solutions", []))
    solution_number = previous_count + 1

    solution_record = build_solution_record(
        details,
        code_filename,
        submission_id,
        fingerprint,
        solution_number,
    )
    metadata.setdefault("solutions", []).append(solution_record)

    metadata.update(
        {
            "number": number,
            "title": question["title"],
            "difficulty": question["difficulty"],
            "language": best_known_language(details.get("lang"), code_filename, metadata.get("language")),
            "folder": folder_name,
            "slug": question["titleSlug"],
            "submission_id": submission_id,
            "runtime": details.get("runtime"),
            "runtime_display": details.get("runtimeDisplay"),
            "memory": details.get("memory"),
            "memory_display": details.get("memoryDisplay"),
            "solution_count": len(metadata["solutions"]),
        }
    )

    solution_for_readme = {
        "analysis": analysis,
        "submission": {
            "lang": details.get("lang"),
            "runtime": details.get("runtime"),
            "runtimeDisplay": details.get("runtimeDisplay"),
            "memory": details.get("memory"),
            "memoryDisplay": details.get("memoryDisplay"),
        },
        "code_filename": code_filename,
    }

    readme_path = folder / "README.md"

    if previous_count == 0:
        # First unique solution: use the exact single-solution README format.
        readme = create_problem_readme(
            question,
            submission=solution_for_readme["submission"],
            analysis=analysis,
            code_filename=code_filename,
        )
        readme_path.write_text(
            readme,
            encoding="utf-8",
        )
    else:
        # Additional unique solution: preserve the existing README and append
        # the new approach. This protects manually improved explanations.
        append_solution_to_readme(
            readme_path,
            solution_for_readme,
            solution_number,
        )

    (folder / "metadata.json").write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"   ✅ Saved unique solution {solution_number}: "
        f"{folder / code_filename}"
    )
    return "imported"


def repair_placeholder_readmes():
    """Repair older generic READMEs once, without touching good entries."""
    if not SOLUTIONS_DIR.exists():
        return 0

    repaired = 0

    for folder in sorted(SOLUTIONS_DIR.iterdir()):
        if not folder.is_dir():
            continue

        readme_path = folder / "README.md"
        metadata_path = folder / "metadata.json"

        if not readme_path.exists() or not metadata_path.exists():
            continue

        try:
            readme_text = readme_path.read_text(encoding="utf-8")
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        source_files = solution_files_in_folder(folder)
        if (
            len(source_files) > 1
            or (
                isinstance(metadata.get("solutions"), list)
                and len(metadata.get("solutions", [])) > 1
            )
        ):
            continue

        placeholder_markers = (
            "Solve the problem using the submitted implementation.",
            "Recognize the algorithmic pattern and maintain the state required by the implementation.",
            "> **🔎 Algorithmic Approach**",
        )

        if not any(marker in readme_text for marker in placeholder_markers):
            continue

        submission_id = metadata.get("submission_id")
        slug = metadata.get("slug")
        if not submission_id or not slug:
            continue

        try:
            print(
                f"\n🛠️ Repairing placeholder README: "
                f"{metadata.get('title', folder.name)}"
            )

            question = get_question(slug)
            details = get_submission_details(str(submission_id))
            code = details.get("code")
            if not code:
                continue

            analysis = normalize_fallback_analysis(
                fallback_analysis(
                    code,
                    [
                        tag.get("name", "")
                        for tag in question.get("topicTags", [])
                        if tag.get("name")
                    ],
                    question,
                ),
                question,
            )

            extension = file_extension(details.get("lang"))
            existing_files = solution_files_in_folder(folder)
            code_filename = (
                existing_files[0].name
                if existing_files
                else f"solution.{extension}"
            )

            readme = create_problem_readme(
                question,
                submission={
                    "lang": details.get("lang"),
                    "runtime": details.get("runtime"),
                    "runtimeDisplay": details.get("runtimeDisplay"),
                    "memory": details.get("memory"),
                    "memoryDisplay": details.get("memoryDisplay"),
                },
                analysis=analysis,
                code_filename=code_filename,
            )

            readme_path.write_text(
                readme,
                encoding="utf-8",
            )

            metadata["solution_count"] = max(
                1,
                metadata.get("solution_count", 1),
            )
            metadata["runtime"] = details.get("runtime")
            metadata["runtime_display"] = details.get("runtimeDisplay")
            metadata["memory"] = details.get("memory")
            metadata["memory_display"] = details.get("memoryDisplay")

            metadata_path.write_text(
                json.dumps(
                    metadata,
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            repaired += 1
            print(f"   ✅ Repaired: {folder}")

        except Exception as exc:
            print(f"   ⚠️ Could not repair {folder}: {exc}")

    return repaired


def repair_existing_language_fields():
    """Repair legacy/missing language metadata and README labels without changing explanations."""
    if not SOLUTIONS_DIR.exists():
        return 0

    repaired = 0
    for folder in sorted(SOLUTIONS_DIR.iterdir()):
        if not folder.is_dir():
            continue

        metadata_path = folder / "metadata.json"
        readme_path = folder / "README.md"
        if not metadata_path.exists():
            continue

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(metadata, dict):
            continue

        changed = False
        solutions = metadata.get("solutions")
        languages = []

        if isinstance(solutions, list) and solutions:
            for item in solutions:
                if not isinstance(item, dict):
                    continue
                resolved = best_known_language(
                    item.get("language"),
                    item.get("filename"),
                    metadata.get("language"),
                )
                if item.get("language") != resolved:
                    item["language"] = resolved
                    changed = True
                if resolved != "Unknown":
                    languages.append(resolved)
        else:
            for path in solution_files_in_folder(folder):
                lang = language_from_filename(path.name)
                if lang != "Unknown":
                    languages.append(lang)

        languages = list(dict.fromkeys(languages))
        display = " · ".join(languages) if languages else "Unknown"
        if metadata.get("language") != display:
            metadata["language"] = display
            changed = True
        if languages and metadata.get("languages") != languages:
            metadata["languages"] = languages
            changed = True

        if patch_readme_language_fields(readme_path, metadata):
            changed = True

        if changed:
            metadata_path.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            repaired += 1

    return repaired


# ============================================================
# Main
# ============================================================

def main():
    print(
        "🚀 Starting LeetCode synchronization..."
    )

    SOLUTIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    state = load_state()

    reset_daily_historical_budgets(
        state
    )

    username = get_username()

    print(
        f"👤 LeetCode user: {username}"
    )

    repaired = repair_placeholder_readmes()
    language_repairs = repair_existing_language_fields()

    if language_repairs:
        print(f"\n🪄 Repaired language fields in {language_repairs} existing README/metadata set(s).")

    if repaired:
        print(
            f"\n🛠️ Repaired {repaired} placeholder README(s)."
        )

    # Always monitor recent accepted submissions. During historical backfill
    # we only queue submissions for problems that have already been scanned;
    # they are reconciled later as complete problems rather than imported one
    # by one.
    monitor_new_accepted_submissions(
        state,
        username,
    )

    if not state["historical_backfill"].get(
        "complete",
        False,
    ):
        print(
            "\n🧭 Mode: HISTORICAL BACKFILL"
        )
        print(
            f"   Daily problem budget: "
            f"{MAX_HISTORICAL_PROBLEMS_PER_DAY}"
        )
        print(
            f"   Daily Gemini budget: "
            f"{MAX_GEMINI_REQUESTS_PER_DAY}"
        )

        result = historical_backfill(
            state,
            username,
        )

        # The historical job may finish on this run. Reconcile at most one
        # queued live problem afterward, still respecting Gemini safety limits.
        if state["historical_backfill"].get("complete", False):
            live_result = process_pending_problem_reconciliations(
                state,
                username,
            )
            for key in ("imported", "duplicate", "semantic_merged", "failed"):
                result[key] = result.get(key, 0) + live_result.get(key, 0)
            result["paused"] = result.get("paused", False) or live_result.get("paused", False)

    else:
        print(
            "\n🧭 Mode: SAFE INCREMENTAL SYNC"
        )

        result = process_pending_problem_reconciliations(
            state,
            username,
        )

    sync_runtime_to_state(
        state
    )

    save_state(
        state
    )

    update_main_readme()

    print(
        "\n📊 Synchronization summary"
    )
    print(
        f"   🆕 Imported unique solutions: "
        f"{result.get('imported', 0)}"
    )
    print(
        f"   ♻️ Exact duplicate submissions removed: "
        f"{result.get('duplicate', 0)}"
    )
    print(
        f"   🧠 Equivalent code variants merged into existing approaches: "
        f"{result.get('semantic_merged', 0)}"
    )
    print(
        f"   ⏭️ Skipped already processed: "
        f"{result.get('skipped', 0)}"
    )
    print(
        f"   ❌ Failed: "
        f"{result.get('failed', 0)}"
    )

    if state["historical_backfill"].get(
        "complete",
        False,
    ):
        print(
            "   ✅ Historical backfill status: COMPLETE"
        )
    else:
        print(
            "   ⏳ Historical backfill status: IN PROGRESS"
        )

    print(
        f"   🤖 Gemini requests used today: "
        f"{GEMINI_RUNTIME['requests_used']}/"
        f"{MAX_GEMINI_REQUESTS_PER_DAY}"
    )

    pending_count = len(
        state["historical_backfill"].get(
            "pending_new_problems",
            [],
        )
        or []
    )
    if pending_count:
        print(
            f"   📡 Pending live problem reconciliations: {pending_count}"
        )

    if result.get(
        "paused",
        False,
    ):
        print(
            "\n⏸️ Historical backfill paused safely. "
            "It will continue on a later run/day without losing progress."
        )

    if result.get(
        "failed",
        0,
    ):
        print(
            "\n❌ Synchronization completed with errors."
        )
        sys.exit(1)

    print(
        "\n✅ Synchronization completed successfully."
    )


if __name__ == "__main__":
    main()

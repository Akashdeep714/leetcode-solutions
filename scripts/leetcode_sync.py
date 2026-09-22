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
        "complete": False,
        "problems": [],
        "problem_index": 0,
        "processed_submission_ids": [],
        "day": "",
        "problems_completed_today": 0,
        "gemini_requests_used_today": 0,
        "gemini_blocked_today": False,
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
    Reset daily counters when the UTC calendar day changes.

    Because the GitHub Action may run every 15 minutes, these persisted
    counters prevent the historical batch from being repeated every run.
    """
    historical = state["historical_backfill"]
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

            status_code = submission.get("status")

            if (
                status_display == "accepted"
                or status_code == 10
            ) and not submission.get("isPending", False):
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
    ).lower()

    names = {
        "python": "Python",
        "python3": "Python",
        "java": "Java",
        "cpp": "C++",
        "c++": "C++",
        "c": "C",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "csharp": "C#",
        "c#": "C#",
        "go": "Go",
        "golang": "Go",
        "rust": "Rust",
        "kotlin": "Kotlin",
        "swift": "Swift",
        "php": "PHP",
        "ruby": "Ruby",
        "scala": "Scala",
        "mysql": "SQL",
        "mssql": "SQL",
        "oracle": "SQL",
    }

    return names.get(
        language,
        language or "Unknown",
    )


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

    GEMINI_RUNTIME["requests_used"] += 1

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
            timeout=90,
        )

        if response.status_code == 429:
            GEMINI_RUNTIME["blocked"] = True
            GEMINI_RUNTIME["last_failure"] = (
                "Gemini returned HTTP 429 (quota/rate limit)."
            )
            print(
                "⏸️ Gemini returned HTTP 429. "
                "Historical backfill will resume on a later run/day."
            )
            return None

        if response.status_code != 200:
            GEMINI_RUNTIME["last_failure"] = (
                f"Gemini request failed with HTTP {response.status_code}."
            )
            print(
                "⚠️ Gemini request failed: "
                f"HTTP {response.status_code}"
            )
            print(
                response.text[:1000]
            )
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


def _solution_block(question, solution, index):
    analysis = solution["analysis"]
    submission = solution["submission"]
    code_filename = solution["code_filename"]
    runtime, memory = format_runtime_memory(submission)
    language = language_name(submission.get("lang"))

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


def historical_backfill(
    state,
    username,
):
    """
    Scan every accepted submission for each solved problem while limiting
    work to five completed problems or eight Gemini requests per day.

    Historical submission IDs have their own state list so the first backfill
    can rescan older submissions even when an older version of the script
    already marked some IDs as processed.
    """
    historical = state["historical_backfill"]

    if historical.get(
        "complete",
        False,
    ):
        return {
            "imported": 0,
            "duplicate": 0,
            "skipped": 0,
            "failed": 0,
            "paused": False,
            "completed_problems": 0,
        }

    discovered = discover_solved_problems(
        username
    )

    merge_discovered_problems(
        historical,
        discovered,
    )

    problems = historical.get(
        "problems",
        []
    )

    problem_index = int(
        historical.get(
            "problem_index",
            0,
        )
        or 0
    )

    if problem_index >= len(problems):
        historical["complete"] = True
        print(
            "🎉 Historical backfill is complete."
        )

        return {
            "imported": 0,
            "duplicate": 0,
            "skipped": 0,
            "failed": 0,
            "paused": False,
            "completed_problems": 0,
        }

    today_completed = int(
        historical.get(
            "problems_completed_today",
            0,
        )
        or 0
    )

    if today_completed >= MAX_HISTORICAL_PROBLEMS_PER_DAY:
        print(
            "⏸️ Daily historical problem budget reached "
            f"({MAX_HISTORICAL_PROBLEMS_PER_DAY})."
        )
        print(
            "   The next calendar day will continue automatically."
        )

        return {
            "imported": 0,
            "duplicate": 0,
            "skipped": 0,
            "failed": 0,
            "paused": True,
            "completed_problems": 0,
        }

    if (
        GEMINI_RUNTIME["blocked"]
        or GEMINI_RUNTIME["requests_used"]
        >= MAX_GEMINI_REQUESTS_PER_DAY
    ):
        print(
            "⏸️ Daily Gemini explanation budget is exhausted "
            "or Gemini is blocked for today."
        )
        print(
            "   The next calendar day will continue automatically."
        )

        return {
            "imported": 0,
            "duplicate": 0,
            "skipped": 0,
            "failed": 0,
            "paused": True,
            "completed_problems": 0,
        }

    historical_processed = set(
        str(x)
        for x in historical.get(
            "processed_submission_ids",
            []
        )
    )

    imported = 0
    duplicate = 0
    skipped = 0
    failed = 0
    completed_problems = 0

    while (
        problem_index < len(problems)
        and today_completed < MAX_HISTORICAL_PROBLEMS_PER_DAY
    ):
        problem = problems[
            problem_index
        ]

        slug = str(
            problem.get(
                "titleSlug",
                "",
            )
        ).strip()

        title = problem.get(
            "title",
            slug,
        )

        if not slug:
            problem_index += 1
            historical["problem_index"] = problem_index
            continue

        print(
            "\n"
            + "=" * 68
        )
        print(
            f"📚 Historical problem "
            f"{problem_index + 1}/{len(problems)}: {title}"
        )
        print("=" * 68)

        try:
            submissions = get_all_accepted_submissions_for_problem(
                slug
            )

            print(
                f"   📥 Found {len(submissions)} accepted "
                "submission(s) for this problem."
            )

        except Exception as exc:
            failed += 1
            print(
                f"   ❌ Could not retrieve submission history: {exc}"
            )
            break

        problem_complete = True

        for submission in submissions:
            submission_id = str(
                submission.get(
                    "id",
                    "",
                )
            ).strip()

            if not submission_id:
                continue

            if submission_id in historical_processed:
                skipped += 1
                continue

            try:
                result = import_submission(
                    submission,
                    require_gemini=True,
                )

                historical_processed.add(
                    submission_id
                )

                historical["processed_submission_ids"] = sorted(
                    historical_processed
                )

                normal_processed = set(
                    str(x)
                    for x in state.get(
                        "processed_submission_ids",
                        []
                    )
                )

                normal_processed.add(
                    submission_id
                )

                state["processed_submission_ids"] = sorted(
                    normal_processed
                )

                if result == "duplicate":
                    duplicate += 1
                else:
                    imported += 1

                sync_runtime_to_state(
                    state
                )
                save_state(
                    state
                )

            except GeminiBackfillPaused as exc:
                print(
                    "   ⏸️ Pausing historical backfill: "
                    f"{exc}"
                )

                problem_complete = False

                sync_runtime_to_state(
                    state
                )
                save_state(
                    state
                )
                break

            except Exception as exc:
                failed += 1

                print(
                    f"   ❌ Failed historical submission "
                    f"{submission_id}: {exc}"
                )

                # Keep this ID unprocessed so a later run retries it.
                problem_complete = False

                save_state(
                    state
                )
                break

        if not problem_complete:
            break

        today_completed += 1
        completed_problems += 1

        historical["problems_completed_today"] = today_completed

        problem_index += 1
        historical["problem_index"] = problem_index

        sync_runtime_to_state(
            state
        )
        save_state(
            state
        )

        print(
            f"   ✅ Historical problem completed: {title}"
        )

    if problem_index >= len(problems):
        historical["complete"] = True

        print(
            "\n🎉 All discovered historical problems have been scanned."
        )

    sync_runtime_to_state(
        state
    )
    save_state(
        state
    )

    return {
        "imported": imported,
        "duplicate": duplicate,
        "skipped": skipped,
        "failed": failed,
        "paused": (
            not historical.get(
                "complete",
                False,
            )
            and (
                today_completed
                >= MAX_HISTORICAL_PROBLEMS_PER_DAY
                or GEMINI_RUNTIME["requests_used"]
                >= MAX_GEMINI_REQUESTS_PER_DAY
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
            f"{item.get('language', 'Unknown')} | "
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

| # | Problem | Difficulty | Language | Approaches |
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
            "language": metadata.get("language") or language_name(details.get("lang")),
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

    if repaired:
        print(
            f"\n🛠️ Repaired {repaired} placeholder README(s)."
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

    else:
        print(
            "\n🧭 Mode: INCREMENTAL SYNC"
        )

        result = incremental_sync(
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
        f"   ♻️ Duplicate solutions skipped: "
        f"{result.get('duplicate', 0)}"
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

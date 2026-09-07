import json
import os
import re
import sys
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
        memory
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

def load_state():
    if not STATE_FILE.exists():
        return {
            "processed_submission_ids": []
        }

    try:
        data = json.loads(
            STATE_FILE.read_text(
                encoding="utf-8"
            )
        )

        ids = data.get(
            "processed_submission_ids",
            [],
        )

        if not isinstance(ids, list):
            ids = []

        return {
            "processed_submission_ids": [
                str(x)
                for x in ids
            ]
        }

    except Exception:
        return {
            "processed_submission_ids": []
        }


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
    limit=20,
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
):
    code_lower = (
        code or ""
    ).lower()

    tag_text = " ".join(
        tags or []
    ).lower()

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

    return {
        "pattern": "🔎 Algorithmic Approach",
        "intuition": (
            "The solution processes the input while maintaining "
            "the state needed to make the next decision efficiently."
        ),
        "approach": [
            "Initialize the required state.",
            "Traverse the relevant input.",
            "Apply the problem-specific condition.",
            "Update the state and produce the final answer.",
        ],
        "why": (
            "The algorithm maintains only the information needed "
            "to construct the result."
        ),
        "time": "Depends on the implementation",
        "space": "Depends on the implementation",
    }


def normalize_fallback_analysis(
    fallback,
    question,
    code,
    tags,
):
    """Convert deterministic fallback fields to the README schema."""
    fallback = fallback or {}

    approach = fallback.get("approach") or []
    if not isinstance(approach, list):
        approach = [str(approach)]

    return {
        "pattern": fallback.get("pattern", "🔎 Algorithmic Approach"),
        "problem_summary": "Solve the problem using the submitted implementation.",
        "intuition": fallback.get(
            "intuition",
            "The implementation processes the input while maintaining the state needed to construct the answer.",
        ),
        "approach": approach,
        "why_it_works": fallback.get(
            "why_it_works",
            fallback.get(
                "why",
                "The implementation maintains the information required to produce the result.",
            ),
        ),
        "time_complexity": str(
            fallback.get("time_complexity") or fallback.get("time") or "O(n)"
        ),
        "space_complexity": str(
            fallback.get("space_complexity") or fallback.get("space") or "O(1)"
        ),
        "key_takeaway": "Recognize the algorithmic pattern and maintain the state required by the implementation.",
    }


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
            "⚠️ GEMINI_API_KEY is not configured. "
            "Using deterministic fallback."
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

RULES:

1. Explain the ACTUAL submitted implementation.
2. Do not replace it with a different algorithm.
3. Do not invent a data structure or optimization that is not present.
4. problem_summary must be a concise paraphrase of the problem.
5. intuition must explain the core idea in beginner-friendly language.
6. approach must contain 4 to 8 concrete ordered steps.
7. why_it_works must explain why THIS implementation produces the result.
8. time_complexity must contain ONLY the Big-O expression.
   Examples: O(1), O(n), O(log n), O(n log n), O(n^2).
   Do NOT include explanations, punctuation, or extra text.
9. space_complexity must contain ONLY the Big-O expression.
   Examples: O(1), O(n), O(log n).
   Do NOT include explanations, punctuation, or extra text.
10. Account for sorting cost when sorting is used.
11. Account for recursion depth when recursion is used.
12. For hash maps and hash sets, use average-case complexity.
13. Explain numeric techniques such as digit extraction when they are used.
14. Keep the writing concise, clear and educational.
15. Do not copy the complete problem statement.
16. Return JSON only.
17. If the submitted code is brute force, explicitly say that it is brute force.
18. If a more optimal solution exists, do not replace the submitted approach
    with it. You may mention the limitation briefly, but document the
    submitted implementation exactly.
19. If the algorithm cannot be confidently inferred from the code, say so
    instead of inventing an explanation.
20. Prefer correctness over sounding sophisticated.
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

        if response.status_code != 200:
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

def create_problem_readme(
    question,
    submission,
    analysis,
    code_filename,
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
        tag.get(
            "name",
            "",
        )
        for tag in question.get(
            "topicTags",
            [],
        )
        if tag.get("name")
    ]

    language = language_name(
        submission.get("lang")
    )

    runtime_raw = (
        submission.get("runtime")
        or "N/A"
    )

    memory_raw = (
        submission.get("memory")
        or "N/A"
    )

    runtime = str(runtime_raw).strip()
    memory = str(memory_raw).strip()

    # LeetCode normally returns values such as "64 ms" and "19.6 MB".
    # Add the expected unit only when LeetCode returns a bare numeric value.
    if runtime != "N/A" and re.fullmatch(
        r"\d+(?:\.\d+)?",
        runtime
    ):
        runtime = f"{runtime} ms"

    if memory != "N/A" and re.fullmatch(
        r"\d+(?:\.\d+)?",
        memory
    ):
        memory = f"{memory} MB"

    tags_display = (
        " · ".join(tags)
        if tags
        else "Not specified"
    )

    approach_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(
            analysis["approach"],
            start=1,
        )
    )

    leetcode_url = (
        "https://leetcode.com/problems/"
        f"{slug}/"
    )

    return f"""# 🧩 {number}. {title}

> **Difficulty:** {difficulty_badge(difficulty)}  
> **Topics:** {tags_display}  
> **Language:** {language}

[🔗 View Problem on LeetCode]({leetcode_url})

---

## 📝 Problem

{analysis["problem_summary"]}

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
| Time | **{analysis["time_complexity"]}** |
| Space | **{analysis["space_complexity"]}** |

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
            f"{item.get('language', 'Unknown')} |"
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

| # | Problem | Difficulty | Language |
|---:|---|---|---|
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
9. Creates the solution folder.
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

def import_submission(
    submission
):
    submission_id = str(
        submission.get("id")
    )

    title = submission.get(
        "title",
        "Unknown",
    )

    slug = submission.get(
        "titleSlug",
        "",
    )

    print(
        f"\n🔎 Processing: {title}"
    )

    question = get_question(
        slug
    )

    details = get_submission_details(
        submission_id
    )

    code = details.get(
        "code"
    )

    if not code:
        raise RuntimeError(
            "LeetCode returned no source code."
        )

    language = language_name(
        details.get("lang")
    )

    tags = [
        tag.get(
            "name",
            "",
        )
        for tag in question.get(
            "topicTags",
            [],
        )
        if tag.get("name")
    ]

    analysis = ai_analysis(
        question,
        code,
        tags,
    )

    required_fields = {
        "pattern",
        "problem_summary",
        "intuition",
        "approach",
        "why_it_works",
        "time_complexity",
        "space_complexity",
        "key_takeaway",
    }

    if analysis and required_fields.issubset(analysis.keys()):
        explanation_source = (
            "AI-assisted analysis"
        )
    else:
        analysis = normalize_fallback_analysis(
            fallback_analysis(
                code,
                tags,
            ),
            question,
            code,
            tags,
        )

        explanation_source = (
            "deterministic fallback analysis"
        )

    print(
        f"   🧠 Explanation: "
        f"{explanation_source}"
    )

    number = int(
        question[
            "questionFrontendId"
        ]
    )

    folder_name = (
        f"{number:04d}-"
        f"{safe_slug(question['title'])}"
    )

    folder = (
        SOLUTIONS_DIR
        / folder_name
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = file_extension(
        details.get("lang")
    )

    code_filename = (
        f"solution.{extension}"
    )

    code_path = (
        folder
        / code_filename
    )

    code_path.write_text(
        code,
        encoding="utf-8",
    )

    readme = create_problem_readme(
        question,
        {
            "lang": language,
            "runtime": details.get(
                "runtime"
            ),
            "memory": details.get(
                "memory"
            ),
        },
        analysis,
        code_filename,
    )

    (
        folder
        / "README.md"
    ).write_text(
        readme,
        encoding="utf-8",
    )

    metadata = {
        "number": number,
        "title": question[
            "title"
        ],
        "difficulty": question[
            "difficulty"
        ],
        "language": language,
        "folder": folder_name,
        "slug": question[
            "titleSlug"
        ],
        "submission_id": submission_id,
        "runtime": details.get(
            "runtime"
        ),
        "memory": details.get(
            "memory"
        ),
    }

    (
        folder
        / "metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"   ✅ Saved: {folder}"
    )


# ============================================================
# Refresh existing README
# ============================================================

def refresh_existing_submission(
    submission
):
    title = submission.get(
        "title",
        "Unknown",
    )

    slug = submission.get(
        "titleSlug",
        "",
    )

    submission_id = str(
        submission.get("id")
    )

    print(
        f"\n🔄 Refreshing README: {title}"
    )

    question = get_question(
        slug
    )

    details = get_submission_details(
        submission_id
    )

    code = details.get(
        "code"
    )

    if not code:
        raise RuntimeError(
            "No source code returned."
        )

    tags = [
        tag.get(
            "name",
            "",
        )
        for tag in question.get(
            "topicTags",
            [],
        )
        if tag.get("name")
    ]

    analysis = ai_analysis(
        question,
        code,
        tags,
    )

    required_fields = {
        "pattern",
        "problem_summary",
        "intuition",
        "approach",
        "why_it_works",
        "time_complexity",
        "space_complexity",
        "key_takeaway",
    }

    if not analysis or not required_fields.issubset(analysis.keys()):
        analysis = normalize_fallback_analysis(
            fallback_analysis(
                code,
                tags,
            ),
            question,
            code,
            tags,
        )

    number = int(
        question[
            "questionFrontendId"
        ]
    )

    folder_name = (
        f"{number:04d}-"
        f"{safe_slug(question['title'])}"
    )

    folder = (
        SOLUTIONS_DIR
        / folder_name
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = file_extension(
        details.get("lang")
    )

    code_path = (
        folder
        / f"solution.{extension}"
    )

    code_path.write_text(
        code,
        encoding="utf-8",
    )

    readme = create_problem_readme(
        question,
        {
            "lang": details.get(
                "lang"
            ),
            "runtime": details.get(
                "runtime"
            ),
            "memory": details.get(
                "memory"
            ),
        },
        analysis,
        code_path.name,
    )

    (
        folder
        / "README.md"
    ).write_text(
        readme,
        encoding="utf-8",
    )

    metadata = read_metadata(
        folder
    )

    metadata.update(
        {
            "number": number,
            "title": question[
                "title"
            ],
            "difficulty": question[
                "difficulty"
            ],
            "language": language_name(
                details.get("lang")
            ),
            "folder": folder_name,
            "slug": question[
                "titleSlug"
            ],
            "submission_id": submission_id,
            "runtime": details.get(
                "runtime"
            ),
            "memory": details.get(
                "memory"
            ),
        }
    )

    (
        folder
        / "metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"   ✅ Refreshed: {folder}"
    )


def read_metadata(
    folder
):
    path = (
        folder
        / "metadata.json"
    )

    if not path.exists():
        return {}

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return {}


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

    processed_ids = set(
        state.get(
            "processed_submission_ids",
            [],
        )
    )

    username = get_username()

    print(
        f"👤 LeetCode user: {username}"
    )

    submissions = get_recent_accepted(
        username,
        limit=20,
    )

    print(
        f"📥 Found {len(submissions)} "
        "recent accepted submissions."
    )

    imported = 0
    refreshed = 0
    failed = 0

    for submission in reversed(
        submissions
    ):
        submission_id = str(
            submission.get("id")
        )

        if not submission_id:
            continue

        try:
            if submission_id in processed_ids:
                refresh_existing_submission(
                    submission
                )

                refreshed += 1

            else:
                import_submission(
                    submission
                )

                processed_ids.add(
                    submission_id
                )

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

    state[
        "processed_submission_ids"
    ] = sorted(
        processed_ids
    )

    save_state(
        state
    )

    update_main_readme()

    print(
        "\n📊 Synchronization summary"
    )

    print(
        f"   🆕 Imported: {imported}"
    )

    print(
        f"   🔄 Refreshed: {refreshed}"
    )

    print(
        f"   ❌ Failed: {failed}"
    )

    if failed:
        print(
            "\n❌ Synchronization completed "
            "with errors."
        )

        sys.exit(1)

    print(
        "\n✅ Synchronization completed "
        "successfully."
    )


if __name__ == "__main__":
    main()

import html
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
LEETCODE_URL = "https://leetcode.com"

SESSION = os.getenv("LEETCODE_SESSION", "").strip()
CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN", "").strip()

SOLUTIONS_DIR = Path("solutions")
STATE_FILE = Path("sync_state.json")

if not SESSION or not CSRF_TOKEN:
    print("❌ Missing LEETCODE_SESSION or LEETCODE_CSRF_TOKEN.")
    sys.exit(1)


# ============================================================
# LeetCode HTTP client
# ============================================================

client = requests.Session()

client.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": LEETCODE_URL,
        "Referer": f"{LEETCODE_URL}/",
        "X-CSRFToken": CSRF_TOKEN,
    }
)

client.cookies.set(
    "LEETCODE_SESSION",
    SESSION,
    domain="leetcode.com",
)

client.cookies.set(
    "csrftoken",
    CSRF_TOKEN,
    domain="leetcode.com",
)


def graphql(query, variables=None, operation_name=None):
    payload = {
        "query": query,
        "variables": variables or {},
    }

    if operation_name:
        payload["operationName"] = operation_name

    response = client.post(
        GRAPHQL_URL,
        json=payload,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"LeetCode GraphQL returned HTTP "
            f"{response.status_code}: "
            f"{response.text[:500]}"
        )

    data = response.json()

    if data.get("errors"):
        raise RuntimeError(
            json.dumps(
                data["errors"],
                ensure_ascii=False,
            )
        )

    return data.get("data", {})


# ============================================================
# GraphQL queries
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
query recentAcSubmissions($username: String!, $limit: Int!) {
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
query submissionDetails($submissionId: Int!) {
    submissionDetails(submissionId: $submissionId) {
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
query questionData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
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
# Language information
# ============================================================

LANGUAGE_EXTENSIONS = {
    "python": "py",
    "python3": "py",
    "cpp": "cpp",
    "c++": "cpp",
    "java": "java",
    "javascript": "js",
    "typescript": "ts",
    "c": "c",
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


LANGUAGE_NAMES = {
    "python": "Python",
    "python3": "Python",
    "cpp": "C++",
    "c++": "C++",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "c": "C",
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


def normalize_language_name(language):
    if isinstance(language, dict):
        return str(
            language.get("name") or ""
        )

    return str(language or "")


def get_language_name(language):
    key = normalize_language_name(
        language
    ).lower()

    return LANGUAGE_NAMES.get(
        key,
        normalize_language_name(language)
        or "Unknown",
    )


def get_extension(language):
    key = normalize_language_name(
        language
    ).lower()

    return LANGUAGE_EXTENSIONS.get(
        key,
        "txt",
    )


# ============================================================
# General helpers
# ============================================================

def safe_slug(text):
    value = str(text or "").lower()
    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        value,
    )

    return value.strip("-")


def difficulty_badge(difficulty):
    return {
        "Easy": "🟢 Easy",
        "Medium": "🟡 Medium",
        "Hard": "🔴 Hard",
    }.get(
        difficulty,
        difficulty or "Unknown",
    )


def format_metric(value):
    return str(
        value
        if value not in (None, "")
        else "N/A"
    )


# ============================================================
# State management
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

        if not isinstance(data, dict):
            return {
                "processed_submission_ids": []
            }

        ids = data.get(
            "processed_submission_ids",
            [],
        )

        if not isinstance(ids, list):
            ids = []

        return {
            "processed_submission_ids": [
                str(item)
                for item in ids
            ]
        }

    except (
        json.JSONDecodeError,
        OSError,
    ):
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
# Problem description conversion
# ============================================================

def html_to_markdown(content):
    soup = BeautifulSoup(
        html.unescape(content or ""),
        "html.parser",
    )

    for pre in soup.find_all("pre"):
        code = pre.get_text("\n")

        pre.replace_with(
            soup.new_string(
                "\n```text\n"
                + code
                + "\n```\n"
            )
        )

    for br in soup.find_all("br"):
        br.replace_with("\n")

    text = soup.get_text("\n")

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
# LeetCode API
# ============================================================

def get_username():
    data = graphql(
        USER_STATUS_QUERY,
        operation_name="globalData",
    )

    status = data.get(
        "userStatus"
    ) or {}

    if not status.get("isSignedIn"):
        raise RuntimeError(
            "LeetCode authentication failed. "
            "Your session may have expired."
        )

    username = status.get(
        "username"
    )

    if not username:
        raise RuntimeError(
            "Unable to determine your LeetCode username."
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
    submission_id,
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
            f"for ID {submission_id}."
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
            f"Could not fetch problem "
            f"'{title_slug}'."
        )

    return question


# ============================================================
# Algorithm analyzer
# ============================================================

def analyze_algorithm(
    code,
    tags,
):
    code_lower = (
        code or ""
    ).lower()

    tag_text = " ".join(
        tags or []
    ).lower()

    patterns = []

    def add(pattern):
        if pattern not in patterns:
            patterns.append(
                pattern
            )

    # Sliding Window
    if (
        "sliding window" in tag_text
        or (
            "left" in code_lower
            and "right" in code_lower
            and (
                "window" in code_lower
                or "substring" in tag_text
            )
        )
    ):
        add("Sliding Window")

    # Binary Search
    if (
        "binary search" in tag_text
        or "bisect" in code_lower
        or (
            "mid" in code_lower
            and "left" in code_lower
            and "right" in code_lower
        )
    ):
        add("Binary Search")

    # Two Pointers
    if (
        "two pointers" in tag_text
        or (
            "left" in code_lower
            and "right" in code_lower
            and "while" in code_lower
        )
    ):
        add("Two Pointers")

    # Dynamic Programming
    if (
        "dynamic programming" in tag_text
        or "lru_cache" in code_lower
        or re.search(
            r"\bdp\b",
            code_lower,
        )
        or "memo" in code_lower
    ):
        add("Dynamic Programming")

    # Backtracking
    if (
        "backtracking" in tag_text
        or "backtrack" in code_lower
    ):
        add("Backtracking")

    # BFS
    if (
        "breadth-first search" in tag_text
        or "bfs" in tag_text
        or "popleft(" in code_lower
        or "deque(" in code_lower
    ):
        add("Queue / BFS")

    # DFS
    if (
        "depth-first search" in tag_text
        or "dfs" in tag_text
    ):
        add("DFS")

    # Heap
    if (
        "heap" in tag_text
        or "priority queue" in tag_text
        or "heapq" in code_lower
        or "priorityqueue" in code_lower
    ):
        add("Heap / Priority Queue")

    # Monotonic Stack / Stack
    if "monotonic stack" in tag_text:
        add("Monotonic Stack")

    elif (
        "stack" in tag_text
        or (
            "append(" in code_lower
            and ".pop(" in code_lower
        )
    ):
        add("Stack")

    # Hash Map
    if (
        "hash table" in tag_text
        or "hash map" in tag_text
        or "hashmap" in code_lower
        or "unordered_map" in code_lower
        or "defaultdict" in code_lower
        or "dict(" in code_lower
    ):
        add("Hash Map")

    # Hash Set
    if (
        "hash set" in tag_text
        or "unordered_set" in code_lower
        or "set(" in code_lower
    ):
        add("Hash Set")

    # Sorting
    if (
        "sorting" in tag_text
        or ".sort(" in code_lower
        or "sorted(" in code_lower
    ):
        add("Sorting")

    # Prefix Sum
    if (
        "prefix sum" in tag_text
        or "prefix" in code_lower
    ):
        add("Prefix Sum")

    # Bit Manipulation
    if (
        "bit manipulation" in tag_text
        or "& 1" in code_lower
        or "n & (n - 1)" in code_lower
    ):
        add("Bit Manipulation")

    # Greedy
    if "greedy" in tag_text:
        add("Greedy")

    # Linked List
    if (
        "linked list" in tag_text
        or "->next" in code_lower
        or ".next" in code_lower
    ):
        add("Linked List")

    if not patterns:
        add("Direct Iterative Approach")

    primary = patterns[0]
    supporting = patterns[1:3]

    # --------------------------------------------------------
    # Intuition
    # --------------------------------------------------------

    intuition_map = {
        "Hash Map": (
            "The key idea is to remember useful information from "
            "elements that have already been processed. A hash map "
            "provides O(1) average lookup, allowing the solution to "
            "avoid repeatedly scanning the input."
        ),

        "Hash Set": (
            "The solution mainly needs fast membership checks. "
            "A hash set keeps track of relevant values that have "
            "already been seen, so each lookup can be performed "
            "efficiently."
        ),

        "Two Pointers": (
            "Two pointers reduce unnecessary comparisons by narrowing "
            "the search space from two positions. The pointer that "
            "cannot lead to a valid or better result is moved, "
            "eliminating work as the scan progresses."
        ),

        "Sliding Window": (
            "The solution maintains a moving window over the input. "
            "The right side expands the window, while the left side "
            "moves only when the current window violates the required "
            "condition."
        ),

        "Binary Search": (
            "Because the search space has an exploitable order, each "
            "comparison can eliminate roughly half of the remaining "
            "possibilities. This reduces a linear search to logarithmic "
            "time."
        ),

        "Dynamic Programming": (
            "The problem contains overlapping subproblems. Instead of "
            "solving the same smaller problem repeatedly, the solution "
            "stores previously computed states and reuses them."
        ),

        "Backtracking": (
            "The solution explores possible choices recursively. "
            "Whenever a choice cannot lead to a valid answer, it is "
            "undone so the next possibility can be explored."
        ),

        "Queue / BFS": (
            "The problem can be explored level by level. A queue stores "
            "the next states to visit, ensuring that states at the "
            "current depth are processed before deeper states."
        ),

        "DFS": (
            "The solution explores one path as deeply as possible before "
            "backtracking to another branch. This is useful when states "
            "naturally form a tree or graph."
        ),

        "Heap / Priority Queue": (
            "A priority queue keeps the most important candidate "
            "immediately available. This avoids repeatedly scanning all "
            "candidates when we only need the current minimum or maximum."
        ),

        "Stack": (
            "A stack is useful when the most recently encountered "
            "unresolved element should be processed first. Push and "
            "pop operations make those updates efficient."
        ),

        "Monotonic Stack": (
            "The stack maintains elements in a useful monotonic order. "
            "When the current element resolves previously pending "
            "elements, they can be popped once and never need to be "
            "reconsidered."
        ),

        "Sorting": (
            "Sorting creates an order that exposes relationships between "
            "elements and makes the required comparisons or grouping "
            "easier."
        ),

        "Prefix Sum": (
            "The solution stores cumulative information so later range "
            "or prefix calculations can be answered without recomputing "
            "earlier elements."
        ),

        "Bit Manipulation": (
            "The solution uses properties of binary representation and "
            "bitwise operations to express the required condition "
            "efficiently."
        ),

        "Greedy": (
            "At every step, the solution chooses the best available "
            "local option. The key observation is that these choices "
            "can be combined to produce the required global result."
        ),

        "Linked List": (
            "The solution works directly with node relationships instead "
            "of random-access indexing. Pointer updates allow the list "
            "to be traversed or modified efficiently."
        ),
    }

    intuition = intuition_map.get(
        primary,
        (
            "The solution processes the input systematically while "
            "keeping only the state necessary to make the next decision "
            "efficiently."
        ),
    )

    # --------------------------------------------------------
    # Approach
    # --------------------------------------------------------

    approach_map = {
        "Hash Map": [
            "Create a hash map to store information about previously processed values.",
            "Traverse the input once.",
            "For each element, compute the value or state needed to satisfy the problem.",
            "Use the hash map for a fast average-time lookup.",
            "Return or update the answer when the required condition is met.",
        ],

        "Hash Set": [
            "Create a set for fast average-time membership checks.",
            "Traverse the input and test whether the relevant value has already been seen.",
            "Add new values to the set as the scan progresses.",
            "Return the result when the required condition is satisfied.",
        ],

        "Two Pointers": [
            "Initialize the two pointers at the appropriate positions.",
            "Compare the elements referenced by the pointers.",
            "Move the pointer that cannot contribute to a valid or better result.",
            "Continue until the search space is exhausted or the answer is found.",
        ],

        "Sliding Window": [
            "Initialize the left and right boundaries of the window.",
            "Expand the right side while processing new elements.",
            "When the window becomes invalid, move the left boundary until validity is restored.",
            "Track the required best or valid result while maintaining the window.",
        ],

        "Binary Search": [
            "Initialize the search boundaries.",
            "Calculate the middle position.",
            "Use the ordering property to determine which half can still contain the answer.",
            "Discard the other half and repeat until the answer is found.",
        ],

        "Dynamic Programming": [
            "Define a state representing a smaller subproblem.",
            "Initialize the necessary base cases.",
            "Compute states while reusing previously solved subproblems.",
            "Use the final state to obtain the answer.",
        ],

        "Backtracking": [
            "Choose one available option.",
            "Recursively explore the state created by that choice.",
            "Undo the choice when returning from recursion.",
            "Continue until all necessary choices are explored or a valid answer is found.",
        ],

        "Queue / BFS": [
            "Initialize the queue with the starting state.",
            "Process states in first-in-first-out order.",
            "Generate and enqueue each valid next state.",
            "Continue until the target is reached or the structure is fully explored.",
        ],

        "DFS": [
            "Start from the relevant node or state.",
            "Explore one branch recursively before moving to the next branch.",
            "Track visited state when necessary.",
            "Continue until the target is found or all reachable states are processed.",
        ],

        "Heap / Priority Queue": [
            "Insert the relevant candidates into a priority queue.",
            "Retrieve the highest-priority candidate when needed.",
            "Update the queue with newly relevant candidates.",
            "Continue until the required result has been obtained.",
        ],

        "Stack": [
            "Initialize an empty stack.",
            "Process the input from left to right.",
            "Push unresolved elements onto the stack.",
            "Pop elements when the current value resolves their pending condition.",
        ],

        "Monotonic Stack": [
            "Maintain a stack whose values follow the required monotonic order.",
            "Process each element once.",
            "Pop elements whose pending relationship is resolved by the current element.",
            "Push the current element or its index for future comparisons.",
        ],

        "Sorting": [
            "Sort the input according to the ordering required by the problem.",
            "Traverse the sorted data and exploit the resulting order.",
            "Avoid comparisons that are no longer necessary because of the ordering.",
        ],

        "Prefix Sum": [
            "Build cumulative information while traversing the input.",
            "Use the stored prefix values to calculate required ranges or totals efficiently.",
            "Return the required result after processing the relevant positions.",
        ],

        "Bit Manipulation": [
            "Identify the relevant property of the binary representation.",
            "Apply the required bitwise operation.",
            "Repeat while relevant bits remain to be processed.",
            "Return the resulting value or condition.",
        ],

        "Greedy": [
            "Evaluate the choices available at the current step.",
            "Select the locally optimal choice.",
            "Update the state and continue.",
            "Return the final result after processing all relevant choices.",
        ],

        "Linked List": [
            "Initialize the required node pointers.",
            "Traverse the list through next-pointer relationships.",
            "Update pointers when the problem requires list manipulation.",
            "Return the required node or result.",
        ],
    }

    approach = approach_map.get(
        primary,
        [
            "Initialize the required state.",
            "Traverse the input.",
            "Apply the problem-specific condition at each step.",
            "Update the result and return the final answer.",
        ],
    )

    # --------------------------------------------------------
    # Complexity
    # --------------------------------------------------------

    complexity = {
        "Hash Map": (
            "O(n)",
            "O(n)",
        ),
        "Hash Set": (
            "O(n)",
            "O(n)",
        ),
        "Two Pointers": (
            "O(n)",
            "O(1)",
        ),
        "Sliding Window": (
            "O(n)",
            "O(n)",
        ),
        "Binary Search": (
            "O(log n)",
            "O(1)",
        ),
        "Dynamic Programming": (
            "Depends on the state space",
            "Depends on the state space",
        ),
        "Backtracking": (
            "Depends on the search space",
            "O(n) auxiliary space",
        ),
        "Queue / BFS": (
            "O(n)",
            "O(n)",
        ),
        "DFS": (
            "O(n)",
            "O(n)",
        ),
        "Heap / Priority Queue": (
            "O(n log n)",
            "O(n)",
        ),
        "Stack": (
            "O(n)",
            "O(n)",
        ),
        "Monotonic Stack": (
            "O(n)",
            "O(n)",
        ),
        "Sorting": (
            "O(n log n)",
            "Depends on sorting implementation",
        ),
        "Prefix Sum": (
            "O(n)",
            "O(n)",
        ),
        "Bit Manipulation": (
            "O(1) to O(log n)",
            "O(1)",
        ),
        "Greedy": (
            "O(n) to O(n log n)",
            "Depends on implementation",
        ),
        "Linked List": (
            "O(n)",
            "O(1) auxiliary space",
        ),
    }

    time, space = complexity.get(
        primary,
        (
            "Depends on the implementation",
            "Depends on the implementation",
        ),
    )

    return {
        "primary": primary,
        "supporting": supporting,
        "intuition": intuition,
        "approach": approach,
        "time": time,
        "space": space,
    }


# ============================================================
# Per-problem README
# ============================================================

def create_problem_readme(
    question,
    submission,
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
        tag.get("name", "")
        for tag in question.get(
            "topicTags",
            [],
        )
        if tag.get("name")
    ]

    language = get_language_name(
        submission.get("lang")
    )

    code = submission.get(
        "code",
        "",
    )

    analysis = analyze_algorithm(
        code,
        tags,
    )

    description = html_to_markdown(
        question.get("content", "")
    )

    tags_display = (
        " · ".join(tags[:6])
        if tags
        else "Not specified"
    )

    supporting_display = (
        " · ".join(
            analysis["supporting"]
        )
        if analysis["supporting"]
        else "None"
    )

    approach_steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(
            analysis["approach"],
            start=1,
        )
    )

    runtime = format_metric(
        submission.get("runtime")
    )

    memory = format_metric(
        submission.get("memory")
    )

    leetcode_url = (
        f"{LEETCODE_URL}/problems/{slug}/"
    )

    return f"""# 🧩 {number}. {title}

> **Difficulty:** {difficulty_badge(difficulty)}  
> **Topics:** {tags_display}  
> **Language:** {language}

[🔗 View Problem on LeetCode]({leetcode_url})

---

## 📝 Problem

{description}

---

## 💡 Intuition

{analysis["intuition"]}

### 🧠 Algorithmic Pattern

| Role | Pattern |
|---|---|
| Primary | **{analysis["primary"]}** |
| Supporting | {supporting_display} |

---

## 🚀 Approach

{approach_steps}

---

## 🔍 Why This Works

The approach avoids unnecessary repeated work by maintaining the
right state or data structure while processing the input.

The key advantage comes from choosing an algorithmic pattern that
reduces the amount of work required at each step.

---

## ⏱️ Complexity

| Metric | Complexity |
|---|---|
| Time | **{analysis["time"]}** |
| Space | **{analysis["space"]}** |

### 📊 LeetCode Performance

| Metric | Result |
|---|---|
| Runtime | `{runtime}` |
| Memory | `{memory}` |

> The Big-O complexity is inferred from the detected algorithmic
> pattern and is intended as a high-level guide.

---

## 💻 Solution

[View the complete {language} solution →](./{code_filename})

---

## 🎯 Key Takeaway

The most valuable part of this problem is recognizing the underlying
pattern and understanding why it reduces unnecessary computation.

---

## 🔗 Useful Links

- [LeetCode Problem]({leetcode_url})
- [My Solution](./{code_filename})

---

⭐ Automatically synchronized from an accepted LeetCode submission.
"""


# ============================================================
# Solution folder / metadata helpers
# ============================================================

def solution_folder_name(question):
    number = int(
        question["questionFrontendId"]
    )

    return (
        f"{number:04d}-"
        f"{safe_slug(question['title'])}"
    )


def find_solution_code(folder):
    if not folder.exists():
        return None

    candidates = sorted(
        folder.glob("solution.*")
    )

    return (
        candidates[0]
        if candidates
        else None
    )


def read_metadata(folder):
    metadata_path = (
        folder / "metadata.json"
    )

    if not metadata_path.exists():
        return {}

    try:
        data = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        return (
            data
            if isinstance(data, dict)
            else {}
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return {}


def save_metadata(
    folder,
    metadata,
):
    (folder / "metadata.json").write_text(
        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


# ============================================================
# Import a new submission
# ============================================================

def import_submission(submission):
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

    if details.get(
        "statusDisplay"
    ) != "Accepted":
        raise RuntimeError(
            f"Submission {submission_id} "
            "is not Accepted."
        )

    code = details.get(
        "code"
    )

    if not code or not code.strip():
        raise RuntimeError(
            f"No source code returned "
            f"for submission {submission_id}."
        )

    language = normalize_language_name(
        details.get("lang")
    )

    folder_name = solution_folder_name(
        question
    )

    folder = (
        SOLUTIONS_DIR
        / folder_name
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = get_extension(
        language
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

    submission_for_readme = {
        "lang": language,
        "code": code,
        "runtime": details.get(
            "runtime"
        ),
        "memory": details.get(
            "memory"
        ),
    }

    readme = create_problem_readme(
        question,
        submission_for_readme,
        code_filename,
    )

    (
        folder / "README.md"
    ).write_text(
        readme,
        encoding="utf-8",
    )

    metadata = {
        "number": question[
            "questionFrontendId"
        ],
        "title": question[
            "title"
        ],
        "difficulty": question[
            "difficulty"
        ],
        "language": get_language_name(
            language
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

    save_metadata(
        folder,
        metadata,
    )

    print(
        f"   ✅ Saved: solutions/{folder_name}"
    )

    return True


# ============================================================
# Refresh README for an existing solution
# ============================================================

def refresh_existing_solution(
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

    print(
        f"\n🔄 Refreshing README: {title}"
    )

    question = get_question(
        slug
    )

    folder_name = solution_folder_name(
        question
    )

    folder = (
        SOLUTIONS_DIR
        / folder_name
    )

    code_path = find_solution_code(
        folder
    )

    if not code_path:
        print(
            "   ⚠️ Existing solution file "
            "not found. Re-importing."
        )

        return import_submission(
            submission
        )

    metadata = read_metadata(
        folder
    )

    code = code_path.read_text(
        encoding="utf-8"
    )

    language = metadata.get(
        "language",
        code_path.suffix.lstrip("."),
    )

    submission_for_readme = {
        "lang": language,
        "code": code,
        "runtime": metadata.get(
            "runtime",
            "Previously recorded",
        ),
        "memory": metadata.get(
            "memory",
            "Previously recorded",
        ),
    }

    readme = create_problem_readme(
        question,
        submission_for_readme,
        code_path.name,
    )

    (
        folder / "README.md"
    ).write_text(
        readme,
        encoding="utf-8",
    )

    return True


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

        metadata = read_metadata(
            folder
        )

        if metadata:
            records.append(
                metadata
            )

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
            f"| {item.get('number', '—')} "
            f"| [{item.get('title', 'Unknown')}]"
            f"(solutions/{item.get('folder', '')}/) "
            f"| {difficulty_badge(item.get('difficulty'))} "
            f"| {item.get('language', 'Unknown')} |"
        )

    if not rows:
        rows.append(
            "| — | Your first solution will appear here | — | — |"
        )

    table = "\n".join(rows)

    readme = f"""# 🧠 LeetCode Solutions

> A continuously growing collection of my LeetCode solutions,
> algorithmic patterns, explanations, and problem-solving notes.

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

## 🔄 Automatic Synchronization

This repository is synchronized automatically using **GitHub Actions**.

Whenever an accepted LeetCode submission is detected, the workflow:

1. Retrieves the accepted submission.
2. Fetches the problem statement and topic tags.
3. Saves the submitted source code.
4. Generates a visitor-friendly problem README.
5. Updates this problem archive.
6. Commits the changes automatically.

### Workflow

**Solve → Submit → Accepted ✅ → GitHub automatically updates**

---

## 🎯 Purpose

This repository is more than a backup of code.

Each solution is organized so visitors can understand the problem,
the core idea, the algorithmic pattern, the complexity, and the implementation.

⭐ One problem at a time. One concept at a time.
"""

    Path("README.md").write_text(
        readme,
        encoding="utf-8",
    )


# ============================================================
# Entry point
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

    imported_count = 0
    refreshed_count = 0
    failed_count = 0

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
                refresh_existing_solution(
                    submission
                )

                refreshed_count += 1

            else:
                import_submission(
                    submission
                )

                processed_ids.add(
                    submission_id
                )

                imported_count += 1

        except Exception as exc:
            failed_count += 1

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
        f"   🆕 Imported: {imported_count}"
    )

    print(
        f"   🔄 Refreshed: {refreshed_count}"
    )

    print(
        f"   ❌ Failed: {failed_count}"
    )

    if failed_count:
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

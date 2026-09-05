import html
import json
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup


GRAPHQL_URL = "https://leetcode.com/graphql/"
LEETCODE_URL = "https://leetcode.com"

SESSION = os.getenv("LEETCODE_SESSION", "").strip()
CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN", "").strip()

SOLUTIONS_DIR = Path("solutions")
STATE_FILE = Path("sync_state.json")


if not SESSION or not CSRF_TOKEN:
    print("❌ Missing LeetCode credentials.")
    sys.exit(1)


# ============================================================
# Session
# ============================================================

client = requests.Session()

client.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": LEETCODE_URL,
    "Referer": LEETCODE_URL + "/",
    "X-CSRFToken": CSRF_TOKEN,
})

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

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise RuntimeError(
            json.dumps(data["errors"], ensure_ascii=False)
        )

    return data.get("data", {})


# ============================================================
# GraphQL
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
    recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
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
# Helpers
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


def safe_slug(text):
    value = text.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def get_state():
    if not STATE_FILE.exists():
        return {
            "processed_submission_ids": []
        }

    try:
        return json.loads(
            STATE_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return {
            "processed_submission_ids": []
        }


def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8",
    )


def load_html_as_markdown(content):
    soup = BeautifulSoup(content or "", "html.parser")

    for pre in soup.find_all("pre"):
        code = pre.get_text("\n")
        pre.replace_with(
            soup.new_string(
                "\n```text\n" + code + "\n```\n"
            )
        )

    for br in soup.find_all("br"):
        br.replace_with("\n")

    text = soup.get_text("\n")
    text = html.unescape(text)

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def difficulty_badge(difficulty):
    return {
        "Easy": "🟢 Easy",
        "Medium": "🟡 Medium",
        "Hard": "🔴 Hard",
    }.get(difficulty, difficulty or "Unknown")


def get_extension(lang):
    return LANGUAGE_EXTENSIONS.get(
        (lang or "").lower(),
        "txt",
    )


def get_language_name(lang):
    return LANGUAGE_NAMES.get(
        (lang or "").lower(),
        lang or "Unknown",
    )


# ============================================================
# Get authenticated account
# ============================================================

def get_username():
    data = graphql(
        USER_STATUS_QUERY,
        operation_name="globalData",
    )

    status = data.get("userStatus") or {}

    if not status.get("isSignedIn"):
        raise RuntimeError(
            "LeetCode authentication failed."
        )

    username = status.get("username")

    if not username:
        raise RuntimeError(
            "Could not determine LeetCode username."
        )

    return username


# ============================================================
# Find accepted submissions
# ============================================================

def get_recent_accepted(username):
    data = graphql(
        RECENT_ACCEPTED_QUERY,
        {
            "username": username,
            "limit": 20,
        },
        operation_name="recentAcSubmissions",
    )

    submissions = data.get(
        "recentAcSubmissionList"
    ) or []

    return submissions


# ============================================================
# Fetch source code
# ============================================================

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

def decode_submission_code(raw_code):
    if not raw_code:
        return None

    try:
        return bytes(
            raw_code,
            "utf-8"
        ).decode(
            "unicode_escape"
        )
    except Exception:
        return raw_code


def extract_submission_code(page):
    """
    LeetCode has changed how submission source is embedded
    several times. Try several known patterns.
    """

    patterns = [
        r"submissionCode\s*:\s*'(.*?)'\s*,\s*editCodeUrl",
        r'"submissionCode"\s*:\s*"((?:\\.|[^"\\])*)"',
        r"submissionCode\s*:\s*'(.*?)'",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            page,
            re.DOTALL,
        )

        if match:
            raw = match.group(1)

            raw = html.unescape(raw)

            try:
                return bytes(
                    raw,
                    "utf-8"
                ).decode(
                    "unicode_escape"
                )
            except Exception:
                return raw

    # Fallback: some pages expose the source
    # in a code/textarea element.
    soup = BeautifulSoup(
        page,
        "html.parser",
    )

    candidates = [
        soup.find(
            "textarea",
            id="submission-code",
        ),
        soup.find(
            "code",
            id="submission-code",
        ),
        soup.find(
            id="submission-code",
        ),
    ]

    for candidate in candidates:
        if candidate:
            text = candidate.get_text()
            if text.strip():
                return text

    return None


def fetch_submission_source(submission):
    submission_id = int(submission.get("id"))

    print("   🔐 Fetching submitted code through LeetCode GraphQL...")

    data = graphql(
        SUBMISSION_DETAILS_QUERY,
        {"submissionId": submission_id},
        operation_name="submissionDetails",
    )

    details = data.get("submissionDetails")

    if not details:
        raise RuntimeError(
            f"LeetCode did not return submission details for {submission_id}"
        )

    if details.get("statusDisplay") != "Accepted":
        raise RuntimeError(
            f"Submission {submission_id} is not Accepted."
        )

    code = details.get("code")

    if not code or not code.strip():
        raise RuntimeError(
            f"No source code returned for submission {submission_id}."
        )

    lang = details.get("lang")

    if isinstance(lang, dict):
        lang_name = lang.get("name", "")
    else:
        lang_name = str(lang or "")

    normalized_details = {
        "id": submission_id,
        "code": code,
        "lang": lang_name,
        "runtime": details.get("runtime"),
        "memory": details.get("memory"),
        "statusDisplay": details.get("statusDisplay"),
    }

    return code, normalized_details


# ============================================================
# Problem details
# ============================================================

def get_question(slug):
    data = graphql(
        QUESTION_QUERY,
        {
            "titleSlug": slug
        },
        operation_name="questionData",
    )

    question = data.get("question")

    if not question:
        raise RuntimeError(
            f"Could not fetch question: {slug}"
        )

    return question


# ============================================================
# README
# ============================================================

def analyze_algorithm(code, tags):
    """
    Detect common algorithmic patterns from the submitted code
    and LeetCode topic tags.

    Returns:
        primary_pattern
        supporting_patterns
        intuition
        approach
        time_complexity
        space_complexity
    """

    code_lower = (code or "").lower()
    tag_text = " ".join(tags).lower()

    patterns = []

    def add(pattern):
        if pattern not in patterns:
            patterns.append(pattern)

    # Hash Map / Hash Set
    if (
        "hash table" in tag_text
        or "hash map" in tag_text
        or "hashmap" in code_lower
        or "defaultdict" in code_lower
        or "unordered_map" in code_lower
        or "dict(" in code_lower
    ):
        add("Hash Map")

    if (
        "hash set" in tag_text
        or "set(" in code_lower
        or "unordered_set" in code_lower
    ):
        add("Hash Set")

    # Two pointers
    if (
        "two pointers" in tag_text
        or (
            "left" in code_lower
            and "right" in code_lower
            and "while" in code_lower
        )
    ):
        add("Two Pointers")

    # Sliding window
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

    # Binary search
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

    # Stack
    if (
        "stack" in tag_text
        or (
            "append(" in code_lower
            and ".pop(" in code_lower
        )
    ):
        add("Stack")

    # Queue / BFS
    if (
        "breadth-first search" in tag_text
        or "bfs" in tag_text
        or "popleft(" in code_lower
        or "deque(" in code_lower
    ):
        add("Queue / BFS")

    # DFS / Backtracking
    if (
        "depth-first search" in tag_text
        or "dfs" in tag_text
        or "backtracking" in tag_text
    ):
        add("DFS / Backtracking")

    # Dynamic Programming
    if (
        "dynamic programming" in tag_text
        or "dp" in code_lower
        or "lru_cache" in code_lower
        or "memo" in code_lower
    ):
        add("Dynamic Programming")

    # Heap / Priority Queue
    if (
        "heap" in tag_text
        or "priority queue" in tag_text
        or "heapq" in code_lower
        or "priorityqueue" in code_lower
    ):
        add("Heap / Priority Queue")

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
        or "cumulative" in code_lower
    ):
        add("Prefix Sum")

    # Bit Manipulation
    if (
        "bit manipulation" in tag_text
        or "bitwise" in tag_text
        or "& 1" in code_lower
        or "n & (n - 1)" in code_lower
        or "^" in code_lower
    ):
        add("Bit Manipulation")

    # Linked List
    if (
        "linked list" in tag_text
        or "->next" in code_lower
        or ".next" in code_lower
    ):
        add("Linked List")

    # Greedy
    if "greedy" in tag_text:
        add("Greedy")

    if not patterns:
        patterns.append("Direct Iterative Approach")

    primary = patterns[0]
    supporting = patterns[1:3]

    # --------------------------------------------------------
    # Intuition
    # --------------------------------------------------------

    intuition_map = {
        "Hash Map": (
            "The key idea is to store information from elements we have "
            "already processed so that the required value can be looked "
            "up quickly. A hash map provides O(1) average lookup time, "
            "which avoids repeatedly scanning the input."
        ),

        "Hash Set": (
            "A set is useful here because we mainly need fast membership "
            "checks. Instead of repeatedly searching the input, we keep "
            "the relevant values in a hash set and test whether an element "
            "has already been seen."
        ),

        "Two Pointers": (
            "The solution uses two pointers to process the input from "
            "different positions. By moving the appropriate pointer after "
            "each comparison, unnecessary combinations are eliminated "
            "instead of checking every possible pair."
        ),

        "Sliding Window": (
            "The problem can be viewed as maintaining a valid window over "
            "the input. The left and right boundaries are adjusted as we "
            "scan the array or string, allowing the solution to process "
            "each element a small number of times."
        ),

        "Binary Search": (
            "The search space has an ordered structure, which means we "
            "do not need to inspect every element. At each step, the "
            "middle element eliminates roughly half of the remaining "
            "possibilities."
        ),

        "Stack": (
            "A stack is useful because the most recently added element is "
            "often the first one that needs to be reconsidered. Push and "
            "pop operations let the solution maintain this information "
            "efficiently."
        ),

        "Queue / BFS": (
            "The problem is naturally processed level by level. A queue "
            "stores the next states to visit, allowing breadth-first "
            "search to explore the structure in the required order."
        ),

        "DFS / Backtracking": (
            "The solution explores one possible path or choice at a time. "
            "When a path cannot produce a valid answer, it backtracks and "
            "tries the next possibility."
        ),

        "Dynamic Programming": (
            "The problem contains overlapping subproblems. Instead of "
            "recomputing the same results repeatedly, the solution stores "
            "previously computed states and reuses them."
        ),

        "Heap / Priority Queue": (
            "A priority queue keeps the most important candidate readily "
            "available. This avoids repeatedly scanning all remaining "
            "elements when we only need the current minimum or maximum."
        ),

        "Sorting": (
            "Sorting puts the input into an order that makes the required "
            "comparisons or grouping much easier. Once ordered, the "
            "algorithm can process the elements without checking every "
            "possible arrangement."
        ),

        "Prefix Sum": (
            "Prefix information lets the solution answer cumulative "
            "queries without recomputing the sum from the beginning each "
            "time. Each position stores enough information to derive "
            "later results efficiently."
        ),

        "Bit Manipulation": (
            "The solution takes advantage of bit-level properties of the "
            "numbers. Bitwise operations can express certain mathematical "
            "conditions much more efficiently than repeatedly performing "
            "the equivalent arithmetic operations."
        ),

        "Linked List": (
            "The solution works directly with node relationships rather "
            "than treating the structure like a random-access array. "
            "Updating or traversing the next pointers lets us manipulate "
            "the list efficiently."
        ),

        "Greedy": (
            "A greedy strategy is used: at each step, the solution makes "
            "the best locally available choice with the goal of building "
            "an optimal global result."
        ),
    }

    intuition = intuition_map.get(
        primary,
        (
            "The solution processes the input systematically while "
            "maintaining the information needed to make each decision "
            "without unnecessary repeated work."
        ),
    )

    # --------------------------------------------------------
    # Approach
    # --------------------------------------------------------

    approach_map = {
        "Hash Map": [
            "Create a hash map to store information about elements already processed.",
            "Iterate through the input once.",
            "For each element, compute or check the value required by the problem.",
            "Use the hash map for an O(1) average-time lookup.",
            "Return or update the result when the required condition is satisfied.",
        ],

        "Hash Set": [
            "Create a set containing the values needed for fast membership checks.",
            "Traverse the input while checking whether the current value has already been seen.",
            "Update the set as new values are processed.",
            "Return the result once the required condition is found.",
        ],

        "Two Pointers": [
            "Initialize pointers at the relevant ends or positions of the input.",
            "Compare the values indicated by the pointers.",
            "Move the appropriate pointer according to the problem condition.",
            "Continue until the pointers meet or the valid search range is exhausted.",
        ],

        "Sliding Window": [
            "Initialize the left and right boundaries of the window.",
            "Expand the right side while processing new elements.",
            "When the window becomes invalid, move the left boundary until it is valid again.",
            "Track the best or required result while maintaining the window.",
        ],

        "Binary Search": [
            "Initialize the search boundaries.",
            "Calculate the middle position.",
            "Determine which half can still contain the answer.",
            "Discard the other half and repeat until the answer is found.",
        ],

        "Stack": [
            "Initialize an empty stack.",
            "Process the input from left to right.",
            "Push elements when they still need to be considered.",
            "Pop elements when the current element resolves the pending condition.",
        ],

        "Queue / BFS": [
            "Initialize a queue with the starting state.",
            "Process states in first-in-first-out order.",
            "Generate and enqueue the next valid states.",
            "Continue until the target state or complete traversal is reached.",
        ],

        "DFS / Backtracking": [
            "Choose the next available option.",
            "Recursively explore the resulting state.",
            "Undo the choice when returning from the recursive call.",
            "Continue until all relevant possibilities have been explored or a valid result is found.",
        ],

        "Dynamic Programming": [
            "Define the state that represents a smaller version of the problem.",
            "Initialize the base cases.",
            "Build or memoize states so repeated work is avoided.",
            "Use previously computed states to construct the final answer.",
        ],

        "Heap / Priority Queue": [
            "Initialize a priority queue with the relevant candidates.",
            "Repeatedly retrieve the highest-priority element.",
            "Process it and add any newly relevant candidates.",
            "Continue until the required number of results or final state is obtained.",
        ],

        "Sorting": [
            "Sort the input using the required ordering.",
            "Traverse the ordered data while applying the problem-specific condition.",
            "Use the sorted structure to avoid unnecessary comparisons.",
        ],

        "Prefix Sum": [
            "Build cumulative information while traversing the input.",
            "Use the stored prefix values to derive range or cumulative results efficiently.",
            "Return the required result after processing the input.",
        ],

        "Bit Manipulation": [
            "Identify the bitwise property used by the problem.",
            "Apply the corresponding bit operation to the current value.",
            "Repeat only while the relevant bits remain to be processed.",
            "Return the resulting value or condition.",
        ],

        "Linked List": [
            "Initialize the required node pointers.",
            "Traverse the list through next-pointer relationships.",
            "Update pointers when the problem requires insertion, deletion, reversal, or comparison.",
            "Return the appropriate node or result.",
        ],

        "Greedy": [
            "Evaluate the available choices at the current step.",
            "Select the locally optimal choice.",
            "Update the state and continue to the next step.",
            "Return the final result after all relevant choices are processed.",
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
    # Complexity estimation
    # --------------------------------------------------------

    time_complexity = "Depends on the exact implementation"
    space_complexity = "Depends on the exact implementation"

    if primary == "Hash Map":
        time_complexity = "O(n)"
        space_complexity = "O(n)"

    elif primary == "Hash Set":
        time_complexity = "O(n)"
        space_complexity = "O(n)"

    elif primary == "Two Pointers":
        time_complexity = "O(n)"
        space_complexity = "O(1)"

    elif primary == "Sliding Window":
        time_complexity = "O(n)"
        space_complexity = "O(n)"

    elif primary == "Binary Search":
        time_complexity = "O(log n)"
        space_complexity = "O(1)"

    elif primary == "Stack":
        time_complexity = "O(n)"
        space_complexity = "O(n)"

    elif primary == "Queue / BFS":
        time_complexity = "O(n)"
        space_complexity = "O(n)"

    elif primary == "DFS / Backtracking":
        time_complexity = "Depends on the search space"
        space_complexity = "O(n) auxiliary space"

    elif primary == "Sorting":
        time_complexity = "O(n log n)"
        space_complexity = "Depends on the sorting implementation"

    elif primary == "Heap / Priority Queue":
        time_complexity = "O(n log n)"
        space_complexity = "O(n)"

    elif primary == "Bit Manipulation":
        if "while" in code_lower:
            time_complexity = "O(log n)"
        else:
            time_complexity = "O(1)"
        space_complexity = "O(1)"

    elif primary == "Prefix Sum":
        time_complexity = "O(n)"
        space_complexity = "O(n)"

    return {
        "primary": primary,
        "supporting": supporting,
        "intuition": intuition,
        "approach": approach,
        "time": time_complexity,
        "space": space_complexity,
    }


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

    code = submission.get("code", "")

    analysis = analyze_algorithm(
        code,
        tags,
    )

    description = load_html_as_markdown(
        question.get("content", "")
    )

    leetcode_url = (
        f"{LEETCODE_URL}/problems/{slug}/"
    )

    tags_display = (
        " · ".join(tags[:6])
        if tags
        else "Not specified"
    )

    supporting_text = (
        " · ".join(analysis["supporting"])
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

    runtime = submission.get(
        "runtime",
        "N/A",
    )

    memory = submission.get(
        "memory",
        "N/A",
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

**Primary:** {analysis["primary"]}

**Supporting:** {supporting_text}

---

## 🚀 Approach

{approach_steps}

---

## 🔍 Why This Works

The approach works because it avoids unnecessary repeated work and
maintains only the information required to make the next decision.

The exact implementation is available in the linked solution file.

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

> **Note:** The complexity above is inferred from the detected
> algorithmic pattern and the submitted implementation.

---

## 💻 Solution

[View the complete {language} solution →](./{code_filename})

---

## 🎯 Key Takeaway

The main lesson from this problem is to recognize the underlying
algorithmic pattern before writing the implementation.

Understanding **why** the chosen data structure or algorithm reduces
unnecessary work is often more valuable than memorizing the solution.

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

        metadata_path = (
            folder / "metadata.json"
        )

        if not metadata_path.exists():
            continue

        try:
            records.append(
                json.loads(
                    metadata_path.read_text(
                        encoding="utf-8"
                    )
                )
            )
        except Exception:
            continue

    records.sort(
        key=lambda x: int(
            x["number"]
        )
        if str(x.get("number", "")).isdigit()
        else 999999
    )

    easy = sum(
        1 for x in records
        if x.get("difficulty") == "Easy"
    )

    medium = sum(
        1 for x in records
        if x.get("difficulty") == "Medium"
    )

    hard = sum(
        1 for x in records
        if x.get("difficulty") == "Hard"
    )

    rows = []

    for record in records:
        rows.append(
            f"| {record['number']} "
            f"| [{record['title']}]"
            f"(solutions/{record['folder']}/) "
            f"| {difficulty_badge(record['difficulty'])} "
            f"| {record['language']} |"
        )

    if not rows:
        rows.append(
            "| — | Your first solution will appear here | — | — |"
        )

    table = "\n".join(rows)

    readme = f"""# 🧠 LeetCode Solutions

> A continuously growing collection of my LeetCode solutions,
> explanations, algorithmic patterns, and problem-solving notes.

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

Whenever a new accepted LeetCode submission is detected, the automation:

1. Retrieves the accepted submission.
2. Fetches the problem description.
3. Creates the solution file.
4. Generates a readable problem README.
5. Updates this problem archive.
6. Commits the changes automatically.

### Workflow

**Solve → Submit → Accepted ✅ → GitHub automatically updates**

---

## 🎯 Purpose

This repository is more than a backup of code.

Each solution is organized so that visitors can understand the
problem, the core idea, the algorithmic approach, and the implementation.

⭐ One problem at a time. One concept at a time.
"""

    Path("README.md").write_text(
        readme,
        encoding="utf-8",
    )


# ============================================================
# Process submission
# ============================================================

def process_submission(submission):
    submission_id = str(submission.get("id"))

    title = submission.get(
        "title",
        "Unknown",
    )

    slug = submission.get(
        "titleSlug",
        "",
    )

    print(f"\n🔎 Processing: {title}")

    question = get_question(slug)

    code, submission_details = fetch_submission_source(
        submission
    )

    submission = {
        **submission,
        **submission_details,
    }

    folder_name = (
        f"{int(question['questionFrontendId']):04d}"
        f"-{safe_slug(question['title'])}"
    )

    folder = SOLUTIONS_DIR / folder_name

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = get_extension(
        submission.get("lang")
    )

    code_filename = f"solution.{extension}"

    code_path = folder / code_filename
    readme_path = folder / "README.md"
    metadata_path = folder / "metadata.json"

    code_path.write_text(
        code,
        encoding="utf-8",
    )

    readme_path.write_text(
        create_problem_readme(
            question,
            submission,
            code_filename,
        ),
        encoding="utf-8",
    )

    metadata = {
        "number": question["questionFrontendId"],
        "title": question["title"],
        "difficulty": question["difficulty"],
        "language": get_language_name(
            submission.get("lang")
        ),
        "folder": folder_name,
        "slug": question["titleSlug"],
        "submission_id": submission_id,
    }

    metadata_path.write_text(
        json.dumps(
            metadata,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"   ✅ Saved: {folder}")

    return True


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

    state = get_state()

    processed_ids = set(
        str(x)
        for x in state.get(
            "processed_submission_ids",
            [],
        )
    )

    username = get_username()

    print(
        f"👤 LeetCode user: {username}"
    )

    submissions = get_recent_accepted(
        username
    )

    print(
        f"📥 Found {len(submissions)} "
        "recent accepted submissions."
    )

    new_processed_ids = []

    for submission in submissions:
        submission_id = str(
            submission.get("id")
        )

        if not submission_id:
            continue

        if submission_id in processed_ids:
    print(
        f"🔄 Refreshing README: "
        f"{submission.get('title')}"
    )

    try:
        slug = submission.get("titleSlug")

        question = get_question(slug)

        folder_name = (
            f"{int(question['questionFrontendId']):04d}"
            f"-{safe_slug(question['title'])}"
        )

        folder = SOLUTIONS_DIR / folder_name

        if not folder.exists():
            print("   ⚠️ Solution folder missing. Re-importing.")
            process_submission(submission)
            continue

        metadata_path = folder / "metadata.json"

        if not metadata_path.exists():
            print("   ⚠️ Metadata missing. Re-importing.")
            process_submission(submission)
            continue

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        language = metadata.get(
            "language",
            "Unknown",
        )

        extension = None

        for ext in LANGUAGE_EXTENSIONS.values():
            candidate = folder / f"solution.{ext}"
            if candidate.exists():
                extension = ext
                code_path = candidate
                break

        if extension:
            code = code_path.read_text(
                encoding="utf-8"
            )

            refreshed_submission = {
                "lang": language,
                "code": code,
                "runtime": "Previously recorded",
                "memory": "Previously recorded",
            }

            readme = create_problem_readme(
                question,
                refreshed_submission,
                code_path.name,
            )

            (folder / "README.md").write_text(
                readme,
                encoding="utf-8",
            )

        continue

    except Exception as exc:
        print(
            f"   ⚠️ README refresh failed: {exc}"
        )

        continue
        try:
            process_submission(
                submission
            )

            new_processed_ids.append(
                submission_id
            )

        except Exception as exc:
            print(
                f"   ❌ Failed: {exc}"
            )

    processed_ids.update(
        new_processed_ids
    )

    state["processed_submission_ids"] = sorted(
        processed_ids
    )

    save_state(state)

    update_main_readme()

    print(
        "\n✅ Synchronization complete."
    )

    if new_processed_ids:
        print(
            f"🎉 Imported "
            f"{len(new_processed_ids)} new solution(s)."
        )
    else:
        print(
            "ℹ️ No new solutions were imported."
        )


if __name__ == "__main__":
    main()

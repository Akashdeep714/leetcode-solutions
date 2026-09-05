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
REPO_ROOT = Path(".")
SOLUTIONS_DIR = REPO_ROOT / "solutions"

SESSION = os.environ.get("LEETCODE_SESSION", "").strip()
CSRF_TOKEN = os.environ.get("LEETCODE_CSRF_TOKEN", "").strip()

if not SESSION or not CSRF_TOKEN:
    print("❌ Missing LeetCode credentials.")
    print("Make sure LEETCODE_SESSION and LEETCODE_CSRF_TOKEN are configured.")
    sys.exit(1)


# ============================================================
# HTTP / GraphQL
# ============================================================

session = requests.Session()

session.headers.update(
    {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Origin": "https://leetcode.com",
        "Referer": "https://leetcode.com/",
        "X-CSRFToken": CSRF_TOKEN,
    }
)

session.cookies.set("LEETCODE_SESSION", SESSION, domain="leetcode.com")
session.cookies.set("csrftoken", CSRF_TOKEN, domain="leetcode.com")


def graphql(query, variables=None, operation_name=None):
    payload = {
        "query": query,
        "variables": variables or {},
    }

    if operation_name:
        payload["operationName"] = operation_name

    response = session.post(
        GRAPHQL_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise RuntimeError(
            "LeetCode GraphQL error: "
            + json.dumps(data["errors"], ensure_ascii=False)
        )

    return data.get("data", {})


# ============================================================
# LeetCode queries
# ============================================================

GLOBAL_DATA_QUERY = """
query globalData {
    userStatus {
        username
        userId
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


SUBMISSION_DETAILS_QUERY = """
query mySubmissionDetail($id: ID!) {
    submissionDetail(submissionId: $id) {
        id
        code
        lang
        runtime
        memory
        statusDisplay
        timestamp
        question {
            titleSlug
            title
            questionId
            questionFrontendId
        }
    }
}
"""


QUESTION_QUERY = """
query questionData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        titleSlug
        content
        difficulty
        topicTags {
            name
            slug
        }
        hints
        exampleTestcases
        sampleTestCase
        isPaidOnly
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
    "golang": "go",
    "go": "go",
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


LANGUAGE_LABELS = {
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
    "golang": "Go",
    "go": "Go",
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
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_to_markdown(raw_html):
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "html.parser")

    # Convert <pre> blocks to fenced code blocks before text conversion.
    for pre in soup.find_all("pre"):
        code = pre.get_text("\n")
        pre.replace_with(soup.new_string(f"\n```text\n{code}\n```\n"))

    # Make lists / paragraphs reasonably readable.
    for tag in soup.find_all(["br"]):
        tag.replace_with("\n")

    text = soup.get_text("\n")

    text = html.unescape(text)

    # Normalize whitespace without destroying code blocks.
    text = re.sub(r"\n[ \t]+\n", "\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_problem_description(content):
    markdown = html_to_markdown(content)

    # Remove occasional duplicated headings inserted by LeetCode HTML.
    markdown = re.sub(
        r"\n+(Example\s*\d*\s*:?)",
        r"\n\n### \1",
        markdown,
        flags=re.IGNORECASE,
    )

    markdown = re.sub(
        r"\n+(Constraints\s*:?)",
        r"\n\n### Constraints",
        markdown,
        flags=re.IGNORECASE,
    )

    return clean_text(markdown)


def language_extension(lang):
    key = (lang or "").strip().lower()
    return LANGUAGE_EXTENSIONS.get(key, "txt")


def language_label(lang):
    key = (lang or "").strip().lower()
    return LANGUAGE_LABELS.get(key, lang or "Unknown")


def difficulty_badge(difficulty):
    mapping = {
        "Easy": "🟢 Easy",
        "Medium": "🟡 Medium",
        "Hard": "🔴 Hard",
    }
    return mapping.get(difficulty, difficulty or "Unknown")


def detect_approach(code, tags):
    """
    Lightweight heuristic explanation generator.

    It does not pretend to understand every algorithm perfectly.
    Instead, it detects common patterns from the submitted code and
    combines them with LeetCode's topic tags.
    """

    code_lower = code.lower()
    tags_lower = {t.lower() for t in tags}

    detected = []

    def add(name):
        if name not in detected:
            detected.append(name)

    if any(x in code_lower for x in ["heapq", "priorityqueue", "priority_queue"]):
        add("Heap / Priority Queue")

    if any(x in code_lower for x in ["deque(", "popleft(", "queue"]):
        add("Queue / BFS")

    if "visited" in code_lower and any(
        x in code_lower for x in ["queue", "deque", "popleft"]
    ):
        add("Graph Traversal")

    if "union" in code_lower and "find" in code_lower:
        add("Disjoint Set Union")

    if any(
        x in code_lower
        for x in ["defaultdict", "counter(", "hashmap", "hash_map"]
    ) or "hash table" in tags_lower:
        add("Hash Map")

    if "set()" in code_lower or "seen" in code_lower:
        add("Hash Set")

    if any(x in code_lower for x in ["left", "right", "two_pointer"]):
        if (
            ("while" in code_lower and "left" in code_lower and "right" in code_lower)
            or "two pointers" in tags_lower
        ):
            add("Two Pointers")

    if "bisect" in code_lower or "binary search" in tags_lower:
        add("Binary Search")

    if "stack" in code_lower or ".pop()" in code_lower:
        if "monotonic" in " ".join(tags_lower):
            add("Monotonic Stack")
        else:
            add("Stack")

    if any(
        x in code_lower
        for x in ["heap", "priority queue", "priorityqueue"]
    ):
        add("Greedy / Best-First Processing")

    if re.search(r"\bdp\b", code_lower) or "dynamic programming" in tags_lower:
        add("Dynamic Programming")

    if "backtracking" in tags_lower or "dfs" in code_lower:
        add("Depth-First Search / Backtracking")

    if "bfs" in code_lower:
        add("Breadth-First Search")

    if "sort(" in code_lower or "sorted(" in code_lower or "sorting" in tags_lower:
        add("Sorting")

    if "binary tree" in tags_lower or "tree" in tags_lower:
        if "recursion" in code_lower or "dfs" in code_lower:
            add("Tree Traversal")

    # Fallback to useful tag-based explanation.
    if not detected and tags:
        detected = tags[:3]

    if not detected:
        detected = ["Direct algorithmic approach"]

    primary = detected[0]
    secondary = detected[1:3]

    explanation = (
        f"This solution primarily uses **{primary}**. "
        "The implementation processes the input while maintaining the "
        "information needed to make the next decision efficiently."
    )

    if secondary:
        explanation += (
            f" It also makes use of **{secondary[0]}**"
            + (f" and **{secondary[1]}**" if len(secondary) > 1 else "")
            + " as supporting techniques."
        )

    explanation += (
        " The code below follows the same strategy as the accepted "
        "submission and is organized to keep the main idea easy to follow."
    )

    return explanation, detected


def extract_number(question):
    frontend_id = str(question.get("questionFrontendId") or "").strip()

    if frontend_id.isdigit():
        return int(frontend_id)

    question_id = str(question.get("questionId") or "").strip()

    if question_id.isdigit():
        return int(question_id)

    return None


def solution_folder_name(question):
    number = extract_number(question)
    title = question.get("title", "leetcode-problem")

    slug = safe_slug(title)

    if number is not None:
        return f"{number:04d}-{slug}"

    return slug


def get_existing_solution_folders():
    if not SOLUTIONS_DIR.exists():
        return set()

    return {
        path.name
        for path in SOLUTIONS_DIR.iterdir()
        if path.is_dir()
    }


# ============================================================
# Fetch functions
# ============================================================

def get_authenticated_username():
    data = graphql(
        GLOBAL_DATA_QUERY,
        operation_name="globalData",
    )

    user = data.get("userStatus") or {}

    if not user.get("isSignedIn"):
        raise RuntimeError("LeetCode session is not signed in.")

    username = user.get("username")

    if not username:
        raise RuntimeError("Unable to determine LeetCode username.")

    return username


def get_recent_accepted(username, limit=20):
    data = graphql(
        RECENT_ACCEPTED_QUERY,
        {
            "username": username,
            "limit": limit,
        },
        operation_name="recentAcSubmissions",
    )

    return data.get("recentAcSubmissionList") or []


def get_submission_details(submission_id):
    data = graphql(
        SUBMISSION_DETAILS_QUERY,
        {"id": str(submission_id)},
        operation_name="mySubmissionDetail",
    )

    return data.get("submissionDetail")


def get_question(slug):
    data = graphql(
        QUESTION_QUERY,
        {"titleSlug": slug},
        operation_name="questionData",
    )

    return data.get("question")


# ============================================================
# README generation
# ============================================================

def generate_problem_readme(question, submission, code_filename):
    title = question.get("title", "LeetCode Problem")
    number = extract_number(question)
    difficulty = question.get("difficulty", "Unknown")
    slug = question.get("titleSlug", "")
    tags = [tag.get("name", "") for tag in question.get("topicTags", [])]
    tags = [tag for tag in tags if tag]

    description = clean_problem_description(question.get("content", ""))

    explanation, techniques = detect_approach(code_from_submission(submission), tags)

    number_text = f"{number}. " if number is not None else ""

    topic_text = " · ".join(tags[:6]) if tags else "Not specified"

    language = language_label(submission.get("lang"))

    runtime = submission.get("runtime") or "N/A"
    memory = submission.get("memory") or "N/A"

    leetcode_url = f"https://leetcode.com/problems/{slug}/"

    technique_list = "\n".join(
        f"- **{technique}**"
        for technique in techniques[:5]
    )

    readme = f"""# 🧩 {number_text}{title}

> **Difficulty:** {difficulty_badge(difficulty)}  
> **Topics:** {topic_text}  
> **Language:** {language}

[🔗 View this problem on LeetCode]({leetcode_url})

---

## 📝 Problem

{description}

---

## 💡 Intuition

{explanation}

---

## 🚀 Approach

The solution follows these main ideas:

{technique_list}

The implementation is kept in `{code_filename}` so the algorithm can be
studied separately from the problem statement.

---

## ⏱️ Complexity

> The exact complexity depends on the structure of the problem and the
> algorithm used. The solution code is preserved exactly from the accepted
> LeetCode submission.

**Runtime reported by LeetCode:** `{runtime}`  
**Memory reported by LeetCode:** `{memory}`

---

## 💻 Solution

[View the complete solution →](./{code_filename})

---

## 🎯 Key Takeaway

The important lesson from this problem is to identify the right data structure
or algorithmic pattern before optimizing the implementation.

---

### 🏆 Accepted Submission

- **Language:** {language}
- **Runtime:** {runtime}
- **Memory:** {memory}

⭐ This solution was automatically synchronized from an accepted LeetCode submission.
"""

    return readme.strip() + "\n"


def code_from_submission(submission):
    return submission.get("code") or ""


# ============================================================
# Main README
# ============================================================

def update_main_readme():
    if not SOLUTIONS_DIR.exists():
        SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    for folder in SOLUTIONS_DIR.iterdir():
        if not folder.is_dir():
            continue

        metadata_file = folder / "metadata.json"

        if not metadata_file.exists():
            continue

        try:
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        rows.append(metadata)

    rows.sort(
        key=lambda item: (
            int(item.get("number", 999999))
            if str(item.get("number", "")).isdigit()
            else 999999
        )
    )

    easy = sum(1 for item in rows if item.get("difficulty") == "Easy")
    medium = sum(1 for item in rows if item.get("difficulty") == "Medium")
    hard = sum(1 for item in rows if item.get("difficulty") == "Hard")

    total = len(rows)

    table_rows = []

    for item in rows:
        number = item.get("number", "-")
        title = item.get("title", "Unknown")
        difficulty = item.get("difficulty", "Unknown")
        language = item.get("language", "Unknown")
        folder = item.get("folder", "")

        difficulty_display = difficulty_badge(difficulty)

        table_rows.append(
            f"| {number} | [{title}](solutions/{folder}/) "
            f"| {difficulty_display} | {language} |"
        )

    solutions_table = "\n".join(table_rows)

    if not solutions_table:
        solutions_table = (
            "| — | Your first accepted solution will appear here | — | — |\n"
        )

    readme = f"""# 🧠 LeetCode Solutions

> **Automatically synchronized from my LeetCode submissions.**

A growing collection of solved LeetCode problems with readable solutions,
algorithmic intuition, complexity notes, and problem explanations.

## 📊 Progress

| Metric | Count |
|---|---:|
| 🧩 Total Solved | **{total}** |
| 🟢 Easy | **{easy}** |
| 🟡 Medium | **{medium}** |
| 🔴 Hard | **{hard}** |

---

## 📚 Problem Archive

| # | Problem | Difficulty | Language |
|---:|---|---|---|
{solutions_table}

---

## 🔄 Automatic Sync

This repository is connected to LeetCode through **GitHub Actions**.

Whenever I submit an accepted solution, the automation:

1. Detects the accepted submission.
2. Fetches the problem details.
3. Fetches the submitted code.
4. Creates a dedicated solution folder.
5. Generates a readable problem README.
6. Updates this problem archive.
7. Commits everything automatically.

So the workflow is simply:

**Solve → Submit → Accepted ✅ → GitHub updates automatically**

---

## 🎯 Goal

The purpose of this repository is not just to store solutions.

It is a learning journal for algorithms, data structures, problem-solving patterns,
and the reasoning behind each solution.

⭐ New problem. New concept. One step better.
"""

    (REPO_ROOT / "README.md").write_text(
        readme.strip() + "\n",
        encoding="utf-8",
    )


# ============================================================
# Process one submission
# ============================================================

def process_submission(submission_summary):
    submission_id = submission_summary.get("id")
    title_slug = submission_summary.get("titleSlug")

    if not submission_id or not title_slug:
        return False

    print(f"🔎 Processing: {submission_summary.get('title', title_slug)}")

    submission = get_submission_details(submission_id)

    if not submission:
        print("   ⚠️ Could not fetch submission details.")
        return False

    if submission.get("statusDisplay") != "Accepted":
        print("   ⏭️ Submission is not accepted.")
        return False

    question = get_question(title_slug)

    if not question:
        print("   ⚠️ Could not fetch problem details.")
        return False

    folder_name = solution_folder_name(question)
    solution_dir = SOLUTIONS_DIR / folder_name

    solution_dir.mkdir(parents=True, exist_ok=True)

    language = submission.get("lang", "text")
    extension = language_extension(language)
    code_filename = f"solution.{extension}"

    code_path = solution_dir / code_filename

    code = submission.get("code") or ""

    if not code.strip():
        print("   ⚠️ Submission contained no source code.")
        return False

    code_path.write_text(code, encoding="utf-8")

    readme = generate_problem_readme(
        question,
        submission,
        code_filename,
    )

    (solution_dir / "README.md").write_text(
        readme,
        encoding="utf-8",
    )

    number = extract_number(question)

    metadata = {
        "number": number if number is not None else "",
        "title": question.get("title", ""),
        "difficulty": question.get("difficulty", ""),
        "language": language_label(language),
        "folder": folder_name,
        "slug": question.get("titleSlug", ""),
        "submission_id": str(submission_id),
    }

    (solution_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"   ✅ Saved: {solution_dir}")

    return True


# ============================================================
# Entry point
# ============================================================

def main():
    print("🚀 Starting LeetCode synchronization...\n")

    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)

    username = get_authenticated_username()

    print(f"👤 LeetCode user: {username}")

    recent = get_recent_accepted(username, limit=20)

    print(f"📥 Found {len(recent)} recent accepted submissions.\n")

    existing = get_existing_solution_folders()
    changed = False

    for submission in reversed(recent):
        try:
            question = {
                "questionFrontendId": "",
                "title": submission.get("title", ""),
            }

            # First try to identify whether this problem already exists
            # by its title/slug.
            slug = submission.get("titleSlug", "")
            candidate = safe_slug(submission.get("title", ""))

            already_exists = any(
                candidate in folder.lower()
                for folder in existing
            )

            if already_exists:
                print(
                    f"⏭️ Already synchronized: {submission.get('title', slug)}"
                )
                continue

            processed = process_submission(submission)

            if processed:
                changed = True

        except Exception as exc:
            print(
                f"❌ Error processing "
                f"{submission.get('title', 'unknown problem')}: {exc}"
            )

    update_main_readme()

    if changed:
        print("\n✅ New solution(s) synchronized.")
    else:
        print("\n✅ No new solutions were found.")

    print("🏁 Synchronization complete.")


if __name__ == "__main__":
    main()

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

def build_intuition(tags):
    tag_names = [
        tag
        for tag in tags
        if tag
    ]

    if tag_names:
        main = ", ".join(
            tag_names[:3]
        )
    else:
        main = "an appropriate algorithmic pattern"

    return (
        "The key to this problem is recognizing the right "
        f"data structure or algorithmic pattern: **{main}**. "
        "Instead of repeatedly checking unnecessary possibilities, "
        "the solution keeps track of the information required to "
        "make each decision efficiently."
    )


def build_approach(tags):
    if not tags:
        return (
            "1. Identify the information required while processing "
            "the input.\n"
            "2. Traverse the input using the chosen algorithm.\n"
            "3. Maintain the required state.\n"
            "4. Return the answer once the required condition is met."
        )

    return (
        "1. Identify the main algorithmic pattern.\n"
        "2. Traverse the input while maintaining the required state.\n"
        f"3. Use the relevant technique ({', '.join(tags[:4])}) "
        "to avoid unnecessary work.\n"
        "4. Return the result after processing the required input."
    )


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

    description = load_html_as_markdown(
        question.get("content", "")
    )

    intuition = build_intuition(tags)
    approach = build_approach(tags)

    leetcode_url = (
        f"{LEETCODE_URL}/problems/{slug}/"
    )

    tags_display = (
        " · ".join(tags[:6])
        if tags
        else "Not specified"
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

{intuition}

---

## 🚀 Approach

{approach}

---

## ⏱️ Complexity

The exact complexity follows from the algorithm used in the accepted
solution.

**Runtime reported by LeetCode:** `{runtime}`  
**Memory reported by LeetCode:** `{memory}`

---

## 💻 Solution

[View the complete {language} solution →](./{code_filename})

---

## 🎯 Key Takeaway

The most important lesson is to recognize the underlying algorithmic
pattern and choose a data structure that avoids unnecessary repeated work.

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
                f"⏭️ Already synced: "
                f"{submission.get('title')}"
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

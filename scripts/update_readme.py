#!/usr/bin/env python3
"""
Tự động cập nhật README.md từ các thư mục bài giải LeetCode (tương thích LeetSync).

Script tự tìm mọi thư mục có dạng <số>-<slug> (vd: 1-two-sum, 0001-two-sum),
ở thư mục gốc hoặc nằm trong easy/ medium/ hard/ hay bất kỳ thư mục con nào.

Thông tin từng bài được lấy theo thứ tự ưu tiên:
    1. Comment đầu file lời giải (Title / Chủ đề / Time / Space)
    2. README.md của bài (do LeetSync tạo): tên bài, độ khó
    3. LeetCode GraphQL (tuỳ chọn, có cache): độ khó, chủ đề, tên bài

Cách dùng:
    python scripts/update_readme.py            # cập nhật README.md
    python scripts/update_readme.py --dry-run  # chỉ in kết quả, không ghi file
    python scripts/update_readme.py --offline  # không gọi LeetCode API
"""
import json
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CACHE = ROOT / ".leetcode_cache.json"

DIFFICULTIES = {
    "easy": ("🟢 Easy", "Easy"),
    "medium": ("🟡 Medium", "Medium"),
    "hard": ("🔴 Hard", "Hard"),
    "unknown": ("❔ Chưa rõ", "Chưa rõ"),
}

# đuôi file -> tên ngôn ngữ (thêm ngôn ngữ mới ở đây)
LANGS = {
    ".py": "Python",
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++",
    ".c": "C",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".cs": "C#",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".php": "PHP",
    ".scala": "Scala",
    ".sql": "SQL",
    ".sh": "Bash",
    ".dart": "Dart",
    ".r": "R",
}

SKIP_DIRS = {"scripts", "templates", "node_modules", "__pycache__"}

FOLDER_RE = re.compile(r"^(\d+)-(.+)$")
TITLE_RE = re.compile(r"LeetCode\s*#?\s*\d+\s*[-–—:.]\s*(.+)", re.I)
TOPICS_RE = re.compile(r"(?:Chủ đề|Topics?|Tags?)\s*:\s*(.+)", re.I)
TIME_RE = re.compile(r"Time(?:\s*complexity)?\s*:\s*(O\(.*\))", re.I)
SPACE_RE = re.compile(r"Space(?:\s*complexity)?\s*:\s*(O\(.*\))", re.I)
README_TITLE_RE = re.compile(r"\b\d+\.\s*([^<\n\]]+?)\s*(?:</a>|</h2>|\]|\n|$)")
README_DIFF_RE = re.compile(r"\b(Easy|Medium|Hard)\b")


def clean(s: str) -> str:
    return s.replace("*/", "").replace('"""', "").replace("'''", "").strip()


def read_text(path: Path, limit: int = 3000) -> str:
    try:
        with path.open(encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except OSError:
        return ""


def rel(path: Path) -> str:
    return "./" + quote(path.relative_to(ROOT).as_posix())


# ----------------------------- LeetCode API (tuỳ chọn) -----------------------------

def fetch_meta(slug: str):
    payload = {
        "query": "query q($s: String!){question(titleSlug:$s){title difficulty topicTags{name}}}",
        "variables": {"s": slug},
    }
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://leetcode.com",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            q = json.load(r)["data"]["question"]
        return {
            "title": q["title"],
            "difficulty": q["difficulty"].lower(),
            "topics": [t["name"] for t in q["topicTags"]],
        }
    except Exception as e:  # mạng lỗi, bị chặn, slug sai... -> bỏ qua
        print(f"⚠️  Không lấy được dữ liệu LeetCode cho '{slug}': {e}", file=sys.stderr)
        return None


# ----------------------------- Đọc từng bài -----------------------------

def parse_problem(folder: Path, cache: dict, online: bool):
    m = FOLDER_RE.match(folder.name)
    files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in LANGS
    )
    if not m or not files:
        return None

    slug = m.group(2).lower()
    info = {
        "num": int(m.group(1)),
        "slug": slug,
        "title": slug.replace("-", " ").title(),
        "difficulty": "",
        "topics": [],
        "time": "",
        "space": "",
        "folder": folder,
        "langs": {},
        "statement": folder / "README.md" if (folder / "README.md").exists() else None,
        "notes": folder / "notes.md" if (folder / "notes.md").exists() else None,
    }
    for part in folder.relative_to(ROOT).parts[:-1]:
        if part.lower() in DIFFICULTIES:
            info["difficulty"] = part.lower()

    title_found = False
    for f in files:
        info["langs"].setdefault(LANGS[f.suffix.lower()], f)
        header = "".join(read_text(f).splitlines(keepends=True)[:40])
        if not title_found and (t := TITLE_RE.search(header)):
            info["title"], title_found = clean(t.group(1)), True
        if not info["topics"] and (t := TOPICS_RE.search(header)):
            info["topics"] = [clean(x) for x in clean(t.group(1)).split(",") if clean(x)]
        if not info["time"] and (t := TIME_RE.search(header)):
            info["time"] = clean(t.group(1))
        if not info["space"] and (t := SPACE_RE.search(header)):
            info["space"] = clean(t.group(1))

    if info["statement"]:
        head = read_text(info["statement"], 800)
        if not title_found and (t := README_TITLE_RE.search(head)):
            info["title"], title_found = clean(t.group(1)), True
        if not info["difficulty"] and (d := README_DIFF_RE.search(head)):
            info["difficulty"] = d.group(1).lower()

    if online and (not info["difficulty"] or not info["topics"] or not title_found):
        meta = cache.get(slug) or fetch_meta(slug)
        if meta:
            cache[slug] = meta
            info["difficulty"] = info["difficulty"] or meta["difficulty"]
            info["topics"] = info["topics"] or meta["topics"]
            if not title_found:
                info["title"] = meta["title"]

    info["difficulty"] = info["difficulty"] or "unknown"
    return info


def collect(cache: dict, online: bool):
    problems = []
    for dirpath, dirnames, _ in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        folder = Path(dirpath)
        if folder != ROOT and FOLDER_RE.match(folder.name):
            if p := parse_problem(folder, cache, online):
                problems.append(p)
    return sorted(problems, key=lambda p: p["num"])


# ----------------------------- Sinh nội dung -----------------------------

def build_progress(problems):
    c = Counter(p["difficulty"] for p in problems)
    cols = ["Easy", "Medium", "Hard"] + (["Chưa rõ"] if c["unknown"] else []) + ["Tổng"]
    vals = [str(c["easy"]), str(c["medium"]), str(c["hard"])]
    if c["unknown"]:
        vals.append(str(c["unknown"]))
    vals.append(f"**{len(problems)}**")
    return (
        "| " + " | ".join(cols) + " |\n"
        "|" + ":----:|" * len(cols) + "\n"
        "| " + " | ".join(vals) + " |"
    )


def build_languages(problems):
    c = Counter(lang for p in problems for lang in p["langs"])
    if not c:
        return "*Chưa có bài nào.*"
    rows = ["| Ngôn ngữ | Số bài |", "|----------|:------:|"]
    rows += [f"| {lang} | {n} |" for lang, n in c.most_common()]
    return "\n".join(rows)


def build_problems(problems):
    if not problems:
        return "*Chưa có bài nào.*"
    rows = [
        "| # | Tên bài | Độ khó | Chủ đề | Lời giải | Time | Space |",
        "|---|---------|:------:|--------|----------|:----:|:-----:|",
    ]
    for p in problems:
        url = f"https://leetcode.com/problems/{p['slug']}/"
        sols = ", ".join(f"[{lang}]({rel(f)})" for lang, f in sorted(p["langs"].items()))
        if p["statement"]:
            sols += f" · [📄]({rel(p['statement'])})"
        if p["notes"]:
            sols += f" · [📝]({rel(p['notes'])})"
        rows.append(
            f"| {p['num']} | [{p['title']}]({url}) | {DIFFICULTIES[p['difficulty']][0]} "
            f"| {', '.join(p['topics']) or '—'} | {sols} "
            f"| {p['time'] or '—'} | {p['space'] or '—'} |"
        )
    return "\n".join(rows)


def build_topics(problems):
    topics = defaultdict(list)
    for p in problems:
        for t in p["topics"]:
            topics[t].append(p)
    if not topics:
        return "*Chưa có dữ liệu chủ đề.*"
    lines = []
    for t in sorted(topics, key=str.lower):
        links = ", ".join(f"[#{p['num']}]({rel(p['folder'])})" for p in topics[t])
        lines.append(f"- **{t}** ({len(topics[t])}): {links}")
    return "\n".join(lines)


# ----------------------------- Ghi README -----------------------------

def replace_block(text: str, name: str, body: str, inline: bool = False) -> str:
    pattern = re.compile(rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"❌ README.md thiếu marker <!-- {name}:START --> ... <!-- {name}:END -->")
    sep = "" if inline else "\n"
    return pattern.sub(lambda m: f"{m.group(1)}{sep}{body}{sep}{m.group(3)}", text, count=1)


def main():
    dry = "--dry-run" in sys.argv
    online = "--offline" not in sys.argv
    if not README.exists():
        sys.exit("❌ Không tìm thấy README.md")

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    old_cache = json.dumps(cache, sort_keys=True)

    problems = collect(cache, online)
    old = README.read_text(encoding="utf-8")

    new = old
    new = replace_block(new, "PROGRESS", build_progress(problems))
    new = replace_block(new, "LANGUAGES", build_languages(problems))
    new = replace_block(new, "PROBLEMS", build_problems(problems))
    new = replace_block(new, "TOPICS", build_topics(problems))

    if not dry and json.dumps(cache, sort_keys=True) != old_cache:
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")

    if new == old:
        print("✅ README đã là bản mới nhất, không có gì thay đổi.")
        return

    new = replace_block(new, "UPDATED", date.today().strftime("%d/%m/%Y"), inline=True)

    if dry:
        print(new)
        return
    README.write_text(new, encoding="utf-8")
    langs = ", ".join(sorted({l for p in problems for l in p["langs"]})) or "—"
    print(f"✅ Đã cập nhật README: {len(problems)} bài | Ngôn ngữ: {langs}")


if __name__ == "__main__":
    main()

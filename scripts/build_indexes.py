from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "articles"
POSTS_PATH = ROOT / "posts.json"
CATEGORIES_PATH = ROOT / "categories.json"

DEFAULT_CATEGORY_META = {
    "paper": {"name": "论文", "description": "基础模型 Transformer 与不同领域的论文阅读笔记。", "icon": "📚", "order": 10},
    "algorithm": {"name": "算法", "description": "YOLO、语音项目、数据集与训练问题相关记录。", "icon": "🧠", "order": 20},
    "deploy": {"name": "模型部署", "description": "RKNN、TVM、ncnn、TensorRT 与模型优化部署实践。", "icon": "🚀", "order": 30},
    "llm": {"name": "大模型", "description": "RAG、CLIP 与大模型相关技术整理。", "icon": "🤖", "order": 40},
    "robot": {"name": "机器人", "description": "机器人算法、硬件与系统集成笔记。", "icon": "🦾", "order": 50},
    "cpp": {"name": "C++", "description": "语法、CMake、编译与工程实践问题记录。", "icon": "C++", "order": 60},
    "python": {"name": "Python", "description": "PyCharm、PyQt 与常用 Python 工具链。", "icon": "Py", "order": 70},
    "dev-env": {"name": "开发环境", "description": "Docker、Git、操作系统与环境安装配置。", "icon": "🛠", "order": 80},
    "software-engineering": {"name": "软件工程", "description": "负载均衡、异步编程与工程稳定性相关内容。", "icon": "⚙", "order": 90},
    "tools": {"name": "其他工具", "description": "X-AnyLabeling 等效率工具的使用记录。", "icon": "🧰", "order": 100},
    "misc": {"name": "其他", "description": "3D、摄影、钢琴选购等兴趣向记录。", "icon": "◌", "order": 110},
    "invest": {"name": "投资", "description": "投资学习与复盘相关笔记。", "icon": "📈", "order": 120},
    "daily": {"name": "日常", "description": "生活与感想的长期记录。", "icon": "☁", "order": 130},
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def title_from_markdown(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return path.stem.replace("-", " ").replace("_", " ").strip().title()


def excerpt_from_markdown(title: str, text: str) -> str:
    buffer: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if buffer:
                break
            continue
        if line.startswith("#"):
            continue
        if line in {"---", "***", "___"}:
            continue
        if re.match(r"^\*\*[^*]+\*\*:", line):
            continue
        if re.match(r"^(日期|分类|标签)\s*[:：]", line):
            continue
        if line.startswith("```"):
            continue
        if line.startswith("- ") or re.match(r"^\d+\.\s", line):
            continue
        buffer.append(line)

    excerpt = normalize_text(" ".join(buffer)) or title
    return excerpt[:117] + "..." if len(excerpt) > 120 else excerpt


def git_date(path: Path) -> str:
    relative_path = path.relative_to(ROOT).as_posix()
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", relative_path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        value = result.stdout.strip()
        if value:
            return value
    except Exception:
        pass
    return date.today().isoformat()


def make_slug(path: Path, used_slugs: set[str]) -> str:
    candidates = [path.stem, "-".join(path.relative_to(ARTICLES_DIR).with_suffix("").parts)]
    for candidate in candidates:
        slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff_-]+", "-", candidate).strip("-").lower()
        if slug and slug not in used_slugs:
            used_slugs.add(slug)
            return slug
    fallback = f"post-{len(used_slugs) + 1}"
    used_slugs.add(fallback)
    return fallback


def build_posts() -> list[dict]:
    posts: list[dict] = []
    used_slugs: set[str] = set()

    for path in sorted(ARTICLES_DIR.rglob("*.md")):
        relative = path.relative_to(ARTICLES_DIR)
        if len(relative.parts) < 2:
            continue

        category_slug = relative.parts[0]
        text = path.read_text(encoding="utf-8")
        title = title_from_markdown(path, text)
        category_meta = DEFAULT_CATEGORY_META.get(category_slug, {})

        posts.append(
            {
                "slug": make_slug(path, used_slugs),
                "title": title,
                "date": git_date(path),
                "excerpt": excerpt_from_markdown(title, text),
                "tags": [],
                "markdown": path.relative_to(ROOT).as_posix(),
                "category": {
                    "slug": category_slug,
                    "name": category_meta.get("name", category_slug),
                },
            }
        )

    posts.sort(key=lambda item: (item["date"], item["slug"]), reverse=True)
    return posts


def build_categories(posts: list[dict]) -> list[dict]:
    category_slugs = {post["category"]["slug"] for post in posts}
    ordered = sorted(category_slugs, key=lambda slug: (DEFAULT_CATEGORY_META.get(slug, {}).get("order", 999), slug))
    return [
        {
            "slug": slug,
            "name": DEFAULT_CATEGORY_META.get(slug, {}).get("name", slug),
            "description": DEFAULT_CATEGORY_META.get(slug, {}).get("description", f"{slug} 分类下的文章。"),
            "icon": DEFAULT_CATEGORY_META.get(slug, {}).get("icon", "·"),
        }
        for slug in ordered
    ]


def write_json(path: Path, payload: list[dict]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    posts = build_posts()
    categories = build_categories(posts)
    write_json(POSTS_PATH, posts)
    write_json(CATEGORIES_PATH, categories)
    print(f"Generated {len(posts)} posts and {len(categories)} categories.")


if __name__ == "__main__":
    main()

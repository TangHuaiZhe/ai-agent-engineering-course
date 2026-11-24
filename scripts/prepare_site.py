"""Prepare an MkDocs tree from the repo's existing course files.

The original Markdown remains the single source of truth.
Generated directories are Git-ignored.

Usage:
    python3 scripts/prepare_site.py
    mkdocs build --strict
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / ".site-src"

ROOT_DOCUMENTS = (
    "README.md",
    "ROADMAP.md",
    "SYLLABUS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
)
CONTENT_DIRS = ("modules", "labs", "projects", "references", "docs", "examples", "tests")
COPY_EXTENSIONS = frozenset(
    {".md", ".py", ".json", ".jsonl", ".yaml", ".yml", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".txt"}
)
IGNORED_DIRS = frozenset({"__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache"})
INLINE_LINK = re.compile(r"(\]\()([^)]+)(\))")


def rewrite_home_links(markdown: str, source_file: Path, root: Path) -> str:
    """Rewrite only links that point at the root README to the site homepage."""
    root_readme = (root / "README.md").resolve()

    def replace(match: re.Match[str]) -> str:
        target = match.group(2)
        if (
            not target or "://" in target or target.startswith(("#", "mailto:"))
            or any(character.isspace() for character in target)
        ):
            return match.group(0)
        path, anchor_mark, fragment = target.partition("#")
        if not path.endswith("README.md"):
            return match.group(0)
        if (source_file.parent / path).resolve() != root_readme:
            return match.group(0)
        updated = path.removesuffix("README.md") + "index.md"
        return match.group(1) + updated + (anchor_mark + fragment if anchor_mark else "") + match.group(3)

    return INLINE_LINK.sub(replace, markdown)


def stage_site(root: Path = ROOT, destination: Path = DESTINATION) -> int:
    root = root.resolve()
    destination = destination.resolve()
    if destination == root or root not in destination.parents:
        raise ValueError("Site staging destination must be inside the source repository")
    if destination.name in CONTENT_DIRS or destination.name in {"scripts", ".github"}:
        raise ValueError("Refusing to overwrite an existing course source directory")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    count = 0

    def emit(source: Path, relative: Path) -> None:
        nonlocal count
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() == ".md":
            target.write_text(
                rewrite_home_links(source.read_text(encoding="utf-8"), source, root),
                encoding="utf-8",
            )
        else:
            shutil.copy2(source, target)
        count += 1

    for filename in ROOT_DOCUMENTS:
        source = root / filename
        if not source.is_file():
            raise FileNotFoundError(f"Missing required course file: {filename}")
        emit(source, Path("index.md" if filename == "README.md" else filename))

    for dirname in CONTENT_DIRS:
        directory = root / dirname
        if not directory.is_dir():
            continue
        for source in sorted(directory.rglob("*")):
            relative = source.relative_to(root)
            if (
                source.is_file()
                and source.suffix.lower() in COPY_EXTENSIONS
                and not (IGNORED_DIRS & set(relative.parts))
            ):
                emit(source, relative)
    return count


if __name__ == "__main__":
    count = stage_site()
    print(f"Prepared {count} course files in {DESTINATION.relative_to(ROOT)}")

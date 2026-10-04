#!/usr/bin/env python3
"""Local-only raw capture example; no git, subprocess, network, or production paths."""
from __future__ import annotations
import argparse, re
from datetime import datetime, timezone
from pathlib import Path

AREAS = {"ai", "mlops", "quant", "career", "finance"}
CATEGORIES = {"task", "project", "reference", "asset", "idea", "archive", "unknown"}
SOURCES = {"manual", "telegram", "web", "url", "idea", "notion", "other"}
TARGETS = {"Inbox", "Tasks", "Projects", "Sources", "Wiki", "Areas/Finance", "Archive", "Review"}

def slugify(title: str) -> str:
    return "-".join(re.findall(r"[A-Za-z0-9]+", title.lower())) or "capture"

def yaml_scalar(value: str | int | float | None) -> str:
    if value is None or value == "": return ""
    if isinstance(value, (int, float)): return str(value)
    return '\"' + str(value).replace("\\", "\\\\").replace('\"', '\\\"') + '\"'

def safe_tag(tag: str) -> str:
    value = tag.strip().lower()
    if value and not re.fullmatch(r"[a-z0-9_-]+", value):
        raise ValueError("tags must match [a-z0-9_-]+")
    return value

def safe_scalar(value: str, name: str) -> str:
    if "\r" in value or "\n" in value:
        raise ValueError(f"{name} must not contain newlines")
    return yaml_scalar(value)

def unique_path(path: Path) -> Path:
    if not path.exists(): return path
    for index in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists(): return candidate
    raise RuntimeError("could not find a unique filename")

def build_note(title: str, content: str, area: str, tags: list[str], date: str, *, source="manual", category="unknown", proposed_target="Inbox", next_action="", importance=3, received_at="") -> str:
    if area not in AREAS or source not in SOURCES or category not in CATEGORIES or proposed_target not in TARGETS: raise ValueError("invalid metadata")
    if not 1 <= importance <= 5: raise ValueError("importance must be between 1 and 5")
    received_at = received_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    for name, value in (("title", title), ("received_at", received_at), ("next_action", next_action)):
        if "\r" in value or "\n" in value:
            raise ValueError(f"{name} must not contain newlines")
    serialized_tags = [safe_tag(tag) for tag in tags if tag.strip()]
    return f'''---\ntype: inbox\nstatus: raw\narea: {area}\ncategory: {category}\ncreated: {date}\nupdated: {date}\nreceived_at: {safe_scalar(received_at, "received_at")}\nimportance: {importance}\ntags: [{", ".join(yaml_scalar(tag) for tag in serialized_tags)}]\nsource: {source}\nproposed_target: {proposed_target}\nnext_action: {safe_scalar(next_action, "next_action")}\n---\n\n# {title}\n\n## Raw\n{content.strip()}\n\n## Processing Log\n- [ ] Preserved raw input\n- [ ] Classified\n'''

def write_capture(root: Path, title: str, content: str, area: str, tags: list[str], **meta) -> Path:
    date = datetime.now(timezone.utc).date().isoformat()
    inbox = root / "content" / "Inbox"; inbox.mkdir(parents=True, exist_ok=True)
    path = unique_path(inbox / f"{date}-{slugify(title)}.md")
    path.write_text(build_note(title, content, area, tags, date, **meta), encoding="utf-8")
    return path

def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("title"); p.add_argument("content"); p.add_argument("--root", type=Path, required=True); p.add_argument("--area", choices=sorted(AREAS), default="ai"); p.add_argument("--category", choices=sorted(CATEGORIES), default="unknown"); p.add_argument("--source", choices=sorted(SOURCES), default="manual"); p.add_argument("--tags", default=""); p.add_argument("--next-action", default="")
    a = p.parse_args(); print(write_capture(a.root, a.title, a.content, a.area, a.tags.split(","), source=a.source, category=a.category, next_action=a.next_action))
if __name__ == "__main__": main()

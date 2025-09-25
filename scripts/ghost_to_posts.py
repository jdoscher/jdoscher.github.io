#!/usr/bin/env python3
"""
Convert a Ghost export JSON to Jekyll-style Markdown files in posts/.
- Keeps posts in a visible posts/ folder (not _posts).
- Preserves title, date, slug, tags, excerpt, canonical_url.
- Skips drafts (status != "published").
- Writes HTML body directly into Markdown (Jekyll renders it fine).

Usage:
  python3 scripts/ghost_to_posts.py ghost-export.json
  # or rely on default 'ghost-export.json' in repo root
"""

import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

EXPORT = sys.argv[1] if len(sys.argv) > 1 else "ghost-export.json"
OUTDIR = Path("posts")
OUTDIR.mkdir(parents=True, exist_ok=True)

def slugify(s: str) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r'[^a-zA-Z0-9\- ]+', '', s).strip().lower()
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s or "post"

def yaml_safe(s: str) -> str:
    """Escape double quotes for YAML double-quoted scalars."""
    return (s or "").replace('"', '\\"')

def iso_to_date(s: str):
    """Parse Ghost ISO timestamp to date()."""
    if not s:
        return datetime.today().date()
    # Ghost uses Z; Python wants +00:00
    return datetime.fromisoformat(s.replace('Z', '+00:00')).date()

def load_ghost(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Ghost export structure: {"db": [{"data": {...}}]}
    db = data.get("db", [{}])[0].get("data", {})
    return {
        "posts": db.get("posts", []),
        "tags": db.get("tags", []),
        "posts_tags": db.get("posts_tags", []),
    }

def build_tag_maps(tags, posts_tags):
    tags_map = {t["id"]: t for t in tags if "id" in t}
    post_to_tags = {}
    for pt in posts_tags:
        pid = pt.get("post_id")
        tid = pt.get("tag_id")
        if pid and tid:
            post_to_tags.setdefault(pid, []).append(tid)
    return tags_map, post_to_tags

def write_post_md(post, tag_names):
    title = post.get("title") or "Untitled"
    slug = post.get("slug") or slugify(title)
    d_raw = post.get("published_at") or post.get("created_at") or post.get("updated_at")
    d = iso_to_date(d_raw)

    fname = f"{d.isoformat()}-{slug}.md"
    path = OUTDIR / fname

    html = (post.get("html") or "").strip()
    excerpt = (post.get("custom_excerpt") or post.get("excerpt") or "").strip()
    canonical_url = post.get("canonical_url") or ""

    # Prepare YAML-safe fields
    safe_title = yaml_safe(title)
    safe_excerpt = yaml_safe(excerpt)

    # Compose front matter
    fm_lines = [
        "---",
        f'title: "{safe_title}"',
        f"date: {d.isoformat()}",
        f"slug: {slug}",
        f"tags: [{', '.join(tag_names)}]" if tag_names else "tags: []",
        f'description: "{safe_excerpt}"' if safe_excerpt else "description: ",
        f"canonical_url: {canonical_url}" if canonical_url else "canonical_url: ",
        "layout: post",
        "---",
        "",
    ]

    with open(path, "w", encoding="utf-8") as out:
        out.write("\n".join(fm_lines))
        out.write(html)
        if not html.endswith("\n"):
            out.write("\n")
    return path

def main():
    if not Path(EXPORT).exists():
        print(f"ERROR: Export file not found: {EXPORT}", file=sys.stderr)
        sys.exit(1)

    payload = load_ghost(EXPORT)
    tags_map, post_to_tags = build_tag_maps(payload["tags"], payload["posts_tags"])

    total = 0
    skipped = 0
    for p in payload["posts"]:
        if p.get("status") != "published":
            skipped += 1
            continue

        tag_ids = post_to_tags.get(p.get("id"), [])
        tag_names = []
        for tid in tag_ids:
            t = tags_map.get(tid)
            if not t:
                continue
            # Prefer tag slug if present; fall back to name normalized.
            slug = t.get("slug")
            if slug:
                tag_names.append(slug)
            else:
                tag_names.append(slugify(t.get("name", "")))

        path = write_post_md(p, tag_names)
        total += 1
        print(f"Wrote: {path}")

    print(f"\nDone. Wrote {total} posts to {OUTDIR}/ (skipped {skipped} non-published).")

if __name__ == "__main__":
    main()


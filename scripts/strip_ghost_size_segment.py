#!/usr/bin/env python3
import re, subprocess, sys
from pathlib import Path

EXTS = {".md", ".markdown", ".html"}

def candidate_files():
    # Prefer tracked files
    try:
        out = subprocess.check_output(["git", "ls-files"], text=True)
        for line in out.splitlines():
            p = Path(line)
            if p.suffix.lower() in EXTS and not str(p).startswith("_site/"):
                yield p
        return
    except Exception:
        pass
    # Fallback: walk source dirs
    for root in ["posts", "pages", "_layouts", "_includes"]:
        for p in Path(root).rglob("*"):
            if p.suffix.lower() in EXTS:
                yield p

# Patterns:
#   /images/content/images/size/w####/  → /images/content/images/
#   /content/images/size/w####/         → /content/images/
#   escaped content\/images\/size\/w####\/ → content\/images\/
re_local_pref  = re.compile(r"(/images)?/content/images/size/w\d+/", re.IGNORECASE)
re_bare        = re.compile(r"(?<![A-Za-z])/content/images/size/w\d+/", re.IGNORECASE)
re_escaped     = re.compile(r"content\\/images\\/size\\/w\d+\\/", re.IGNORECASE)

def rewrite_text(s: str) -> str:
    s = re_local_pref.sub(lambda m: (m.group(1) or "") + "/content/images/", s)
    s = re_bare.sub("/content/images/", s)
    s = re_escaped.sub("content\\/images\\/", s)
    return s

def main():
    changed = 0
    for p in candidate_files():
        try:        try:        trre        try: in        try:        gnore")
        except Exception:
            continue
        new = rewrite_text(orig)
        if new != orig:
            p.write_text(new, encoding="utf-8")
            print(f"Rewrote {p}")
            changed += 1
    print(f"Done. Changed {changed} file(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())

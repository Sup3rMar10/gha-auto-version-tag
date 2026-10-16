"""Work out the next version from conventional commit messages.

  type!: ... or "BREAKING CHANGE" -> major     feat -> minor     fix, perf -> patch
  anything else (docs, chore, ci, plain text) -> no release
Prints the new tag (for example v1.2.0), or nothing if no release is due.
"""
import re
import subprocess
import sys

TAG = re.compile(r"v(\d+)\.(\d+)\.(\d+)")
HEADER = re.compile(r"^(\w+)(\([^)]*\))?(!)?:")


def parse(tag):
    m = TAG.fullmatch(tag or "")
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def level(messages):
    best = None
    for msg in messages:
        m = HEADER.match(msg.strip())
        if "BREAKING CHANGE" in msg or (m and m.group(3)):
            return "major"
        if m and m.group(1) == "feat":
            best = "minor"
        elif m and m.group(1) in ("fix", "perf") and best is None:
            best = "patch"
    return best


def next_tag(last_tag, messages):
    lvl = level(messages)
    if lvl is None:
        return None
    major, minor, patch = parse(last_tag)
    if lvl == "major":
        major, minor, patch = major + 1, 0, 0
    elif lvl == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1
    return f"v{major}.{minor}.{patch}"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout


def main():
    last = git("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*").strip() or None
    rng = f"{last}..HEAD" if last else "HEAD"
    messages = [m for m in git("log", "--format=%B%x00", rng).split("\x00") if m.strip()]
    tag = next_tag(last, messages)
    print(tag or "")


if __name__ == "__main__":
    main()

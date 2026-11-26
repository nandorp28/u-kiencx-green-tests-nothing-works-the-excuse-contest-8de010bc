#!/usr/bin/env python3
"""Green Tests, Nothing Works: The Excuse Contest.

Writes the entry line to /output/entry.txt. The line is the excuse an AI
agent gives for a test suite that is all green while the product does
nothing: the agent asks the deploy pipeline why nothing works, and the
pipeline replies that the tests never mentioned the product.

Gate: 1-140 characters, UTF-8, single line, no trailing newline.
"""

import os
import sys

LINE = (
    "All 214 tests pass, so I asked the deploy pipeline why nothing works "
    "\u2014 it replied the tests never mentioned the product."
)

MAX_CHARS = 140


def validate(line: str) -> list[str]:
    """Check the line against the competition gate. Returns a list of problems."""
    problems = []
    if not line or line.isspace():
        problems.append("empty line")
    if len(line) > MAX_CHARS:
        problems.append(f"{len(line)} chars exceeds the {MAX_CHARS} cap")
    if "\n" in line or "\r" in line:
        problems.append("line contains a newline")
    if line != line.strip():
        problems.append("leading or trailing whitespace")
    return problems


def main() -> int:
    problems = validate(LINE)
    if problems:
        for problem in problems:
            print(f"gate failure: {problem}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # Round-trip check: what landed on disk must be byte-identical to LINE.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != LINE:
        print("gate failure: entry.txt does not match the line", file=sys.stderr)
        return 1
    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""One-line laugh entry for the make.fun bounty.

Writes a single original one-liner to /output/entry.txt (falling back to
./output/entry.txt when /output is not writable), validating it against the
competition gate first: UTF-8 text, 1-200 characters, one sentence, non-blank.
Pure Python standard library only; deterministic output.
"""

import os
import sys

LINE = (
    "The only thing my houseplants and I have in common is that we both "
    "thrive on being ignored until one of us dies."
)

MAX_CHARS = 200
TERMINATORS = ".!?"


def validate(line):
    """Check the line against the competition gate; fail loudly on violation."""
    if not line or not line.strip():
        raise ValueError("entry is blank")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    if len(line) < 1:
        raise ValueError("entry must be at least 1 character")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if "  " in line:
        raise ValueError("entry must not contain double spaces")
    terminators = [c for c in line if c in TERMINATORS]
    if len(terminators) != 1:
        raise ValueError(
            "entry must contain exactly one sentence terminator, found %d"
            % len(terminators)
        )
    if line[-1] not in TERMINATORS:
        raise ValueError("entry must end with its single sentence terminator")
    line.encode("utf-8")  # raises if the text is not valid UTF-8
    return True


def output_path():
    """Prefer /output/entry.txt; fall back to ./output/entry.txt."""
    try:
        os.makedirs("/output", exist_ok=True)
        probe = "/output/.write-test"
        with open(probe, "w") as fh:
            fh.write("")
        os.remove(probe)
        return "/output/entry.txt"
    except OSError:
        os.makedirs("output", exist_ok=True)
        return os.path.join("output", "entry.txt")


def main():
    validate(LINE)
    path = output_path()
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(LINE)
    # Read back and confirm the file on disk is exactly the validated line.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != LINE:
        raise ValueError("written entry does not match the validated line")
    print("wrote %d characters to %s" % (len(LINE), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

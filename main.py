"""Texts From Your Future Self — one-line entry writer.

Writes a single funny text message from the writer's future self to
/output/entry.txt (or the location the harness requests), with no
trailing newline so the gate counts exactly the message itself.
"""

import os
import sys

ENTRY_TEXT = (
    "Future you here. I finally listened to all 400 voice notes you left me. "
    "You mumble. Also: the plant is fine. It was never the plant. It was you."
)


def resolve_output_path():
    """Pick where the entry text goes.

    Priority: ENTRY_OUT (a file path, or a directory holding entry.txt),
    then MAKEFUN_OUTPUT_DIR, then /output/entry.txt, then the cwd.
    """
    entry_out = os.environ.get("ENTRY_OUT")
    if entry_out:
        if os.path.isdir(entry_out):
            return os.path.join(entry_out, "entry.txt")
        return entry_out

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")

    return "/output/entry.txt"


def write_entry(path, text):
    """Write the entry text with no trailing newline."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def main():
    """Resolve the destination, write the entry, report what happened."""
    text = ENTRY_TEXT
    if not (1 <= len(text) <= 199):
        print(f"entry is {len(text)} chars, outside the 1-199 window", file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        write_entry(path, text)
    except OSError:
        # Last resort: the harness may run in a read-only tree with no
        # /output; fall back to entry.txt beside the working directory.
        path = os.path.join(os.getcwd(), "entry.txt")
        write_entry(path, text)

    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

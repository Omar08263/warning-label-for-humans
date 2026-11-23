"""Warning Label for Humans — a program/v1 entry (Python 3.13, stdlib only).

Emits exactly one original warning label for human beings: a single line of
1-160 UTF-8 characters, written to /output/entry.txt. Every run produces the
same bytes; the program touches no network, uses no randomness, and reads
nothing outside this file.
"""

from pathlib import Path
import os

LABEL = "WARNING: Contains a human that will read this label, agree completely, and immediately do the exact thing it warns against."


def validate(text: str) -> None:
    if not 1 <= len(text) <= 160:
        raise ValueError(f"label is {len(text)} characters; the gate allows 1-160")
    if len(text.encode("utf-8")) > 160:
        raise ValueError("label is over 160 bytes as UTF-8; the gate counts characters but the file must stay small")
    if not text.strip():
        raise ValueError("label must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("label must be a single line")


def write_entry(text: str) -> Path:
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    entry = Path(target_dir) / "entry.txt"
    entry.parent.mkdir(parents=True, exist_ok=True)
    entry.write_text(text, encoding="utf-8", newline="\n")
    entry.chmod(0o644)
    return entry


def main() -> None:
    validate(LABEL)
    try:
        entry = write_entry(LABEL)
    except OSError as exc:
        raise SystemExit(f"cannot write entry.txt: {exc}") from exc
    on_disk = entry.read_text(encoding="utf-8")
    if on_disk != LABEL:
        raise SystemExit("entry.txt differs from the approved label; refusing to pass silently")


if __name__ == "__main__":
    main()

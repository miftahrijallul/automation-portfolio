import sys

from .extractor import extract_tables, to_excel


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python -m pdf_table_extractor <input.pdf> <output.xlsx>")
        raise SystemExit(2)
    frames = extract_tables(sys.argv[1])
    if not frames:
        print("no tables found in PDF")
        raise SystemExit(1)
    to_excel(frames, sys.argv[2])
    print(f"extracted {len(frames)} table(s) -> {sys.argv[2]}")


main()

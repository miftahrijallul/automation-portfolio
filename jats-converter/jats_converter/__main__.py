import json
import sys

from .builder import build_jats
from .docx_reader import read_docx


def main() -> None:
    if len(sys.argv) != 4:
        print("usage: python -m jats_converter <manuscript.docx> <meta.json> <out.xml>")
        raise SystemExit(2)
    docx_path, meta_path, out_path = sys.argv[1:4]
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    sections, refs = read_docx(docx_path)
    xml_bytes = build_jats(meta, sections, refs)
    with open(out_path, "wb") as f:
        f.write(xml_bytes)
    print(f"sections={len(sections)} refs={len(refs)} -> {out_path}")


main()

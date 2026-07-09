import docx

REF_TITLES = ("references", "daftar pustaka", "bibliography", "reference")


def _is_heading(para, text: str) -> bool:
    """Heading = paragraf ber-style Heading, ATAU paragraf pendek yang
    seluruh run-nya bold (pola naskah umum: INTRODUCTION, Methods, dst.)."""
    style = (para.style.name or "").lower()
    if style.startswith("heading"):
        return True
    runs = [r for r in para.runs if r.text.strip()]
    all_bold = bool(runs) and all(r.bold for r in runs)
    return (
        all_bold
        and len(text) <= 60
        and "," not in text
        and not text.endswith(".")
        and not text.lower().startswith("keywords")
    )


def read_docx(path: str) -> "tuple[list, list]":
    """Split a manuscript DOCX into (sections, refs).

    Heading-styled paragraphs start a new section; paragraphs under a
    references-type heading become citation strings.
    """
    document = docx.Document(path)
    sections: list = []
    refs: list = []
    current_title = None
    current_paras: list = []
    in_refs = False

    def flush():
        nonlocal current_title, current_paras
        if current_title is not None and current_paras:
            sections.append((current_title, current_paras))
        current_title, current_paras = None, []

    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if _is_heading(para, text):
            flush()
            if text.lower().rstrip(":") in REF_TITLES:
                in_refs = True
                continue
            in_refs = False
            current_title = text
        elif in_refs:
            refs.append(text)
        elif current_title is not None:
            current_paras.append(text)

    flush()
    return sections, refs

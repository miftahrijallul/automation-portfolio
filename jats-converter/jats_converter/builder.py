from lxml import etree


def _sub(parent, tag, text=None, **attrs):
    el = etree.SubElement(parent, tag, **attrs)
    if text is not None:
        el.text = text
    return el


def build_jats(meta: dict, sections: list, refs: list) -> bytes:
    """Build a JATS 1.3 article XML document.

    meta keys: journal_title, issn, publisher, title, authors [{given, surname, aff}],
    abstract, keywords [str], volume, issue, year, fpage, lpage, doi.
    sections: list of (section_title, [paragraph, ...]).
    refs: list of citation strings.
    """
    article = etree.Element(
        "article",
        attrib={"dtd-version": "1.3", "article-type": "research-article"},
    )

    front = _sub(article, "front")

    journal_meta = _sub(front, "journal-meta")
    jtg = _sub(journal_meta, "journal-title-group")
    _sub(jtg, "journal-title", meta["journal_title"])
    _sub(journal_meta, "issn", meta["issn"], **{"pub-type": "ppub"})
    publisher = _sub(journal_meta, "publisher")
    _sub(publisher, "publisher-name", meta["publisher"])

    article_meta = _sub(front, "article-meta")
    _sub(article_meta, "article-id", meta["doi"], **{"pub-id-type": "doi"})
    tg = _sub(article_meta, "title-group")
    _sub(tg, "article-title", meta["title"])

    contrib_group = _sub(article_meta, "contrib-group")
    for author in meta["authors"]:
        contrib = _sub(contrib_group, "contrib", **{"contrib-type": "author"})
        name = _sub(contrib, "name")
        _sub(name, "surname", author["surname"])
        _sub(name, "given-names", author["given"])
        aff = _sub(contrib, "aff")
        aff.text = author["aff"]

    pub_date = _sub(article_meta, "pub-date", **{"publication-format": "print"})
    _sub(pub_date, "year", meta["year"])
    _sub(article_meta, "volume", meta["volume"])
    _sub(article_meta, "issue", meta["issue"])
    _sub(article_meta, "fpage", meta["fpage"])
    _sub(article_meta, "lpage", meta["lpage"])

    abstract = _sub(article_meta, "abstract")
    _sub(abstract, "p", meta["abstract"])

    kwd_group = _sub(article_meta, "kwd-group")
    for kw in meta["keywords"]:
        _sub(kwd_group, "kwd", kw)

    body = _sub(article, "body")
    for sec_title, paragraphs in sections:
        sec = _sub(body, "sec")
        _sub(sec, "title", sec_title)
        for para in paragraphs:
            _sub(sec, "p", para)

    back = _sub(article, "back")
    ref_list = _sub(back, "ref-list")
    _sub(ref_list, "title", "References")
    for i, citation in enumerate(refs, start=1):
        ref = _sub(ref_list, "ref", id=f"r{i}")
        _sub(ref, "mixed-citation", citation)

    return etree.tostring(
        article,
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True,
        doctype=(
            '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) '
            'Journal Publishing DTD v1.3 20210610//EN" '
            '"JATS-journalpublishing1-3.dtd">'
        ),
    )

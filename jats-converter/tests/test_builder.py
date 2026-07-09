from lxml import etree

from jats_converter.builder import build_jats

META = {
    "journal_title": "Journal of Animal Science (Sample)",
    "issn": "0000-0000",
    "publisher": "Sample University Press",
    "title": "Effect of Something on Something Else",
    "authors": [
        {"given": "Author", "surname": "One", "aff": "University A, Indonesia"},
        {"given": "Author", "surname": "Two", "aff": "University B, Indonesia"},
    ],
    "abstract": "This study evaluates something important.",
    "keywords": ["broiler", "feed additive"],
    "volume": "26",
    "issue": "2",
    "year": "2026",
    "fpage": "142",
    "lpage": "146",
    "doi": "10.0000/sample.00002",
}

SECTIONS = [
    ("Introduction", ["First paragraph.", "Second paragraph."]),
    ("Methods", ["How it was done."]),
]

REFS = [
    "Kari, Z. A. et al. (2022). Phytobiotics in poultry. Journal X, 1(1), 1-10.",
    "Celano, R. et al. (2021). Onion flavonoids. Journal Y, 2(2), 20-30.",
]


def test_build_jats_produces_valid_structure():
    xml_bytes = build_jats(META, SECTIONS, REFS)
    root = etree.fromstring(xml_bytes)

    assert root.tag == "article"
    assert root.get("dtd-version") == "1.3"
    assert root.findtext(".//journal-title") == META["journal_title"]
    assert root.findtext(".//article-title") == META["title"]
    surnames = [e.text for e in root.findall(".//contrib//surname")]
    assert surnames == ["One", "Two"]
    assert root.findtext(".//abstract/p") == META["abstract"]
    kwds = [e.text for e in root.findall(".//kwd")]
    assert kwds == META["keywords"]
    assert root.findtext(".//article-id[@pub-id-type='doi']") == META["doi"]

    secs = root.findall("body/sec")
    assert len(secs) == 2
    assert secs[0].findtext("title") == "Introduction"
    assert [p.text for p in secs[0].findall("p")] == SECTIONS[0][1]

    refs = root.findall("back/ref-list/ref")
    assert len(refs) == 2
    assert refs[0].findtext("mixed-citation") == REFS[0]

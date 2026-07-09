# jats-converter

Convert journal manuscripts (DOCX) into JATS 1.3 XML — the format required by DOAJ, PubMed Central, and most indexing services.

## Usage

```
pip install -r requirements.txt
python -m jats_converter manuscript.docx meta.json output.xml
```

`meta.json` carries the article metadata (journal title, ISSN, authors, abstract, keywords, volume/issue/pages, DOI):

```json
{
  "journal_title": "Journal of Animal Science",
  "issn": "0000-0000",
  "publisher": "University Press",
  "title": "Article title",
  "authors": [{"given": "First", "surname": "Author", "aff": "University, Country"}],
  "abstract": "...",
  "keywords": ["kw1", "kw2"],
  "volume": "26", "issue": "2", "year": "2026",
  "fpage": "142", "lpage": "146",
  "doi": "10.0000/example"
}
```

## What it handles

- Front matter: journal-meta + article-meta (authors, abstract, keywords, DOI, pagination)
- Body sections from Word headings — both proper `Heading` styles and the common bold-paragraph convention (`INTRODUCTION`, `Methods`, ...)
- Reference list detection (`References` / `Daftar Pustaka` / `Bibliography`)
- Verified on real published manuscripts (11 sections, 22 references extracted from a live example)

## Limitations (roadmap)

- Tables and figures are not yet converted (paragraph text only)
- References are emitted as `mixed-citation` strings, not element-parsed citations

Built with lxml and python-docx. Tested with pytest (`python -m pytest`).

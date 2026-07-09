# pdf-table-extractor

Extract tables from PDF files into clean Excel spreadsheets. One command, one sheet per table.

## Usage

```
pip install -r requirements.txt
python -m pdf_table_extractor input.pdf output.xlsx
```

## What it handles

- Multi-page PDFs — every page is scanned for tables
- Multiple tables per document — each lands on its own Excel sheet
- Header row detection — first row becomes column names

## Example

Input: a PDF invoice/report with gridded tables. Output: `output.xlsx` with sheets `Table1`, `Table2`, ...

Built with [pdfplumber](https://github.com/jsvine/pdfplumber) and pandas. Tested with pytest (`python -m pytest`).

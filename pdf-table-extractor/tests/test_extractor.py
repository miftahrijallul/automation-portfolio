from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from pdf_table_extractor.extractor import extract_tables


def make_pdf(path):
    data = [["name", "qty"], ["apple", "3"], ["orange", "5"]]
    table = Table(data)
    table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.black)]))
    SimpleDocTemplate(str(path), pagesize=A4).build([table])


def test_extract_tables_reads_gridded_table(tmp_path):
    pdf = tmp_path / "sample.pdf"
    make_pdf(pdf)
    frames = extract_tables(str(pdf))
    assert len(frames) == 1
    df = frames[0]
    assert list(df.columns) == ["name", "qty"]
    assert df.iloc[0]["name"] == "apple"
    assert df.iloc[1]["qty"] == "5"

import pandas as pd
import pdfplumber


def extract_tables(pdf_path: str) -> list:
    """Extract every detectable table from a PDF, one DataFrame per table."""
    frames: list = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                if not table or len(table) < 2:
                    continue
                header, *rows = table
                frames.append(pd.DataFrame(rows, columns=header))
    return frames


def to_excel(frames: list, out_path: str) -> None:
    with pd.ExcelWriter(out_path) as writer:
        for i, df in enumerate(frames, start=1):
            df.to_excel(writer, sheet_name=f"Table{i}", index=False)

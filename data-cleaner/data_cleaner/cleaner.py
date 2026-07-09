import pandas as pd


def clean(df: pd.DataFrame) -> "tuple[pd.DataFrame, dict]":
    """Normalize headers, trim whitespace, drop duplicates, report data quality."""
    report: dict = {"rows_in": len(df)}
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].str.strip()
    before = len(out)
    out = out.drop_duplicates().reset_index(drop=True)
    report["duplicates_removed"] = before - len(out)
    report["missing_per_column"] = {k: int(v) for k, v in out.isna().sum().items()}
    report["rows_out"] = len(out)
    return out, report

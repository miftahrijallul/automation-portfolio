import pandas as pd

from data_cleaner.cleaner import clean


def test_clean_trims_dedupes_and_reports():
    df = pd.DataFrame(
        {
            " Name ": ["  Andi", "  Andi", None],
            "Qty ": ["1", "1", "2"],
        }
    )
    out, report = clean(df)
    assert list(out.columns) == ["name", "qty"]
    assert out.iloc[0]["name"] == "Andi"
    assert report["rows_in"] == 3
    assert report["duplicates_removed"] == 1
    assert report["rows_out"] == 2
    assert report["missing_per_column"]["name"] == 1

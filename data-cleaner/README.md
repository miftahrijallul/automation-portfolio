# data-cleaner

Clean messy CSV data in one command: normalize headers, trim whitespace, remove duplicates — and get a data-quality report.

## Usage

```
pip install -r requirements.txt
python -m data_cleaner input.csv output.csv
```

Prints a JSON quality report:

```json
{
  "rows_in": 5,
  "duplicates_removed": 1,
  "missing_per_column": {"customer_name": 1, "product": 0, "qty": 0, "price": 0},
  "rows_out": 4
}
```

## Before / after

See [examples/messy_sales.csv](examples/messy_sales.csv) → [examples/clean_sales.csv](examples/clean_sales.csv).

Built with pandas. Tested with pytest (`python -m pytest`).

import json
import sys

import pandas as pd

from .cleaner import clean


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python -m data_cleaner <input.csv> <output.csv>")
        raise SystemExit(2)
    df = pd.read_csv(sys.argv[1])
    out, report = clean(df)
    out.to_csv(sys.argv[2], index=False)
    print(json.dumps(report, indent=2))


main()

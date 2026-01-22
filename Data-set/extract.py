import pandas as pd
from collections import Counter
import re

# ———————— Config ————————
CSV_PATH = "/home/mradul/Desktop/Ekadyu/AI-Transliteration/Data-set/data_res_com.csv"
ADDRESS_COLUMNS = ["masked_address"]  # adjust based on actual column names
OUTPUT_LIMIT = 1000  # number of common tokens to keep
MIN_FREQ = 10       # only keep tokens occurring at least this many times
# ——————————————————————

def tokenize(text: str) -> list[str]:
    # remove punctuation, split on whitespace
    text = re.sub(r"[^a-zA-Z0-9\u0900-\u097F ]+", " ", text)
    tokens = text.strip().lower().split()
    return tokens

def main():
    df = pd.read_csv(CSV_PATH)
    counter = Counter()

    for col in ADDRESS_COLUMNS:
        if col not in df.columns:
            continue

        for val in df[col].dropna():
            tokens = tokenize(str(val))
            counter.update(tokens)

    # filter low-frequency tokens
    common = [(tok, freq) for tok, freq in counter.items() if freq >= MIN_FREQ]
    common.sort(key=lambda x: x[1], reverse=True)

    # print or save top OUTPUT_LIMIT tokens
    for tok, freq in common[:OUTPUT_LIMIT]:
        print(f"{tok}\t{freq}")

if __name__ == "__main__":
    main()


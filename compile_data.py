import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv('data/venice_golden_lion.tsv', delimiter='\t')
    print(df)

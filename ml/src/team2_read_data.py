import pandas as pd

def read_csv_with_tab_separator(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df
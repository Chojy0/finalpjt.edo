import pandas as pd

def load_and_process_data(file_path):
    """
    Load and preprocess data from the Excel file.
    Args:
        file_path (str): Path to the Excel file.
    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df = pd.read_excel(file_path)
    df = df.dropna(subset=['구분', '총합'])  # Remove rows with NaN in '구분' or '총합'
    df['구분'] = df['구분'].astype(str)
    df['총합'] = pd.to_numeric(df['총합'], errors='coerce')
    return df

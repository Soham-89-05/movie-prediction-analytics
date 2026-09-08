import pandas as pd

def clean_dataset(file_path, output_path="cleaned_dataset.xlsx"):
    """
    Cleans a dataset by standardizing column names, removing duplicates, handling missing values,
    stripping whitespace, and converting numeric columns.

    Parameters:
        file_path (str): Path to the input dataset (Excel or CSV)
        output_path (str): Path to save the cleaned dataset
    """
    # Load dataset
    try:
        df = pd.read_excel(file_path)
    except Exception:
        df = pd.read_csv(file_path)
    
    print("Original dataset shape:", df.shape)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Handle null / empty cells
    df = df.replace(["", " ", "NA", "N/A", "na", "n/a"], pd.NA)  # mark as NA
    df = df.dropna(how="all")  # drop rows fully empty
    df = df.fillna(method="ffill").fillna(method="bfill")  # fill missing forward/backward

    # Convert numeric columns properly
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # Save cleaned dataset
    df.to_excel(output_path, index=False)
    
    print("Cleaned dataset shape:", df.shape)
    print(f"✅ Cleaned data saved to {output_path}")
    
    return df

cleaned_df = clean_dataset("movies_raw_90.xlsx")

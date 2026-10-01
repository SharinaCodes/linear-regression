# -----------------------------
# Imports
# -----------------------------

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
random.seed(0)

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = './data/salary_data.csv'
CLEANED_DATA_PATH = './data/cleaned_dataset.csv'
OUTCOME = 'salary'

NUM_COLS = [
    'age', 'years_of_experience'
]

CAT_COLS = [
    'gender', 'education_level', 'job_title'
]



# -----------------------------
# Utilities
# -----------------------------
def die (message, exc=None):
    """
    Provide a consistent framework for error handling.
    """
    print(message)
    if exec is not None:
        print(exc)
    raise SystemExit(1)

def print_section(title):
    """
    Privides a consistent way to print section headings.
    """
    print(f"=== {title} ===")

def load_data(path, title):
    """
    Loads the data set, renames columns, and prints verification
    """
    print_section(title)
    try:
        df = pd.read_csv(path)
        
        print(df.head())
        return df
    except Exception as e:
        die(f"Failed to load file: {path}", e)

def save_csv(df, path):
    """
    Provide a consistent way to save .csv files.
    """
    try:
        df.to_csv(path, index=False)
        print(f"Saved: {path}")
    except Exception as e:
        die(f"Failed to save file: {path}", e)

# -----------------------------
# Part I - Descriptive Statistics
# -----------------------------

def preview_data(df, title):
    print_section(title)
    print(f"The dataset has {df.shape[0]} columns and {df.shape[1]} rows")    
    
    print(f"\nThe data has the following data types.")
    print(df.info())

def clean_data(df, title):
    print_section(title)

    # preserve original dataset
    df_clean = df.copy()

    # rename columns
    print(f"\nColumns before rename: {df_clean.columns}")
    rename = {'Age': 'age', 'Gender': 'gender', 'Education Level': 'education_level', 'Job Title': 'job_title', 'Years of Experience': 'years_of_experience', 'Salary': 'salary'}
    df_clean.rename(columns=rename, inplace=True)
    print(f"\nColumns after rename: {df_clean.columns}")

    # drop nulls
    print(f"\nMissing values before clean: {df_clean.isnull().sum().sum()}")
    df_clean = df_clean.dropna()
    print(f"Missing values after clean: {df_clean.isnull().sum().sum()}")

    # drop error
    print(f"\nMinimum salary before cleaning: {df_clean.salary.min()}")
    df_clean = df_clean[df_clean['salary'] != 350.0]
    print(f"Mininum salary after clean: {df_clean.salary.min()}")

    return df_clean
    
# -----------------------------
# Main
# -----------------------------

def main():
    print_section("Data Review")
    df = load_data(DATA_PATH, "Load Data")
    print()

    preview_data(df, "Preview Data")
    print()

    df_clean = clean_data(df, "Clean Data")
    print()

    explore_data(df_clean, "Explore Data")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        die("Unexpected error.", e)
# -----------------------------
# Imports
# -----------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = './data/salary_data.csv'
CLEANED_DATA_PATH = './data/cleaned_dataset.csv'
IMG_PATH = './reports/figures/'

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
    if exc is not None:
        print(exc)
    raise SystemExit(1)

def print_section(title):
    """
    Provides a consistent way to print section headings.
    """
    print(f"=== {title} ===")

def load_data(path, title):
    """
    Loads the data set and prints verification
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

def save_image(fig, filename):
    """
    Provide a consistent way to save images.
    """
    path = os.path.join(IMG_PATH, filename)
    try:
        os.makedirs(IMG_PATH, exist_ok=True)
        fig.savefig(path, bbox_inches='tight')
        print(f"Image saved: {path}")
    except Exception as e:
        die(f"Failed to save image: {path}", e)



# -----------------------------
# Part I - Descriptive Statistics
# -----------------------------

def preview_data(df, title):
    """
    Shows general information about the dataset
    """
    print_section(title)
    print(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns")    
    
    print(f"\nThe data has the following data types.\n")
    df.info()

def clean_data(df, title):
    """
    Cleans the dataset and saves a cleaned copy.
    """
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
    print(f"\nMinumum salary before cleaning: {df_clean.salary.min()}")
    df_clean = df_clean[df_clean['salary'] != 350.0]
    print(f"Mininum salary after clean: {df_clean.salary.min()}")

    # save cleaned data
    save_csv(df_clean, CLEANED_DATA_PATH)

    return df_clean

def explore_data(df_clean, title):
    """
    Show descriptive statistics for all variables.
    """
    print_section(title)

    print("Numeric descriptive statistics")
    print(df_clean[NUM_COLS + [OUTCOME]].describe().round(2))

    print("Categorical descriptive statistics")
    for cat in CAT_COLS:
                # .sort_index() ensures ranked data is in order
        counts = df_clean[cat].value_counts(dropna=False).sort_index()
        percents = (
            df_clean[cat]
            .value_counts(normalize=True, dropna=False)
            .sort_index() * 100
        )

        summary = pd.DataFrame({
            "counts": counts,
            "percent": percents.round(2)
        })
        
        print(summary)
        print()

def graph_data(df_clean, title):
    print_section(title)

    fig, ax = plt.subplots()
    df_clean['salary'].plot(kind='hist', bins=range(0, 260000, 10000), ax=ax)
    ax.set_title('Salary Distribution')
    ax.set_xlabel('Salary')
    ax.set_ylabel('Number of Salaries')

    save_image(fig, 'salary_distribution.png')
    plt.show()
    plt.close(fig)

    fig, ax = plt.subplots()
    df_clean.plot(kind='box', column='salary', by='gender', ax=ax)
    ax.set_title('Salary by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Salary')

    save_image(fig, 'salary_by_gender.png')
    plt.show()
    plt.close()

    fig, ax = plt.subplots()
    df_clean.plot(kind='box', column='salary', by='education_level', ax=ax)
    ax.set_title('Salary by Education Level')
    ax.set_xlabel('Education Level')
    ax.set_ylabel('Salary')

    save_image(fig, 'salary_by_education.png')
    plt.show()
    plt.close()

    fig, ax = plt.subplots()
    df_clean.plot(kind='scatter', x='years_of_experience', y='salary', ax=ax)
    ax.set_title('Salary by Years of Experience')
    ax.set_xlabel('Years of Experience')
    ax.set_ylabel('Salary')

    save_image(fig, 'salary_by_experience.png')
    plt.show()
    plt.close()

    fig, ax = plt.subplots()
    df_clean.plot(kind='scatter', x='age', y='salary', ax=ax)
    ax.set_title('Salary by Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Salary')

    save_image(fig, 'salary_by_age.png')
    plt.show()
    plt.close()

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
    print()

    graph_data(df_clean, "Data vs Salary")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        die("Unexpected error.", e)
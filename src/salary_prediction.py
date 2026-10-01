# -----------------------------
# Imports
# -----------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os
from pathlib import Path
import statsmodels.api as sm 
from statsmodels.tools.eval_measures import rmse
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data' / 'salary_data.csv'
CLEANED_DATA_PATH = BASE_DIR / 'data' / 'cleaned_dataset.csv'
IMG_PATH = BASE_DIR / 'reports' / 'figures'


# constants
OUTCOME = 'salary'
NUM_COLS = [
    'age', 'years_of_experience'
]
CAT_COLS = [
    'gender', 'education_level', 'job_title'
]
FLAG_WORDS = ['director', 'junior', 'senior', 'manager', 'analyst', 'engineer']
SHOW_PLOTS = False

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

def finish_figure(fig, filename):
    """
    Save a figure, optionally show it, and close it.
    """
    save_image(fig, filename)
    if SHOW_PLOTS:
        plt.show()
    plt.close(fig)



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
    print(f"\nMinimum salary before cleaning: {df_clean.salary.min()}")
    df_clean = df_clean[df_clean['salary'] != 350.0]
    print(f"Minimum salary after clean: {df_clean.salary.min()}")

    # change job_title to lowercase
    print(f"Job titles before clean: {df_clean['job_title'].head().values}")
    df_clean['job_title'] = df_clean['job_title'].str.lower()
    print(f"Job titles after clean: {df_clean['job_title'].head().values}")

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

    finish_figure(fig, 'salary_distribution.png')

    fig, ax = plt.subplots()
    df_clean.plot(kind='box', column='salary', by='gender', ax=ax)
    ax.set_title('Salary by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Salary')

    finish_figure(fig, 'salary_by_gender.png')

    fig, ax = plt.subplots()
    df_clean.plot(kind='box', column='salary', by='education_level', ax=ax)
    ax.set_title('Salary by Education Level')
    ax.set_xlabel('Education Level')
    ax.set_ylabel('Salary')

    finish_figure(fig, 'salary_by_education.png')

    fig, ax = plt.subplots()
    df_clean.plot(kind='scatter', x='years_of_experience', y='salary', ax=ax)
    ax.set_title('Salary by Years of Experience')
    ax.set_xlabel('Years of Experience')
    ax.set_ylabel('Salary')

    finish_figure(fig, 'salary_by_experience.png')

    fig, ax = plt.subplots()
    df_clean.plot(kind='scatter', x='age', y='salary', ax=ax)
    ax.set_title('Salary by Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Salary')

    finish_figure(fig, 'salary_by_age.png')
    
    fig, ax = plt.subplots(figsize=(9, 5))
    groups = []
    labels = []
    for kw in FLAG_WORDS:
        salaries = df_clean.loc[df_clean['job_title'].str.contains(kw), 'salary']
        groups.append(salaries)
        labels.append(f"{kw}\n(n={len(salaries)})")

    ax.boxplot(groups, tick_labels=labels)
    ax.set_title('Salary by Job Title Keyword')
    ax.set_xlabel('Title contains')
    ax.set_ylabel('Salary')

    finish_figure(fig, 'salary_by_title_keyword.png')
    
def check_correlation(df_clean, title):
    """
    Checks for correlation between age and years of experience
    """
    print_section(title)
    print(f"Salary and years of experience: {df_clean['years_of_experience'].corr(df_clean['salary'])}")
    print(f"Salary and age: {df_clean['age'].corr(df_clean['salary'])}")
    print(f"Years of experience and age: {df_clean['years_of_experience'].corr(df_clean['age'])}")

def encode_data(df_clean, title):
    """
    Creates job title keyword flags for modeling.
    """
    print_section(title)

    df_model = df_clean.copy()

    print("Dataset before encoding:")
    df_model.info()

    # group job titles
    for word in FLAG_WORDS:
        df_model['is_' + word] = df_model['job_title'].str.contains(word).astype(int)
        print(f"is_{word}: {df_model['is_' + word].sum()} rows flagged")

    df_model = df_model.drop('job_title', axis=1)

    # codify gender
    df_model['is_male'] = (df_model['gender'] == 'Male').astype(int)
    print(f"is_male: {df_model['is_male'].sum()} rows flagged")
    df_model = df_model.drop('gender', axis=1)

    # encode education levels (baseline: Bachelor's)
    edu = pd.get_dummies(df_model['education_level'], prefix='edu', drop_first=True, dtype=int)
    edu.columns = edu.columns.str.lower().str.replace("'", "", regex=False)
    print(f"Education dummies (baseline Bachelor's): {edu.sum().to_dict()}")
    df_model = df_model.join(edu)
    df_model = df_model.drop('education_level', axis=1)

    print("\nDataset after encoding:")
    df_model.info()

    return df_model

def fit_initial_model(df_model, title):
    """
    Fits OLS model with model dataset.
    """
    print_section(title)

    y = df_model[OUTCOME]
    X = df_model.drop(columns=[OUTCOME, 'age'])
    # keep initial columns
    initial_vars = X.columns.tolist()
    X = sm.add_constant(X)

    # Fit OLS
    model_init = sm.OLS(y, X).fit()
    print(model_init.summary())
    return y, X, initial_vars

def optimize_model(y, X, inital_vars, title):
    """
    Performs backward stepwise elimination by removing predictors with p-values greater than 0.05 until all remaining predictors are significant.
    """
    print_section(title)

    current_vars = inital_vars.copy()

    # loops thorugh the df
    while True:
        X_loop = sm.add_constant(X[current_vars])

        # apply the model to the current variable
        loop_model = sm.OLS(y, X_loop)
        # fit the model
        loop_results = loop_model.fit()

        # removes the intercept so only the predictor p-values are evaluated
        pvals = loop_results.pvalues.drop("const", errors="ignore")

        # checks to see if any high p-values remain
        if pvals.max() <= 0.05:
            # exits loop
            print("Done. All p-values <= 0.05.")
            break

        # store the index of the highest p-value
        worst = pvals.idxmax()
        print(f"Remove {worst} (p = {pvals.max():.4f})")
        # removes the predictor with the highest p-value
        current_vars.remove(worst)
        
    print("\nFinal Variables:")
    print(current_vars)
    print()

    return current_vars

def fit_final_model(y, X, current_vars, title):
    """
    Fits OLS model with optimized variables only.
    """
    print_section(title)

    final_X = sm.add_constant(X[current_vars])
    final_results = sm.OLS(y, final_X).fit()

    print(final_results.summary())
    print()

    return final_results, final_X

def interpret_model(model_sig, y):
    print("Confidence intervals")
    print(model_sig.conf_int(alpha=0.05))
    print(f"\nin-sample RMSE: {rmse(y, model_sig.fittedvalues)}")

def check_assumptions(model_sig, final_X, final_vars):
    """
    Checks linearity and equal variance (residual plot, Breusch-Pagan),
    normality of residuals (Q-Q plot), and multicollinearity (VIF).
    """
    print_section("Check Assumptions")
    residuals = model_sig.resid
    fitted = model_sig.fittedvalues

    # linearity and equal variance
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(fitted, residuals, alpha=0.5, s=15)
    ax.axhline(y=0, color='red', linestyle='--')
    ax.set_title('Residuals vs. Fitted Values')
    ax.set_xlabel('Fitted Values')
    ax.set_ylabel('Residuals')
    finish_figure(fig, 'residuals_vs_fitted.png')

    bp_stat, bp_pvalue, _, _ = het_breuschpagan(residuals, final_X)
    print(f"Breusch-Pagan p-value: {bp_pvalue:.4f}")

    # normality of residuals
    fig, ax = plt.subplots()
    sm.qqplot(residuals, line='45', fit=True, ax=ax)
    ax.set_title('Q-Q Plot of Residuals')
    finish_figure(fig, 'residuals_qq.png')

    # multicollinearity (computed with the constant, reported without it)
    vif = pd.DataFrame({
        'Variable': final_vars,
        'VIF': [variance_inflation_factor(final_X.values, final_X.columns.get_loc(var))
                for var in final_vars]
    })
    print("\nVariance Inflation Factors:")
    print(vif.sort_values('VIF', ascending=False))

def predict_example(model_sig, final_X, profile, actual=None):
    """
    Predicts salary for one employee profile and optionally reports the residual.
    """
    print_section("Example Prediction")

    # one row with the same columns as the model, all zeros
    row = pd.DataFrame(0, index=[0], columns=final_X.columns)
    row['const'] = 1

    for var, value in profile.items():
        if var in row.columns:
            row[var] = value
        else:
            print(f"Note: {var} is not in the final model and was ignored")

    predicted = model_sig.predict(row)[0]
    print(f"Predicted salary: ${predicted:,.2f}")

    if actual is not None:
        print(f"Actual salary:    ${actual:,.2f}")
        print(f"Residual:         ${actual - predicted:,.2f}")

    return predicted


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
    print()

    check_correlation(df_clean, "Correlations Check")
    print()

    df_model = encode_data(df_clean, "Encode titles")
    print()

    y, X, initial_vars = fit_initial_model(df_model, "Initial Regression Model")
    print()

    final_vars = optimize_model(y, X, initial_vars, "Backwards Stepwise Elimination")
    print()

    model_sig, final_X = fit_final_model(y, X, final_vars, "Final Optimized Regression Model")
    print()

    interpret_model(model_sig, y)
    print()

    check_assumptions(model_sig, final_X, final_vars)

    predict_example(model_sig, final_X,
                {'years_of_experience': 5, 'is_male': 1, 'is_senior': 1, 'is_engineer': 1},
                actual=110000)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        die("Unexpected error.", e)
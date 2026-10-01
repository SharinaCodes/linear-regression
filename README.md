# Linear Regression
## Salary Prediction (Employee Salary Data)

This project analyzes an employee salary dataset using:

* **Descriptive statistics** (distributions, group comparisons, correlation)
* **Multiple linear regression** (ordinary least squares)

The goal is to determine which factors (gender, education level, years of experience, and job title) are significantly related to salary, and to quantify how much each one is associated with a change in salary.

## Project Structure

```
.
├── data/
│   └── salary_data.csv
├── docs/
│   └── project_brief.md
├── notebooks/
│   └── salary_prediction_project.ipynb
├── reports/
│   └── Model Salary Data with Linear Regression.pdf
├── src/
│   └── salary_prediction.py
└── README.md
```

## Requirements

These are inferred from the notebook imports:

* Python 3.x
* `pandas`
* `numpy`
* `matplotlib`
* `statsmodels`

Install:

```bash
pip install pandas numpy matplotlib statsmodels
```

## How to Run

### Run the script

From inside `src/` (recommended, because `DATA_PATH` is `../data/salary_data.csv`):

```bash
cd src
python salary_prediction.py
```

If you run from the project root, the relative path likely won't resolve (unless you change `DATA_PATH` or handle paths dynamically).

### Run the notebook

Open and run:

* `notebooks/salary_prediction_project.ipynb`

The presentation of results is in `reports/Model Salary Data with Linear Regression.pdf`.

## Data

* `data/salary_data.csv` is the dataset used by the analysis. It contains 375 employee records with Age, Gender, Education Level, Job Title, Years of Experience, and Salary.
* `docs/project_brief.md` describes the project requirements, the analysis questions, and the deliverables.

## What the Analysis Does

`salary_prediction` (notebook and script):

* loads the CSV and renames the columns to lowercase with underscores
* drops the 2 rows with missing values and the $350 salary record (a likely entry error)
* summarizes employee counts by education level and the salary distribution
* compares salary by gender and by education level, and correlates salary with years of experience
* creates binary flags from Job Title for Director, Junior, Senior, Manager, Analyst, and Engineer
* creates a gender flag (1 = male) and education dummies (Bachelor's as the baseline)
* fits an initial OLS model, removes predictors that aren't significant at α = 0.05, and refits
* reports model fit and interprets coefficients with 95% confidence intervals

The regression uses `statsmodels` OLS:

```python
import statsmodels.api as sm
```

# Project Brief: Model Salary Data with Linear Regression

## Overview

Build a multiple linear regression model on employee salary data and interpret the results. The goal is to find which variables are related to salary and how they are related. The analysis is completed in a Jupyter notebook, and the results are presented in a slide deck.

Source: Udacity, Statistics for Data Analysis Nanodegree, "Model Salary Data with Linear Regression" project.

## Dataset

`salary_data.csv` has one row per employee and the following columns:

| Column | Type |
| --- | --- |
| Age | float |
| Gender | string |
| Education Level | string |
| Job Title | string |
| Years of Experience | float |
| Salary | float |

Dataset download: [salary_data.csv](https://video.udacity-data.com/topher/2024/December/6761cf4e_salary_data/salary_data.csv)

## Notebook Requirements

### Part I: Descriptive Statistics

1. Read `salary_data.csv` into a DataFrame and inspect the first few rows.
2. Report the number of rows in the dataset.
3. Determine whether any rows have missing values, choose a method for handling them, and apply it.
4. Count employees at each Education Level and plot the counts as a bar chart.
5. Identify the possible values of Salary and describe its distribution.

### Part II: Regression

1. Compare salary by gender. Is there evidence that one gender earns more than the other?
2. Compare salary by education level. Is there evidence that salary increases with education?
3. Compare salary by years of experience. Is there evidence that salary is associated with more experience?
4. Create a binary flag from Job Title for each of these keywords: Director, Junior, Senior, Manager, Analyst, Engineer.
5. Create a gender flag: 1 if male, 0 otherwise.
6. Use `statsmodels` to fit a linear model predicting Salary from gender, the job title flags, years of experience, and education.

### Part III: Interpret Results

1. Identify which features in the initial model are not significantly related to salary. Remove them and refit, keeping only significant features.
2. For each additional year of experience, report the expected change in salary and its 95% confidence interval.
3. Report the expected salary difference between someone with a Senior title and someone with none of the other title flags.
4. Report the expected salary difference between someone with a PhD and someone with neither a PhD nor a Master's, with its 95% confidence interval.
5. Predict the salary of a male senior engineer with 5 years of experience and a bachelor's degree.
6. If that employee actually earns $110,000, calculate the residual.
7. Assess how well the model fits, and identify the metrics or plots that would show whether it predicts salary well.

## Presentation Requirements

The slide deck has three sections. All results come from the notebook.

### Data Description

- Number of employees in the dataset
- How missing data were handled
- Range of salaries
- Plots or estimates suggesting which features are likely correlated with salary

### Regression Results

- Regression output from the linear model
- Which variables are statistically significant in their relationship with salary
- Removal of variables that are not statistically significant
- How well the model fits the data

### Interpretation of Model Results

For two variables in the model:

- The expected range of change in salary associated with a change in the variable
- The confidence level for that range

Example format: "We can be 95% confident that salary will increase between $X and $Y when moving from no title to a director title."

## Deliverables

| Deliverable | Format |
| --- | --- |
| Completed analysis notebook | `.ipynb` |
| Completed slide deck | Google Slides link with view access, or `.pptx` |

Both deliverables are required for submission.

> Note: The notebook says to check the work against the project rubric. The rubric is not included in the project files.

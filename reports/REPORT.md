# Salary Prediction with Linear Regression

## Summary
* 

## Question
This analysis sought to determine which employee characteristics impact salary. 
* parity in hiring

## Data
The salary dataset contains 375 employees along with their characteristics. The salaries in the dataset ranged from $350 to $250,000. The dataset contained the following data types:

| Column Name | Data Type |
|:--- |:---|
| Age | float |
| Gender | string |
| Education Level | string |
| Job Title | string |
| Years of Experience | float |
| Salary | float|

## Approach
### Cleaning
Because the dataset is small, I focused on retaining as many rows as possible. I dropped missing values, as they made up a negibile amount of the dataset. I also dropped the smallest salary value as it appeared to be an error in this ocntext. Additionally, I standardized column names to make the dataset easier to work with and converted `job_titles` to lowercase for similar reason. I chose to leave outliers, as they're relevant to the research question.

# Data Exploration
To get a sense of the data, I viewed descriptive statistics for all variables. A graph `salary` showed that the distribution was multimodal. Salaries clustered around certain numbers, with the largest peak in the \$40-50k bin, and a second large peak around \$95k. The graph shows a steep decline in the number of salaries at around \$190k. The data also has a slight right skew.

![alt text](figures/salary_distribution.png)

The dataset showed evidence that male salaries were higher than famale salaries. The average salary for men was around 8% higher than for women. The median salary for men was around 11% higher than for women. 

![alt text](figures/salary_by_gender.png) 

The data also showed evidence that salaries are higher for increased education. The median salary for a master's degree was about 85% higher than for a bachlor's degree. The median salary for a doctorate was about 138% higher than for a bachelor's degreen and about 29% higher than for a master's degree.

![alt text](figures/salary_by_education.png) 

There was also evidence that salaries are associated with increased eyars of experience.A correlation of 0.93 indicates a strong, postive correlation. The scatterplot also shows that salaries grow along with years of experience.

![alt text](figures/salary_by_experience.png) 

### Encoding

## Analysis
The analysis was perfomred using `statsmodels` OLS. Initially



## Results


## Assumptions and Limitations
* residuals spread for high earners

## Next Steps


## How to Reproduce
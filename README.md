# SWE-DS-Salary-Estimator
SWE-DS-Salary-Estimator is a project to estimate the Salary Range for SWE and Data Science Job (MAE: ~4k). The main idea is by training several models using real data and find the best model to be used as the predictor. The data are scrapped from glassdoor.com using Selenium. Then, Data Cleaning and Analysis performed in order to provide the training data and gather information of how the data distributed and related one another.

Thus, the 4 mains steps for this project are:
* Scrapped SWE and Data Science job postings from glassdoor.com using Selenium (over 5000 postings)
* Cleaned the scrapped data to provide the training data and separate the parameter and result.
* Performed Exploritory Data Analysis gather information of how the data distributed and related one another.
* Trained Linear, XGBoost, Random Forest Regressors and Deep Learning to find the best model with minimum Mean Value Error (MAE).
* Provided Client API to run prediction model using Flask.

## 
**Python Version:** 3.7  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
**Run Locally:**
1. ```pip install -r requirements.txt```  to install all the web framework requirements.
2. ```python wsgi``` to start the Flask API server.
3. ```python request``` to run the provided example prediction test from `test_data.csv`
Currently for display, `test_data.csv` contains the cleaned data which can be run in `request.py`. The main `input_data_parser` function will get csv file location and return input data for the model.

## Glassdoor Web Scraping
Scraped 5000+ SWE and Data Science job postings distributed across 4 main cities: Toronto, Vancouver, New York and California from glassdoor.com using Selenium. The result are provided:
*	Job title
*	Job Location
* Job Company
*	Salary Estimate
*	Company Rating
*	Company Rating Numbers
*	Company Size
*	Company Type 
*	Company Industry
*	Company Sector
*	Company Revenue
*	Company Founded Date

Beside of the program, the scrapping function can be used separately which will return a csv files for a job using job name and job location as the parameter.
(Additionally, there are also LinkedIn scrapper provided there which functionally work and can be used to add job postings from LinkedIn)

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:
*	Parsed numeric data out of salary from `Salary Estimate` column.
*	Separated Salary Range to `Maximum` and `Minimum` from `Salary Estimate` column
*	Parsed currency code from `Salary Estimate` column
*	Converted Hourly salary to Anual Salary.
*	Cleaned up `Job Company` and `Company Rating` from additional strings.
*	Assigned `"Unknown"` value for missing company information.
*	Added new column `Level` from parsing `Job title` to get seniority level.
*	Added new column `Role` to get classification role from `Job Title`

## Exploritory Data Analysis
The Data provided for training are consisting of categorical and regression data. So, for each type of data, analysis was performed to find the relation of each data and the distribution. By using Seaborn and Matplotlib, the plotted data can be seen as below:

![alt text](https://github.com/Jocn2020/SWE-DS-Salary-Estimator/blob/main/EDA_img/regression_data_summary.png "Regression Data Summary")
![alt text](https://github.com/Jocn2020/SWE-DS-Salary-Estimator/blob/main/EDA_img/company_founded_distribution.png "Company Founded Year Distribution")
![alt text](https://github.com/Jocn2020/SWE-DS-Salary-Estimator/blob/main/EDA_img/rating_boxplot.png "Company Rating Box plot")
![alt text](https://github.com/Jocn2020/SWE-DS-Salary-Estimator/blob/main/EDA_img/roles_%20barplot.png "Roles Bar plot")

## Model Building and Performance
First, the cleaned data will be converted to dummy in order to handle classification data. The standard for the model will be Mean Value Error. 
There are 4 models trained consisting of: 
1. Linear Regression: Always start with the simplest one.
2. Two Layers Neural Network: Checking how deep learning model can fit with regression data.
3. XGBoost: Checking how Gradient Descent Boosting performance toward regression data.
4. Random Forest: Common model used for regression prediction

The MAE for each model are provided bellow:
*	**Linear Regression**: MAE = ~16792.18
*	**Two Layers Neural Network** : MAE = ~11382.29
*	**Random Forest** : MAE = ~4477.67
*	**XGBoost** : MAE = ~9070.99

The Random Forest can be seen to outperfomed the other models so it will be used as the main prediction model.

## Deployment
The best model is deployed using Flask API and can be used to predict the Salary Range based on the information provided after data cleaning. The Flask API Endpoint will take request from list of informations then return the prediction.

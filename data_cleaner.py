import pandas as pd
import math

# clean data from scrapping result, based on data_cleaner.ipynb
def get_dataset(jobs_json):
    jobs_df= pd.read_csv(jobs_json)
    jobs_df['Company Rating'] = jobs_df['Company Rating'].apply(lambda x: '0' if x == '-1' else x)

    # drop estimated salary which is nan
    jobs_df.dropna(subset = ["Salary Estimate"], inplace=True)
    # get salary est range and convert K to 000
    salary_est = jobs_df['Salary Estimate'].apply(lambda x: str(x).replace('K','000').split('(')[0].split('-'))
    salary_currency = jobs_df['Salary Estimate'].apply(lambda x: str(x).split('$')[0] if str(x).split('$')[0] != '' else 'USD')

    # remove currency from salary_est
    salary_est = salary_est.apply(lambda x: [salary.split('$')[1] for salary in x])

    # replace salary that contains per hour to yearly, assuming working days = 40hr/week * 52
    total_hours = 40*52
    salary_est_float = salary_est.apply(lambda x: [float(salary.split()[0])*total_hours if "per hour" in ''.join(x).lower() 
                                            else float(salary) for salary in x])

    # replace salary with no range to set max and min = salary
    salary_est_range = salary_est_float.apply(lambda x: x + [x[0]] if len(x) < 2 else x)

    # split into maximum and minimum
    salary_est_final = pd.DataFrame()
    salary_est_final["Minimum"] = salary_est_range.apply(lambda x: x[0])
    salary_est_final["Maximum"] = salary_est_range.apply(lambda x: x[1])
    salary_est_final['Currency'] = salary_currency

    # clean up company data
    jobs_df_cleaned = jobs_df.copy()
    del jobs_df_cleaned['Salary Estimate'] # remove salary from test data
    jobs_df_cleaned['Job Title'] = jobs_df_cleaned['Job Title']
    jobs_df_cleaned['Job Company'] = jobs_df_cleaned['Job Company'].apply(lambda x: x.split('\n')[0])
    jobs_df_cleaned['Company Rating'] = jobs_df_cleaned['Company Rating'].apply(lambda x: float(x.split('\n')[0]))
    jobs_df_cleaned['Company Founded'] = jobs_df_cleaned['Company Founded'].apply(lambda x: int(x) if not math.isnan(x) else 0)
    jobs_df_cleaned.fillna("Unknown", inplace=True)

    # Get Seniority Job level
    def seniority(title):
        if "sr" in title.lower() or "senior" in title.lower() or "principal" in title.lower() or "lead" in title.lower():
            return "Senior"
        elif "intern" in title.lower():
            return "Intern"
        elif "grad" in title.lower() or "entry" in title.lower() or "junior" in title.lower():
            return "Junior"
        else:
            return "Normal"
        
    jobs_df_cleaned["Level"] = jobs_df['Job Title'].apply(lambda x: seniority(x))
    return pd.concat([jobs_df_cleaned, salary_est_final], axis=1)


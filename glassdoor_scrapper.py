from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pdb import set_trace as bp
import pandas as pd
import time
import json
import os

def get_glassdoor_jobs(job_keyword, job_location, num_of_jobs):
    driver = webdriver.Chrome('./chromedriver')
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + job_keyword + \
    '&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1\
    &minRating=0.0&industryId=-1&sgocId=-1&seniorityType=entry&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    location_search = driver.find_element(By.XPATH, '//input[contains(@aria-label,"Search Location")]')
    location_search.send_keys(job_location)
    search_button = driver.find_element(By.XPATH, '//button[contains(@title, "Submit search")]')
    search_button.click()
    time.sleep(1)
    jobs = []
    current_page = 1
    
    while len(jobs) < num_of_jobs:
        job_list = driver.find_elements(By.XPATH, '//li[contains(@class,"react-job-listing")]')
        page_selects = driver.find_elements(By.XPATH,"//div[@class='middle']//li")

        def job_title(job):
            return job.find_element(By.XPATH, '//div[contains(@class,"e1tk4kwz2")]').text
        def job_company(job):
            return job.find_element(By.XPATH, '//div[contains(@class,"e1tk4kwz5")]').text
        def job_loc(job):
            return job.find_element(By.XPATH, '//div[contains(@class,"e1tk4kwz1")]').text
        def job_company_salary_est(job):
            try:
                salary = job.find_element(By.XPATH, './/span[contains(@data-test,"detailSalary")]')
                return salary.text
            except NoSuchElementException:
                return '-1'
        def job_company_rating(job):
            try:
                rating = job.find_element(By.XPATH, '//div[contains(@data-test,"rating-info")]')
                num_ratings = driver.find_element(By.XPATH, '//div[contains(text(),"Ratings")]')
                return (rating.text, num_ratings.text.split(' ')[0])
            except NoSuchElementException:
                return ('-1', '0')
        def company_overview(job):
            try:
                overviews = job.find_elements(By.XPATH, '//div[contains(@class,"css-daag8o")]')
                overview_dict = {}
                if overviews:
                    for overview in overviews:
                        overview_data = overview.find_elements(By.XPATH, './/span')
                        overview_dict['Company ' + overview_data[0].text] = overview_data[1].text
                return overview_dict
            except NoSuchElementException:
                return {}

        for job in job_list:
            job.click()
            # sign in pop up skip
            try:
                driver.find_element(By.XPATH, "//span[contains(@alt,'Close')]").click()
            except NoSuchElementException:
                pass
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@data-test,'hero-header')]")))
            except TimeoutException:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@data-test,'hero-header')]")))
            job_data = {
                'Job Title': job_title(job),
                'Job Company': job_company(job),
                'Job Location': job_loc(job),
                'Salary Estimate': job_company_salary_est(job),
                'Company Rating': job_company_rating(job)[0],
                'Company Rating Numbers':  job_company_rating(job)[1],
            }
            job_data.update(company_overview(job))
            if job_data['Salary Estimate'] != '-1':
                jobs.append(job_data)

        for i,page in enumerate(page_selects):
            if str(current_page) == page.text:
                page_selects[i+1].click()
                current_page += 1
                time.sleep(2)
                break
            
    return jobs

if __name__ == "__main__":
    roles_checkpoint = {
        "Software Engineer": {
            "Toronto": {
                "number": 500, 
                "complete": False
            },
            "Vancouver": {
                "number": 500, 
                "complete": False
            },
            "New York": {
                "number": 900, 
                "complete": False
            },
            "San Francisco": {
                "number": 900, 
                "complete": False
            }
        },
        "Data Science": {
            "Toronto": {
                "number": 500, 
                "complete": False
            },
            "Vancouver": {
                "number": 500, 
                "complete": False
            },
            "New York": {
                "number": 900, 
                "complete": False
            },
            "San Francisco": {
                "number": 900, 
                "complete": False
            }
        }
    }
    if not os.path.isfile('job_checkpoint.json'):
        with open('job_checkpoint.json', 'w') as f:
            json.dump(roles_checkpoint, f)

    with open('job_checkpoint.json', 'r') as f:
        roles = json.loads(f.read())

    for role in roles:
        for location in roles[role]:
            location_info = roles[role][location]
            if not location_info["complete"]: 
                jobs_dataframe = pd.DataFrame(get_glassdoor_jobs(role, location, location_info["number"]))
                jobs_dataframe.to_csv('glassdoor_jobs_' + role.replace(" ","_") + '_' + location.replace(" ","_") + '.csv', index=False)
                roles[role][location]["complete"] = True  
                with open("job_checkpoint.json", "w") as jsonFile:
                    json.dump(roles, jsonFile)
                
                    

        
        


        
        







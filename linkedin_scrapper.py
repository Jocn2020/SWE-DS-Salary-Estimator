from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_scrapper import Element, MultiElement 
from pdb import set_trace as bp
import time

def search_job(driver, role, loc=None):
    search_job = Element(driver, '//input[contains(@aria-label,"job titles")]')
    search_loc = Element(driver, '//input[contains(@aria-label,"Location")]')
    # insert search input
    search_job.clear()
    search_job.send_keys(role)
    if loc:
        search_loc.clear()
        search_loc.send_keys("Canada")
        search_loc.send_keys(Keys.ENTER)
    else:
        search_job.send_keys(Keys.ENTER)
    WebDriverWait(driver,10).until(EC.visibility_of_element_located(
            (By.XPATH, "//ul[contains(@class,'jobs-search')]")))

def browse_all_jobs(driver, num_of_jobs):
    i = 2
    while i <= int(num_of_jobs/25)+1: 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i = i + 1
        try:
            driver.find_element_by_xpath('//button[contains(.,"See more jobs")]').click()
            time.sleep(5)
        except:
            pass
            time.sleep(5)

def get_all_jobs(driver):
    jobs_lists = driver.find_element(By.XPATH, "//ul[contains(@class,'jobs-search')]")
    jobs = jobs_lists.find_elements(By.XPATH,".//li")
    result = {
        'role': [],
        'company': [],
        'location': [],
        'job-type': [],
        'num-of-employees': [],
        'company-type': []
    }
    return [job.find_element(By.XPATH, ".//h3[contains(@class,'_title')]").text for job in jobs]

if __name__ == "__main__":
    PATH = "./chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.linkedin.com/jobs/search?")
    WebDriverWait(driver,10).until(EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(.,'LinkedIn')]")))
    search_job(driver, "Software Engineer", "Canada")
    bp()
    browse_all_jobs(driver, 500)
    result = get_all_jobs(driver)



    
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("ACCESS_EMAIL")
password = os.getenv("PASSWORD")

#Details of the course module
program_id="1467"
course_id="21986"
module_id="133624"

#Initializing the URLs
program_url="https://teach.upgrad.com/course/"+program_id+"/modulegroups"
course_url="https://teach.upgrad.com/course/"+program_id+"/modulegroup/"+course_id
module_url="https://teach.upgrad.com/course/"+program_id+"/module/"+module_id


#Starting the webdriver
s = Service(executable_path="C:\\chromedriver.exe")
driver=webdriver.Chrome(service=s)
driver.maximize_window()
driver.get("https://teach.upgrad.com/")

#Logging in
driver.find_element(by=By.XPATH, value="//input[@name='username']").send_keys(username)
driver.find_element(by=By.XPATH, value="//input[@name='password']").send_keys(password)
time.sleep(2)
driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()

#Waiting for it to load
WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//*[@class='courses-container']")))
time.sleep(5)

url="https://teach.upgrad.com/course/1467/module/133624/session/418291/segment/2164869"
driver.get(url)
WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//div[@class='editor']//p")))
text="""Hey, just testing this text content upload script. Hope you don't mind.
Second paragraph begins here.
Third paragraph begins here. Jaabbaaa.
"""
time.sleep(3)
driver.find_element(by=By.XPATH, value="//div[@class='editor']//p").send_keys(text)
driver.find_element(by=By.XPATH, value="//button[@class='save-components btn btn-primary main-button']").click()
time.sleep(5)

driver.close()
driver.quit()
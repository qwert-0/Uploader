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

driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value="//div[@id='add-video']"))
time.sleep(3)

name="Caltech - Cyber - B01 - 1.4.1-V01"
id="6305934503112"

handles=driver.window_handles
driver.switch_to.window(handles[0])

WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control name"]')))
driver.find_element(by=By.XPATH, value='//*[@class="form-horizontal save-video-form"]//input[@class="form-control name"]').send_keys(name)
driver.find_element(by=By.XPATH, value='//*[@class="form-horizontal save-video-form"]//input[@class="form-control jwplayerid"]').send_keys(id)
time.sleep(2)

driver.find_element(by=By.XPATH, value='//*[@class="form-horizontal save-video-form"]//button[@class="btn btn-default btn-primary modal-save-button"]').click()
time.sleep(3)

driver.get(url)

driver.close()
driver.quit()
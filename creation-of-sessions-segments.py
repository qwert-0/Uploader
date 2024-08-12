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

content={}
content["Overview of an Application"]=["Module Introduction", "Session Introduction", "Overview of a Program", "Exploiting the Linux $PATH Variable", "Memory Layout", "Session Summary"]
content["Second session"]=["Module Introduction", "Session Introduction", "Overview of a Program", "Exploiting the Linux $PATH Variable"]

url=module_url
driver.get(url)
WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//*[@class='module-name module-info-cell ellipsis']")))
module_name=driver.find_element(by=By.XPATH, value="//div[@class='module-name module-info-cell ellipsis']").get_attribute("innerHTML").strip()
module_name=module_name.replace("&amp;","&")
print(module_name)
time.sleep(1)

i=0

for sessions in content.keys():
    #clicking session creation button
    create_session_button=driver.find_element(by=By.XPATH, value='//div[@id="sessions"]//button[@class="btn-default create-session-btn"]')
    create_session_button.click()
    time.sleep(1)

    handles=driver.window_handles
    driver.switch_to.window(handles[0])

    session_name_field=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@id="session-name"]')))
    session_name_field.send_keys(sessions)
    time.sleep(1)

    session_button=driver.find_element(by=By.XPATH, value='//button[@id="add-session"]')
    session_button.click()
    time.sleep(5)

    for segments in content[sessions]:
        time.sleep(2)
        handles=driver.window_handles
        driver.switch_to.window(handles[0])

        create_segment_buttons=driver.find_elements(by=By.XPATH, value='//*[@id="segment-list-container"]//button')
        #create_segment_button.click()
        driver.execute_script("arguments[0].click();", create_segment_buttons[i])
        time.sleep(1)

        handles=driver.window_handles
        driver.switch_to.window(handles[0])

        segment_name_field=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@id="segment-name"]')))
        segment_name_field.send_keys(segments)
        time.sleep(1)

        segment_button=driver.find_element(by=By.XPATH, value='//button[@id="add-segment"]')
        segment_button.click()

        time.sleep(3)

        back_button=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@class="glyphicon glyphicon-chevron-left"]')))
        back_button.click()
        WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//*[@class='module-name module-info-cell ellipsis']")))
    time.sleep(3)
    i+=1

driver.close()
driver.quit()
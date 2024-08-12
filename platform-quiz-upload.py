from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
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


driver.find_element(by=By.XPATH, value="//div[@id='add-content']").click()
time.sleep(3)

handles=driver.window_handles
driver.switch_to.window(handles[0])

WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control name"]')))
quiz_name_field=driver.find_element(by=By.XPATH, value='//input[@class="form-control name"]')
driver.execute_script("arguments[0].click();", quiz_name_field)
quiz_name_field.send_keys("Testing name")
time.sleep(1)

driver.find_element(by=By.XPATH, value="//button[@class='btn btn-default btn-primary modal-save-button']").click()
time.sleep(3)

type="mcq"
name="testing name"
problem_statement="Just testing the problem statement"
num_options="4"
options=["option1","option2","option3","option4"]
feedbacks=["feedback for "+x for x in options]
correct_options=["1","2"]

WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//div[@class="scq-option-button question-type btn btn-primary"]')))

if type=="scq":
    driver.find_element(by=By.XPATH, value="//div[@class='scq-option-button question-type btn btn-primary']").click()

elif type=="mcq":
    driver.find_element(by=By.XPATH, value="//div[@class='mcq-option-button question-type btn btn-primary']").click()

time.sleep(3)

question_name_field=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control question-title"]')))
driver.execute_script("arguments[0].click();", question_name_field)
question_name_field.send_keys(name)
time.sleep(1)

driver.switch_to.frame(driver.find_element(by=By.XPATH, value="//iframe[@class='cke_wysiwyg_frame cke_reset']"))

driver.find_element(by=By.XPATH, value="/html/body").click()
time.sleep(2)

driver.find_element(by=By.XPATH, value="/html/body/p").send_keys(problem_statement)
driver.switch_to.default_content()

drop_menu=Select(driver.find_element(by=By.NAME, value="option-count"))
drop_menu.select_by_value(num_options)

"""if type=="scq":
    ques_options=driver.find_elements(by=By.XPATH, value='//div[@class="form-control option-input-field cke_editable cke_editable_inline cke_contents_ltr placeholder"]')
    ques_feed=driver.find_elements(by=By.XPATH, value='//div[@class="scq-feedback-input form-control cke_editable cke_editable_inline cke_contents_ltr placeholder"]')
    
    i=0
    for opt,feed in zip(ques_options,ques_feed):
        opt.send_keys(options[i])
        feed.send_keys(feedbacks[i])
        i+=1

    time.sleep(2)
    correct_option_click=driver.find_elements(by=By.XPATH, value="//form[@class='single-option-quiz question-form']//input[@class='radio-button']")[int(correct_option)-1]
    driver.execute_script("arguments[0].click();", correct_option_click)
    time.sleep(10)"""

if type=="mcq":
    ques_options=driver.find_elements(by=By.XPATH, value='//div[@class="mcq-text-input form-control option-input-field cke_editable cke_editable_inline cke_contents_ltr placeholder"]')
    ques_feed=driver.find_elements(by=By.XPATH, value='//div[@class="mcq-feedback-input form-control cke_editable cke_editable_inline cke_contents_ltr placeholder"]')
    
    i=0
    for opt,feed in zip(ques_options,ques_feed):
        opt.send_keys(options[i])
        feed.send_keys(feedbacks[i])
        i+=1

    for j in correct_options:
        correct_option_click=driver.find_elements(by=By.XPATH, value="//form[@class='checkbox-option-quiz question-form']//input[@class='mcq-checkbox-input radio-button']")[int(j)-1]
        driver.execute_script("arguments[0].click();", correct_option_click)

#setting number of attempts as 2
attempts_menu=Select(driver.find_element(by=By.NAME, value="attempts-allowed"))
attempts_menu.select_by_value("2")

#checking graded
driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value="//input[@name='is_graded']"))

#clicking submit
driver.find_element(by=By.XPATH, value="//button[@class='btn btn-default btn-primary main-button-quiz-builder disable-submit-for-image-upload']").click()
time.sleep(4)
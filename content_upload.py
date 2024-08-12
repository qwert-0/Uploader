from operator import mod
from pip import main
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

#This is the function for logging in to the platform.
#driver is the webdriver, user is the username and passw is the password for logging in to the teaching platform.
def logging_in(driver,user,passw):
    #In case there is some error, run this function to reset all cookies and relogin.
    driver.delete_all_cookies()
    driver.get("https://teach.upgrad.com/")

    #waiting for the fields to load
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))

    #sending the username and password to the fields
    driver.find_element(by=By.XPATH, value="//input[@name='username']").send_keys(username)
    driver.find_element(by=By.XPATH, value="//input[@name='password']").send_keys(passwword)
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()  #clicking the login button

    #Waiting for it to load
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//*[@class='courses-container']")))
    time.sleep(5)



#Function for creating the sessions and segments.
#driver is the webdriver, url is the module url and content_dic is the dictionary of sessions and segments
def create_sessions_segments(driver,url,content_dic):
    driver.get(url)
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//*[@class='module-name module-info-cell ellipsis']")))     #waiting for the page to load properly
    module_name=driver.find_element(by=By.XPATH, value="//div[@class='module-name module-info-cell ellipsis']").get_attribute("innerHTML").strip()
    module_name=module_name.replace("&amp;","&")        #converting the encoded format into readable format
    print(module_name)
    time.sleep(1)

    i=0

    for sessions in content_dic.keys():
        #clicking session creation button
        create_session_button=driver.find_element(by=By.XPATH, value='//div[@id="sessions"]//button[@class="btn-default create-session-btn"]')
        create_session_button.click()
        time.sleep(1)

        #switching to the new handle
        handles=driver.window_handles
        driver.switch_to.window(handles[0])

        #inputting the session name and adding the session
        session_name_field=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@id="session-name"]')))
        session_name_field.send_keys(sessions)
        time.sleep(1)
        session_button=driver.find_element(by=By.XPATH, value='//button[@id="add-session"]')
        session_button.click()
        time.sleep(3)

        #for each segment in the dictionary of sessions
        for segments in content_dic[sessions]:
            time.sleep(2)
            #switching to the previous handle to avoid issues
            handles=driver.window_handles
            driver.switch_to.window(handles[0])

            #clicking on the create segments button
            create_segment_buttons=driver.find_elements(by=By.XPATH, value='//*[@id="segment-list-container"]//button')
            driver.execute_script("arguments[0].click();", create_segment_buttons[i])
            time.sleep(1)

            #switching to the new handle
            handles=driver.window_handles
            driver.switch_to.window(handles[0])

            #inputting the segment name and adding the segment
            segment_name_field=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@id="segment-name"]')))
            segment_name_field.send_keys(segments)
            time.sleep(1)
            segment_button=driver.find_element(by=By.XPATH, value='//button[@id="add-segment"]')
            segment_button.click()
            time.sleep(3)

            #since clicking on the submit button will take us to the newly created segment's page, clicking on the back button to go back to the previous page
            back_button=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//*[@class="glyphicon glyphicon-chevron-left"]')))
            back_button.click()
            WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//*[@class='module-name module-info-cell ellipsis']")))
        time.sleep(3)
        i+=1


#Function for inserting platform text into the segment
#driver is the web driver, url is the segment url and text is the platform text to be inserted
def platform_text_upload(driver,url,text):
    driver.get(url)
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//div[@class='editor']//p")))       #waiting for the page to load properly
    time.sleep(3)
    #inputting the text and clicking on save changes
    driver.find_element(by=By.XPATH, value="//div[@class='editor']//p").send_keys(text)
    driver.find_element(by=By.XPATH, value="//button[@class='save-components btn btn-primary main-button']").click()
    time.sleep(5)



def quiz_upload(driver,url,name,type,ques_name,statement,options,feedbacks,correct_option):
    driver.get(url)
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//div[@class='editor']//p")))       #waiting for the page to load properly

    num_options=str(len(options))       #number of options is the length of the options list

    #clicking on the add quiz button
    driver.find_element(by=By.XPATH, value="//div[@id='add-content']").click()
    time.sleep(3)

    #switching to the next window handle
    handles=driver.window_handles
    driver.switch_to.window(handles[0])

    #inputting the quiz name and clicking on submit
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control name"]')))
    quiz_name_field=driver.find_element(by=By.XPATH, value='//input[@class="form-control name"]')
    driver.execute_script("arguments[0].click();", quiz_name_field)
    quiz_name_field.send_keys("Testing name")
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//button[@class='btn btn-default btn-primary modal-save-button']").click()
    time.sleep(3)

    #checking for question type and clicking on respective button for adding question
    if type=="scq":
        driver.find_element(by=By.XPATH, value="//div[@class='scq-option-button question-type btn btn-primary']").click()

    elif type=="mcq":
        driver.find_element(by=By.XPATH, value="//div[@class='mcq-option-button question-type btn btn-primary']").click()

    time.sleep(3)

    #entering the question name
    question_name_field=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control question-title"]')))
    driver.execute_script("arguments[0].click();", question_name_field)
    question_name_field.send_keys(name)

    #switching to the iframe and entering the problem decription
    driver.switch_to.frame(driver.find_element(by=By.XPATH, value="//iframe[@class='cke_wysiwyg_frame cke_reset']"))
    driver.find_element(by=By.XPATH, value="/html/body").click()
    driver.find_element(by=By.XPATH, value="/html/body/p").send_keys(problem_statement)
    driver.switch_to.default_content()      #switching back to the main content

    #selecting the drop down meny and setting the option as number of options
    drop_menu=Select(driver.find_element(by=By.NAME, value="option-count"))
    drop_menu.select_by_value(num_options)

    #finding the elements for options and feedbacks
    ques_options=driver.find_elements(by=By.XPATH, value='//div[@class="form-control option-input-field cke_editable cke_editable_inline cke_contents_ltr placeholder"]')
    ques_feed=driver.find_elements(by=By.XPATH, value='//div[@class="scq-feedback-input form-control cke_editable cke_editable_inline cke_contents_ltr placeholder"]')

    i=0
    #iterating through each option and inputting the option and feedback
    for opt,feed in zip(ques_options,ques_feed):
        opt.send_keys(options[i])
        feed.send_keys(feedbacks[i])
        i+=1

    #setting the correct option
    correct_option_click=driver.find_elements(by=By.XPATH, value="//form[@class='single-option-quiz question-form']//input[@class='radio-button']")[int(correct_option)-1]
    driver.execute_script("arguments[0].click();", correct_option_click)

    #setting number of attempts as 2
    attempts_menu=Select(driver.find_element(by=By.NAME, value="attempts-allowed"))
    attempts_menu.select_by_value("2")

    #checking graded
    driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value="//input[@name='is_graded']"))
    
    #clicking submit
    driver.find_element(by=By.XPATH, value="//button[@class='btn btn-default btn-primary main-button-quiz-builder disable-submit-for-image-upload']").click()
    time.sleep(4)

def video_upload(driver,url,name,id):
    driver.get(url)
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, "//div[@class='editor']//p")))       #waiting for the page to load properly

    #clicking on the add video button
    driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value="//div[@id='add-video']"))
    time.sleep(3)

    #switching to the new window handle
    handles=driver.window_handles
    driver.switch_to.window(handles[0])

    #entering the video details and adding the video
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '//input[@class="form-control name"]')))
    driver.find_element(by=By.XPATH, value='//*[@class="form-horizontal save-video-form"]//input[@class="form-control name"]').send_keys(name)
    driver.find_element(by=By.XPATH, value='//*[@class="form-horizontal save-video-form"]//input[@class="form-control jwplayerid"]').send_keys(id)
    time.sleep(2)
    driver.find_element(by=By.XPATH, value='//*[@class="form-horizontal save-video-form"]//button[@class="btn btn-default btn-primary modal-save-button"]').click()
    time.sleep(3)

    #going back to the segment url
    driver.get(url)
    

if __name__=="__main__":
    #Initializing the URLs
    #module_url=input("Enter the module url (in the format 'https://teach.upgrad.com/course/1467/module/133624'):")
    module_url="https://teach.upgrad.com/course/1467/module/133624"
    segment_url="https://teach.upgrad.com/course/1467/module/133624/session/418291/segment/2164869"


    
    #Details of sessions and segments
    content={}
    content["Overview of an Application"]=["Module Introduction", "Session Introduction", "Overview of a Program", "Exploiting the Linux $PATH Variable", "Memory Layout", "Session Summary"]
    content["Second session"]=["Module Introduction", "Session Introduction", "Overview of a Program", "Exploiting the Linux $PATH Variable"]

    #text for platform upload
    text="Hey, just testing this text content upload script.\n\nSecond paragraph begins here.\n\nThird paragraph begins here. Jaabbaaa."

    #quiz details
    quiz_name="Testing quiz name"
    question_type="scq"
    question_name="testing name"
    problem_statement="Just testing the problem statement"
    options=["option1","option2","option3","option4"]
    feedbacks=["feedback for "+x for x in options]
    correct_option="3"

    #video details
    video_name="Caltech - Cyber - B01 - 1.4.1-V01"
    video_id="6305934503112"

    #Starting the webdriver
    s = Service(executable_path="C:\\chromedriver.exe")
    main_driver=webdriver.Chrome(service=s)
    main_driver.maximize_window()

    logging_in(main_driver,username,password)
    platform_text_upload(main_driver,segment_url,text)
    quiz_upload(main_driver,segment_url,quiz_name,question_type,question_name,problem_statement,options,feedbacks,correct_option)
    video_upload(main_driver,segment_url,video_name,video_id)

    main_driver.get(segment_url)
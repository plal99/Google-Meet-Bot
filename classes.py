
#! Change below only

JOIN_PEOPLE = 5
LEAVE_PEOPLE = 15

#! Change above only

LEAVE_PEOPLE_SEC = LEAVE_PEOPLE + 3



import re
import os
from dotenv import load_dotenv
# import datetime
import time
# Selenium necessary library functions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from notify import sendDiscord, sendTelegram, sendWhatsapp

# loading environment
load_dotenv()


# gmail username and password
USERNAME = os.getenv("USERNAME1")
PASSWORD = os.getenv("PASSWORD")

# Function for checking the number of people inside meeting
def hasNumbers(inputString):
    return re.search('\s[0-9]+\s', inputString)     


class GoogleMeet():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.link = ""
        self.options = webdriver.ChromeOptions()

        # Setting preferences
        # self.options.add_argument("--mute-audio")
        
        # self.options.add_argument("--profile-directory=Profile 1")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--window-size=800,600")
        self.options.add_experimental_option("prefs", { \
                "profile.default_content_setting_values.media_stream_camera": 2,
                "profile.default_content_setting_values.media_stream_mic": 2, 
                # "profile.default_content_setting_values.geolocation": 2, 
                "profile.default_content_setting_values.notifications": 2 
        })

        # This takes the profile of the user. #* Mainly because, to eliminate the logging in part.
        self.options.add_argument("user-data-dir=C:\\Users\\lalpr\\AppData\\Local\\Google\\Chrome\\User Data")

        # Driver - Chrome
        self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=self.options)


    def join(self, link, subject):
        
        self.link = link
        self.subject = subject

        # waiting untill the element is available in the website
        wait = WebDriverWait(self.browser, 10)

        # ! START - Profile loaded, so no need to login
        # # google page
        # url = 'https://accounts.google.com/'
        # self.browser.get(url)
       
        # # Finding username textbox and logging the username
        # wait.until(EC.element_to_be_clickable((By.ID, 'identifierId'))).send_keys(self.username)
        # wait.until(EC.element_to_be_clickable((By.ID, 'identifierNext'))).click()
        
        # # Finding password textbox and logging the password
        # wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(self.password)
        # wait.until(EC.element_to_be_clickable((By.ID, 'passwordNext'))).click()
        # print("Logged In")
        # time.sleep(3)

        #! END

        # Going to google meet link
        self.browser.get(link)

        # Refreshing because google found out our automation works
        time.sleep(2)
        self.browser.refresh()

        # Clicking on the dismiss button which comes when camera and mic is off by default in line __inti__ function
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div/div[2]/div[3]/div/span/span'))).click()
        
        # After clicking dismiss button, waiting till somebody joins
        # If nobody is there, an the div class is changes dynamically. This causes error if nobody is there in meeting
        time.sleep(4)
        check = None
        while check is None:
            try:
                inMeet = self.browser.find_elements_by_xpath('//div[@class = "Yi3Cfd"]')
                check = inMeet[0]
            except:
                # Exception comes if nobody is there. So this step is important
                print("Nobody is in the meeting...")
                time.sleep(2)
                pass
        
        # This waits till a space seperated number comes ie. xxx and 12 other in meeting (Here code runs till this 12 number is found)
        while not (hasNumbers(inMeet[0].text)):
            print(inMeet[0].text)
            time.sleep(2)
            inMeet = self.browser.find_elements_by_xpath('//div[@class = "Yi3Cfd"]')

        # Data about join button
        joinClass = self.browser.find_element_by_xpath("/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span")

        # Gets the number of people before the joining the meeting (taking the above example : peopleNum = 12)
        peopleNum = re.findall('\s+[0-9]+\s+', inMeet[0].text)[0].rstrip().lstrip()

        # Loops till number of people inside the meeting (before we enter the meeting) is less than a value
        while (int(peopleNum) < JOIN_PEOPLE):
            time.sleep(2)
            inMeet = self.browser.find_elements_by_xpath('//div[@class = "Yi3Cfd"]')
            peopleNum = re.findall('\s[0-9]+\s', inMeet[0].text)[0].rstrip().lstrip()
            print(peopleNum)
        print("Joining class - People num : ", peopleNum)
        
        # Click on the join button
        joinClass.click()

        # messaging part
        message = "Joined "+ self.subject +" class"
        sendDiscord(message)
        sendTelegram(message)
        sendWhatsapp(message)
        time.sleep(5)

    def leave(self, link, subject):
        self.link = link
        self.subject = subject

        # Gets the number of people inside the meeting
        online = self.browser.find_elements_by_xpath('//span[@class = "wnPUne N0PJ8e"]')
        onlineNum = re.findall('[0-9]+', online[0].text)[0].rstrip().lstrip()
        maxPeople = int(onlineNum)

        # Wait till some students enter the class. This is make sure that our leaving time is at 15 students
        # If this not done, instant leaving would happen
        while (int(onlineNum) < LEAVE_PEOPLE_SEC):
            online = self.browser.find_elements_by_xpath('//span[@class = "wnPUne N0PJ8e"]')
            onlineNum = re.findall('[0-9]+', online[0].text)[0].rstrip().lstrip()
            maxPeople = int(onlineNum)

        # Loops till the number of people is greater than a value
        while (int(onlineNum) >= LEAVE_PEOPLE):
            time.sleep(5)
            online = self.browser.find_elements_by_xpath('//span[@class = "wnPUne N0PJ8e"]')
            onlineNum = re.findall('[0-9]+', online[0].text)[0].rstrip().lstrip()

            # To get the maximum number of people inside the meeting during the entire course of the meeting
            if (int(onlineNum) > maxPeople):
                maxPeople = int(onlineNum)
                print("Max people: ", maxPeople)

            # When lots of people leave(greater than 10), we get a notification
            if (maxPeople - int(onlineNum) > 10):
                sendDiscord("Class about to get over")
                sendWhatsapp("Class about to get over")
                sendTelegram("Class about to get over")
                maxPeople = int(onlineNum)

            print("Online people: ", onlineNum)
        
        # Clicking on the people element to activate leave button and then clicking on leave button using javascipt
        self.browser.find_element_by_xpath('//span[@class = "wnPUne N0PJ8e"]').click()
        button = self.browser.find_element_by_xpath('/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[9]/div[2]/div[2]/div/div[1]')
        self.browser.execute_script("arguments[0].click();", button)

        # messaging part
        message = "Leaving "+ subject +" class"
        sendDiscord(message)
        sendWhatsapp(message)
        sendTelegram(message)
        print("Log out")
        
        # Closing the browser
        self.browser.quit()
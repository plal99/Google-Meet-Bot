# $ pip install notify-run
# $ notify-run configure https://notify.run/oduMTzm40TzRcNv4
# $ notify-run send "Hello from notify.run"

TIMETABLE_MODIFICATION_ENABLED = False

import re
import os
import time
import datetime
import sqlite3
import requests
from dotenv import load_dotenv
from discord_webhooks import DiscordWebhooks
from twilio.rest import Client 
# Selenium necessary library functions
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# import pause
# from pynput.mouse import Button, Controller

# This module is for notification (very hassle free - please check it out)
from notify_run import Notify

# loading environment
load_dotenv()

# discord
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

# gmail username and password
USERNAME = os.getenv("USERNAME1")
PASSWORD = os.getenv("PASSWORD")

# whatsapp twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUM = os.getenv("TWILIO_NUM")
MY_NUM = os.getenv("MY_NUM")

# client = Client(TWILIO_SID, TWILIO_TOKEN)

# telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# connection to sql database
conn = sqlite3.connect('timetable.db')
db = conn.cursor()

def sendTelegram(message):
    send_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + TELEGRAM_CHAT_ID + '&text=' + message
    
    response = requests.get(send_text)

def sendDiscord(message):
    webhook = DiscordWebhooks(DISCORD_WEBHOOK)
    # webhook.set_content(title='Seems like no class today',
    #                     description="No join button found! Assuming no class.")
    webhook.set_content(title = message)
    webhook.send()

def sendWhatsapp(message):
    pass


# Function for checking the number of people inside meeting
def hasNumbers(inputString):
    return re.search('\s[0-9]+\s', inputString)

def createSubjectTable():
    table = """ CREATE TABLE IF NOT EXISTS sub (
                                            id INTEGER PRIMARY KEY,
                                            subject text NOT NULL,
                                            link text
                                        ); """
    db.execute(table)

    sub = {}
    sub[1] = [1, 'ITC', 'https://meet.google.com/dfv-owvb-cpn']
    sub[2] = [2, 'PR', 'https://meet.google.com/egs-mtrt-fic']
    sub[3] = [3, 'MWR', 'https://meet.google.com/inr-ikma-mku']
    sub[4] = [4, 'CC', 'https://meet.google.com/wsm-tyxk-qcj']
    sub[5] = [5, 'SP', 'https://meet.google.com/vbm-bixc-evs']
    sub[6] = [6, 'LAB', 'https://meet.google.com/tog-aqpg-msa']
    sub[7] = [7, 'MEMS', 'https://meet.google.com/onn-po-geddye']
    sub[8] = [8, 'OC', 'https://meet.google.com/ywh-zkes-zhy']
    sub[9] = [9, 'NIL', 'NIL'] # This is for making tempTimeTable have no class during modification

    for i in sub:
        id = sub.get(i)[0]
        subject = sub.get(i)[1]
        link=sub.get(i)[2]
        db.execute("INSERT OR IGNORE INTO sub (id, subject, link) VALUES('%s', '%s', '%s')"%(id, subject, link))

    conn.commit()



def createTimeTable():
    days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    for day in days:
        db.execute(""" CREATE TABLE IF NOT EXISTS '%s' (
                                                time text NOT NULL,
                                                subject text NOT NULL
                                            ); """ % day)

    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("830", "ITC"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("930", "PR"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1030", "MWR"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1130", "CC"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))

    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("830", "CS"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("930", "ITC"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1030", "MEMS"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1130", "MWR"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1230", "LAB"))

    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("830", "OC"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("930", "CS"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1030", "ITC"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1130", "PR"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1230", "MEMS"))

    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("830", "CC"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("930", "OC"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1030", "CS"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1130", "ITC"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1230", "PR"))

    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("855", "CC"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("950", "OC"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1045", "MWR"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1140", "MEMS"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))

    conn.commit()

def createTempTimeTable():
    # This is to create a temp timetable so that in case some teachers modify the timetable just before a class,
    # you can make neccesory modifications
    
    days = ["mondayTemp", "tuesdayTemp", "wednesdayTemp", "thursdayTemp", "fridayTemp"]
    for day in days:
        db.execute(""" CREATE TABLE IF NOT EXISTS '%s' (
                                                time text NOT NULL,
                                                subject text NOT NULL
                                            ); """ % day)

    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "ITC"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "PR"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "MWR"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "CC"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))

    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "CS"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "ITC"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "MEMS"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "MWR"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "LAB"))

    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "OC"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "CS"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "ITC"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "PR"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "MEMS"))

    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "CC"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "OC"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "CS"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "ITC"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "PR"))

    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("855", "CC"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("950", "OC"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1045", "MWR"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1140", "MEMS"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))

    conn.commit()

def modifyTempTimeTable(day, p1, p2, p3, p4, p5):

    perm = db.execute("SELECT * FROM '%s'" % (day))
    perm = perm.fetchall()

    # subs here are all times(better time than subs)
    sub1 = perm[0][0]
    sub2 = perm[1][0]
    sub3 = perm[2][0]
    sub4 = perm[3][0]
    sub5 = perm[4][0]

    dayTemp = day + 'Temp'

    # print(sub1, sub2, sub3, sub4, sub5, dayTemp, day, p1, p2, p3, p4, p5)
    if (p1 != 0):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p1, sub1))
    if (p2 != 0):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p2, sub2))
    if (p3 != 0):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p3, sub3))
    if (p4 != 0):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p4, sub4))
    if (p5 != 0):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p5, sub5))

    conn.commit()
    # perm = db.execute("SELECT * FROM '%s'" % (dayTemp))
    # perm = perm.fetchall()
    # print(perm)

def dropTempTimeTable():
    days = ["mondayTemp", "tuesdayTemp", "wednesdayTemp", "thursdayTemp", "fridayTemp"]
    for day in days:
        db.execute("DROP TABLE IF EXISTS '%s'" % (day))
    conn.commit()

def getLink():
    x = datetime.datetime.now()
    day = x.strftime("%A").lower()
    time = int(x.strftime("%H") + x.strftime("%M"))
    # time = 1045
    mtime = '0'

    if day == 'friday':
        if (time >= 855 and time < 950):
            mtime = '855'
        if (time >= 950 and time < 1045):
            mtime = '950'
        if (time >= 1045 and time < 1140):
            mtime = '1045'
        if (time >= 1140 and time < 1230):
            mtime = '1140'
        if (time >= 1230 and time < 1330):
            mtime = '1230'
    else :
        if (time >= 830 and time < 930):
            mtime = '830'
        if (time >= 930 and time < 1030):
            mtime = '930'
        if (time >= 1030 and time < 1130):
            mtime = '1030'
        if (time >= 1130 and time < 1230):
            mtime = '1130'
        if (time >= 1230 and time < 1330):
            mtime = '1230'

    day = day + 'Temp'
    db.execute("SELECT * FROM '%s' WHERE time = '%s'"%(day, mtime))
    data = db.fetchall()
    classTime = data[0][0]
    subj = data[0][1]

    db.execute("SELECT link FROM sub WHERE subject = '%s'" % subj)
    data = db.fetchall()
    
    link = data[0][0]

    return [subj, link, classTime]     

class GoogleMeet():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.link = ""
        self.options = webdriver.ChromeOptions()

        # Setting preferences
        # self.options.add_argument("--mute-audio")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--window-size=800,600")
        self.options.add_experimental_option("prefs", { \
                "profile.default_content_setting_values.media_stream_camera": 2,
                "profile.default_content_setting_values.media_stream_mic": 2, 
                # "profile.default_content_setting_values.geolocation": 2, 
                "profile.default_content_setting_values.notifications": 2 
        })

        # Driver - Chrome
        self.browser = webdriver.Chrome(options=self.options)


    def join(self, link, subject):
        
        self.link = link
        self.subject = subject

        # waiting untill the element is available in the website
        wait = WebDriverWait(self.browser, 10)

        # google page
        url = 'https://accounts.google.com/'
        self.browser.get(url)
       
        # Finding username textbox and logging the username
        wait.until(EC.element_to_be_clickable((By.ID, 'identifierId'))).send_keys(self.username)
        wait.until(EC.element_to_be_clickable((By.ID, 'identifierNext'))).click()
        
        # Finding password textbox and logging the password
        wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(self.password)
        wait.until(EC.element_to_be_clickable((By.ID, 'passwordNext'))).click()
        print("Logged In")
        time.sleep(3)

        # Going to google meet link
        self.browser.get(link)

        # Refreshing because google found out our automation works
        time.sleep(3)
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
        while (int(peopleNum) < 5):
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
        while (int(onlineNum) < 16):
            online = self.browser.find_elements_by_xpath('//span[@class = "wnPUne N0PJ8e"]')
            onlineNum = re.findall('[0-9]+', online[0].text)[0].rstrip().lstrip()
            maxPeople = int(onlineNum)

        # Loops till the number of people is greater than a value
        while (int(onlineNum) >= 12):
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
                # maxPeople = int(onlineNum)

            print("Online people: ", onlineNum)
        
        # Clicking on the people element to activate leave button and then clicking on leave button using javascipt
        self.browser.find_element_by_xpath('//span[@class = "wnPUne N0PJ8e"]').click()
        button = self.browser.find_element_by_xpath('/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[9]/div[2]/div[2]/div/div[1]')
        self.browser.execute_script("arguments[0].click();", button)

        # messaging part
        message = "Leaving "+ subject +"class"
        sendDiscord(message)
        sendWhatsapp(message)
        sendTelegram(message)
        print("Log out")
        
        # Closing the browser
        self.browser.quit()


if __name__ == "__main__":
    
    

    if(TIMETABLE_MODIFICATION_ENABLED):
        choice = input("Do you want to modify TT for a day (press y/n): ")
        while(choice.lower() == 'y'):
            Mday = input("Enter day to be changed: ")
            Mp1 = input("Enter 1st subject (0: No change, NIL: No class, sub_name: Subject): ")
            Mp2 = input("Enter 2nd subject (0: No change, NIL: No class, sub_name: Subject): ")
            Mp3 = input("Enter 3rd subject (0: No change, NIL: No class, sub_name: Subject): ")
            Mp4 = input("Enter 4th subject (0: No change, NIL: No class, sub_name: Subject): ")
            Mp5 = input("Enter 5th subject (0: No change, NIL: No class, sub_name: Subject): ")

            modifyTempTimeTable(Mday, Mp1, Mp2, Mp3, Mp4, Mp5)
            sendWhatsapp("Timetable for "+ Mday+ " modified")

            choice = input("Do you want to modify TT for another day (or remodify) (press y/n): ")


    # Wait till 8.30AM and 8.55AM if we start program before the class starts
    x = datetime.datetime.now()
    day = x.strftime("%A").lower()
    time1 = int(x.strftime("%H") + x.strftime("%M"))


    if (day == "friday"):
        if (time1 < 855):  # friday time table is different
            print("Waiting for class start time...")
            x = datetime.datetime.now()
            time1 = int(x.strftime("%H") + x.strftime("%M"))
            print("Sleeping for ", (856-time1)*60, " seconds")
            time.sleep((856-time1)*60)
    else:
        if (time1 < 830):
            print("Waiting for class start time...")
            x = datetime.datetime.now()
            time1 = int(x.strftime("%H") + x.strftime("%M"))
            print("Sleeping for ", (831-time1)*60, " seconds")
            time.sleep((831-time1)*60)


    # Loop to make sure the code runs till timetable ends
    prev_subject = 'ITC'
    while(time1 <= 1330):
        data = getLink()
        subject = data[0]
        link = data[1]
        classTime = int(data[2])
        nextClassTime = classTime + 100

        if (time1 % 100) <= 59 and (time1 % 100) >= 30:
            sleepTime = (nextClassTime - time1 - 40) 
        if (time1 % 100) <= 29 and (time1 % 100) >= 0:
            sleepTime = (nextClassTime - time1) 

        if prev_subject != subject:
            if (subject != 'MEMS' and subject != "NIL"):
                obj = GoogleMeet(USERNAME, PASSWORD)
                obj.join(link, subject)
                obj.leave(link, subject)
                prev_subject = subject
            
            else:
                print("MEMS-NIL")
                print("Sleeping for ", sleepTime, " minutes...")
                time.sleep(sleepTime * 60)
        else:
            print("Waiting after class...")
            print("Sleeping for ", sleepTime, " minutes...")
            time.sleep(sleepTime*60)


        x = datetime.datetime.now()
        time1 = int(x.strftime("%H") + x.strftime("%M"))
        
    dropTempTimeTable()
    createTempTimeTable()

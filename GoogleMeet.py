
# As we I am having college mail id, I can enter the meet link without permission. So If you dont have permission, you
# change code so as to ask for permission.

import time
import datetime
from math import floor


from dbStuff import *
from notify import *
from classes import *


def main():

    # Wait till 8.30AM and 8.55AM if we start program before the class starts
    try:
        x = datetime.datetime.now()
        day = x.strftime("%A").lower()
        time1 = int(x.strftime("%H") + x.strftime("%M"))


        if (day == "friday"):
            if (time1 < 855):  # friday time table is different
                print("Waiting for class start time...")
                x = datetime.datetime.now()
                time1 = int(x.strftime("%H") + x.strftime("%M"))
                print("Sleeping for ", (856 - time1), " minutes")
                time.sleep((856-time1)*60)
        else:
            if (time1 < 830):
                print("Waiting for class start time...")
                x = datetime.datetime.now()
                time1 = int(x.strftime("%H") + x.strftime("%M"))
                print("Sleeping for ", (831 - time1), " minutes")
                slt = 831 - time1
                sendTelegram("Sleeping for " +str(slt) + " minutes. Waiting for start of class")
                sendDiscord("Sleeping for "+str(slt)+" minutes. Waiting for start of class")
                time.sleep((831-time1)*60)


        # Loop to make sure the code runs till timetable ends
        prev_subject = '.'
        while(time1 <= 1325):
            data = getLink()
            subject = data[0]
            link = data[1]

            # For making sure code works properly when same subjects for two consecutive hours
            nextSubject = data[4]
            sameSubjectAgain = False
            if (subject == nextSubject) and subject != 'NIL':
                sameSubjectAgain = True

            # * To get the time right
            # classTime = int(data[2])
            # classTimeMin = classTime%100
            # classTimeHour = floor(classTime/100)
            
            # nextClassTime is neesed for the sleeping time 
            nextClassTime = int(data[3])
            nextClassTimeMin = nextClassTime%100
            nextClassTimeHour = floor(nextClassTime/100)

            # timedelta for calculations the difference between the leaving time and the next hour.
            t1 = datetime.timedelta(hours=int(x.strftime("%H")), minutes=int(x.strftime("%M")))
            t2 = datetime.timedelta(hours=nextClassTimeHour, minutes=nextClassTimeMin)

            sleepTime = int((t2-t1)/datetime.timedelta(minutes=1))+1    #! This will be in minutes
            
            hourAttended = False
            if prev_subject != subject:
                if (subject != 'MEMS' and subject != 'NIL'):
                    obj = GoogleMeet(USERNAME, PASSWORD)
                    sendDiscord("Class: " + subject)
                    sendTelegram("Class: " + subject)
                    obj.join(link, subject)
                    obj.leave(link, subject)
                    sendDiscord("Next class: " + nextSubject)
                    sendTelegram("Next class: " + nextSubject)
                    hourAttended = True
                    prev_subject = subject
                    if sameSubjectAgain and hourAttended:
                        prev_subject = '.'
                        # ? Sleep till next hour and attend the next hour
                        x = datetime.datetime.now()
                        t1 = datetime.timedelta(hours=int(x.strftime("%H")), minutes=int(x.strftime("%M")))
                        t2 = datetime.timedelta(hours=nextClassTimeHour, minutes=nextClassTimeMin)

                        sleepTime = int((t2-t1)/datetime.timedelta(minutes=1))
                        time.sleep(sleepTime * 60)
                        
                
                else:
                    print("MEMS-NIL")
                    sendDiscord("Sleeping for " + str(sleepTime) + " minutes...")
                    sendTelegram("Sleeping for "+str(sleepTime)+" minutes...")
                    print("Sleeping for ", sleepTime, " minutes...")
                    time.sleep(sleepTime * 60)
            else:
                print("Waiting after class...")
                print("Sleeping for ", sleepTime, " minutes...")
                sendDiscord("Sleeping for " + str(sleepTime) + " minutes...")
                sendTelegram("Sleeping for "+str(sleepTime)+" minutes...")
                time.sleep(sleepTime*60)


            x = datetime.datetime.now()
            time1 = int(x.strftime("%H") + x.strftime("%M"))

    except:
        sendDiscord("Some error occured! Exiting...")
        sendTelegram("Some error occured! Exiting...")


if __name__ == "__main__":
    main()


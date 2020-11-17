import sqlite3
import os
from dotenv import load_dotenv
from discord_webhooks import DiscordWebhooks


load_dotenv()

DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

conn = sqlite3.connect('timetable.db')
db = conn.cursor()

def sendDiscord(message):
    webhook = DiscordWebhooks(DISCORD_WEBHOOK)
    # webhook.set_content(title='Seems like no class today',
    #                     description="No join button found! Assuming no class.")
    webhook.set_content(title = message)
    webhook.send()

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

    perm = db.execute("SELECT * FROM '%s'" % (day+'Temp'))
    perm = perm.fetchall()

    sendDiscord("Timetable for "+day+" changed.")
    sendDiscord(perm)

    

choice = input("Do you want to modify TT for a day (press y/n): ")
while(choice.lower() == 'y'):
    Mday = input("Enter day to be changed: ")
    Mp1 = input("Enter 1st subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp2 = input("Enter 2nd subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp3 = input("Enter 3rd subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp4 = input("Enter 4th subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp5 = input("Enter 5th subject (0: No change, NIL: No class, sub_name: Subject): ")

    modifyTempTimeTable(Mday, Mp1, Mp2, Mp3, Mp4, Mp5)
    
    choice = input("Do you want to modify TT for another day (or remodify) (press y/n): ")




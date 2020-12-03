import sqlite3
import os
from dotenv import load_dotenv
import datetime

load_dotenv()


def createSubjectTable():
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()
    table = """ CREATE TABLE IF NOT EXISTS sub (
                                            id INTEGER PRIMARY KEY,
                                            subject text NOT NULL,
                                            link text
                                        ); """
    db.execute(table)

    ITC_LINK = os.getenv("ITC_LINK")
    PR_LINK = os.getenv("PR_LINK")
    MWR_LINK = os.getenv("MWR_LINK")
    CC_LINK = os.getenv("CC_LINK")
    SP_LINK = os.getenv("SP_LINK")
    LAB_LINK = os.getenv("LAB_LINK")
    MEMS_LINK = os.getenv("MEMS_LINK")
    OC_LINK = os.getenv("OC_LINK")
    CS_LINK = os.getenv("CS_LINK")
    NIL_LINK = os.getenv("NIL_LINK")

    sub = {}
    sub[1] = [1, 'ITC', ITC_LINK]
    sub[2] = [2, 'PR', PR_LINK]
    sub[3] = [3, 'MWR', MWR_LINK]
    sub[4] = [4, 'CC', CC_LINK]
    sub[5] = [5, 'SP', SP_LINK]
    sub[6] = [6, 'LAB', LAB_LINK]
    sub[7] = [7, 'MEMS', MEMS_LINK]
    sub[8] = [8, 'OC', OC_LINK]
    sub[9] = [9, 'NIL', NIL_LINK]  # This is for making tempTimeTable have no class during modification
    sub[10] = [10, 'CS', CS_LINK]

    for i in sub:
        id = sub.get(i)[0]
        subject = sub.get(i)[1]
        link=sub.get(i)[2]
        db.execute("INSERT OR IGNORE INTO sub (id, subject, link) VALUES('%s', '%s', '%s')"%(id, subject, link))

    conn.commit()
    conn.close()

def dropSubjectTable():
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()
    db.execute("DROP TABLE IF EXISTS '%s'" % ("sub"))
    conn.commit()
    conn.close()

def createTimeTable():
    ''' This is the permanent timetable. You make copies of this to the temp timetables. Done only once. Whatever changes 
    made to time and subject should be made to createTempTimeTable()'''

    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()

    days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    for day in days:
        db.execute(""" CREATE TABLE IF NOT EXISTS '%s' (
                                                nos INTEGER PRIMARY KEY,
                                                time text NOT NULL,
                                                subject text NOT NULL
                                            ); """ % day)

    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("830", "ITC"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("930", "PR"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1030", "MWR"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1130", "CC"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))
    db.execute("INSERT OR IGNORE INTO monday (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("830", "CS"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("930", "ITC"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1030", "MEMS"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1130", "MWR"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1230", "LAB"))
    db.execute("INSERT OR IGNORE INTO tuesday (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("830", "OC"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("930", "CS"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1030", "ITC"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1130", "PR"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1230", "MEMS"))
    db.execute("INSERT OR IGNORE INTO wednesday (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("830", "CC"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("930", "OC"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1030", "CS"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1130", "ITC"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1230", "PR"))
    db.execute("INSERT OR IGNORE INTO thursday (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("855", "CC"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("950", "OC"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1045", "MWR"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1140", "MEMS"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))
    db.execute("INSERT OR IGNORE INTO friday (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    conn.commit()
    conn.close()

def createTempTimeTable():
    '''This is to create a temp timetable so that in case some teachers modify the timetable just before a class,
        you can make neccesory modifications. Done whenevr needed.'''
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()


    days = ["mondayTemp", "tuesdayTemp", "wednesdayTemp", "thursdayTemp", "fridayTemp"]
    for day in days:
        db.execute(""" CREATE TABLE IF NOT EXISTS '%s' (
                                                nos INTEGER PRIMARY KEY,
                                                time text NOT NULL,
                                                subject text NOT NULL
                                            ); """ % day)

    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "ITC"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "PR"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "MWR"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "CC"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))
    db.execute("INSERT OR IGNORE INTO mondayTemp (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "CS"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "ITC"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "MEMS"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "MWR"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "LAB"))
    db.execute("INSERT OR IGNORE INTO tuesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "OC"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "CS"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "ITC"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "PR"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "MEMS"))
    db.execute("INSERT OR IGNORE INTO wednesdayTemp (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("830", "CC"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("930", "OC"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1030", "CS"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1130", "ITC"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "PR"))
    db.execute("INSERT OR IGNORE INTO thursdayTemp (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("855", "CC"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("950", "OC"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1045", "MWR"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1140", "MEMS"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1230", "SP"))
    db.execute("INSERT OR IGNORE INTO fridayTemp (time, subject) VALUES ('%s', '%s')" % ("1330", "NIL"))

    conn.commit()
    conn.close()

def modifyTempTimeTable(day, p1, p2, p3, p4, p5):

    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()

    day = day.lower()
    perm = db.execute("SELECT time, subject FROM '%s'" % (day))
    perm = perm.fetchall()

    # subs here are all times(better time than subjects)
    sub1 = perm[0][0]
    sub2 = perm[1][0]
    sub3 = perm[2][0]
    sub4 = perm[3][0]
    sub5 = perm[4][0]

    dayTemp = day + 'Temp'

    # print(sub1, sub2, sub3, sub4, sub5, dayTemp, day, p1, p2, p3, p4, p5)
    if (p1 != '0'):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p1, sub1))
    if (p2 != '0'):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p2, sub2))
    if (p3 != '0'):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p3, sub3))
    if (p4 != '0'):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p4, sub4))
    if (p5 != '0'):
        db.execute("UPDATE '%s' SET subject = '%s' WHERE time = '%s'" % (dayTemp, p5, sub5))

    conn.commit()

    # perm = db.execute("SELECT * FROM '%s'" % (day+'Temp'))
    # perm = perm.fetchall()

    # sendDiscord("Timetable for "+day+" changed.")
    # perm = db.execute("SELECT * FROM '%s'" % (dayTemp))
    # perm = perm.fetchall()
    # print(perm)
    conn.close()

def dropTempTimeTable():
    ''' Drop all the temp timetables'''
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()

    days = ["mondayTemp", "tuesdayTemp", "wednesdayTemp", "thursdayTemp", "fridayTemp"]
    for day in days:
        db.execute("DROP TABLE IF EXISTS '%s'" % (day))
    
    conn.commit()
    conn.close()

def getLink():
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()

    x = datetime.datetime.now()
    day = x.strftime("%A").lower()
    time = int(x.strftime("%H") + x.strftime("%M"))
    # time = 1045 #! For debugging only
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
    nosTemp = data[0][0]
    classTime = data[0][1]
    subj = data[0][2]

    db.execute("SELECT time, subject FROM '%s' WHERE nos = '%s'"% (day, nosTemp+1))
    data = db.fetchall()
    nextClassTime = data[0][0]
    nextSubj = data[0][1]

    db.execute("SELECT link FROM sub WHERE subject = '%s'" % subj)
    data = db.fetchall()
    
    link = data[0][0]

    conn.close()

    return [subj, link, classTime, nextClassTime, nextSubj]

def printTimetable():
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()

    x = datetime.datetime.now()
    day = x.strftime("%A").lower()

    day = day + 'Temp'
    db.execute("SELECT * FROM '%s' "%(day))
    data = db.fetchall()
    sub1 = data[0][2]
    sub2 = data[1][2]
    sub3 = data[2][2]
    sub4 = data[3][2]
    sub5 = data[4][2]

    conn.close()

    return [sub1, sub2, sub3, sub4, sub5]

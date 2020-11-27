# Google Meet Bot : Online class attender
This is a google meet bot I made for attending your classes. This will 
- Join your class when a number of people are already in it (or wait)
- Leave the class when it reaches a threshold amount of people
- Notify you when classes are about to end (notifies you each and every step)

## How it works
Two codes are needed to run to make this code perfect.
- `GoogleMeet.py` : This code is made in such a way that, if you run the code before the first class start time, it would wait for the start time and attend all the classes in the temporary timetable.
- `telegramBot.py` : This is actually a telegram bot. It can change your time table, do all kinds of stuff by just using some telegram messages. Mainly we are using it to change timetable in the realtime.

Steps to follow:
1. Run `telegramBot.py`. Change timetable if needed (before any current class starts obviously).
2. Run `GoogleMeet.py`.
3. Relax !!!

## In details
### Database
I used sqlite for making a database. There are mainly 3 sets of tables.
- **_sub_** : This contains all the subjects and their corresponding permanent links
- **_monday, tuesday, wednesday, thursday, friday_**: These are permanent timetables each having their corresponding days classes
- **_mondayTemp, tuesdayTemp, wednesdayTemp, thursdayTemp, fridayTemp_**: These are temporary timetables each having their corresponding days classes. If timetable is modified, it is being written here. We overite this temp timetable each time we run the code.

### Joining
I used selenium library for automating the joining and leaving part. It logs in to google and then redirects to your google meet link stored in the database. It waits till someone is in the meeting and joins only when a threshold number of people are present.

### Leaving
It takes into account how much people are in the meeting per 5 seconds, and the maximum number of people present in the class. It will leave the class when number of people inside it goes below a threshold. It even notifies you when classes are about to end automattically

### Notification 
This app has many notification architechtures present
- **_Whatsapp_** (twilio sandbox) : It will notify everything by whatsapp. You need to have account in twilio and register. It costs about 0.0085$ for 1 message and you'll get 15$ when signing up. If you are a college student then you will have a college mail and then you can register github pro for free and get 50$ in twilio.
- **_Discord_** : I created a channel for me and took the discord webhook. It is free and i'll get all notifications in it
- **_Telegram_** : I created a bot in telegram and notifications come in the form of messages from that bot
- **_Notify-run_** : It send you push notifications to browser

## What you have to do:
- You have to create a telegram bot for the start.
### Install
 - Clone the repository `git clone https://github.com/plal99/Google-Meet-Bot.git`
 - Install requirements.txt `pip install -r requirements.txt`

### Make necessary changes
- `.env` : Make necessary changes to the env files so as to fit your personal details.
- Change the `dbStuff.py` so as to fit your requirements. This means changing
    - Links to all the classes
    - Class timings
    - Class subjects (Make sure you name all subjects consistently)


# Disclaimer
Don't use this project to automate your classes. See this project only as a way of understanding automation works and how it can even be implemented in your day to day life. I will never promote anyone to use this for attending online classes.
Classes are important and respect your teachers. :)

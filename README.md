# Google Meet Bot : Online class attender
This is a Google Meet bot I made for attending your classes. This will 
- Join your class when a number of people are already in it (or wait)
- Leave the class when it reaches a threshold amount of people
- Notify you when classes are about to end (notifies you each and every step)

You can change the timetable real-time using telegram from your phone. Almost everything can be controlled from telegram.

## How it works
Two codes are needed to run to make this code perfect.
- `GoogleMeet.py` : This code is made in such a way that, if you run the code before the first class start time, it would wait for the start time and attend all the classes in the temporary timetable.
- `telegramBot.py` : This is actually a telegram bot. It can change your time table; do all kinds of stuff by just using some telegram messages. Mainly we are using it to change timetable in the real-time.

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
It takes into account how much people are in the meeting per 5 seconds, and the maximum number of people present in the class. It will leave the class when number of people inside it goes below a threshold. It even notifies you when classes are about to end automatically

## Telegram bot 
By asking /help in the bot you can see all the functionalities it can implement.

```
/start  :  Start automatic session
/tt day s1 s2 s3 s4 s5 s6  :  Change timetable for anyday
/dtt  :  Drop temp tables
/ctt  :  Create temp tables
/timetable  :  View current day timetable

```

### Notification 
This app has many notification architectures present
- **_Whatsapp_** (twilio sandbox) : It will notify everything by whatsapp. You need to have account in twilio and register. It costs about 0.0085$ for 1 message and you'll get 15$ when signing up. If you are a college student then you will have a college mail and then you can register github pro for free and get 50$ in twilio.
- **_Discord_** : I created a channel for me and took the discord webhook. It is free and i'll get all notifications in it
- **_Telegram_** : I created a bot in telegram and notifications come in the form of messages from that bot. You can also make changes to timetable using this telegram API.
- **_Notify-run_** : It send you push notifications to browser

## What you have to do:
#### You have some work to do of course (After doing all those work, you will freeeeee-est person in your class, I guarantee !!!)
- You have to create a telegram bot and get the `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`. [How to make a telegram bot](https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e)
- If you want discord functionality too, you have to make an account in discord, make a channel, and get the `DISCORD_WEBHOOK` for that channel.(This is only for notification purposes, telegram is more than enough, but if you want to explore all features, please look around) [Start exploring from here](https://www.digitalocean.com/community/tutorials/how-to-use-discord-webhooks-to-get-notifications-for-your-website-status-on-ubuntu-18-04)
- For whatsapp custom notifications visit [Twilio](https://www.twilio.com/docs/whatsapp/api). I am not much interested in this because, whatsapp do not have any api features till now and they are current provided by twilio sandbox for experimentation. So they have some issues and I am more than content with telegram. (Please check it out if you are interested in learning stuff)
- Create / Make changes to a `.env` file (I haven't created it in this repository obviously due to privacy reasons.)
- Change class timings, subject names, and links to suit your classes.
- Make change to match the your chrome profile of college mail id, so as to remove the need to login using the selenium (I have commented the solution in `join()` of `classes.py`) (You have to make changes in `__init__` of `classes.py` in the __user-data-dir__). I came up with this because, google now has a way to know whether a bot is loggin in or not. So it blocks before you log in. SO if the profile is loaded, google cannot know whether it is a bot or not.
- Run `telegramBot.py` prior to the other code. This is not necessary but is essential if first hour is changed.
- Run `GoogleMeet.py` some time before your class time (Whenever you want :wink:)


__*I recommend to run it in your PC because, if you need to study (like me :sweat_smile:) you can view it. Deploying to Heroku will take some time. Heroku has some issues. I am using sqlite3 for database purposes. The problem is that Heroku supports sqlite3, but the database will get overwritten with garbage values every 24 hours or so. Heroku's native database support is postgreSQL. So after perfecting my code, I will migrate from sqlite3 to postgreSQL and then it will be heaven my friends.*__
### Install
 - Clone the repository `git clone https://github.com/plal99/Google-Meet-Bot.git`
 - Install requirements.txt `pip install -r requirements.txt`

## Make necessary changes
- `.env` : Make necessary changes to the env files so as to fit your personal details requirements(username, password, tokens, chatid, class links).
- Change the `dbStuff.py` so as to fit your class requirements requirements. This means changing
    - Links to all the classes (links should be in the `.env` file)
    - Class timings (in `createTimeTable()` and `createTempTimeTable()` functions)
    - Class subjects (Make sure you name all subjects consistently)
- This currently joins a class when there are atleast 5 people and leaves the class when less than 15 people, warns you of class getting over when more than 10 people leave the class. So you are covered from all sides. So make changes in `class.py` (`JOIN_PEOPLE` and `LEAVE_PEOPLE`)


# Disclaimer
Don't use this project to automate your classes. See this project only as a way of understanding how automation works and how it can even be implemented in your day to day life. I will never promote anyone to use this for attending online classes nor use it myself.

Classes are important and respect your teachers :slightly_smiling_face:.

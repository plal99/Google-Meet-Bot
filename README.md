# Google Meet Bot 
This is a google meet bot I made for attending your classes. This will 
- Join your class when a number of people are already in it (or wait)
- Leave the class when it reaches a threshold amount of people
- Notify you when classes are about to end (notifies you each and every step)

## How it works
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

## Install
 - Clone the repository `git clone https://github.com/plal99/Google-Meet-Bot.git`
 - Install requirements.txt `pip install -r requirements.txt`


# Disclaimer
Don't use this project to automate your classes. See this project only as a way of understanding automation works and how it can even be implemented in your day to day life. I will never promote anyone to use this for attending online classes.
Classes are important and respect your teachers. :)
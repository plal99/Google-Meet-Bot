from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from bot import TELEGRAM_TOKEN, sqlite3, sendDiscord
# @run_async
# def restart(update, context):
#     restart_message = context.bot.send_message(chat_id=update.message.chat_id, text="Restarting, Please wait!")

conn = sqlite3.connect('checktt.db', check_same_thread=False)
db = conn.cursor()

def modifyTempTimeTable(day, p1, p2, p3, p4, p5):

    day = day.lower()
    perm = db.execute("SELECT time, subject FROM '%s'" % (day))
    perm = perm.fetchall()

    # subs here are all times(better time than subs)
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

    perm = db.execute("SELECT * FROM '%s'" % (day+'Temp'))
    perm = perm.fetchall()

    sendDiscord("Timetable for "+day+" changed.")
    # perm = db.execute("SELECT * FROM '%s'" % (dayTemp))
    # perm = perm.fetchall()
    # print(perm)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def tt(update, context):

    data = update.message.text.split()
    
    day = data[1]
    s1 = data[2]
    s2 = data[3]
    s3 = data[4]
    s4 = data[5]
    s5 = data[6]

    print(day, s1, s2, s3, s4, s5)

    
    modifyTempTimeTable(day, s1, s2, s3, s4, s5)


updater = Updater(TELEGRAM_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

dp.add_handler(CommandHandler("tt", tt))

# dp.add_handler(MessageHandler(Filters.text, tt))

# Start the Bot
updater.start_polling()

print("Hello world")

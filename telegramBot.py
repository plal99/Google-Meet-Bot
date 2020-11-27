from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from bot import *
# @run_async
# def restart(update, context):
#     restart_message = context.bot.send_message(chat_id=update.message.chat_id, text="Restarting, Please wait!")

def start(update, context):
    main()
    update.message.reply_text('Starting the class')

# def startdb(update, context):
    # conn = sqlite3.connect('checktt.db', check_same_thread=False)
    # db = conn.cursor()
#     update.message.reply_text('Connection with database established')

# def stopdb(update, context):
#     conn.close()
#     update.message.reply_text('Connection with database closed')

def help(update, context):
    update.message.reply_text('/start  :  Start automatic session')
    update.message.reply_text('/tt day s1 s2 s3 s4 s5 s6  :  Change timetable for anyday')
    update.message.reply_text('/dtt  :  Drop temp tables')
    update.message.reply_text('/ctt  :  Create temp tables')
    # update.message.reply_text('/startdb  :  Start connection with database')
    # update.message.reply_text('/stopdb  :  Drop connection with database')

def ttChange(update, context):

    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()
    data = update.message.text.split()
    
    day = data[1]
    s1 = data[2]
    s2 = data[3]
    s3 = data[4]
    s4 = data[5]
    s5 = data[6]

    print(day, s1, s2, s3, s4, s5)

    
    modifyTempTimeTable(day, s1, s2, s3, s4, s5)
    update.message.reply_text('Time table modified')
    sendDiscord("Time table modified")
    conn.close()

def dtt(update, context):
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()    
    dropTempTimeTable()
    conn.close()
    update.message.reply_text('Dropped all temp tables')

def ctt(update, context):
    conn = sqlite3.connect('checktt.db', check_same_thread=False)
    db = conn.cursor()
    createTempTimeTable()
    conn.close()
    update.message.reply_text('Created all temp tables')


updater = Updater(TELEGRAM_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tt", ttChange))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("dtt", dtt))
dp.add_handler(CommandHandler("ctt", ctt))
# dp.add_handler(CommandHandler("startdb", startdb))
# dp.add_handler(CommandHandler("stopdb", stopdb))


# Start the Bot
updater.start_polling()

print("Start doing your thing!")

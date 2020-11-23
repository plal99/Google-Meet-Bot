from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from bot import *
# @run_async
# def restart(update, context):
#     restart_message = context.bot.send_message(chat_id=update.message.chat_id, text="Restarting, Please wait!")

def start(update, context):
    main()
    update.message.reply_text('Starting the class')

def help(update, context):
    update.message.reply_text('/start  :  Start automatic session')
    update.message.reply_text('/tt day s1 s2 s3 s4 s5 s6  :  Change timetable')
    update.message.reply_text('/dtt  :  Drop temp tables')
    update.message.reply_text('/ctt  :  Create temp tables')

def ttChange(update, context):

    data = update.message.text.split()
    
    day = data[1]
    s1 = data[2]
    s2 = data[3]
    s3 = data[4]
    s4 = data[5]
    s5 = data[6]

    print(day, s1, s2, s3, s4, s5)

    
    modifyTempTimeTable(day, s1, s2, s3, s4, s5)

def dtt(update, context):
    dropTempTimeTable()
    update.message.reply_text('Dropped all temp tables')
def ctt(update, context):
    createTempTimeTable()
    update.message.reply_text('Created all temp tables')


updater = Updater(TELEGRAM_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tt", ttChange))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("dtt", dtt))
dp.add_handler(CommandHandler("ctt", ctt))


# Start the Bot
updater.start_polling()

print("Start doing your thing!")

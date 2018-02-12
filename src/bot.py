from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from FootballData import FootballData
import logging
import os
import sys
from threading import Thread

bot_token = os.environ['BOT_TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - '
                           '%(levelname)s - %(message)s',
                    level=os.environ['LOG_LEVEL'])

logger = logging.getLogger(__name__)

fd = FootballData(os.environ['PROTOCOL'] + '://' + os.environ['FOOTBALL_DATA_HOSTNAME'])


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def ranking(bot, update, args):
    if len(args) == 0:
        ret = fd.ranking(0)
    elif len(args) > 1:
        ret = 'Too much arguments'
    elif not RepresentsInt(args[0]):
        ret = 'Argument must be an integer'
    elif int(args[0]) < 1:
        ret = 'Argument must be at least 1'
    elif int(args[0]) > 38:
        ret = 'Matchday out of range'
    else:
        ret = fd.ranking(args[0])
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='Markdown', text=ret)


def results(bot, update, args):
    if len(args) == 0:
        ret = fd.results(0)
    elif len(args) > 1:
        ret = 'Too much arguments'
    elif not RepresentsInt(args[0]):
        ret = 'Argument must be an integer'
    elif int(args[0]) < 1:
        ret = 'Argument must be at least 1'
    else:
        ret = fd.results(args[0])
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='Markdown', text=ret)


def players(bot, update, args):
    if len(args) == 0:
        ret = 'Syntax: /players <team name>'
    elif len(args) == 1:
        ret = fd.players(args[0])
    else:
        ret = 'Too much arguments'
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='Markdown', text=ret)


def player(bot, update, args):
    if len(args) < 2:
        ret = 'Syntax: /player <team name> <player number>'
    elif len(args) == 2:
        ret = fd.player(args[0], args[1])
    else:
        ret = 'Too much arguments'
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='Markdown', text=ret)


def matchday(bot, update, args):
    if len(args) == 0:
        ret = fd.matchday(0)
    elif len(args) > 1:
        ret = 'Too much arguments'
    elif not RepresentsInt(args[0]):
        ret = 'Argument must be an integer'
    elif int(args[0]) < 1:
        ret = 'Argument must be at least 1'
    else:
        ret = fd.matchday(args[0])
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='Markdown', text=ret)


def leader(bot, update):
    ret = fd.leader()
    bot.send_photo(chat_id=update.message.chat_id, photo=ret)


def pic(bot, update, args):
    if len(args) != 1:
        ret = 'Syntax: /team <team name>'
        bot.send_message(chat_id=update.message.chat_id,
                         parse_mode='Markdown', text=ret)
    else:
        ret = fd.pic(args[0])
        if ret == 'Wrong team name':
            bot.send_message(chat_id=update.message.chat_id,
                             parse_mode='Markdown', text=ret)
        else:
            bot.send_photo(chat_id=update.message.chat_id, photo=ret)


def help(bot, update):
    ret = open('help.txt', 'r').read()
    bot.send_message(chat_id=update.message.chat_id,
                     parse_mode='Markdown', text=ret)


def info(bot, update):
    ret = 'chat_id: ' + str(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=ret)


def main():

    def stop_and_restart():
        # Gracefully stop the Updater and replace the current
        # process with a new one
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("ranking", ranking, pass_args=True))
    dp.add_handler(CommandHandler("results", results, pass_args=True))
    dp.add_handler(CommandHandler("players", players, pass_args=True))
    dp.add_handler(CommandHandler("player", player, pass_args=True))
    dp.add_handler(CommandHandler("matchday", matchday, pass_args=True))
    dp.add_handler(CommandHandler("leader", leader))
    dp.add_handler(CommandHandler("pic", pic, pass_args=True))
    dp.add_handler(CommandHandler("help", help))

    # handler for admin only
    dp.add_handler(CommandHandler('restart', restart,
                                  filters=Filters.user(username='@andmazz')))
    dp.add_handler(CommandHandler('info', info, filters=Filters.user(username='@andmazz')))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot

    # for developing
    updater.start_polling()

    # for production
    # updater.start_webhook(listen='0.0.0.0',
    #                       port=8443,
    #                       url_path=bot_token,
    #                       key='key.pem',
    #                       cert='cert.pem',
    #                       webhook_url='https://64.137.249.79:8443/'
    #                       + bot_token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

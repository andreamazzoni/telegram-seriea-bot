import logging
import config
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import Update, Bot, InputTextMessageContent, InlineQueryResultArticle
from footballdata import FootballData

bot_token = config.bot_token
football_data_token = config.fd_token
football_data_hostname = config.fd_hostname
football_data_protocol = config.fd_protocol
log_level = config.loglevel

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)
logger = logging.getLogger(__name__)

fd = FootballData(football_data_protocol + '://' + football_data_hostname, football_data_token)


def representint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def ranking(bot, update, args):
    if len(args) == 0:
        ret = fd.ranking(0)
    elif len(args) > 1:
        ret = 'Too much arguments'
    elif not representint(args[0]):
        ret = 'Argument must be an integer'
    elif int(args[0]) < 1:
        ret = 'Argument must be at least 1'
    elif int(args[0]) > 38:
        ret = 'Matchday out of range'
    else:
        ret = fd.ranking(args[0])
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=ret)


def players(bot, update, args):
    if len(args) == 0:
        ret = 'Syntax: /players <team name>'
    elif len(args) == 1:
        ret = fd.players(args[0])
    else:
        ret = 'Too much arguments'
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=ret)


def player(bot, update, args):
    if len(args) < 2:
        ret = 'Syntax: /player <team name> <player number>'
    elif len(args) == 2:
        ret = fd.player(args[0], args[1])
    else:
        ret = 'Too much arguments'
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=ret)


def matchday(bot, update, args):
    if len(args) == 0:
        ret = fd.matchday_sa()
    elif args[0].lower() == 'cl':
        ret = fd.matchday_cl()
    else:
        ret = "Wrong argument"
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=ret)


def help(bot, update):
    ret = open('help.txt', 'r').read()
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=ret)


def info(bot, update):
    ret = 'chat_id: ' + str(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=ret)


def scorers(bot, update):
    ret = fd.get_scorers()
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=ret)


def inline(bot, update):
    query_results = list()
    query_results.append(
        InlineQueryResultArticle(
            id='matchday',
            title='Matchday',
            input_message_content=InputTextMessageContent(
                message_text=fd.matchday(0),
                parse_mode='Markdown'
            )
        )
    )
    query_results.append(
        InlineQueryResultArticle(
            id='ranking',
            title='Ranking',
            input_message_content=InputTextMessageContent(
                message_text=fd.ranking(0),
                parse_mode='Markdown'
            )
        )
    )
    bot.answer_inline_query(update.inline_query.id, query_results)


def run(message):

    bot = Bot(config.bot_token)
    dp = Dispatcher(bot, None, workers=0)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("ranking", ranking, pass_args=True))
    dp.add_handler(CommandHandler("players", players, pass_args=True))
    dp.add_handler(CommandHandler("player", player, pass_args=True))
    dp.add_handler(CommandHandler("matchday", matchday, pass_args=True))
    dp.add_handler(CommandHandler("scorers", scorers))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('info', info, filters=Filters.user(username='@andmazz')))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # inline
    inline_handler = InlineQueryHandler(inline)
    dp.add_handler(inline_handler)

    # decode update and try to process it
    update = Update.de_json(message, bot)
    dp.process_update(update)

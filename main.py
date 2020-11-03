from datetime import datetime, date, time, timedelta
import logging

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from data import db_session
from data.admins import Admin
from data.battles import Battle
from data.guilds import Guild

TOKEN = ''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update):
    logger.warning(f'Update {update} caused error {bot.error}')


castles = ['🍁', '☘', '🍆', '🌹', '🐢', '🦇', '🖤']


def add_guilds(bot, update):
    if ('⛺' in update.message.text or '😴' in update.message.text) and update.message.forward_from_chat.username == 'ChatWarsDigest':
        battletime = update.message.forward_date
        session = db_session.create_session()
        guilds = filter(lambda x: '[' in x, update.message.text.split())
        existing_guilds = [_[0] for _ in session.query(Guild.tag).all()]
        tags = set()
        for guild in guilds:
            tag = guild[0] + guild.split('[')[-1].split(']')[0]
            if tag not in existing_guilds and tag not in tags:
                session.add(Guild(tag=tag))
            tags.add(tag)
        session.commit()
        for tag in tags:
            session.add(Battle(guildid=session.query(Guild.id).filter(Guild.tag == tag).one()[0], battletime=battletime.replace(minute=0, second=0)))
        session.commit()
        update.message.reply_text('Результаты сражений приняты.')


def isAuthorized(userid):
    session = db_session.create_session()
    return userid in [admin[0] for admin in session.query(Admin.userid).all()]


def start(bot, update):
    userid = update.message.from_user.id
    if isAuthorized(userid):
        update.message.reply_text('Этот бот умеет следить за активностью гильдий в ЧВ3. '
                                  'Для этого фордвадните в этот чат сводки замковых битв и используйте команду /lazy')


def lazy(bot,update):
    userid = update.message.from_user.id
    if isAuthorized(userid):
        session = db_session.create_session()
        all_guilds = set(_[0]for _ in session.query(Guild.tag).all())
        last_battle_guilds = [_[0]for _ in  list(session.query(Battle.guildid).filter(Battle.battletime > datetime.now() - timedelta(hours=8)).all())]
        last_battle_guilds = set(_[0]for _ in session.query(Guild.tag).filter(Guild.id.in_(last_battle_guilds)).all())
        result = all_guilds.difference(last_battle_guilds)
        update.message.reply_text(', '.join(sorted(list(result))))


def add_guilds2(bot,update):
    if ('⛺' in update.message.text or '😴' in update.message.text) and \
            update.message.forward_from_chat.username == 'ChatWarsDigest':
        battletime = update.message.forward_date
        session = db_session.create_session()
        guilds = map(lambda x: x.strip(','), filter(lambda x: x[0] in castles, update.message.text.split()))
        existing_guilds = [_[0] for _ in session.query(Guild.tag).all()]
        tags = set()
        for guild in guilds:
            tag = guild
            if tag not in existing_guilds and tag not in tags:
                session.add(Guild(tag=tag))
            tags.add(tag)
        session.commit()
        for tag in tags:
            session.add(Battle(guildid=session.query(Guild.id).filter(Guild.tag == tag).one()[0],
                               battletime=battletime.replace(minute=0, second=0)))
        session.commit()
        update.message.reply_text('Результаты сражений приняты.')


def main():
    db_session.global_init("db/guilds")
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.forwarded, add_guilds2))
    dp.add_handler(CommandHandler('lazy',lazy))

    dp.add_error_handler(error)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

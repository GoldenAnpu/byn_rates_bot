import logging
from scraper import collect_rates_and_dates, gather_page_into_local_html, get_today_date
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import os

PORT = int(os.environ.get('PORT', 443))
TOKEN = os.environ['B_TOKEN']  # telegram token stored in env variables
application = Application.builder().token(TOKEN).build()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_currency_name(currency):
    if currency == 'eur':
        m_currency = '*EUR/BYN*'
        return m_currency
    elif currency == 'usd':
        m_currency = '*USD/BYN*'
        return m_currency
    else:
        m_currency = '*Unknown currency*'
        return m_currency


def get_days_name(collected_data):
    c_today_date = collected_data[0]
    _, today_day_num = get_today_date()
    if int(today_day_num) == int(c_today_date):
        day0 = 'Today'
        day1 = 'Tomorrow'
        return day0, day1
    elif int(today_day_num) >= int(c_today_date):
        day0 = 'Yesterday'
        day1 = 'Today'
        return day0, day1
    else:
        day0 = c_today_date
        day1 = str(c_today_date + 1)
        # need add log here
        return day0, day1


def get_message_depending_rates(currency):
    m_currency = get_currency_name(currency)
    gather_page_into_local_html()
    collected_data = collect_rates_and_dates(currency)
    today_rate = collected_data[2]
    tomorrow_rate = collected_data[3]
    day0 = get_days_name(collected_data)[0]
    day1 = get_days_name(collected_data)[1]

    ad_message = ''
    if day0 == 'Yesterday':
        ad_message = '\nCome back later to check rates for tomorrow!'

    if (today_rate or tomorrow_rate) is None:
        message0 = str(m_currency + f'\n 💩 Currencies unavailable 💩')
        return message0
    elif abs(today_rate - tomorrow_rate) <= 0.05:
        message1 = str(m_currency + f'\n{day0}: {today_rate}\n{day1}: {tomorrow_rate}' + ad_message)
        return message1
    elif 0.05 <= abs(today_rate - tomorrow_rate) <= 0.1:
        message2 = str(m_currency +
                       f'\n{day0}: {today_rate}\n{day1}: {tomorrow_rate}\n'
                       f'*WARNING:* rates differ by {"{0:0.4f}".format(abs(today_rate - tomorrow_rate))}\n' +
                       ad_message)
        return message2
    else:
        message3 = str(m_currency +
                       f'\n{day0}: {today_rate}\n{day1}: {tomorrow_rate}\n'
                       f"Holy Jesus! Rates differ by {'{0:0.4f}'.format(abs(today_rate - tomorrow_rate))}\n" +
                       ad_message)
        return message3


# Commands

async def bot_help(update: Update, context: CallbackContext):
    await update.message.reply_text("Can't help you now 🥲")


async def get_usd(update: Update, context: CallbackContext):
    await update.message.reply_text(get_message_depending_rates('usd'), parse_mode='Markdown')


async def get_eur(update: Update, context: CallbackContext):
    await update.message.reply_text(get_message_depending_rates('eur'), parse_mode='Markdown')


async def start(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    await update.message.reply_text(f"Welcome, *{name}*!\nIf you wanna get actual information about currency rates "
                                    "just go to the menu!\nOr use commands /get_usd and /get_eur instead!\n"
                                    "Have a nice day!", parse_mode='Markdown')


async def unknown(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


async def unknown_text(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "*Sorrybro*\nI can't understand you, don't send '%s' again" % update.message.text, parse_mode='Markdown')


application.add_handler(CommandHandler('get_usd', get_usd))
application.add_handler(CommandHandler('get_eur', get_eur))
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', bot_help))
application.add_handler(MessageHandler(filters.COMMAND, unknown))
application.add_handler(MessageHandler(filters.TEXT, unknown_text))
application.run_polling()

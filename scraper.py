import lxml.html
import json
import datetime
import pytz
from urllib.request import urlopen


def get_today_date():
    today_stamp = datetime.datetime.now(pytz.timezone("Europe/Minsk"))
    today_day_num = today_stamp.strftime('%d')
    return today_stamp, today_day_num


def get_time_of_changes():  # used to prevent gathering info from target site on every request
    try:
        with open('change_time.json', 'r+') as json_time:
            time_of_changes = datetime.datetime.strptime(json.load(json_time)['time'], '%Y-%m-%d %H:%M:%S.%f')
    except json.decoder.JSONDecodeError:
        with open('change_time.json', 'w+') as json_time:
            json.dump({"time": "2022-01-01 00:00:01.000000"}, json_time)  # possible to use any date from the past
            time_of_changes =  datetime.datetime.strptime("2022-01-01 00:00:01", '%Y-%m-%d %H:%M:%S')
    except FileNotFoundError:
        with open('change_time.json', 'w+') as json_time:
            json.dump({"time": "2022-01-01 00:00:01.000000"}, json_time)  # possible to use any date from the past
            time_of_changes = datetime.datetime.strptime("2022-01-01 00:00:01", '%Y-%m-%d %H:%M:%S')
    return time_of_changes


def set_time_of_changes(check_time):
    time_of_changes = check_time + datetime.timedelta(days=1)
    time_of_changes = time_of_changes.replace(hour=14, minute=00, second=00)
    with open('change_time.json', 'w+') as json_time:
        jsn_str = {"time": f"{time_of_changes}"}
        json_time.seek(0)
        json.dump(jsn_str, json_time)


def gather_page_into_local_html():
    time_of_changes = get_time_of_changes()
    today_stamp, _ = get_today_date()
    check_time = today_stamp.replace(tzinfo=None)
    if check_time > time_of_changes:
        with open('site_body.html', "bw+") as html_file:
            site_body = lxml.html.parse(urlopen('https://banki24.by/currencies/nbrb'))
            site_body.write(html_file)
        set_time_of_changes(check_time)


def collect_rates_and_dates(currency):
    # gathering NBRB rates for today and tomorrow
    table_path = '/html/body/div[1]/div[4]/div[1]/div[4]/div[2]//'
    with open('site_body.html', 'r') as site_html:
        next_level = lxml.html.fromstring(site_html.read())
        we_day_td = int((next_level.xpath(table_path + 'tr[1]/td[3]/text()')[0].strip().rsplit(" "))[0])
        we_day_tm = int((next_level.xpath(table_path + 'tr[1]/td[4]/text()')[0].strip().rsplit(" "))[0])
        we_usd_td = float(next_level.xpath(table_path + 'tr[2]/td[3]/text()')[0].strip().replace(",", "."))
        we_usd_tm = float(next_level.xpath(table_path + 'tr[2]/td[4]/text()')[0].strip().replace(",", "."))
        we_eur_td = float(next_level.xpath(table_path + 'tr[3]/td[3]/text()')[0].strip().replace(",", "."))
        we_eur_tm = float(next_level.xpath(table_path + 'tr[3]/td[4]/text()')[0].strip().replace(",", "."))
    if currency == 'usd':
        return we_day_td, we_day_tm, we_usd_td, we_usd_tm
    elif currency == 'eur':
        return we_day_td, we_day_tm, we_eur_td, we_eur_tm


gather_page_into_local_html()
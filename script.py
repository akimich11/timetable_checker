import traceback
from threading import Thread

import telebot
from selenium import webdriver
from time import sleep
import sys

from selenium.common.exceptions import WebDriverException

bot = telebot.TeleBot(token='1934090305:AAEQVPnZer-7TBMEwbTW_1n3pS3PBBELcmg')
AKIM_ID = 270241310
MDA_ID = -1001626267087


def check_timetable(chat_id, manual_check=True):
    if manual_check:
        bot.send_message(chat_id, 'ща проверю')
    driver = webdriver.PhantomJS()
    driver.get('http://fpmi.bsu.by/ru/main.aspx?guid=20381')
    try:
        driver.find_element_by_id('__tab_Tabs_2801_ctl03').click()
        div_block = driver.find_element_by_id('Tabs_2801_ctl03')
        refs = div_block.find_elements_by_tag_name('a')
        found = False
        for ref in refs:
            if ref.text.lower().startswith('расписание'):
                bot.send_message(chat_id, ref.get_property('href'))
                return True
        if not found and manual_check:
            bot.send_message(chat_id, 'пока расписания нет')
    except WebDriverException:
        bot.send_message(AKIM_ID, 'Беда с селениумом:\n' + traceback.format_exc())
    driver.quit()


def periodic_check():
    while True:
        found = check_timetable(MDA_ID, False)
        if not found:
            sleep(60)
        else:
            sys.exit(0)


if __name__ == '__main__':
    bot.send_message(AKIM_ID, 'started')
    Thread(target=periodic_check).start()


@bot.message_handler(commands=['check'])
def check_response(message):
    check_timetable(message.chat.id)


bot.polling(none_stop=True)

import traceback

import telebot
from selenium import webdriver
from time import sleep

from selenium.common.exceptions import WebDriverException

bot = telebot.TeleBot(token='1934090305:AAEQVPnZer-7TBMEwbTW_1n3pS3PBBELcmg')

if __name__ == '__main__':
	bot.send_message(270241310, 'started')


def check_timetable(message, manual_check=True):
	if manual_check:
		bot.send_message(message.chat.id, 'ща проверю')
	driver = webdriver.PhantomJS()
	driver.get('http://fpmi.bsu.by/ru/main.aspx?guid=20381')
	try:
		driver.find_element_by_id('__tab_Tabs_2801_ctl02').click()
		block = driver.find_element_by_id('Tabs_2801_ctl02')
		refs = block.find_elements_by_tag_name('a')
		found = False
		for ref in refs:
			if ref.text.lower().startswith('расписан'):
				bot.send_message(message.chat.id, ref.get_property('href'))
				found = True
				break
		if not found and manual_check:
			bot.send_message(message.chat.id, 'пока расписания нет')
	except WebDriverException:
		bot.send_message(270241310, 'Беда с селениумом:\n' + traceback.format_exc())
	driver.quit()


@bot.message_handler(commands=['check'])
def check_response(message):
	check_timetable(message)


@bot.message_handler(commands=['start_checking'])
def start_checking(message):
	if message.from_user.id == 270241310:
		bot.send_message(message.chat.id, 'буду чекать каждые 60 секунд, если появится - скину')
		while True:
			check_timetable(message, False)
			sleep(60)


bot.polling(none_stop=True)

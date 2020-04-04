import time
import telebot 
import requests
import numpy as np 
import re 
from telegram import *
import random
import calcData as datacalc
from flask import Flask, request
import os

TOKEN = "893266649:AAFv46pw1DkwuBIYFXfPrryFZNjV0x5lZEo"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
#bot = telebot.TeleBot()

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i
@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Hello , This is Covid-19 chatbot created by Data Science Nuggets. You can use this bot for Updates on Covid-19.\n commands \n cases - to get all the cases of covid - 19')

@bot.message_handler(commands=['help']) # help message handler
def send_query(message):
    bot.reply_to(message, 'send query on @khanshahrukh786')

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def covidbot(msg):

	#userName = msg['from']['first_name']

	#content_type, chat_type, chat_id = telepot.glance(msg)

	if (msg):
		command = msg.text
		print ('Got command: %s' % command)
		

		#if  '/start' in command:
		#	bot.sendMessage(chat_id, "Hello , This is Covid-19 chatbot created by Data Science Nuggets. You can use this bot for Updates on Covid-19.\n commands \n cases - to get all the cases of covid - 19\n deaths - to get number of deathsdue to covid - 19\n recovered - to get all the  recoverd cases of covid - 19 \n news  - to get all the lastest news of covid - 19\n top - to get an image of the top effected countries")
																																																																																																																																																																																																														

		if 'cases' in command:
			my_list = datacalc.calcData.GloBal_Total(True)
			messagetext = "Total Cases: " + str(my_list[0]) + "\n New Cases: " + str(my_list[1]) + "\n Total Deaths: " + str(my_list[2]) + "\n New Deaths: " + str(my_list[3]) + "\n Total Recovered: " + str(my_list[4]) + "\n New Recovered: "+str(my_list[5]) +"\n Total Active: " + str(my_list[6])
			bot.reply_to(msg, messagetext)
		

		if 'country' in command:
			country_command  = command.split(" ")
			if (len(country_command)>=2):
				country_text = " ".join(country_command[1:])
				my_list = datacalc.calcData.country_data(True, country_text)
				if(len(my_list[7])<4):
					my_list[7] = str(my_list[7]).upper()
				else:
					my_list[7] = str(my_list[7]).capitalize()
				messagetext = "Country: " + str(my_list[7]) + "\n Total Cases: " + str(my_list[0]) + "\n New Cases: " + str(my_list[1]) + "\n Total Deaths: " + str(my_list[2]) + "\n New Deaths: " + str(my_list[3]) + "\n Total Recovered: " + str(my_list[4]) + "\n New Recovered: "+ str(my_list[5])+ "\n Total Active: " + str(my_list[6])
				bot.reply_to(msg, messagetext)
			else:
				country_text = "India"
				my_list = datacalc.calcData.country_data(True, country_text)
				list_countries = datacalc.calcData.country_list(True)
				messagetext = str(list_countries) + "\n Example: /country India \n Results: \n " + "Country: " + str(my_list[7]) + "\n Total Cases: " + str(my_list[0]) + "\n New Cases: " + str(my_list[1]) + "\n Total Deaths: " + str(my_list[2]) + "\n New Deaths: " + str(my_list[3]) + "\n Total Recovered: " + str(my_list[4]) + "\n New Recovered: "+ str(my_list[5])+ "\n Total Active: " + str(my_list[6])
				bot.reply_to(msg, messagetext)

		if 'symptoms' in command:
			url = "https://drive.google.com/open?id=1rERaCYPTHgoFX0VirFRuY4ygoH-rpflg"
			bot.send_photo(msg, url)
		
		if "don" in command:
			Dont_urls = ["https://www.dropbox.com/s/kyfbs666kx2i4i7/dont1.jpg?dl=0", "https://www.dropbox.com/s/q7pswod5pvika45/dont2.jpg?dl=0", "https://www.dropbox.com/s/svccvtsfewkyslm/dont3.jpg?dl=0"]
			for item in Dont_urls:
				bot.send_photo(msg, item)
				
			#url = 'https://www.dropbox.com/s/pmbv9kbijmkgvhz/do1.jpg?dl=0'
			
		
		elif 'do' in command:
			Do_urls = ["https://www.dropbox.com/s/pmbv9kbijmkgvhz/do1.jpg?dl=0", "https://www.dropbox.com/s/wns67ulmzogngtp/do2.jpg?dl=0", "https://www.dropbox.com/s/psex5njfowxu2vb/do3.jpg?dl=0"]
			for item in Do_urls:
				bot.send_photo(msg, item)

    			
		if 'news' in command:
			# country_list =['in', 'us', 'gb'] 
			# button_list = [[KeyboardButton(s)] for s in country_list]
			# reply_markup = ReplyKeyboardMarkup(button_list)
			# bot.sendMessage(command, "A two-column menu", reply_markup=reply_markup)
			val1= command.split(" ")
			API_KEY = '2850ab2ec8504fe389bb02b98a601ca9'
			if len(val1) < 2:
				val1.append("in")
			params = {
				'q': 'coronavirus',
				'source': 'bbc-news',
				'sortBy': 'top',
				'language': 'en',
				#'category': 'business',
				'country': val1[1],
				#'apiKey': API_KEY,
			}

			headers = {
				'X-Api-Key': API_KEY,  # KEY in header to hide it from url
			}

			url = 'https://newsapi.org/v2/top-headlines'

			response = requests.get(url, params=params, headers=headers)
			data = response.json()
			articles = data["articles"] 
			results = [arr["title"] for arr in articles]
			result_url = [arr["url"] for arr in articles]
			# print(results)
			# print(data)
			news_head = ["Headline Now: \n "]
			for index, item in enumerate(results):
				#<a href="www.google.com">www.google.com</a>
				#news_head.append(str(index + 1)+ ": "+"<html> <a href="+result_url[index]+">"+ item +"</a></html>"+"\n \n")
				news_head.append(str(index + 1)+ ": "+ item +"\n \n")
			head_news = " ".join(news_head)
			bot.reply_to(msg, head_news)

# def at_converter(message):
#     texts = message.text.split()
#     at_text = findat(texts)
#     if at_text == '@': # in case it's just the '@', skip
#         pass
#     else:
#         insta_link = "https://instagram.com/{}".format(at_text[1:])
#         bot.reply_to(message, insta_link)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://enigmatic-sea-82733.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="192.1.1.0", port=int(os.environ.get('PORT', 5000)))
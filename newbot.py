from telegram.ext import Updater,CommandHandler,CallbackQueryHandler,MessageHandler,Filters
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token="Your Bot token here", use_context=True)
#Take the bot token from bot father and paste it here
dispatcher = updater.dispatcher

def start(update,context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hlo! i am on")

def option(update,context):
	button = [
	[InlineKeyboardButton("send message",callback_data="1")],
	[InlineKeyboardButton("cancel",callback_data="2")]
	]
	markup = InlineKeyboardMarkup(button)
	context.bot.send_message(chat_id=update.effective_chat.id,text = "choose any option",reply_markup=markup)

def button(update,context):
	query = update.callback_query
	if(query.data == str(1)):
		context.bot.edit_message_text(chat_id=query.message.chat_id,text="Please Enter The Phone number",
		message_id=query.message.message_id)
	else:
		context.bot.edit_message_text(chat_id=query.message.chat_id,text="Restart The Bot",
		message_id = query.message.message_id)

def get_msg(update,context):
	data = [update.message.text]
	message = data[1]
	context.bot.send_message(chat_id=update.effective_chat.id,text="Enter the message")
	url = "https://www.fast2sms.com/dev/bulk"
	payload ={"sender_id":"FSTSMS",
	"message":message,
	"language":"english",
	"route":"p",
	"numbers":str(data[1])}
	headers = {'authorization': "paste Your fast2sms api authentication key here",'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache"}
	response = requests.request("POST", url,
	data=payload, headers=headers)
	print(response.text)

start_handler= CommandHandler("start",start)
dispatcher.add_handler(start_handler)
option_handler = CommandHandler("option",option)
dispatcher.add_handler(option_handler)
button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)
msg_handler = MessageHandler(Filters.text,get_msg)
dispatcher.add_handler(msg_handler)

if __name__ == "__main__":
	updater.start_polling()
	#In production dont use polling either use webhook mode and deploy on heroku or any other platform
	"""updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('here paste ur app link: ex-https://herokubot.com/' + TOKEN)"""

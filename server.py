import telebot

TOKEN_BOT = '5527778025:AAEfVELZka7GANfp6iH5AbadHAlFsnNNg4U'
bot = telebot.TeleBot(TOKEN_BOT)

if __name__=='__main__':
    from functions import bot
    bot.polling(non_stop=True)
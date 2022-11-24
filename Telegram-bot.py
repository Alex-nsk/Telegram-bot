import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Bot поможет сконвертировать несколько популярных валют. ' \
           'Чтобы начать работу ведите команды в следующем порядке: \n<Имя валюты> \ ' \
           '<Имя валюты в которую перевести> \ <Количество переводимой валюты>  \
           \nПосмотреть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')

        base, sym, amount = values
        total_sym = CryptoConverter.convert(base, sym, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {sym} - {total_sym}'
        bot.send_message(message.chat.id, text)


bot.polling()
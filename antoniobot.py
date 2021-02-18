import telebot
import requests
import os
API_TOKEN = '1631065433:AAHPP0BmOLqH0nFM46_JV5CQAt58yvXxHnI'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Bienvenido a SaasCountries_bot \n' +
        '\n' +
        'Creado para complementar el artículo http://saasradar.net, que muestra el proceso de implementación de un Bot paso a paso \n' +
        '\n' +
        'Tienes a tu disposición los siguientes comandos: \n' +
        '/start : Iniciar bot \n' +
        '/stop : Detener bot \n' +
        '/info_pais <país>: Devuelve información de un país dado \n' +
        '/capital <capital>: Devuelve el país dada su capital \n'
    )

@bot.message_handler(commands=['capital'])
def capital(message):
    arr = message.text.split(' ')
    capital = ''
    for word in arr:
        if (word != arr[0]):
            capital += word
            if (word != arr[-1]):
                capital += ' '
    url = 'https://restcountries.eu/rest/v2/capital/' + capital
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        bot.send_message(
            message.chat.id, data[0]['name'])
    else:
        bot.reply_to(
            message, 'No se ha podido encontrar la capital, asegúrese de escribirla con su nombre en inglés')


@bot.message_handler(commands=['info_pais'])
def info_pais(message):
    arr = message.text.split(' ')
    country = ''
    for word in arr:
        if (word != arr[0]):
            country += word
            if (word != arr[-1]):
                country += ' '
    url = 'https://restcountries.eu/rest/v2/name/' + country
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        text = ''
        if (len(data) != 1):
            text += 'Se encontraron ' + \
                str(len(data))+'elementos en su búsqueda'
        for item in data:
            text += '\n \n'
            text += 'Información sobre ' + item['name'] + '\n'
            text += 'Población: ' + str(item['population']) + '\n'
            text += 'Región: ' + item['region'] + '\n'
            text += 'Subregión: ' + item['subregion'] + '\n'
            text += 'Capital: ' + item['capital'] + '\n'
            text += 'Idiomas: '
            for lang in item['languages']:
                text += lang['name']
                if (lang != data[0]['languages'][-1]):
                    text += ', '

        bot.send_message(
            message.chat.id, text)
    else:
        bot.reply_to(
            message, 'No se ha podido encontrar el país, asegúrese de escribirlo con su nombre en inglés')


bot.polling()
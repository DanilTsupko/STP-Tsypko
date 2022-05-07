import telebot, wikipedia, re
bot = telebot.TeleBot('5112512916:AAEkSiTnfv5QIjz4uccsVyWCgAYWKBCYQos')
#Встановили соловїну мову
wikipedia.set_lang("uk")
# Чистимо текст статті в Wikipedia і обмежуємо його тисячею символів
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Отримуємо першу тисячу символів
        wikitext=ny.content[:1000]

        wikimas=wikitext.split('.')
        # Відкидаємо все після останньої точки
        wikimas = wikimas[:-1]
        # Створюємо порожню змінну для тексту
        wikitext2 = ''
        # Проходимося рядками, де немає знаків «рівно» (тобто всі, крім заголовків)
        for x in wikimas:
            if not('==' in x):
                    # Якщо в рядку залишилося більше трьох символів, додаємо її до нашої змінної та повертаємо втрачені при розділенні рядків точки на місце
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Тепер за допомогою регулярних виразів прибираємо розмітк
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2

    # Обробляємо виняток, який міг повернути модуль wikipedia за запитом
    except Exception as e:
        return 'Упс незнаю такого'

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я вас слухаю')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))
# Запускаем бота
bot.polling(none_stop=True, interval=0)
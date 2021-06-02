from telebot import types

from tg_ui.token import TOKEN
import telebot
bot = telebot.TeleBot(TOKEN)
population_id = None


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global population_id
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, займёмся исследованием популяций?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == '/start':
        bot.send_message(message.from_user.id, "Давай создадим тебе собственную популяцию для исследований")
        population_id = create_population()
        if population_id is not None:
            bot.send_message(message.from_user.id, "Популяция успешно создана, давай добавим в неё особей")
            bot.send_message(message.from_user.id,
                             "Укажи подряд два значения: жизнеспособность особи от 0 до 1 и шанс размножиться от 0 до 1")
            bot.send_message(message.from_user.id, "Например, так: 0.5 0.3")
            bot.register_next_step_handler(message, add_individual)

        else:
            bot.send_message(message.from_user.id, "Произошла какая-то ошибка, попробуй начать сначала")
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help')


def create_population() -> int:
    # тут создание популяции И ВОЗВРАТ ТОКЕНА
    return 0


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global individual_parameters
    if call.data == "Добавить ещё":
        bot.send_message(call.message.chat.id, "Тогда введи новые параметры")
        bot.register_next_step_handler(call.message, add_individual)
    elif call.data == "Перейти к исследованиям":
        bot.send_message(call.message.chat.id, "Введи агрессивность среды от 0 до 1 и скорость мутаций особей от 0 до 1")
        bot.register_next_step_handler(call.message, run_research)


def send_keyboard(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Добавить ещё', callback_data='Добавить ещё')  # кнопка «Да»
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Перейти к исследованиям', callback_data='Перейти к исследованиям')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id,
                     text="Что делать дальше?",
                     reply_markup=keyboard)


def add_individual(message):
    individual_parameters = {"type": message.text}
    try:
        parameters = list(map(float, message.text.split()))
        individual_parameters['lifetime'] = 3
        individual_parameters['p_for_death'] = 1 - parameters[0]
        individual_parameters['p_for_reproduction'] = parameters[1]
        # ЗАПРОС НА ДОБАВЛЕНИЕ ПО ГЛОБАЛЬНОМУ ТОКЕНУ
    except Exception:
        bot.send_message(message.from_user.id, 'Что-то не так с параметрами, попробуй ещё')
    send_keyboard(message)


def run_research(message):
    try:
        parameters = list(map(float, message.text.split()))
        # ТУТ ФОРМИРУЕТСЯ ЗАПРОС НА ЗАПУСК РЕСЕРЧА
        # ПОТОМ ПРЯМ JSON ОТПРАВИТЬ В ОТВЕТ
    except Exception:
        bot.send_message(message.from_user.id, 'Что-то не так с параметрами, попробуй ещё')


bot.polling(none_stop=True, interval=0)

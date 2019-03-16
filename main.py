import config
from bot import Bot
import telebot
import datetime
import Poster
from models import *
import codecs
import os

bot = Bot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    user, is_created = User.get_or_create(id=message.from_user.id)

    if is_created == False:
        try:
            bot.delete_message(chat_id=message.from_user.id, message_id=user.last_message_id)
        except Exception:
            pass

    btn_rfm = telebot.types.InlineKeyboardButton(text='RFM анализ 📊', callback_data='rfm')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(btn_rfm)

    message_id = bot.send_animation(chat_id=message.from_user.id, file_id=config.MEDIA['GIF']['worker'],
                                    text='Выбирите действие...',
                                    keyboard=keyboard)
    user.name = message.from_user.first_name
    user.status = STATUS[0]
    user.last_message_id = message_id
    user.save()


@bot.callback_query_handler(func=lambda call: User.get(id=call.from_user.id).status == STATUS[0])
def rfm_message(call):
    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    one_month_ago_btn = telebot.types.InlineKeyboardButton(text='Один Месяц 📅',
                                                           callback_data=(datetime.date.today() - datetime.timedelta(
                                                               365 / 12)).isoformat())

    three_month_ago_btn = telebot.types.InlineKeyboardButton(text='Три Месяца 📅',
                                                             callback_data=(datetime.date.today() - datetime.timedelta(
                                                                 3 * 365 / 12)).isoformat())

    half_years_ago_btn = telebot.types.InlineKeyboardButton(text='Полгода 📅',
                                                            callback_data=(datetime.date.today() - datetime.timedelta(
                                                                6 * 365 / 12)).isoformat())

    one_years_ago_btn = telebot.types.InlineKeyboardButton(text='Год назад 📅',
                                                           callback_data=(datetime.date.today() - datetime.timedelta(
                                                               365)).isoformat())

    back_btn = telebot.types.InlineKeyboardButton(text='Нaзад 🔙', callback_data='back')

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(one_month_ago_btn, three_month_ago_btn)
    keyboard.add(half_years_ago_btn, one_years_ago_btn)
    keyboard.add(back_btn)

    message_id = bot.send_animation(chat_id=call.from_user.id, text='Выбирите период для анализа, '
                                                                    'либо введите дату в формате: Год-месяц-день 🗓',
                                    keyboard=keyboard, file_id=config.MEDIA['GIF']['rfm'])
    user = User.get(id=call.from_user.id)
    user.status = STATUS[1]
    user.last_message_id = message_id
    user.save()


@bot.message_handler(func=lambda call: User.get(id=call.from_user.id).status == STATUS[1])
def rfm_mes(message):
    try:
        datetime.datetime.strptime(message.text, '%Y-%m-%d')
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text='Вы ввели дату в неверном формате, '
                                                            'повторите попытку, например: "2019.03.25"')
        return

    if datetime.datetime.strptime(message.text, '%Y-%m-%d') > datetime.datetime.today():
        bot.send_message(chat_id=message.from_user.id, text=f"Полегче, "
        f"мы не в будуещем.\nСегодня {datetime.datetime.today().date().isoformat()}")
        return

    send_excel(chat_id=message.from_user.id, date_from=message.text)


@bot.callback_query_handler(func=lambda call: User.get(id=call.from_user.id).status == STATUS[1])
def rfm_call(call):
    if call.data == 'back':
        start_message(call)
    else:
        send_excel(chat_id=call.from_user.id, date_from=call.data)


def send_excel(chat_id, date_from):
    bot.send_chat_action(chat_id=chat_id, action='upload_document')
    clients = Poster.AnaliseClients(Poster.User(token=config.POSTER_TOKEN).get_clients(date_from=date_from))

    file_name = f"RFM {date_from} to {datetime.datetime.today().date().isoformat()}.xlsx"
    excel_file = codecs.open(clients.RFM.export_to_excel(file_name), 'rb')

    bot.send_document(chat_id=chat_id, data=excel_file)

    excel_file.close()
    os.remove(file_name)


if __name__ == '__main__':
    config.DB.connect()
    config.DB.create_tables([User])
    config.DB.close()
    bot.polling(none_stop=True)

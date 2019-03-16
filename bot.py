import telebot
import requests


class Bot(telebot.TeleBot):
    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                     parse_mode=None, disable_notification=None):
        super().send_chat_action(chat_id=chat_id, action='typing')
        return super().send_message(chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup,
                                    parse_mode, disable_notification)

    def send_animation(self, chat_id, file_id, keyboard=None, text=None, duration=None, thumb=None,
                       width=None, height=None):
        super().send_chat_action(chat_id=chat_id, action='typing')
        data = {'chat_id': chat_id,
                'animation': file_id,
                'caption': text,
                'parse_mode': 'Markdown',
                'reply_markup': keyboard.to_json() if keyboard is not None else None,
                'width': width,
                'height': height,
                'duration': duration,
                'thumb': thumb}

        url = f'https://api.telegram.org/bot{self.token}/sendAnimation'

        r = requests.post(url=url, data=data).json()
        return r['result']['message_id']

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None,
                   disable_notification=None):
        super().send_chat_action(chat_id=chat_id, action='typing')
        return super().send_photo(chat_id, photo, caption, reply_to_message_id, reply_markup, parse_mode,
                                  disable_notification)

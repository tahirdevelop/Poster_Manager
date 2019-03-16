import peewee

POSTER_TOKEN = ""  # Enter poster token
TELEGRAM_TOKEN = ""  # Enter telegram token

DB = peewee.SqliteDatabase('Telegram.db')

MEDIA = {
    'GIF': {
        'worker': 'CgADAgADlAIAAvFsaEiiYeohiHsYFAI',
        'rfm': 'CgADAgADPQQAAgvIYUhEu_H0-FwEuQI'
    },
}

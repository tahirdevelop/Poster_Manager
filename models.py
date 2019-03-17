from peewee import *
from config import DB


STATUS = [
    'choose_category',
    'choose_period_of_rfm'
]

class User(Model):
    id = IntegerField(primary_key=True, unique=True, null=False)
    name = CharField(null=True)
    status = CharField(null=True)
    last_message_id = IntegerField(null=True)

    class Meta:
        database = DB
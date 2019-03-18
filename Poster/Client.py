import datetime


class Client:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.phone_number = kwargs['phone_number']
        self.count_order = kwargs['count_order']
        self.total_payed_sum = kwargs['total_payed_sum']
        self.last_order_date = datetime.datetime.fromtimestamp(int(kwargs['last_order_date']) / 1e3).date()
        self.last_order_date_timestamp = int(kwargs['last_order_date'])

#  TODO CREATE COMPOSITIONS FOR CLIENT AND ORDERS
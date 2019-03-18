import requests
from Poster.Client import Client


class User:

    def __init__(self, token):
        self.token = token

    def get_client(self, id):
        r = requests.get(f'htpitps://joinposter.com/api/clients.getClient?token={self.token}&client_id={id}').json()[
            'response'][0]
        c = requests.get(f'https://joinposter.com/api/dash.getTransactions?token={self.token}&'
                         f'type=clients&id={id}&status=2').json()['response']
        last_order_date = c[0]['date_close']
        count_order = len(c)
        return Client(id=r['client_id'], name=r['firstname'] + r['lastname'],
                      phone_number=r['phone'], last_order_date=last_order_date,
                      count_order=count_order, total_payed_sum=int(r['total_payed_sum']) / 100)

    def get_clients(self):
        poster_clients = requests.get(f'https://joinposter.com/api/'
                                      f'clients.getClients?token={self.token}').json()['response']

        poster_orders = requests.get(f'https://joinposter.com/api/dash.getTransactions?'
                                     f'token={self.token}&status=2&date_from=19900101').json()['response']

        find_orders = lambda client: client.update(
            {'orders': list(filter(lambda order: order['client_id'] == client['client_id'], poster_orders))}
        )
        clients = []
        for client in poster_clients:
            find_orders(client)
            clients.append(client)

        return [Client(id=client['client_id'],
                       phone_number=client['phone'],
                       count_order=len(client['orders']),
                       name=client['firstname'] + client['lastname'],
                       total_payed_sum=int(client['total_payed_sum']) / 100,
                       last_order_date=client['orders'][0]['date_close'] if client['orders'] else 0)
                for client in clients]

    def get_clients_by_date(self, date_from):
        poster_clients = requests.get(f'https://joinposter.com/api/'
                                      f'clients.getClients?token={self.token}').json()['response']

        poster_orders = requests.get(f'https://joinposter.com/api/dash.getTransactions?'
                                     f'token={self.token}&status=2&date_from={date_from}').json()['response']
        clients = []
        for c in poster_clients:
            order = list(filter(lambda x: x['client_id'] == c['client_id'], poster_orders))
            count_order = len(order)

            if count_order == 0:
                continue
            last_order_date = order[0]['date_close']
            clients.append(Client(id=c['client_id'], name=c['firstname'] + c['lastname'],
                                  phone_number=c['phone'], last_order_date=last_order_date,
                                  count_order=count_order, total_payed_sum=int(c['total_payed_sum']) / 100))

        return clients
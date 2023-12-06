import requests
import simplejson
from urllib.parse import urljoin
from fe.access.auth import Auth


class Buyer:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = urljoin(url_prefix, "buyer/")
        self.user_id = user_id
        self.password = password
        self.token = ""
        self.terminal = "my terminal"
        self.auth = Auth(url_prefix)
        code, self.token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 200

    def new_order(self, store_id: str, book_id_and_count: [(str, int)]) -> (int, str):
        books = []
        for id_count_pair in book_id_and_count:
            books.append({"id": id_count_pair[0], "count": id_count_pair[1]})
        json = {"user_id": self.user_id, "store_id": store_id, "books": books}
        # print(simplejson.dumps(json))
        url = urljoin(self.url_prefix, "new_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        response_json = r.json()
        return r.status_code, response_json.get("order_id")

    def payment(self, order_id: str):
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "order_id": order_id,
        }
        url = urljoin(self.url_prefix, "payment")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def add_funds(self, add_value: str) -> int:
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "add_value": add_value,
        }
        url = urljoin(self.url_prefix, "add_funds")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def receive_goods(self, order_id: str):
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "order_id": order_id
        }
        url = urljoin(self.url_prefix, 'receive_goods')
        headers = {'token': self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def cancel_order(self, user_id: str, password: str, order_id: str):
        json = {
            "user_id": user_id,
            "password": password,
            "order_id": order_id
        }
        url = urljoin(self.url_prefix, 'cancel_order')
        headers = {'token': self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def view_order_history(self, user_id: str, password: str):
        json = {
            "user_id": user_id,
            "password": password,
        }
        url = urljoin(self.url_prefix, 'view_order_history')
        headers = {'token': self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

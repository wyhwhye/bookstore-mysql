from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.buyer import Buyer

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")


@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    books: [] = request.json.get("books")
    id_and_count = []
    for book in books:
        book_id = book.get("id")
        count = book.get("count")
        id_and_count.append((book_id, count))

    b = Buyer()
    code, message, order_id = b.new_order(user_id, store_id, id_and_count)
    return jsonify({"message": message, "order_id": order_id}), code


@bp_buyer.route("/payment", methods=["POST"])
def payment():
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    password: str = request.json.get("password")
    b = Buyer()
    code, message = b.payment(user_id, password, order_id)
    return jsonify({"message": message}), code


@bp_buyer.route("/add_funds", methods=["POST"])
def add_funds():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    add_value = request.json.get("add_value")
    b = Buyer()
    code, message = b.add_funds(user_id, password, add_value)
    return jsonify({"message": message}), code



@bp_buyer.route("/receive_goods", methods=["POST"])
def receive_goods():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    order_id = request.json.get("order_id")
    b = Buyer()
    code, message = b.receive_order(user_id, password, order_id)
    return jsonify({"message": message}), code


@bp_buyer.route("/cancel_order", methods=["POST"])
def cancel_order():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    order_id = request.json.get("order_id")
    b = Buyer()
    code, message = b.cancel_order(user_id, password, order_id)
    return jsonify({"message": message}), code


@bp_buyer.route("/view_order_history", methods=["POST"])
def view_order_history():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    b = Buyer()
    code, message, orders = b.view_order_history(user_id=user_id, password=password)
    return jsonify({"message": message, "orders": orders}), code


@bp_buyer.route("/search_books", methods=["POST"])
def search_books():
   store_id = request.json.get("store_id")
   title = request.json.get("title")
   tags = request.json.get("tags")
   content = request.json.get("content")
   if not store_id:
       store_id = ''
   if not title:
       title = ''
   if not tags:
       tags = ''
   if not content:
       content = ''
   b = Buyer()
   code, message, books = b.search_books(store_id=store_id, title=title, tags=tags, content=content)
   return jsonify({"message": message, "books": books}), code
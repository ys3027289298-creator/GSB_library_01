"""图书馆核心逻辑：图书、读者、借阅、逾期和分类。"""

import json


def new_game():
    return {
        "books": {},
        "readers": {"R1": True, "R2": True},
        "loans": {},
        "loan_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return state


def add_book(state, book_id, shelf):
    state["books"][book_id] = {
        "shelf": shelf,
        "borrowed_by": None,
        "on_shelf": True,
        "overdue_days": 0,
        "stock": 1,
        "category": None,
        "reserved_by": None,
    }
    return True


def borrow(state, book_id, reader_id):
    book = state["books"].get(book_id)
    if book is None or not state["readers"].get(reader_id, False):
        return False
    if book["borrowed_by"] == reader_id:
        return True
    if book["borrowed_by"] is not None:
        return False
    book["borrowed_by"] = reader_id
    book["on_shelf"] = False
    state["loans"][state["loan_id"]] = book_id
    state["loan_id"] += 1
    return True


def return_book(state, book_id):
    book = state["books"].get(book_id)
    if book is None or book["borrowed_by"] is None:
        return False
    book["borrowed_by"] = None
    book["on_shelf"] = True
    return True


def late_fee(state, book_id):
    book = state["books"].get(book_id)
    if book is None:
        return 0
    return max(0, book["overdue_days"])


def deactivate_reader(state, reader_id):
    if reader_id not in state["readers"]:
        return False
    state["readers"][reader_id] = False
    return True


def reserve(state, book_id, reader_id):
    book = state["books"].get(book_id)
    if book is None or not state["readers"].get(reader_id, False):
        return False
    if book["reserved_by"] is None or book["reserved_by"] == reader_id:
        book["reserved_by"] = reader_id
        return True
    return False


def recategorize(state, book_id, category):
    book = state["books"].get(book_id)
    if book is None:
        return False
    book["category"] = category
    return True


def cancel_reservation(state, book_id, reader_id):
    book = state["books"].get(book_id)
    if book is None or book["reserved_by"] != reader_id:
        return False
    book["reserved_by"] = None
    return True


def damage_book(state, book_id):
    book = state["books"].get(book_id)
    if book is None or book["stock"] <= 0:
        return False
    book["stock"] -= 1
    return True


def main():
    print("图书馆 - 命令: add/borrow/return/fee/deactivate/reserve/cancel/damage/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()

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
    state["loan_id"] += 1
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
    state["books"][book_id]["borrowed_by"] = reader_id
    state["books"][book_id]["on_shelf"] = False
    state["loans"][state["loan_id"]] = book_id
    return True


def return_book(state, book_id):
    state["books"][book_id]["borrowed_by"] = None
    return True


def late_fee(state, book_id):
    days = state["books"][book_id]["overdue_days"]
    return days - 1


def deactivate_reader(state, reader_id):
    state["readers"][reader_id] = False
    return True


def reserve(state, book_id, reader_id):
    if state["books"][book_id]["reserved_by"] is None:
        state["books"][book_id]["reserved_by"] = reader_id
        return True
    return False


def recategorize(state, book_id, category):
    return True


def cancel_reservation(state, book_id, reader_id):
    return True


def damage_book(state, book_id):
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

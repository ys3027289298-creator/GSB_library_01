"""图书馆核心逻辑：图书、读者、借阅、逾期和分类。"""

import json


ILLEGAL_COMMAND = object()


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
    try:
        state = json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        return new_game()
    if not isinstance(state, dict):
        return new_game()
    state.setdefault("books", {})
    state.setdefault("readers", {})
    state.setdefault("loans", {})
    if not isinstance(state["loan_id"], int) or state["loan_id"] < 0:
        state["loan_id"] = 0
    return state


def add_book(state, book_id, shelf):
    if not book_id or not shelf or book_id in state["books"]:
        return False
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
    if book is None:
        return False
    if not state["readers"].get(reader_id):
        return False
    if book["stock"] <= 0 or not book["on_shelf"] or book["borrowed_by"] is not None:
        return False
    state["books"][book_id]["borrowed_by"] = reader_id
    state["books"][book_id]["on_shelf"] = False
    state["loan_id"] += 1
    state["loans"][state["loan_id"]] = book_id
    return True


def return_book(state, book_id):
    book = state["books"].get(book_id)
    if book is None:
        return False
    for loan_id, loaned_book in list(state["loans"].items()):
        if loaned_book == book_id:
            del state["loans"][loan_id]
            break
    book["borrowed_by"] = None
    book["on_shelf"] = book["stock"] > 0
    book["overdue_days"] = 0
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
    if book is None or not state["readers"].get(reader_id):
        return False
    if book["reserved_by"] == reader_id:
        return True
    if book["reserved_by"] is None:
        state["books"][book_id]["reserved_by"] = reader_id
        return True
    return False


def recategorize(state, book_id, category):
    book = state["books"].get(book_id)
    if book is None or not category:
        return False
    book["category"] = category
    return True


def cancel_reservation(state, book_id, reader_id):
    book = state["books"].get(book_id)
    if book is None:
        return False
    if book["reserved_by"] in (None, reader_id):
        book["reserved_by"] = None
        return True
    return True


def damage_book(state, book_id):
    book = state["books"].get(book_id)
    if book is None or book["stock"] <= 0:
        return False
    book["stock"] -= 1
    if book["stock"] == 0:
        book["on_shelf"] = False
    return True


def handle_command(state, raw):
    parts = raw.split()
    if not parts:
        return None
    command, args = parts[0], parts[1:]
    if command == "add" and len(args) == 2:
        return add_book(state, args[0], args[1])
    if command == "borrow" and len(args) == 2:
        return borrow(state, args[0], args[1])
    if command == "return" and len(args) == 1:
        return return_book(state, args[0])
    if command == "fee" and len(args) == 1:
        return late_fee(state, args[0])
    if command == "deactivate" and len(args) == 1:
        return deactivate_reader(state, args[0])
    if command == "reserve" and len(args) == 2:
        return reserve(state, args[0], args[1])
    if command == "cancel" and len(args) == 2:
        return cancel_reservation(state, args[0], args[1])
    if command == "recategorize" and len(args) >= 2:
        return recategorize(state, args[0], " ".join(args[1:]))
    if command == "damage" and len(args) == 1:
        return damage_book(state, args[0])
    return ILLEGAL_COMMAND


def main():
    print("图书馆 - 命令: add/borrow/return/fee/deactivate/reserve/cancel/damage/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if raw == "quit":
            break
        result = handle_command(state, raw)
        if result is None:
            continue
        if result is ILLEGAL_COMMAND:
            print("非法命令")
        elif isinstance(result, bool):
            print("ok" if result else "失败")
        else:
            print(result)


if __name__ == "__main__":
    main()

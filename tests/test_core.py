import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_borrow(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        core.borrow(state, "B1", "R1")
        result = core.borrow(state, "B1", "R2")
        self.assertFalse(result)

    def test_02_return_frees_shelf(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        core.borrow(state, "B1", "R1")
        core.return_book(state, "B1")
        self.assertTrue(state["books"]["B1"]["on_shelf"])

    def test_03_late_fee_no_off_by_one(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        state["books"]["B1"]["overdue_days"] = 5
        self.assertEqual(core.late_fee(state, "B1"), 5)

    def test_04_no_borrow_by_inactive_reader(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        core.deactivate_reader(state, "R1")
        result = core.borrow(state, "B1", "R1")
        self.assertFalse(result)

    def test_05_cancel_reservation_releases(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        core.reserve(state, "B1", "R1")
        core.cancel_reservation(state, "B1", "R1")
        result = core.reserve(state, "B1", "R2")
        self.assertTrue(result)

    def test_06_recategorize_updates_search(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        core.recategorize(state, "B1", "科幻")
        self.assertEqual(state["books"]["B1"]["category"], "科幻")

    def test_07_damage_updates_stock(self):
        state = core.new_game()
        core.add_book(state, "B1", "S1")
        state["books"]["B1"]["stock"] = 3
        core.damage_book(state, "B1")
        self.assertEqual(state["books"]["B1"]["stock"], 2)

    def test_08_load_preserves_loan_id(self):
        state = core.new_game()
        state["loan_id"] = 7
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["loan_id"], 7)


if __name__ == "__main__":
    unittest.main()

import unittest

from src.tender_search import _connect, load_tenders, search_tenders


class TenderSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = _connect()
        load_tenders(self.conn)

    def test_search_by_supplier(self) -> None:
        rows = list(search_tenders(self.conn, supplier="Кукла"))
        self.assertEqual(len(rows), 3)

    def test_search_by_customer(self) -> None:
        rows = list(search_tenders(self.conn, customer="УКРГАЗВИДОБУВАННЯ"))
        self.assertEqual(len(rows), 1)
        self.assertIn("УКРГАЗВИДОБУВАННЯ", rows[0]["customer"])

    def test_search_by_budget_range(self) -> None:
        rows = list(search_tenders(self.conn, min_value=200000, max_value=220000))
        self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()

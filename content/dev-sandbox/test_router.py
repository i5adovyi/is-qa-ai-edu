"""One test intentionally fails in the shipped exercise fixture."""
import unittest
from router import take_step

class RouterContract(unittest.TestCase):
    def test_first_step(self):
        self.assertEqual(take_step(0, 3), 1)

    def test_last_allowed_step(self):
        self.assertEqual(take_step(2, 3), 3)

    def test_exhausted_budget(self):
        with self.assertRaises(RuntimeError):
            take_step(3, 3)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            take_step(True, 3)

    def test_negative_count(self):
        with self.assertRaises(ValueError):
            take_step(-1, 3)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
from funcs import func

class Test(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(func.sum(2,3), 5)

    @patch('funcs.func.misformatted_func')
    def test_misformatted_func(self, mock_misformatted_func):
        func.misformatted_func("one", "two", "three")
        mock_misformatted_func.assert_called_with("one", "two", "three")

if __name__ == "__main__":
    unittest.main()
import unittest
from unittest.mock import patch
from funcs import func

class Test(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(func.sum(2,3), 5)

    # Any misformatted functions would not pass flake8 format checks. All related tests would not be executed.
    # @patch('funcs.func.misformatted_func')
    # def test_misformatted_func(self, mock_misformatted_func):
    #     func.misformatted_func("one", "two", "three")
    #     mock_misformatted_func.assert_called_with("one", "two", "three")

    @patch('funcs.func.corr_formatted_func')
    def test_corr_formatted_func(self, mock_corr_formatted_func):
        func.corr_formatted_func("one", "two", "three")
        mock_corr_formatted_func.assert_called_with("one", "two", "three")

if __name__ == "__main__":
    unittest.main()
import unittest
from unittest.mock import patch
from funcs import func

class Test(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(func.sum(2,3), 5)

if __name__ == "__main__":
    unittest.main()
    
import unittest
from pricing import *

class TestPricing(unittest.TestCase):
    def test_pricing_function(self):
        self.assertEqual(pricing_function(args), expected_output)

if __name__ == '__main__':
    unittest.main()
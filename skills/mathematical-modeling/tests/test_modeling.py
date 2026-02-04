import unittest
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from weighted_score import calculate_weighted_matrix
from npv_calculator import calculate_npv

class TestModeling(unittest.TestCase):

    def test_weighted_score(self):
        criteria = {"A": 0.5, "B": 0.5}
        options = {
            "Opt1": {"A": 10, "B": 0},  # Score 5
            "Opt2": {"A": 8, "B": 8}    # Score 8
        }
        result = calculate_weighted_matrix(criteria, options)
        self.assertEqual(result["best_option"], "Opt2")
        self.assertEqual(result["ranked_options"][0]["total_score"], 8.0)

    def test_npv(self):
        # Invest 100, get 110 next year. Rate 10%
        # NPV = -100 + 110/1.1 = -100 + 100 = 0
        flows = [-100, 110]
        rate = 0.1
        npv = calculate_npv(rate, flows)
        self.assertEqual(npv, 0.0)

        # Invest 100, get 105. Rate 10% -> NPV negative
        npv_neg = calculate_npv(0.1, [-100, 105])
        self.assertLess(npv_neg, 0)

if __name__ == '__main__':
    unittest.main()

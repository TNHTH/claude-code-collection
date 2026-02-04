"""
Unit tests for Advanced Mathematical Models (Monte Carlo & Bayes)
"""

import unittest
import statistics
from scripts.monte_carlo import run_monte_carlo_pert, validate_inputs
from scripts.bayes_updater import calculate_posterior, validate_probability

class TestMonteCarlo(unittest.TestCase):

    def test_pert_validation(self):
        """Test input validation for PERT."""
        # Valid inputs
        try:
            validate_inputs(2, 5, 10)
        except ValueError:
            self.fail("validate_inputs raised ValueError unexpectedly!")

        # Invalid inputs
        with self.assertRaises(ValueError):
            validate_inputs(10, 5, 2)  # Wrong order
        with self.assertRaises(ValueError):
            validate_inputs(2, 10, 5)  # Nominal > Pessimistic

    def test_simulation_run(self):
        """Test a basic simulation run."""
        # Fix seed for reproducibility
        result = run_monte_carlo_pert(2, 5, 10, n_samples=1000, seed=42)

        self.assertIsNotNone(result)
        # With 2, 5, 10, mean should be around (2+5+10)/3 = 5.66 for Triangular
        # Or (2 + 4*5 + 10)/6 = 5.33 for Beta-PERT approximation
        # Random triangular mean is (low + high + mode) / 3
        expected_mean = (2 + 10 + 5) / 3
        self.assertAlmostEqual(result.mean, expected_mean, delta=0.5)

        # Check percentiles logic
        self.assertTrue(result.p10 < result.p50 < result.p90)
        self.assertTrue(result.p10 >= 2)
        self.assertTrue(result.p90 <= 10)

class TestBayesUpdater(unittest.TestCase):

    def test_probability_validation(self):
        """Test input validation for probabilities."""
        with self.assertRaises(ValueError):
            validate_probability(1.5, "test")
        with self.assertRaises(ValueError):
            validate_probability(-0.1, "test")

    def test_posterior_calculation(self):
        """Test classic medical example."""
        # Disease 1%, Sens 95%, Spec 90%
        # P(E) = 0.95*0.01 + 0.10*0.99 = 0.0095 + 0.099 = 0.1085
        # Post = 0.0095 / 0.1085 ≈ 0.0875

        result = calculate_posterior(0.01, 0.95, 0.90)
        self.assertAlmostEqual(result.posterior, 0.0876, delta=0.0001)

    def test_perfect_test(self):
        """Test a perfect test case."""
        # Prior 50%, Sens 100%, Spec 100%
        result = calculate_posterior(0.5, 1.0, 1.0)
        self.assertEqual(result.posterior, 1.0)

    def test_useless_test(self):
        """Test a useless test (coin flip)."""
        # Prior 50%, Sens 50%, Spec 50%
        # Result should equal prior
        result = calculate_posterior(0.5, 0.5, 0.5)
        self.assertEqual(result.posterior, 0.5)

if __name__ == '__main__':
    unittest.main()

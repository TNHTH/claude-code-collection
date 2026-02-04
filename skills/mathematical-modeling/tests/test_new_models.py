import unittest
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../scripts'))

import trend_forecast
import path_finder

class TestTrendForecast(unittest.TestCase):
    def test_perfect_linear(self):
        # y = 2x + 1
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 7, 9, 11]
        result = trend_forecast.fit_predict(x, y, [6])

        self.assertAlmostEqual(result['slope'], 2.0)
        self.assertAlmostEqual(result['intercept'], 1.0)
        self.assertAlmostEqual(result['r_squared'], 1.0)
        self.assertAlmostEqual(result['predictions'][0], 13.0)

    def test_imperfect_data(self):
        x = [1, 2, 3]
        y = [1, 2, 2] # Slight deviation
        result = trend_forecast.fit_predict(x, y, [4])
        # Slope should be 0.5, Intercept 0.666...
        self.assertLess(result['r_squared'], 1.0)
        self.assertGreater(result['r_squared'], 0.0)

class TestPathFinder(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

    def test_simple_path(self):
        start = (0, 0)
        end = (2, 2)
        result = path_finder.find_path(self.grid, start, end)

        self.assertNotIn('error', result)
        self.assertIsInstance(result['path'], list)
        self.assertEqual(result['path'][0], start)
        self.assertEqual(result['path'][-1], end)

    def test_blocked_path(self):
        # Wall blocking the way
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]
        start = (0, 0)
        end = (0, 2)
        result = path_finder.find_path(grid, start, end)

        self.assertIn('error', result)
        self.assertEqual(result['error'], "No path found")

if __name__ == '__main__':
    unittest.main()

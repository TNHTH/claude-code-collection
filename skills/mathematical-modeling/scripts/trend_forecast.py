"""
Trend Forecast Module
Implements simple Linear Regression (Least Squares) using pure Python.
Category: Prediction
"""

import math
import statistics

def fit_predict(x_values, y_values, future_x):
    """
    Fits a linear regression model (y = mx + b) and predicts values for future_x.

    Args:
        x_values (list[float]): Independent variable data points.
        y_values (list[float]): Dependent variable data points.
        future_x (list[float]): X values to predict.

    Returns:
        dict: {
            "slope": float,
            "intercept": float,
            "r_squared": float,
            "predictions": list[float],
            "equation": str
        }
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")

    if len(x_values) < 2:
        raise ValueError("Need at least 2 data points for regression")

    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x*y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x*x for x in x_values)
    sum_y2 = sum(y*y for y in y_values)

    # Calculate slope (m) and intercept (b)
    # m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x^2)
    denominator = (n * sum_x2 - sum_x**2)
    if denominator == 0:
        raise ValueError("Vertical line: x values are all the same")

    m = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - m * sum_x) / n

    # Calculate R-squared
    # Total Sum of Squares (SST) = sum((y - mean_y)^2)
    # Sum of Squared Errors (SSE) = sum((y - predicted_y)^2)
    # R2 = 1 - (SSE / SST)

    mean_y = sum_y / n
    sst = sum((y - mean_y)**2 for y in y_values)
    sse = sum((y - (m * x + b))**2 for x, y in zip(x_values, y_values))

    if sst == 0:
        r_squared = 1.0 if sse == 0 else 0.0
    else:
        r_squared = 1.0 - (sse / sst)

    # Predict
    predictions = [m * x + b for x in future_x]

    return {
        "slope": m,
        "intercept": b,
        "r_squared": r_squared,
        "predictions": predictions,
        "equation": f"y = {m:.4f}x + {b:.4f}"
    }

if __name__ == "__main__":
    # Test
    X = [1, 2, 3, 4, 5]
    Y = [2, 4, 5, 4, 5]
    result = fit_predict(X, Y, [6, 7])
    print(result)

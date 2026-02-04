"""
Monte Carlo Simulation for Risk Assessment (PERT Estimation)

This module provides tools for estimating risks using Monte Carlo simulations,
specifically using PERT (Program Evaluation and Review Technique) logic.
It uses the Triangular distribution as a proxy for the Beta distribution used in PERT.
"""

import random
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class SimulationResult:
    """Immutable data class for simulation results."""
    mean: float
    median: float
    std_dev: float
    p10: float  # 10th percentile (Optimistic case in risk terms)
    p50: float  # 50th percentile (Median)
    p90: float  # 90th percentile (Pessimistic case in risk terms)
    samples: tuple  # Store samples as tuple for immutability (optional, can be large)

def validate_inputs(optimistic: float, nominal: float, pessimistic: float) -> None:
    """
    Validates the input parameters for PERT estimation.

    Args:
        optimistic: The best case scenario (lowest value).
        nominal: The most likely scenario (mode).
        pessimistic: The worst case scenario (highest value).

    Raises:
        ValueError: If inputs are not logically ordered (opt <= nom <= pess).
    """
    if not (optimistic <= nominal <= pessimistic):
        raise ValueError(
            f"Inputs must satisfy: optimistic ({optimistic}) <= "
            f"nominal ({nominal}) <= pessimistic ({pessimistic})"
        )

def run_monte_carlo_pert(
    optimistic: float,
    nominal: float,
    pessimistic: float,
    n_samples: int = 10000,
    seed: Optional[int] = None
) -> SimulationResult:
    """
    Runs a Monte Carlo simulation using a Triangular distribution (PERT approximation).

    Args:
        optimistic: The minimum expected value.
        nominal: The most likely value (mode).
        pessimistic: The maximum expected value.
        n_samples: Number of simulation iterations.
        seed: Random seed for reproducibility.

    Returns:
        SimulationResult containing statistical analysis of the simulation.
    """
    validate_inputs(optimistic, nominal, pessimistic)

    if seed is not None:
        random.seed(seed)

    # Generate samples using Triangular distribution
    # random.triangular(low, high, mode)
    # Note: Python's random.triangular takes (low, high, mode)
    samples_list = [
        random.triangular(optimistic, pessimistic, nominal)
        for _ in range(n_samples)
    ]

    # Calculate statistics
    mean_val = statistics.mean(samples_list)
    median_val = statistics.median(samples_list)
    std_dev_val = statistics.stdev(samples_list)

    # Calculate percentiles
    # quantiles returns a list of cut points.
    # For P10, P50, P90, we can use quantiles or just sort and pick.
    # statistics.quantiles is available in Python 3.8+
    try:
        quantiles = statistics.quantiles(samples_list, n=100)
        p10 = quantiles[9]   # 10th percentile
        p50 = quantiles[49]  # 50th percentile
        p90 = quantiles[89]  # 90th percentile
    except AttributeError:
        # Fallback for older python versions if needed
        sorted_samples = sorted(samples_list)
        p10 = sorted_samples[int(n_samples * 0.1)]
        p50 = sorted_samples[int(n_samples * 0.5)]
        p90 = sorted_samples[int(n_samples * 0.9)]

    return SimulationResult(
        mean=round(mean_val, 2),
        median=round(median_val, 2),
        std_dev=round(std_dev_val, 2),
        p10=round(p10, 2),
        p50=round(p50, 2),
        p90=round(p90, 2),
        samples=tuple(samples_list) # Keep immutable copy if needed
    )

if __name__ == "__main__":
    # Example usage
    try:
        print("Running Monte Carlo Simulation for Project Task A...")
        # Optimistic: 2 days, Nominal: 5 days, Pessimistic: 12 days
        result = run_monte_carlo_pert(2, 5, 12)

        print(f"Input: Opt=2, Nom=5, Pess=12")
        print(f"Mean: {result.mean}")
        print(f"P10 (Best Case): {result.p10}")
        print(f"P50 (Median): {result.p50}")
        print(f"P90 (Worst Case): {result.p90}")
        print(f"Risk Spread (P90-P10): {round(result.p90 - result.p10, 2)}")

    except ValueError as e:
        print(f"Error: {e}")

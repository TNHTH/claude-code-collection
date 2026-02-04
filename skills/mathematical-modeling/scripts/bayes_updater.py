"""
Bayesian Inference Updater

This module provides tools for updating probabilities based on new evidence using Bayes' theorem.
Useful for medical diagnosis, hiring decisions, and filtering false positives.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass(frozen=True)
class BayesResult:
    """Immutable data class for Bayesian update results."""
    prior: float
    posterior: float
    evidence_probability: float
    likelihood_ratio_positive: float

def validate_probability(prob: float, name: str) -> None:
    """
    Validates that a probability is between 0 and 1.

    Args:
        prob: The probability value to check.
        name: The name of the parameter for the error message.

    Raises:
        ValueError: If probability is not in [0, 1].
    """
    if not (0.0 <= prob <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0, got {prob}")

def calculate_posterior(
    prior: float,
    sensitivity: float,
    specificity: float
) -> BayesResult:
    """
    Calculates the posterior probability of a hypothesis given a positive test result.

    P(H|E) = P(E|H) * P(H) / P(E)
    where:
    - H is the Hypothesis (e.g., User has the disease/skill)
    - E is the Evidence (e.g., Positive test result)
    - P(E|H) is Sensitivity (True Positive Rate)
    - P(E|not H) is (1 - Specificity) (False Positive Rate)

    Args:
        prior: Prior probability of the hypothesis P(H).
        sensitivity: Probability of positive test given hypothesis is true P(E|H).
        specificity: Probability of negative test given hypothesis is false P(not E|not H).

    Returns:
        BayesResult containing the posterior probability and intermediate values.
    """
    validate_probability(prior, "Prior")
    validate_probability(sensitivity, "Sensitivity")
    validate_probability(specificity, "Specificity")

    # P(H)
    p_h = prior

    # P(not H)
    p_not_h = 1.0 - prior

    # P(E|H) = Sensitivity
    p_e_given_h = sensitivity

    # P(E|not H) = False Positive Rate = 1 - Specificity
    p_e_given_not_h = 1.0 - specificity

    # Total Probability of Evidence P(E)
    # P(E) = P(E|H)*P(H) + P(E|not H)*P(not H)
    p_e = (p_e_given_h * p_h) + (p_e_given_not_h * p_not_h)

    if p_e == 0:
        # Avoid division by zero if evidence is impossible
        return BayesResult(
            prior=prior,
            posterior=0.0,
            evidence_probability=0.0,
            likelihood_ratio_positive=0.0
        )

    # Posterior P(H|E)
    posterior = (p_e_given_h * p_h) / p_e

    # Likelihood Ratio Positive (Sensitivity / (1 - Specificity))
    lr_plus = 0.0
    if p_e_given_not_h > 0:
        lr_plus = sensitivity / p_e_given_not_h
    else:
        lr_plus = float('inf')  # Perfect test

    return BayesResult(
        prior=round(prior, 4),
        posterior=round(posterior, 4),
        evidence_probability=round(p_e, 4),
        likelihood_ratio_positive=round(lr_plus, 2)
    )

if __name__ == "__main__":
    # Example: Medical Test
    # Disease prevalence (Prior) = 1% (0.01)
    # Test Sensitivity (True Positive) = 95% (0.95)
    # Test Specificity (True Negative) = 90% (0.90)

    try:
        print("Running Bayesian Update for Medical Test...")
        prior_val = 0.01
        sens_val = 0.95
        spec_val = 0.90

        result = calculate_posterior(prior_val, sens_val, spec_val)

        print(f"Prior Probability: {result.prior*100}%")
        print(f"Sensitivity: {sens_val*100}%")
        print(f"Specificity: {spec_val*100}%")
        print(f"Evidence Probability P(E): {result.evidence_probability}")
        print(f"Posterior Probability P(H|E): {result.posterior*100}%")
        print(f"Likelihood Ratio (+): {result.likelihood_ratio_positive}")

    except ValueError as e:
        print(f"Error: {e}")

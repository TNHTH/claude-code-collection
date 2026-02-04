from typing import Dict, List, Tuple, Any

def calculate_weighted_matrix(
    criteria: Dict[str, float],
    options: Dict[str, Dict[str, float]]
) -> Dict[str, Any]:
    """
    Calculate weighted scores for options based on criteria weights.

    Args:
        criteria: Dict mapping criteria names to weights (should sum to 1.0 or 100)
        options: Dict mapping option names to a dict of scores for each criterion

    Returns:
        Dict containing ranked results and detailed breakdown
    """
    # Normalize weights if they sum to > 1.01 (e.g., 100)
    total_weight = sum(criteria.values())
    if total_weight > 1.01:
        normalized_criteria = {k: v / total_weight for k, v in criteria.items()}
    else:
        normalized_criteria = criteria

    results = []

    for opt_name, scores in options.items():
        total_score = 0.0
        breakdown = {}
        for crit, weight in normalized_criteria.items():
            score = scores.get(crit, 0.0)
            weighted_val = score * weight
            total_score += weighted_val
            breakdown[crit] = weighted_val

        results.append({
            "option": opt_name,
            "total_score": round(total_score, 2),
            "breakdown": breakdown
        })

    # Sort by total score descending
    results.sort(key=lambda x: x["total_score"], reverse=True)

    return {
        "ranked_options": results,
        "best_option": results[0]["option"] if results else None
    }

if __name__ == "__main__":
    # Example usage
    criteria_ex = {"Salary": 0.4, "Work-Life": 0.3, "Growth": 0.3}
    options_ex = {
        "Company A": {"Salary": 9, "Work-Life": 6, "Growth": 7},
        "Company B": {"Salary": 7, "Work-Life": 9, "Growth": 8}
    }
    print(calculate_weighted_matrix(criteria_ex, options_ex))

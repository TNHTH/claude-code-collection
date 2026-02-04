from typing import List

def calculate_npv(rate: float, cash_flows: List[float]) -> float:
    """
    Calculate Net Present Value.

    Args:
        rate: Discount rate per period (e.g., 0.05 for 5%)
        cash_flows: List of cash flows starting from t=0.
                    Negative for outflows, positive for inflows.

    Returns:
        NPV value
    """
    npv_value = 0.0
    for t, flow in enumerate(cash_flows):
        npv_value += flow / ((1 + rate) ** t)

    return round(npv_value, 2)

def compare_scenarios(rate: float, scenarios: List[dict]) -> List[dict]:
    """
    Compare multiple NPV scenarios.

    Args:
        rate: Discount rate
        scenarios: List of dicts with 'name' and 'flows'
    """
    results = []
    for sc in scenarios:
        val = calculate_npv(rate, sc['flows'])
        results.append({"name": sc['name'], "npv": val})

    results.sort(key=lambda x: x["npv"], reverse=True)
    return results

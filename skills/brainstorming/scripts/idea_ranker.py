from typing import List, Dict, Any

def calculate_ice_score(impact: float, confidence: float, ease: float) -> float:
    """
    计算 ICE 分数
    Impact (1-10): 预期影响力
    Confidence (1-10): 成功信心
    Ease (1-10): 实施容易度
    """
    return round(impact * confidence * ease, 2)

def rank_ideas(ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    对想法列表进行排序
    期望格式: [{'text': '...', 'ice': {'i': 10, 'c': 5, 'e': 8}}]
    """
    for idea in ideas:
        ice = idea.get('ice', {})
        score = calculate_ice_score(
            ice.get('i', 0),
            ice.get('c', 0),
            ice.get('e', 0)
        )
        idea['score'] = score

    return sorted(ideas, key=lambda x: x['score'], reverse=True)

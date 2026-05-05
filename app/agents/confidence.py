def normalize(value: float, min_val: float = 0, max_val: float = 1) -> float:
    """
    Ensure value stays between 0 and 1
    """
    return max(min_val, min(max_val, value))


def compute_confidence(
    financial_score: float,
    sentiment_score: float,
    risk_score: float = 0.2
) -> float:
    """
    Improved confidence calculation:
    - weighted inputs
    - normalized values
    - penalized by risk
    """

    financial = normalize(financial_score)
    sentiment = normalize(sentiment_score)
    risk = normalize(risk_score)

    weighted_score = (0.6 * financial) + (0.4 * sentiment)

    adjusted_score = weighted_score * (1 - risk)

    final_score = normalize(adjusted_score)

    return round(final_score, 2)
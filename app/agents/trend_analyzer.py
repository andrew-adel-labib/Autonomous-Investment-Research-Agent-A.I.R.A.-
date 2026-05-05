def analyze_trend(prices: list) -> str:
    """
    Improved trend detection using moving averages
    """

    if not prices or len(prices) < 2:
        return "unknown"

    short_avg = sum(prices[-3:]) / 3

    long_avg = sum(prices[:3]) / 3

    diff = short_avg - long_avg
    threshold = 0.01 * long_avg

    if diff > threshold:
        return "uptrend"
    elif diff < -threshold:
        return "downtrend"
    else:
        return "sideways"
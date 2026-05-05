def reflect_on_analysis(result):
    notes = []

    confidence = result.get("confidence", 0)
    insights = result.get("insights", [])
    sources = result.get("sources", [])
    data_quality = result.get("data_quality", 0)

    if len(sources) < 2:
        notes.append("Limited data sources available")
        confidence *= 0.85

    if any("Sentiment Score: 0" in i for i in insights):
        notes.append("No strong sentiment detected")
        confidence *= 0.9

    try:
        for i in insights:
            if "P/E Ratio" in i:
                pe = float(i.split(":")[1])
                if pe > 40:
                    notes.append("High valuation risk (P/E > 40)")
                    confidence *= 0.9
    except Exception:
        pass

    if data_quality < 0.4:
        notes.append("Low data quality detected")
        confidence *= 0.85

    confidence = round(max(min(confidence, 1.0), 0.0), 2)

    if confidence < 0.3:
        result["signal"] = "Uncertain"
        notes.append("Signal downgraded due to low confidence")

    result["confidence"] = confidence
    result["uncertainty"] = round(1 - confidence, 2)
    result["reflection_notes"] = notes

    return result
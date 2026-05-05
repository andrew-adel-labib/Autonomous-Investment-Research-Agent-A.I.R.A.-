def reflect_on_analysis(result):
    notes = []

    if len(result.get("sources", [])) < 2:
        result["confidence"] *= 0.7
        notes.append("Low data sources → confidence reduced")

    if result["confidence"] < 0.3:
        result["signal"] = "Uncertain"
        notes.append("Low confidence → signal downgraded to Uncertain")

    result["reflection_notes"] = notes
    return result
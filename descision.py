def decide(score):
    if score >= 80:
        return "NEXT"
    elif score >= 60:
        return "IMPROVE"
    else:
        return "RETRY"

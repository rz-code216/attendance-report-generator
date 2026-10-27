from domain.models import ReportType

# Words that appear only in one type (lowercase)
_TYPE_A_MARKERS = ["break", "place", "site", "100%", "125%", "150%", "sat 150", "bonus", "travel"]
_TYPE_B_MARKERS = ["entry", "exit", "notes", "hourly rate", "employee", "time card", "working days", "total payment"]


def classify(text: str) -> ReportType:
    lowered = text.lower()
    score_a = sum(marker in lowered for marker in _TYPE_A_MARKERS)
    score_b = sum(marker in lowered for marker in _TYPE_B_MARKERS)

    if score_a == score_b:
        raise ValueError(f"Cannot classify report (A={score_a}, B={score_b})")
    return ReportType.TYPE_A if score_a > score_b else ReportType.TYPE_B
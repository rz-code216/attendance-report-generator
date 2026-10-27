import re

# Characters the OCR often confuses with digits
_DIGIT_FIXES = str.maketrans({
    "O": "0", "o": "0",
    "l": "1", "I": "1", "|": "1", "│": "1",
    "S": "5", "B": "8", "Z": "2",
})

_DIGITLIKE = r"[0-9OolI|│SBZ]"

# Something that looks like a time: 1-2 digit-like chars, ':' or ';', 2 digit-like chars
_TIME_LIKE = re.compile(rf"(?<!\w)({_DIGITLIKE}{{1,2}}) ?[:;] ?({_DIGITLIKE}{{2}})(?!\w)")


def _fix_time(match: re.Match) -> str:
    hours = match.group(1).translate(_DIGIT_FIXES)
    minutes = match.group(2).translate(_DIGIT_FIXES)
    return f"{hours}:{minutes}"


def clean(raw_text: str) -> str:
    """Fix common OCR mistakes inside time-like tokens only."""
    return _TIME_LIKE.sub(_fix_time, raw_text)

_STRAY = str.maketrans({"[": " ", "]": " ", "(": " ", ")": " ", "'": " "})

_DATE_LIKE = re.compile(r"(\d{2})[/7iIl|](\d{2})[/7iIl|](20\d{2})")


def clean(raw_text: str) -> str:
    text = raw_text.translate(_STRAY)                      # brackets/quotes -> space
    text = _DATE_LIKE.sub(r"\1/\2/\3", text)               # 21703/2024 -> 21/03/2024
    return _TIME_LIKE.sub(_fix_time, text)                 # time fixes from before
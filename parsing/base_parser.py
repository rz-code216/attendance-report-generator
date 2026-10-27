import re
from abc import ABC, abstractmethod
from datetime import date, time

from domain.models import (
    AttendanceReport, AttendanceRow, ReportSummary, ReportType,
)
from parsing.cleaning import clean   # שם הפונקציה אצלך? אם שונה, תעדכני

DATE_RE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\b")
DECIMAL_RE = re.compile(r"\b\d+\.\d{2}\b")


# ---------- helpers shared by both parsers ----------

def parse_time(text: str) -> time:
    hours, minutes = text.split(":")
    return time(int(hours), int(minutes))


def time_to_minutes(text: str) -> int:
    """'8:30' -> 510"""
    hours, minutes = text.split(":")
    return int(hours) * 60 + int(minutes)


def hours_to_minutes(text: str) -> int:
    """'6.50' -> 390"""
    return round(float(text) * 60)


def parse_date(text: str) -> date:
    day, month, year = (int(p) for p in text.split("/"))
    if year < 100:
        year += 2000
    return date(year, month, day)


class BaseParser(ABC):
    report_type: ReportType

    # ---------- the shared flow (Template Method) ----------
    def parse(self, raw_text: str) -> AttendanceReport:
        lines = [l for l in clean(raw_text).splitlines() if l.strip()]
        summary = self._parse_summary(lines)

        rows = []
        for line in lines:
            if self._is_header_line(line):
                continue
            row = self._parse_row(line)
            if row is not None:
                rows.append(row)

        return AttendanceReport(self.report_type, tuple(rows), summary)

    # ---------- shared helper ----------
    @staticmethod
    def _leftover_words(line: str) -> list[str]:
        """Words left after removing dates, times and decimals.
        First word = the day, the rest = place (A) or notes (B)."""
        for pattern in (DATE_RE, TIME_RE, DECIMAL_RE):
            line = pattern.sub(" ", line)
        return line.split()

    # ---------- default: a data row always contains a date ----------
    def _is_header_line(self, line: str) -> bool:
        return DATE_RE.search(line) is None

    # ---------- each subclass fills only what differs ----------
    @abstractmethod
    def _parse_row(self, line: str) -> AttendanceRow | None: ...

    @abstractmethod
    def _parse_summary(self, lines: list[str]) -> ReportSummary: ...
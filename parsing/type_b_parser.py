import re

from domain.models import AttendanceRow, ReportSummary, ReportType
from parsing.base_parser import (
    BaseParser, DATE_RE, TIME_RE,
    parse_date, parse_time, time_to_minutes,
)

NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
MONTH_RE = re.compile(r"\b[A-Za-z]{3}-\d{2}\b")


class TypeBParser(BaseParser):
    report_type = ReportType.TYPE_B

    def _parse_row(self, line: str) -> AttendanceRow | None:
        date_match = DATE_RE.search(line)
        if date_match is None:
            return None

        work_date = parse_date(date_match.group())
        times = TIME_RE.findall(line)
        words = self._leftover_words(line)
        day = words[0] if words else ""
        notes = " ".join(words[1:]) or None

        if len(times) == 3:
            entry, exit_, total = times
            return AttendanceRow(
                date=work_date,
                day=day,
                entry=parse_time(entry),
                exit=parse_time(exit_),
                total_minutes=time_to_minutes(total),
                notes=notes,
            )

        # Holiday / Saturday row: only date, day, notes
        return AttendanceRow(
            date=work_date, day=day, entry=None, exit=None,
            total_minutes=None, notes=notes,
        )

    def _parse_summary(self, lines: list[str]) -> ReportSummary:
        days = total_minutes = rate = payment = month = None

        for line in lines:
            if DATE_RE.search(line):
                continue
            if "ימי עבודה" in line:
                days = int(NUMBER_RE.findall(line)[0])
            elif "שעות חודשיות" in line:
                total_minutes = time_to_minutes(TIME_RE.findall(line)[0])
            elif "מחיר לשעה" in line:
                rate = float(NUMBER_RE.findall(line)[0])
            elif "לתשלום" in line:
                payment = float(NUMBER_RE.findall(line)[0])
            if month is None and (m := MONTH_RE.search(line)):
                month = m.group()

        if None in (days, total_minutes, rate, payment):
            raise ValueError("Type B summary is incomplete")

        return ReportSummary(
            days=days,
            total_minutes=total_minutes,
            hourly_rate=rate,
            total_payment=payment,
            month=month,
            employee_name=None,   # TODO: להתאים לשורה האמיתית
        )
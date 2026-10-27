import re

from domain.models import AttendanceRow, ReportSummary, ReportType
from parsing.base_parser import (
    BaseParser, DATE_RE, DECIMAL_RE, TIME_RE,
    hours_to_minutes, parse_date, parse_time, time_to_minutes,
)

SUMMARY_RE = re.compile(r"סה.{0,2}כ")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


class TypeAParser(BaseParser):
    report_type = ReportType.TYPE_A

    def _parse_row(self, line: str) -> AttendanceRow | None:
        date_match = DATE_RE.search(line)
        if date_match is None:
            return None

        work_date = parse_date(date_match.group())
        times = TIME_RE.findall(line)
        decimals = DECIMAL_RE.findall(line)
        words = self._leftover_words(line)
        day = words[0] if words else ""
        place = " ".join(words[1:]) or None

        # Full working day: entry, exit, break + 5 numbers
        if len(times) == 3 and len(decimals) == 5:
            entry, exit_, brk = times
            total, h100, h125, h150, sat = decimals
            return AttendanceRow(
                date=work_date,
                day=day,
                entry=parse_time(entry),
                exit=parse_time(exit_),
                total_minutes=hours_to_minutes(total),
                place=place,
                break_min=time_to_minutes(brk),
                hours_100_min=hours_to_minutes(h100),
                hours_125_min=hours_to_minutes(h125),
                hours_150_min=hours_to_minutes(h150),
                hours_sat_min=hours_to_minutes(sat),
            )

        # Saturday / holiday: no entry or exit, stays empty
        return AttendanceRow(
            date=work_date, day=day, entry=None, exit=None,
            total_minutes=None, place=place,
        )

    def _parse_summary(self, lines: list[str]) -> ReportSummary:
        for line in lines:
            if SUMMARY_RE.search(line) and not DATE_RE.search(line):
                nums = NUMBER_RE.findall(line)
                if len(nums) >= 8:
                    return ReportSummary(
                        days=int(nums[0]),
                        total_minutes=hours_to_minutes(nums[1]),
                        hours_100_min=hours_to_minutes(nums[2]),
                        hours_125_min=hours_to_minutes(nums[3]),
                        hours_150_min=hours_to_minutes(nums[4]),
                        hours_sat_min=hours_to_minutes(nums[5]),
                        bonus=float(nums[6]),
                        travel=float(nums[7]),
                        company_name=lines[0],   # TODO: להתאים לשורה האמיתית
                    )
        raise ValueError("Type A summary line not found")
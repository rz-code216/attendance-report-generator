from dataclasses import dataclass
from datetime import date, time
from enum import Enum


class ReportType(Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"


@dataclass(frozen=True)
class AttendanceRow:
    # --- in both types ---
    date: date
    day: str                                  # "Monday"
    entry: time | None                        # None on Saturday / holiday rows
    exit: time | None
    total_minutes: int | None                 # 390 means 6.5 hours

    # --- type A only ---
    place: str | None = None                  # "Site 1"
    break_min: int | None = None              # 30
    hours_100_min: int | None = None
    hours_125_min: int | None = None
    hours_150_min: int | None = None
    hours_sat_min: int | None = None

    # --- type B only ---
    notes: str | None = None                  # "Holiday"


@dataclass(frozen=True)
class ReportSummary:
    # --- in both types ---
    days: int                                 # A: "Days", B: "Working days in month"
    total_minutes: int

    # --- type A only ---
    hours_100_min: int | None = None
    hours_125_min: int | None = None
    hours_150_min: int | None = None
    hours_sat_min: int | None = None
    bonus: float | None = None                # money: decision still open
    travel: float | None = None               # money: decision still open
    company_name: str | None = None

    # --- type B only ---
    employee_name: str | None = None
    month: str | None = None                  # "Apr-24"
    hourly_rate: float | None = None          # money: decision still open
    total_payment: float | None = None        # money: decision still open


@dataclass(frozen=True)
class AttendanceReport:
    report_type: ReportType
    rows: tuple[AttendanceRow, ...]           # tuple, not list: cannot be changed
    summary: ReportSummary
from datetime import date, time, timedelta
from domain.models import AttendanceRow

a = AttendanceRow(date(2024, 3, 1), "Friday", time(8, 0), time(15, 0), 6.5,
                  place="Site 1", break_duration=timedelta(minutes=30),
                  hours_100=6.5, hours_125=0.0, hours_150=0.0, hours_sat=0.0)

b = AttendanceRow(date(2024, 4, 10), "Wednesday", None, None, None, notes="Holiday")
print(a, b, sep="\n")
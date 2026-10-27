from pathlib import Path

from domain.models import ReportType
from parsing import get_parser
from parsing.classifier import classify
from parsing.cleaning import clean
from parsing.ocr import list_pdfs, ocr_pdf

# main.py נמצא בתיקיית השורש של הפרויקט, ולכן parent אחד בלבד
INPUT_DIR = Path(__file__).parent / "data" / "inputs"

DEBUG_TEXT = False   # True כדי להדפיס RAW ו-CLEANED


def process(pdf: Path) -> None:
    raw = ocr_pdf(pdf)                       # 1. OCR
    cleaned = clean(raw)                     # 2. ניקוי (לזיהוי הסוג)
    report_type = ReportType(classify(cleaned))   # 3. זיהוי סוג

    if DEBUG_TEXT:
        print("=== RAW ===")
        print(raw)
        print("=== CLEANED ===")
        print(cleaned)

    parser = get_parser(report_type)         # 4. בחירת פרסר (Factory)
    report = parser.parse(raw)               # parse מנקה בעצמו, ולכן מעבירים raw

    print(f"{pdf.name} -> {report_type.value}")
    print(f"  rows: {len(report.rows)}")
    print(f"  summary: {report.summary}")
    if report.rows:
        print(f"  first row: {report.rows[0]}")


def main() -> None:
    pdfs = list_pdfs(INPUT_DIR)
    if not pdfs:
        print(f"No PDFs found in {INPUT_DIR}")
        return

    for pdf in pdfs:
        print(f"\n===== {pdf.name} =====")
        try:
            process(pdf)
        except Exception as e:             # קובץ אחד שנכשל לא עוצר את השאר
            print(f"  FAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
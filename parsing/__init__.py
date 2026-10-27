from domain.models import ReportType
from parsing.base_parser import BaseParser
from parsing.type_a_parser import TypeAParser
from parsing.type_b_parser import TypeBParser

_PARSERS = {
    ReportType.TYPE_A: TypeAParser,
    ReportType.TYPE_B: TypeBParser,
}


def get_parser(report_type):
    return _PARSERS[report_type]()

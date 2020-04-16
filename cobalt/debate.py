from .akn import StructuredDocument
from .openstructure import OpenStructure


class DebateStructure(StructuredDocument):
    structure_type = "debateStructure"
    main_content_tag = "debateBody"


class DebateRecord(DebateStructure):
    document_type = "debateRecord"


# TODO: check that debateReport falls under OpenStructure
#  (there might be two StructuredDocument classes that
#  both use mainBody but have other differences)
class DebateReport(OpenStructure):
    document_type = "debateReport"

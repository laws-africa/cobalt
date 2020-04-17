from .akn import StructuredDocument


class OpenStructure(StructuredDocument):
    structure_type = "openStructure"
    main_content_tag = "mainBody"


class DebateReport(OpenStructure):
    document_type = "debateReport"


class Document(OpenStructure):
    document_type = "doc"


class Statement(OpenStructure):
    document_type = "statement"

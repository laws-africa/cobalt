from .akn import StructuredDocument


class OpenStructure(StructuredDocument):
    structure_type = "openStructure"
    main_content_tag = "mainBody"


class Document(OpenStructure):
    document_type = "document"


class Statement(OpenStructure):
    document_type = "statement"

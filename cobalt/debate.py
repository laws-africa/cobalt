from .akn import StructuredDocument


class DebateStructure(StructuredDocument):
    structure_type = "debateStructure"
    main_content_tag = "debateBody"


class DebateRecord(DebateStructure):
    document_type = "debate"

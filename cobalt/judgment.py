from .akn import StructuredDocument


class JudgmentStructure(StructuredDocument):
    structure_type = "judgmentStructure"
    main_content_tag = "judgmentBody"


class Judgment(JudgmentStructure):
    document_type = "judgment"

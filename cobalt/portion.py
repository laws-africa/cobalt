from .akn import StructuredDocument


class PortionStructure(StructuredDocument):
    structure_type = "portionStructure"
    main_content_tag = "portionBody"


class Portion(PortionStructure):
    document_type = "portion"

from .akn import StructuredDocument
from .collection import CollectionStructure


class AmendmentStructure(StructuredDocument):
    structure_type = "amendmentStructure"
    main_content_tag = "amendmentBody"


class Amendment(AmendmentStructure):
    document_type = "amendment"


class AmendmentList(CollectionStructure):
    document_type = "amendmentList"

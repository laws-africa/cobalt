from .akn import StructuredDocument


class DebateStructure(StructuredDocument):
    structure_type = "debateStructure"
    main_content_tag = "debateBody"


class Debate(DebateStructure):
    document_type = "debate"

    @classmethod
    def empty_document_content(cls, E):
        return E('debateBody',
                 E('debateSection',
                   E('p', eId="dbsect_nn_1__p_1")), eId="dbsect_nn_1")

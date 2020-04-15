"""
Cobalt's class hierarchy mimics that of the Akoma Ntoso standard. There is a primary root class for
all Akoma Ntoso documents. There are subclasses for each of the Akoma Ntoso document structure types,
such as hierarchicalStructure, debateStructure, etc. Finally, there is a class for each Akoma Ntoso
document type (act, bill, judgment, etc.) that extends the corresponding structure type.
"""

import re
from lxml import etree
from lxml import objectify


ENCODING_RE = re.compile(r'encoding="[\w-]+"')

DATE_FORMAT = "%Y-%m-%d"

AKN_NAMESPACES = {
    '2.0': 'http://www.akomantoso.org/2.0',
    '3.0': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0',
}


def datestring(value):
    if value is None:
        return ""
    elif isinstance(value, str):
        return value
    else:
        return "%04d-%02d-%02d" % (value.year, value.month, value.day)


# Create a new objectify parser that doesn't remove blank text nodes
objectify_parser = etree.XMLParser()
objectify_parser.set_element_class_lookup(objectify.ObjectifyElementClassLookup())


class AkomaNtosoDocument:
    """ Base class for Akoma Ntoso documents.
    """
    _parser = objectify_parser

    def __init__(self, xml=None):
        encoding = ENCODING_RE.search(xml, 0, 200)
        if encoding:
            # lxml doesn't like unicode strings with an encoding element, so
            # change to bytes
            xml = xml.encode('utf-8')

        self.root = objectify.fromstring(xml, parser=objectify_parser)
        self.namespace = self.get_namespace()

        self._maker = objectify.ElementMaker(annotate=False, namespace=self.namespace, nsmap=self.root.nsmap)
        # the "source" attribute used on some elements where it is required.
        # contains: name, id, url
        self.source = ["cobalt", "cobalt", "https://github.com/laws-africa/cobalt"]

    def parse(self, xml, document_type=None):
        """ Parse XML and ensure it's Akoma Ntoso. Raises ValueError on error. Returns the root element.
        """
        root = objectify.fromstring(xml, parser=self._parser)

        # ensure the root element is correct
        name = root.tag.split('}', 1)[1]
        if name != 'akomaNtoso':
            raise ValueError(f"XML root element must be akomaNtoso, but got {name} instead")

        return root

    def to_xml(self, encoding='utf-8'):
        return etree.tostring(self.root, encoding=encoding)

    def get_namespace(self):
        akn_namespaces = [ns[1] for ns in sorted(list(AKN_NAMESPACES.items()), reverse=True)]
        namespaces = list(self.root.nsmap.values())
        for ns in akn_namespaces:
            if ns in namespaces:
                return ns

        raise ValueError(f"Expected to find one of the following Akoma Ntoso XML namespaces: {', '.join(akn_namespaces)}. Only these namespaces were found: {', '.join(namespaces)}")


class Fragment(AkomaNtosoDocument):
    pass


# ----------------------------------------------------------------------------------
# Document structure classes

class StructuredDocument(AkomaNtosoDocument):
    """ Common base class for AKN documents with a known document structure.
    """

    structure_type = None
    """ The name of the this document's structural type.
    """

    main_content_element = None
    """ The name of the structural type's main content element.
    """

    document_type = None
    """ The name of the document type, corresponding to the primary document XML element.
    """

    def parse(self, xml, document_type=None):
        """ Parse XML and ensure it's Akoma Ntoso.
        Raises ValueError on error. Returns the root element.
        """
        root = super().parse(xml, document_type)

        if root.countchildren() < 1:
            raise ValueError("XML root element must have at least one child")

        name = root.getchildren()[0].tag.split('}', 1)[1]
        if name != self.document_type:
            raise ValueError(f"Expected {self.document_type} as first child of root element, but got {name} instead")

        return root


class AmendmentStructure(StructuredDocument):
    structure_type = "amendmentStructure"
    main_content_element = "amendmentBody"


class CollectionStructure(StructuredDocument):
    structure_type = "collectionStructure"
    main_content_element = "collectionBody"


class DebateStructure(StructuredDocument):
    structure_type = "debateStructure"
    main_content_element = "debateBody"


class HierarchicalStructure(StructuredDocument):
    structure_type = "hierarchicalStructure"
    main_content_element = "body"


class JudgmentStructure(StructuredDocument):
    structure_type = "judgmentStructure"
    main_content_element = "judgmentBody"


class OpenStructure(StructuredDocument):
    structure_type = "openStructure"
    main_content_element = "mainBody"


class PortionStructure(StructuredDocument):
    structure_type = "portionStructure"
    main_content_element = "portionBody"


# ----------------------------------------------------------------------------------
# Document type classes
# the following have moved into their own files:
# - act


class Amendment(AmendmentStructure):
    document_type = "amendment"


class AmendmentList(CollectionStructure):
    document_type = "amendmentList"


class Bill(HierarchicalStructure):
    document_type = "bill"


class Collection(CollectionStructure):
    document_type = "collection"


class DebateRecord(DebateStructure):
    document_type = "debateRecord"


class DebateReport(OpenStructure):
    document_type = "debateReport"


class Document(OpenStructure):
    document_type = "document"


class Judgment(JudgmentStructure):
    document_type = "judgment"


class Portion(PortionStructure):
    document_type = "portion"


class Statement(OpenStructure):
    document_type = "statement"

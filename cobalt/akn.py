"""
Cobalt's class hierarchy mimics that of the Akoma Ntoso standard. There is a primary root class for
all Akoma Ntoso documents. There are subclasses for each of the Akoma Ntoso document structure types,
such as hierarchicalStructure, debateStructure, etc. Finally, there is a class for each Akoma Ntoso
document type (act, bill, judgment, etc.) that extends the corresponding structure type.
"""
from collections import OrderedDict

import re
from lxml import etree
from lxml import objectify
from iso8601 import parse_date

from .uri import FrbrUri


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

    def __init__(self, xml):
        super().__init__(xml)

        # make, eg. ".act" an alias for ".main"
        setattr(self, self.document_type, self.main)

        # make, eg. ".body" an alias for ".main_content"
        setattr(self, self.main_content_element, self.main_content)

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

    @property
    def main(self):
        """ Get the root document element.
        """
        return getattr(self.root, self.document_type)

    @property
    def main_content(self):
        """ Get the main content element of the document.
        """
        return getattr(self.main, self.main_content_element)

    @property
    def meta(self):
        """ Get the root document element.
        """
        return self.main.meta

    @property
    def title(self):
        """ Short title """
        return self.meta.identification.FRBRWork.FRBRalias.get('value')

    @title.setter
    def title(self, value):
        self.meta.identification.FRBRWork.FRBRalias.set('value', value)

    @property
    def work_date(self):
        """ Date from the FRBRWork element """
        return parse_date(self.meta.identification.FRBRWork.FRBRdate.get('date')).date()

    @work_date.setter
    def work_date(self, value):
        self.meta.identification.FRBRWork.FRBRdate.set('date', datestring(value))

    @property
    def expression_date(self):
        """ Date from the FRBRExpression element """
        return parse_date(self.meta.identification.FRBRExpression.FRBRdate.get('date')).date()

    @expression_date.setter
    def expression_date(self, value):
        self.meta.identification.FRBRExpression.FRBRdate.set('date', datestring(value))
        # update the URI
        self.frbr_uri = self.frbr_uri

    @property
    def manifestation_date(self):
        """ Date from the FRBRManifestation element """
        return parse_date(self.meta.identification.FRBRManifestation.FRBRdate.get('date')).date()

    @manifestation_date.setter
    def manifestation_date(self, value):
        self.meta.identification.FRBRManifestation.FRBRdate.set('date', datestring(value))

    @property
    def language(self):
        """ The 3-letter ISO-639-2 language code of this document """
        return self.meta.identification.FRBRExpression.FRBRlanguage.get('language', 'eng')

    @language.setter
    def language(self, value):
        self.meta.identification.FRBRExpression.FRBRlanguage.set('language', value)
        # update the URI
        self.frbr_uri = self.frbr_uri

    @property
    def frbr_uri(self):
        """ The FRBR Work URI as a :class:`FrbrUri` instance that uniquely identifies this document universally. """
        uri = self.meta.identification.FRBRExpression.FRBRuri.get('value')
        if uri:
            return FrbrUri.parse(uri)
        else:
            return FrbrUri.empty()

    @frbr_uri.setter
    def frbr_uri(self, uri):
        if not isinstance(uri, FrbrUri):
            uri = FrbrUri.parse(uri)

        uri.language = self.meta.identification.FRBRExpression.FRBRlanguage.get('language', 'eng')
        uri.expression_date = '@' + datestring(self.expression_date)

        if uri.work_component is None:
            uri.work_component = 'main'

        # set URIs of the main document and components
        for component, element in self.components().items():
            uri.work_component = component
            ident = element.find('.//{*}meta/{*}identification')

            ident.FRBRWork.FRBRuri.set('value', uri.uri())
            ident.FRBRWork.FRBRthis.set('value', uri.work_uri())
            ident.FRBRWork.FRBRcountry.set('value', uri.country)

            ident.FRBRExpression.FRBRuri.set('value', uri.expression_uri(False))
            ident.FRBRExpression.FRBRthis.set('value', uri.expression_uri())

            ident.FRBRManifestation.FRBRuri.set('value', uri.expression_uri(False))
            ident.FRBRManifestation.FRBRthis.set('value', uri.expression_uri())

    def expression_frbr_uri(self):
        """ The FRBR Expression URI as a :class:`FrbrUri` instance that uniquely identifies this document universally. """
        uri = self.meta.identification.FRBRExpression.FRBRuri.get('value')
        if uri:
            return FrbrUri.parse(uri)
        else:
            return FrbrUri.empty()

    @property
    def year(self):
        """ The year, derived from :data:`frbr_uri`. Read-only. """
        return self.frbr_uri.date.split("-", 1)[0]

    @property
    def number(self):
        """ The number, derived from :data:`frbr_uri`. Read-only. """
        return self.frbr_uri.number

    @property
    def nature(self):
        """ The nature of the document, such as an act, derived from :data:`frbr_uri`. Read-only. """
        return self.frbr_uri.doctype

    def components(self):
        """ Get an `OrderedDict` of component name to :class:`lxml.objectify.ObjectifiedElement`
        objects.
        """
        components = OrderedDict()
        components['main'] = self.main

        # components/schedules
        for doc in self.root.iterfind('./{*}components/{*}component/{*}doc'):
            name = doc.meta.identification.FRBRWork.FRBRthis.get('value').split('/')[-1]
            components[name] = doc

        return components

    def _ensure(self, name, after):
        """ Hack help to get an element if it exists, or create it if it doesn't.
        *name* is a dotted path from *self*, *after* is where to place the new
        element if it doesn't exist. """
        node = self._get(name)
        if node is None:
            # TODO: what if nodes in the path don't exist?
            node = self._make(name.split('.')[-1])
            after.addnext(node)

        return node

    def _ensure_lifecycle(self):
        try:
            after = self.meta.publication
        except AttributeError:
            after = self.meta.identification
        node = self._ensure('meta.lifecycle', after=after)

        if not node.get('source'):
            node.set('source', '#' + self.source[1])
            self._ensure_reference('TLCOrganization', self.source[0], self.source[1], self.source[2])

        return node

    def _ensure_reference(self, elem, name, id, href):
        references = self._ensure('meta.references', after=self._ensure_lifecycle())

        ref = references.find('./{*}%s[@id="%s"]' % (elem, id))
        if ref is None:
            ref = self._make(elem)
            ref.set('id', id)
            ref.set('href', href)
            ref.set('showAs', name)
            references.insert(0, ref)
        return ref

    def _make(self, elem):
        return getattr(self._maker, elem)()

    def _get(self, name, root=None):
        parts = name.split('.')
        node = root or self

        for p in parts:
            try:
                node = getattr(node, p)
            except AttributeError:
                return None
        return node


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

"""
Cobalt's class hierarchy mimics that of the Akoma Ntoso standard. There is a single root class for
all Akoma Ntoso documents. There are subclasses for each of the Akoma Ntoso document structure types,
such as hierarchicalStructure, debateStructure, etc. Finally, there is a class for each Akoma Ntoso
document type (act, bill, judgment, etc.) that extends the corresponding structure type.
"""
from collections import OrderedDict
import re
from datetime import date

from lxml import etree, objectify
from lxml.builder import ElementMaker
from iso8601 import parse_date

from .uri import FrbrUri


ENCODING_RE = re.compile(r'encoding="[\w-]+"')

DATE_FORMAT = "%Y-%m-%d"

AKN_NAMESPACES = {
    '2.0': 'http://www.akomantoso.org/2.0',
    '3.0': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0',
}
DEFAULT_VERSION = '3.0'

# a placeholder date that indicates a null date, used in the XML where a date is required by may not be known
NULL_DATE = '0001-01-01'


def datestring(value):
    """ Format a date as an XML-suitable string. If the date is None, uses NULL_DATE.
    """
    if value is None:
        return NULL_DATE
    elif isinstance(value, str):
        return value
    else:
        return "%04d-%02d-%02d" % (value.year, value.month, value.day)


def parsedate(value):
    """ Parse an XML date string into a real date. If the value is the NULL_DATE, returns None.
    """
    if value == NULL_DATE:
        return None
    return parse_date(value).date()


# Create a new objectify parser that doesn't remove blank text nodes
objectify_parser = etree.XMLParser()
objectify_parser.set_element_class_lookup(objectify.ObjectifyElementClassLookup())


def get_maker(version=DEFAULT_VERSION):
    ns = AKN_NAMESPACES[version]
    return ElementMaker(nsmap={None: ns}, namespace=ns)


class AkomaNtosoDocument:
    """ Base class for Akoma Ntoso documents.

    :ivar root: :class:`lxml.objectify.ObjectifiedElement` root of the XML document
    :ivar namespace: primary XML namespace
    """
    _parser = objectify_parser
    # the "source" attribute used on some elements where it is required.
    # contains: name, id, url
    source = ["cobalt", "cobalt", "https://github.com/laws-africa/cobalt"]

    def __init__(self, xml=None):
        # TODO: we can do this better
        encoding = ENCODING_RE.search(xml, 0, 200)
        if encoding:
            # lxml doesn't like unicode strings with an encoding element, so
            # change to bytes
            xml = xml.encode('utf-8')

        self.parse(xml)
        self.maker = objectify.ElementMaker(annotate=False, namespace=self.namespace, nsmap=self.root.nsmap)

    def parse(self, xml, document_type=None):
        """ Parse XML and ensure it's Akoma Ntoso with a known namespace. Raises ValueError on error.
        """
        self.root = objectify.fromstring(xml, parser=self._parser)

        # ensure the root element is correct
        name = self.root.tag.split('}', 1)[-1]
        if name != 'akomaNtoso':
            raise ValueError(f"XML root element must be akomaNtoso, but got {name} instead")

        self.namespace = self.get_namespace()

    def to_xml(self, *args, encoding='utf-8', **kwargs):
        return etree.tostring(self.root, *args, encoding=encoding, **kwargs)

    def get_namespace(self):
        akn_namespaces = [ns[1] for ns in sorted(list(AKN_NAMESPACES.items()), reverse=True)]
        namespaces = list(self.root.nsmap.values())
        for ns in akn_namespaces:
            if ns in namespaces:
                return ns

        raise ValueError(f"Expected to find one of the following Akoma Ntoso XML namespaces: {', '.join(akn_namespaces)}. Only these namespaces were found: {', '.join(namespaces)}")

    def ensure_element(self, name, after, at=None, attribs=None):
        """ Helper to get an element if it exists, or create it if it doesn't.

        :param name: dotted path from `self` or `at`
        :param after: element after which to place the new element if it doesn't exist
        :param at: element at which to start looking, (defaults to self if None)
        """
        node = self.get_element(name, root=at)
        if node is None:
            # TODO: what if nodes in the path don't exist?
            node = self.make_element(name.split('.')[-1], attribs)
            after.addnext(node)

        return node

    def get_element(self, name, root=None):
        """ Lookup a dotted-path element, start at root (or self if root is None). Returns None if the element doesn't exist.
        """
        parts = name.split('.')
        # this avoids an lxml warning about testing against None
        if root is not None:
            node = root
        else:
            node = self

        for p in parts:
            try:
                node = getattr(node, p)
            except AttributeError:
                return None
        return node

    def make_element(self, elem, attribs=None):
        attribs = attribs or {}
        return getattr(self.maker, elem)(**attribs)


class StructuredDocument(AkomaNtosoDocument):
    """ Common base class for AKN documents with a known document structure.
    """

    structure_type = None
    """ The name of this document's structural type.
    """

    main_content_tag = None
    """ The name of the structural type's main content element.
    """

    document_type = None
    """ The name of the document type, corresponding to the primary document XML element.
    """

    non_eid_portions = "arguments background conclusions decision header introduction motivation preamble" \
                       " preface remedies".split()
    """ Portion names that are valid portions, but don't have eids, for use with get_portion_element.
    """

    @classmethod
    def for_document_type(cls, document_type):
        """ Return the subclass for this document type.
        """
        def check_subclasses(klass):
            for k in klass.__subclasses__():
                if k.document_type and k.document_type.lower() == document_type:
                    return k
                # recurse
                x = check_subclasses(k)
                if x:
                    return x

        document_type = document_type.lower()
        return check_subclasses(cls)

    @classmethod
    def empty_document(cls, version=DEFAULT_VERSION):
        """ Return XML for an empty document of this type, using the given AKN version.
        """
        today = datestring(date.today())
        frbr_uri = FrbrUri(
            country='za',
            locality=None,
            doctype=cls.document_type,
            subtype=None,
            date=today,
            number='1',
            work_component='main',
            language='eng',
            actor=None,
            prefix=('' if version == '2.0' else 'akn'),
        )

        maker = get_maker(version)
        content = cls.empty_document_content(maker)
        attrs = cls.empty_document_attrs()

        doc = maker.akomaNtoso(
            maker(cls.document_type,
                  cls.empty_meta(frbr_uri, maker=maker, for_root=True),
                  content,
                  **attrs)
        )
        return etree.tostring(doc, encoding='unicode')

    @classmethod
    def empty_meta(cls, frbr_uri, version=DEFAULT_VERSION, maker=None, for_root=True):
        """ Create a meta element for an frbr_uri, using the provided version or element maker.
        """
        today = datestring(date.today())
        maker = maker or get_maker(version)

        if for_root:
            # only generate top-level references if this is the root document
            refs = [maker.references(
                maker.TLCOrganization(eId=cls.source[1], href=cls.source[2], showAs=cls.source[0]),
                source=f"#{cls.source[1]}"
            )]
        else:
            refs = []

        return maker.meta(
            maker.identification(
                maker.FRBRWork(
                    maker.FRBRthis(value=frbr_uri.work_uri()),
                    maker.FRBRuri(value=frbr_uri.work_uri(work_component=False)),
                    maker.FRBRalias(value="Untitled", name="title"),
                    maker.FRBRdate(date=frbr_uri.date, name="Generation"),
                    maker.FRBRauthor(href=""),
                    maker.FRBRcountry(value=frbr_uri.place),
                    maker.FRBRnumber(value=frbr_uri.number),
                ),
                maker.FRBRExpression(
                    maker.FRBRthis(value=frbr_uri.expression_uri()),
                    maker.FRBRuri(value=frbr_uri.expression_uri(work_component=False)),
                    maker.FRBRdate(date=today, name="Generation"),
                    maker.FRBRauthor(href=""),
                    maker.FRBRlanguage(language=frbr_uri.language),
                ),
                maker.FRBRManifestation(
                    maker.FRBRthis(value=frbr_uri.manifestation_uri()),
                    maker.FRBRuri(value=frbr_uri.manifestation_uri(work_component=False)),
                    maker.FRBRdate(date=today, name="Generation"),
                    maker.FRBRauthor(href=""),
                ),
                source=f"#{cls.source[1]}"
            ),
            *refs
        )

    @classmethod
    def empty_document_content(cls, maker):
        return maker(cls.main_content_tag)

    @classmethod
    def empty_document_attrs(cls):
        return {'name': cls.document_type.lower()}

    def __init__(self, xml=None):
        """ Setup a new instance with the string in `xml`, or an empty document if the XML is not given.
        """
        if not xml:
            # use an empty document
            xml = self.empty_document()
        super().__init__(xml)

        # make, eg. ".act" an alias for ".main"
        setattr(self, self.document_type, self.main)

        # make, eg. ".body" an alias for ".main_content"
        setattr(self, self.main_content_tag, self.main_content)

    def parse(self, xml, document_type=None):
        """ Parse XML and ensure it's Akoma Ntoso.
        Raises ValueError on error. Returns the root element.
        """
        super().parse(xml, document_type)

        doc_root = self.root.find(f'./{{{self.namespace}}}{self.document_type}')
        if doc_root is None:
            raise ValueError(f"Expected {self.document_type} as a child of root element")

    @property
    def main(self):
        """ Get the main document element (normally the first child of the root element).
        """
        return getattr(self.root, self.document_type)

    @property
    def main_content(self):
        """ Get the main content element of the document.
        """
        return getattr(self.main, self.main_content_tag)

    @property
    def meta(self):
        """ Get the meta element of the document.
        """
        return self.main.meta

    @property
    def title(self):
        """ Short title """
        # look for the FRBRalias element with name="title", falling back to any alias
        title = None
        for alias in self.meta.identification.FRBRWork.iterchildren(f'{{{self.namespace}}}FRBRalias'):
            if alias.get('name') == 'title':
                return alias.get('value')
            title = alias.get('value')
        return title

    @title.setter
    def title(self, value):
        # set the title on an alias attribute with name="title"
        aliases = self.meta.identification.FRBRWork.xpath('a:FRBRalias[@name="title"]', namespaces={'a': self.namespace})
        if not aliases:
            alias = self.ensure_element('meta.identification.FRBRWork.FRBRalias', self.meta.identification.FRBRWork.FRBRuri)
            alias.set('name', 'title')
            aliases = [alias]
        aliases[0].set('value', value)

    @property
    def work_date(self):
        """ Date from the FRBRWork element. Normally, this date must match the date portion of the work's FRBR URI.
        However, since that may be a partial date (such as just a year), this return value may be different to the
        date string stored in the FRBRdate element. In particular, if the date is just a year, the month and day
        both default to 1.
        """
        return parse_date(self.meta.identification.FRBRWork.FRBRdate.get('date')).date()

    @property
    def expression_date(self):
        """ Date from the FRBRExpression element """
        return parse_date(self.meta.identification.FRBRExpression.FRBRdate.get('date')).date()

    @expression_date.setter
    def expression_date(self, value):
        self.meta.identification.FRBRExpression.FRBRdate.set('date', datestring(value))
        # set expression date of the components
        for component, element in list(self.components().items())[1:]:
            element.doc.meta.identification.FRBRExpression.FRBRdate.set('date', datestring(value))

        # update the URI
        self.frbr_uri = self.frbr_uri

    @property
    def manifestation_date(self):
        """ Date from the FRBRManifestation element """
        return parse_date(self.meta.identification.FRBRManifestation.FRBRdate.get('date')).date()

    @manifestation_date.setter
    def manifestation_date(self, value):
        self.meta.identification.FRBRManifestation.FRBRdate.set('date', datestring(value))
        # set expression date of the components
        for component, element in list(self.components().items())[1:]:
            element.doc.meta.identification.FRBRManifestation.FRBRdate.set('date', datestring(value))

    @property
    def language(self):
        """ The 3-letter ISO-639-2 language code of this document.
        """
        return self.meta.identification.FRBRExpression.FRBRlanguage.get('language', 'eng')

    @language.setter
    def language(self, value):
        self.meta.identification.FRBRExpression.FRBRlanguage.set('language', value)
        # update the URI
        self.frbr_uri = self.frbr_uri

    @property
    def frbr_uri(self):
        """ The FRBR Manifestation URI as a :class:`cobalt.uri.FrbrUri` instance that uniquely identifies this document universally.
        """
        uri = self.meta.identification.FRBRManifestation.FRBRuri.get('value')
        if uri:
            return FrbrUri.parse(uri)

    @frbr_uri.setter
    def frbr_uri(self, uri):
        if not isinstance(uri, FrbrUri):
            uri = FrbrUri.parse(uri)

        uri.language = self.meta.identification.FRBRExpression.FRBRlanguage.get('language', 'eng')
        uri.expression_date = '@' + datestring(self.expression_date)
        work_component = uri.work_component or 'main'

        # set URIs of the main document and components
        for component, element in self.components().items():
            uri.work_component = component or work_component
            ident = element.find(f'.//{{{self.namespace}}}meta/{{{self.namespace}}}identification')

            ident.FRBRWork.FRBRuri.set('value', uri.uri())
            ident.FRBRWork.FRBRthis.set('value', uri.work_uri())
            ident.FRBRWork.FRBRcountry.set('value', uri.place)
            ident.FRBRWork.FRBRdate.set('date', uri.date)

            if uri.subtype:
                self.ensure_element('FRBRsubtype', at=ident.FRBRWork, after=ident.FRBRWork.FRBRcountry).set('value', uri.subtype)
                after = ident.FRBRWork.FRBRsubtype
            else:
                after = ident.FRBRWork.FRBRcountry
                try:
                    # remove existing subtype
                    ident.FRBRWork.remove(ident.FRBRWork.FRBRsubtype)
                except AttributeError:
                    pass

            # this must come after subtype if it exists, otherwise country
            self.ensure_element('FRBRnumber', at=ident.FRBRWork, after=after).set('value', uri.number)

            ident.FRBRExpression.FRBRuri.set('value', uri.expression_uri(False))
            ident.FRBRExpression.FRBRthis.set('value', uri.expression_uri())
            ident.FRBRExpression.FRBRlanguage.set('language', uri.language)

            ident.FRBRManifestation.FRBRuri.set('value', uri.expression_uri(False))
            ident.FRBRManifestation.FRBRthis.set('value', uri.expression_uri())

    def expression_frbr_uri(self):
        """ The FRBR Expression URI as a :class:`cobalt.uri.FrbrUri` instance that uniquely identifies this document
        universally.
        """
        uri = self.meta.identification.FRBRExpression.FRBRuri.get('value')
        if uri:
            return FrbrUri.parse(uri)
        else:
            return FrbrUri.empty()

    def components(self):
        """ Get an `OrderedDict` of component name to :class:`lxml.objectify.ObjectifiedElement`
        objects. Components are this document, and `<component>` and `<attachment>` elements inside this document.
        """
        components = OrderedDict()
        frbr_uri = FrbrUri.parse(self.meta.identification.FRBRWork.FRBRthis.get('value'))
        components[frbr_uri.work_component] = self.main

        xpath = './a:attachments/a:attachment/a:*/a:meta | ./a:components/a:component/a:*/a:meta'
        for meta in self.main.xpath(xpath, namespaces={'a': self.namespace}):
            frbr_uri = FrbrUri.parse(meta.identification.FRBRWork.FRBRthis.get('value'))
            name = frbr_uri.work_component
            components[name] = meta.getparent().getparent()

        return components

    def get_portion_element(self, portion, component=None):
        """ Get a single portion of this document. The `portion` is usually an eId, as specified by
        https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html#_Toc531692279.

        The optional `component` is the ancestor element within which to look for the portion.

        Range portions (eg. `chp_1->chp_3`) are not supported by this function.
        """
        root = component or self.root

        if portion in self.non_eid_portions:
            # these are valid portions that don't have eids
            xpath = f'.//a:{portion}'
        else:
            portion = portion.replace('"', '')
            xpath = f'.//a:*[@eId="{portion}"]'

        for x in root.xpath(xpath, namespaces={'a': self.namespace}):
            return x

    def _ensure_lifecycle(self):
        try:
            after = self.meta.publication
        except AttributeError:
            after = self.meta.identification
        node = self.ensure_element('meta.lifecycle', after=after)

        if not node.get('source'):
            node.set('source', '#' + self.source[1])
            self._ensure_reference('TLCOrganization', self.source[0], self.source[1], self.source[2])

        return node

    def _ensure_reference(self, elem, name, id, href):
        references = self.ensure_element('meta.references', after=self._ensure_lifecycle())

        ref = references.find(f'./{{{self.namespace}}}{elem}[@eId="{id}"]')
        if ref is None:
            ref = self.make_element(elem)
            ref.set('eId', id)
            ref.set('href', href)
            ref.set('showAs', name)
            references.insert(0, ref)
        return ref

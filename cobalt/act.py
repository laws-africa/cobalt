import re
from collections import OrderedDict

from lxml import objectify
from lxml import etree
import arrow

from .uri import FrbrUri
from .toc import TOCBuilder


ENCODING_RE = re.compile('encoding="[\w-]+"')

DATE_FORMAT = "%Y-%m-%d"


def datestring(value):
    if value is None:
        return ""
    elif isinstance(value, basestring):
        return value
    else:
        return "%04d-%02d-%02d" % (value.year, value.month, value.day)


class Base(object):
    def __init__(self, xml=None):
        encoding = ENCODING_RE.search(xml, 0, 200)
        if encoding:
            # lxml doesn't like unicode strings with an encoding element, so
            # change to bytes
            xml = xml.encode('utf-8')

        self.root = objectify.fromstring(xml)
        self.namespace = self.root.nsmap[None]

        self._maker = objectify.ElementMaker(annotate=False, namespace=self.namespace, nsmap=self.root.nsmap)
        # the "source" attribute used on some elements where it is required.
        # contains: name, id, url
        self.source = ["cobalt", "cobalt", "https://github.com/Code4SA/cobalt"]

    def to_xml(self):
        return etree.tostring(self.root, encoding='utf-8', pretty_print=True)


class Fragment(Base):
    pass


class Act(Base):
    """
    An act is a lightweight wrapper around an `Akoma Ntoso 2.0 XML <http://www.akomantoso.org/>`_ act document.
    It provides methods to help access and manipulate the underlying XML directly, in particular
    the metadata for the document.

    The Act object provides quick access to certain sections of the document:

    :ivar root: :class:`lxml.objectify.ObjectifiedElement` root of the XML document
    :ivar meta: :class:`lxml.objectify.ObjectifiedElement` meta element
    :ivar body: :class:`lxml.objectify.ObjectifiedElement` body element

    .. seealso::
        http://www.akomantoso.org/docs/akoma-ntoso-user-documentation/metadata-describes-the-content
    """

    def __init__(self, xml=None):
        """ Setup a new instance with the string in `xml`. """
        if not xml:
            # use an empty document
            xml = EMPTY_DOCUMENT
        super(Act, self).__init__(xml)

        self.act = self.root.act
        self.meta = self.act.meta
        self.body = self.act.body

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
        return arrow.get(self.meta.identification.FRBRWork.FRBRdate.get('date')).date()

    @work_date.setter
    def work_date(self, value):
        self.meta.identification.FRBRWork.FRBRdate.set('date', datestring(value))

    @property
    def expression_date(self):
        """ Date from the FRBRExpression element """
        return arrow.get(self.meta.identification.FRBRExpression.FRBRdate.get('date')).date()

    @expression_date.setter
    def expression_date(self, value):
        self.meta.identification.FRBRExpression.FRBRdate.set('date', datestring(value))
        # update the URI
        self.frbr_uri = self.frbr_uri

    @property
    def manifestation_date(self):
        """ Date from the FRBRManifestation element """
        return arrow.get(self.meta.identification.FRBRManifestation.FRBRdate.get('date')).date()

    @manifestation_date.setter
    def manifestation_date(self, value):
        self.meta.identification.FRBRManifestation.FRBRdate.set('date', datestring(value))

    @property
    def publication_name(self):
        """ Name of the publication in which this act was published """
        pub = self._get('meta.publication')
        return pub.get('name') if pub is not None else None

    @publication_name.setter
    def publication_name(self, value):
        value = value or ""
        pub = self._ensure('meta.publication', after=self.meta.identification)
        pub.set('name', value)
        pub.set('showAs', value)

    @property
    def publication_date(self):
        """ Date of the publication """
        pub = self._get('meta.publication')
        if pub is not None and pub.get('date'):
            return arrow.get(pub.get('date')).date()
        return None

    @publication_date.setter
    def publication_date(self, value):
        self._ensure('meta.publication', after=self.meta.identification)\
            .set('date', datestring(value))

    @property
    def publication_number(self):
        """ Sequence number of the publication """
        pub = self._get('meta.publication')
        return pub.get('number') if pub is not None else None

    @publication_number.setter
    def publication_number(self, value):
        self._ensure('meta.publication', after=self.meta.identification)\
            .set('number', value or "")

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
        uri = self.meta.identification.FRBRWork.FRBRuri.get('value')
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
        for component, element in self.components().iteritems():
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
        """ The act year, derived from :data:`frbr_uri`. Read-only. """
        return self.frbr_uri.date.split("-", 1)[0]

    @property
    def number(self):
        """ The act number, derived from :data:`frbr_uri`. Read-only. """
        return self.frbr_uri.number

    @property
    def nature(self):
        """ The nature of the document, such as an act, derived from :data:`frbr_uri`. Read-only. """
        return self.frbr_uri.doctype

    @property
    def body_xml(self):
        """ The raw XML string of the `body` element of the document. When
        setting this property, XML must be rooted at a `body` element. """
        return etree.tostring(self.body, pretty_print=True)

    @body_xml.setter
    def body_xml(self, xml):
        new_body = objectify.fromstring(xml or EMPTY_BODY)
        new_body.tag = 'body'
        self.body.getparent().replace(self.body, new_body)
        self.body = new_body

    @property
    def amendments(self):
        amendments = []

        for e in self.meta.iterfind('.//{*}lifecycle/{*}eventRef[@type="amendment"]'):
            date = arrow.get(e.get('date')).date()
            event = AmendmentEvent(date=date)
            amendments.append(event)

            id = e.get('source')[1:]
            source = self.meta.findall('.//{*}references/{*}passiveRef[@id="%s"]' % id)
            if source:
                event.amending_title = source[0].get('showAs')
                event.amending_uri = source[0].get('href')

        amendments.sort(key=lambda a: a.date)
        return amendments

    @amendments.setter
    def amendments(self, value):
        # delete existing entries
        for e in self.meta.iterfind('.//{*}lifecycle/{*}eventRef[@type="amendment"]'):
            # delete the passive ref elements
            id = e.get('source')[1:]
            for node in self.meta.iterfind('.//{*}references/{*}passiveRef[@id="%s"]' % id):
                node.getparent().remove(node)

            # delete the event
            e.getparent().remove(e)

        if not value:
            # no amendments
            self.act.set('contains', 'originalVersion')
        else:
            self.act.set('contains', 'singleVersion')
            lifecycle = self._ensure_lifecycle()
            references = self._ensure('meta.references', after=lifecycle)

            for i, event in enumerate(value):
                date = datestring(event.date)
                ref = 'amendment-%s-source' % i

                # create the lifecycle element
                node = self._make('eventRef')
                node.set('id', 'amendment-' + date)
                node.set('date', date)
                node.set('type', 'amendment')
                node.set('source', '#' + ref)
                lifecycle.append(node)

                # create the passive ref
                node = self._make('passiveRef')
                node.set('id', ref)
                node.set('href', event.amending_uri)
                node.set('showAs', event.amending_title)
                references.append(node)

    @property
    def repeal(self):
        e = self.meta.find('.//{*}lifecycle/{*}eventRef[@type="repeal"]')
        if e is not None:
            date = arrow.get(e.get('date')).date()
            event = RepealEvent(date=date)

            id = e.get('source')[1:]
            source = self.meta.findall('.//{*}references/{*}passiveRef[@id="%s"]' % id)
            if source:
                event.repealing_title = source[0].get('showAs')
                event.repealing_uri = source[0].get('href')
            return event

    @repeal.setter
    def repeal(self, value):
        # delete existing entries
        for e in self.meta.iterfind('.//{*}lifecycle/{*}eventRef[@type="repeal"]'):
            # delete the passive ref elements
            id = e.get('source')[1:]
            for node in self.meta.iterfind('.//{*}references/{*}passiveRef[@id="%s"]' % id):
                node.getparent().remove(node)

            # delete the event
            e.getparent().remove(e)

        if value:
            lifecycle = self._ensure_lifecycle()
            references = self._ensure('meta.references', after=lifecycle)

            date = datestring(value.date)
            ref = 'repeal-source'

            # create the lifecycle element
            node = self._make('eventRef')
            node.set('id', 'repeal-' + date)
            node.set('date', date)
            node.set('type', 'repeal')
            node.set('source', '#' + ref)
            lifecycle.append(node)

            # create the passive ref
            node = self._make('passiveRef')
            node.set('id', ref)
            node.set('href', value.repealing_uri)
            node.set('showAs', value.repealing_title)
            references.append(node)

    def components(self):
        """ Get an `OrderedDict` of component name to :class:`lxml.objectify.ObjectifiedElement`
        objects.
        """
        components = OrderedDict()
        components['main'] = self.act

        # components/schedules
        for doc in self.root.iterfind('./{*}components/{*}component/{*}doc'):
            name = doc.meta.identification.FRBRWork.FRBRthis.get('value').split('/')[-1]
            components[name] = doc

        return components

    def table_of_contents(self, builder=None):
        """ Get the table of contents of this document as a list of :class:`cobalt.toc.TOCElement` instances. """
        builder = builder or TOCBuilder()
        return builder.table_of_contents(self)

    def get_subcomponent(self, component, subcomponent):
        """ Get the named subcomponent in this document, such as `chapter/2` or 'section/13A'.
        :class:`lxml.objectify.ObjectifiedElement` or `None`.
        """
        def search_toc(items):
            for item in items:
                if item.component == component and item.subcomponent == subcomponent:
                    return item.element

                if item.children:
                    found = search_toc(item.children)
                    if found:
                        return found

        return search_toc(self.table_of_contents())

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


class AmendmentEvent(object):
    """ An event that amended a document.

    :ivar date: :class:`datetime.date` date of the event
    :ivar amending_title: String title of the amending document
    :ivar amending_uri: String form of the FRBR URI of the amending document
    """
    def __init__(self, date=None, amending_title=None, amending_uri=None):
        self.date = date
        self.amending_title = amending_title
        self.amending_uri = amending_uri


class RepealEvent(object):
    """ An event that repealed a document.

    :ivar date: :class:`datetime.date` date of the event
    :ivar repealing_title: String title of the repealing document
    :ivar repealing_uri: String form of the FRBR URI of the repealing document
    """
    def __init__(self, date=None, repealing_title=None, repealing_uri=None):
        self.date = date
        self.repealing_title = repealing_title
        self.repealing_uri = repealing_uri


EMPTY_DOCUMENT = """<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="originalVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/za/act/1900/1/main"/>
          <FRBRuri value="/za/act/1900/1"/>
          <FRBRalias value="Untitled"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/za/act/1900/1/eng@/main"/>
          <FRBRuri value="/za/act/1900/1/eng@"/>
          <FRBRdate date="1900-01-01" name="Generation"/>
          <FRBRauthor href="#council" as="#author"/>
        </FRBRManifestation>
      </identification>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/Code4SA/cobalt" showAs="cobalt"/>
      </references>
    </meta>
    <body>
      <section id="section-1">
        <content>
          <p></p>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
"""

EMPTY_BODY = """
<body>
  <section id="section-1">
    <content>
      <p></p>
    </content>
  </section>
</body>
"""

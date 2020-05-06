from iso8601 import parse_date

from .akn import StructuredDocument, datestring


class HierarchicalStructure(StructuredDocument):
    structure_type = "hierarchicalStructure"
    main_content_tag = "body"


class Act(HierarchicalStructure):
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
    document_type = "act"

    @property
    def publication_name(self):
        """ Name of the publication in which this act was published """
        pub = self.get_element('meta.publication')
        return pub.get('name') if pub is not None else None

    @publication_name.setter
    def publication_name(self, value):
        value = value or ""
        pub = self.ensure_element('meta.publication', after=self.meta.identification)
        pub.set('name', value)
        pub.set('showAs', value)

    @property
    def publication_date(self):
        """ Date of the publication """
        pub = self.get_element('meta.publication')
        if pub is not None and pub.get('date'):
            return parse_date(pub.get('date')).date()
        return None

    @publication_date.setter
    def publication_date(self, value):
        self.ensure_element('meta.publication', after=self.meta.identification)\
            .set('date', datestring(value))

    @property
    def publication_number(self):
        """ Sequence number of the publication """
        pub = self.get_element('meta.publication')
        return pub.get('number') if pub is not None else None

    @publication_number.setter
    def publication_number(self, value):
        self.ensure_element('meta.publication', after=self.meta.identification)\
            .set('number', value or "")

    @property
    def amendments(self):
        amendments = []

        for e in self.meta.iterfind(f'.//{{{self.namespace}}}lifecycle/{{{self.namespace}}}eventRef[@type="amendment"]'):
            date = parse_date(e.get('date')).date()
            event = AmendmentEvent(date=date)
            amendments.append(event)

            id = e.get('source')[1:]
            source = self.meta.findall(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@id="{id}"]')
            if source:
                event.amending_title = source[0].get('showAs')
                event.amending_uri = source[0].get('href')

        amendments.sort(key=lambda a: a.date)
        return amendments

    @amendments.setter
    def amendments(self, value):
        # delete existing entries
        for e in self.meta.iterfind(f'.//{{{self.namespace}}}lifecycle/{{{self.namespace}}}eventRef[@type="amendment"]'):
            # delete the passive ref elements
            id = e.get('source')[1:]
            for node in self.meta.iterfind(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@id="{id}"]'):
                node.getparent().remove(node)

            # delete the event
            e.getparent().remove(e)

        if not value:
            # no amendments
            self.act.set('contains', 'originalVersion')
        else:
            self.act.set('contains', 'singleVersion')
            lifecycle = self._ensure_lifecycle()
            references = self.ensure_element('meta.references', after=lifecycle)

            for i, event in enumerate(value):
                date = datestring(event.date)
                ref = f'amendment-{i}-source'

                # create the lifecycle element
                node = self.make_element('eventRef')
                node.set('id', 'amendment-' + date)
                node.set('date', date)
                node.set('type', 'amendment')
                node.set('source', '#' + ref)
                lifecycle.append(node)

                # create the passive ref
                node = self.make_element('passiveRef')
                node.set('id', ref)
                node.set('href', event.amending_uri)
                node.set('showAs', event.amending_title)
                references.append(node)

    @property
    def repeal(self):
        e = self.meta.find(f'.//{{{self.namespace}}}lifecycle/{{{self.namespace}}}eventRef[@type="repeal"]')
        if e is not None:
            date = parse_date(e.get('date')).date()
            event = RepealEvent(date=date)

            id = e.get('source')[1:]
            source = self.meta.findall(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@id="{id}"]')
            if source:
                event.repealing_title = source[0].get('showAs')
                event.repealing_uri = source[0].get('href')
            return event

    @repeal.setter
    def repeal(self, value):
        # delete existing entries
        for e in self.meta.iterfind(f'.//{{{self.namespace}}}lifecycle/{{{self.namespace}}}eventRef[@type="repeal"]'):
            # delete the passive ref elements
            id = e.get('source')[1:]
            for node in self.meta.iterfind(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@id="{id}"]'):
                node.getparent().remove(node)

            # delete the event
            e.getparent().remove(e)

        if value:
            lifecycle = self._ensure_lifecycle()
            references = self.ensure_element('meta.references', after=lifecycle)

            date = datestring(value.date)
            ref = 'repeal-source'

            # create the lifecycle element
            node = self.make_element('eventRef')
            node.set('id', 'repeal-' + date)
            node.set('date', date)
            node.set('type', 'repeal')
            node.set('source', '#' + ref)
            lifecycle.append(node)

            # create the passive ref
            node = self.make_element('passiveRef')
            node.set('id', ref)
            node.set('href', value.repealing_uri)
            node.set('showAs', value.repealing_title)
            references.append(node)


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


class Bill(HierarchicalStructure):
    document_type = "bill"

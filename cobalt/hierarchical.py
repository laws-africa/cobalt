from .akn import StructuredDocument, datestring, NULL_DATE, parsedate


class HierarchicalStructure(StructuredDocument):
    structure_type = "hierarchicalStructure"
    main_content_tag = "body"


class Act(HierarchicalStructure):
    """
    An Akoma Ntoso Act document.
    """
    document_type = "act"

    @classmethod
    def empty_document_content(cls, E):
        return E('body',
                 E('section',
                   E('content',
                     E('p', eId="sec_nn_1__p_1")),
                   eId="sec_nn_1")
                 )

    @property
    def publication_name(self):
        """ Name of the publication in which this act was published.
        """
        pub = self.get_element('meta.publication')
        return pub.get('name') if pub is not None else None

    @publication_name.setter
    def publication_name(self, value):
        value = value or ""
        pub = self.ensure_publication()
        pub.set('name', value)
        pub.set('showAs', value)

    @property
    def publication_date(self):
        """ Date of publication as a `datetime.date` object.
        """
        pub = self.get_element('meta.publication')
        if pub is not None and pub.get('date'):
            return parsedate(pub.get('date'))
        return None

    @publication_date.setter
    def publication_date(self, value):
        self.ensure_publication().set('date', datestring(value))

    @property
    def publication_number(self):
        """ Sequence number of the publication.
        """
        pub = self.get_element('meta.publication')
        return pub.get('number') if pub is not None else None

    @publication_number.setter
    def publication_number(self, value):
        self.ensure_publication().set('number', value or "")

    @property
    def amendments(self):
        amendments = []

        for e in self.meta.iterfind(f'.//{{{self.namespace}}}lifecycle/{{{self.namespace}}}eventRef[@type="amendment"]'):
            date = parsedate(e.get('date'))
            event = AmendmentEvent(date=date)
            amendments.append(event)

            eid = e.get('source')[1:]
            source = self.meta.findall(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@eId="{eid}"]')
            if source:
                event.amending_title = source[0].get('showAs')
                event.amending_uri = source[0].get('href')

        amendments.sort(key=lambda a: a.date)
        return amendments

    @amendments.setter
    def amendments(self, value):
        # delete existing entries
        lifecycle = self.meta.find(f'{{{self.namespace}}}lifecycle')
        if lifecycle is not None:
            for e in lifecycle.findall(f'./{{{self.namespace}}}eventRef[@type="amendment"]'):
                # delete the passive ref elements
                eid = e.get('source')[1:]
                for node in self.meta.iterfind(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@eId="{eid}"]'):
                    node.getparent().remove(node)
                # delete the event
                lifecycle.remove(e)

        if not value:
            # no amendments, default is originalVersion so it doesn't need to be set explicitly
            if 'contains' in self.act.attrib:
                del self.act.attrib['contains']
            # lifecycle cannot be empty§
            if lifecycle is not None and not lifecycle.getchildren():
                lifecycle.getparent().remove(lifecycle)

        else:
            self.act.set('contains', 'singleVersion')
            lifecycle = self._ensure_lifecycle()
            references = self.ensure_element('meta.references', after=lifecycle)
            if not references.get('source'):
                references.set('source', '#' + self.source[1])

            for i, event in enumerate(value):
                date = datestring(event.date)
                ref = f'amendment-{i}-source'

                # create the lifecycle element
                node = self.make_element('eventRef')
                node.set('eId', 'amendment-' + date)
                node.set('date', date)
                node.set('type', 'amendment')
                node.set('source', '#' + ref)
                lifecycle.append(node)

                # create the passive ref
                node = self.make_element('passiveRef')
                node.set('eId', ref)
                node.set('href', event.amending_uri)
                node.set('showAs', event.amending_title)
                references.append(node)

    @property
    def repeal(self):
        e = self.meta.find(f'.//{{{self.namespace}}}lifecycle/{{{self.namespace}}}eventRef[@type="repeal"]')
        if e is not None:
            date = parsedate(e.get('date'))
            event = RepealEvent(date=date)

            id = e.get('source')[1:]
            source = self.meta.findall(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@eId="{id}"]')
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
            for node in self.meta.iterfind(f'.//{{{self.namespace}}}references/{{{self.namespace}}}passiveRef[@eId="{id}"]'):
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
            node.set('eId', 'repeal-' + date)
            node.set('date', date)
            node.set('type', 'repeal')
            node.set('source', '#' + ref)
            lifecycle.append(node)

            # create the passive ref
            node = self.make_element('passiveRef')
            node.set('eId', ref)
            node.set('href', value.repealing_uri)
            node.set('showAs', value.repealing_title)
            references.append(node)
        else:
            try:
                if len(list(self.meta.lifecycle.iterchildren())) == 0:
                    # remove empty lifecycle
                    self.meta.remove(self.meta.lifecycle)
            except AttributeError:
                pass

    def ensure_publication(self):
        return self.ensure_element('meta.publication', after=self.meta.identification,
                                   attribs={'showAs': '', 'name': '', 'date': NULL_DATE})


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
    """
    An Akoma Ntoso Bill document.
    """
    document_type = "bill"

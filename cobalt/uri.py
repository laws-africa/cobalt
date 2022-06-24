import re

FRBR_URI_RE = re.compile(r"""^(/(?P<prefix>akn))?            # optional 'akn' prefix
                              /(?P<country>[a-z]{2})         # country
                              (-(?P<locality>[^/]+))?        # locality code
                              /(?P<doctype>[^/]+)            # document type
                              (/(?P<subtype>[^0-9][^/]*))?   # subtype (optional, cannot start with a number)
                              (/(?P<actor>[^0-9][^/]*))?     # actor (optional), cannot start with a number
                              /(?P<date>[0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?)  # date
                              /(?P<number>[^/]+)             # number
                              (/                             # optional expression language and date
                                  (?P<language>[a-z]{3})                    # language (eg. eng)
                                  (?P<expression_date>[@:][^/]*)?           # expression date (eg. @ or @2012-12-22 or :2012-12-22)
                              )?
                              (/
                                  (!(?P<work_component>[^~.]+?))?           # optional component (eg. !main or !schedule1)
                                  (~(?P<portion>[^.]+))?                    # optional portion
                              )?
                              (\.(?P<format>[a-z0-9]+))?     # optional format (eg. .xml, .akn, .html, .pdf)
                              $""", re.X)


class FrbrUri(object):
    """
    An object for working with
    `Akoma Ntoso 3.0 FRBR URIs <https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/os/akn-nc-v1.0-os.html>`_ (IRIs).

    URIs can be parsed from a plain string using :meth:`parse` or they can be
    constructed directly. URIs can be manipulated in-place once constructed,
    which is useful for turning a work-level URI into an expression or
    manifestation URI.

    URIs can be transformed back to the string form of work, expression and
    manifestation URIs using the :meth:`work_uri`, :meth:`expression_uri` and
    :meth:`manifestation_uri` methods.

    Example::

        >>> uri = FrbrUri.parse('/akn/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/!main~part_1.xml')
        >>> uri.prefix
        'akn'
        >>> uri.country
        'za'
        >>> uri.locality
        'jhb'
        >>> uri.doctype
        'act'
        >>> uri.subtype
        'by-law'
        >>> uri.date
        '2003'
        >>> uri.number
        'public-health'
        >>> uri.language
        'eng'
        >>> uri.expression_date
        ':2015-01-01'
        >>> uri.work_component
        'main'
        >>> uri.portion
        'part_1'
        >>> uri.format
        'xml'
        >>> uri.work_uri()
        '/za-jhb/act/by-law/2003/public-health'
        >>> uri.expression_uri()
        '/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/!main~part_1'
        >>> uri.manifestation_uri()
        '/za-jhb/act/by-law/2003/public-health/eng:2015-01-01/!main~part_1.xml'

    :ivar prefix: optional `akn` prefix
    :ivar country: two letter country code
    :ivar locality: locality within the country, may be None
    :ivar doctype: type of document (eg. ``act``)
    :ivar subtype: document subtype, may be None
    :ivar actor: emenating actor, may be None
    :ivar date: document data (str), YYYY[-MM[-DD]]
    :ivar number: document number (str)
    :ivar work_component: name of the work component, may be None
    :ivar language: three-letter expression language code, may be None
    :ivar expression_date: expression date (str), [@:]YYYY[-MM[-DD]], may be None
    :ivar format: format extension, may be None
    """

    default_language = 'eng'

    def __init__(self, country, locality, doctype, subtype, actor, date, number, work_component=None, language=None,
                 expression_date=None, format=None, portion=None, prefix="akn"):
        self.prefix = prefix
        self.country = country
        self.locality = locality
        self.doctype = doctype
        self.subtype = subtype
        self.actor = actor
        self.date = date
        self.number = number
        self.work_component = work_component
        self.portion = portion

        self.language = language or self.default_language
        self.expression_date = expression_date
        self.format = format

    def clone(self):
        """ Return a copy of this FrbrUri object.
        """
        return FrbrUri(
            prefix=self.prefix,
            country=self.country,
            locality=self.locality,
            doctype=self.doctype,
            subtype=self.subtype,
            actor=self.actor,
            date=self.date,
            number=self.number,
            work_component=self.work_component,
            language=self.language,
            expression_date=self.expression_date,
            portion=self.portion,
            format=self.format,
        )

    def uri(self):
        """ String form of the work URI, excluding the work component, if any. """
        return self.work_uri(work_component=False)

    def work_uri(self, work_component=True):
        """ String form of the work URI. """
        country = self.country
        parts = ['']
        if self.locality:
            country = country + "-" + self.locality

        if self.prefix:
            parts.append(self.prefix)

        parts += [country, self.doctype]

        if self.subtype:
            parts.append(self.subtype)
            if self.actor:
                parts.append(self.actor)

        parts += [self.date, self.number]

        if work_component and self.work_component:
            parts += ['!' + self.work_component]

        return '/'.join(parts)

    def expression_uri(self, work_component=True):
        """ String form of the expression URI. """
        if not self.language:
            raise ValueError("Expression URI requires a language.")

        uri = self.work_uri(work_component=False) + "/" + self.language

        if self.expression_date is not None:
            uri = uri + self.expression_date

        # if we have a work component, use it
        slashed = False
        if work_component and self.work_component:
            slashed = True
            uri = uri + "/!" + self.work_component

        if self.portion:
            if not slashed:
                uri = uri + "/"
            uri = uri + "~" + self.portion

        return uri

    def manifestation_uri(self, work_component=True):
        """ String form of the manifestation URI. """
        uri = self.expression_uri(work_component)
        if self.format:
            uri = uri + "." + self.format
        return uri

    def __str__(self):
        if self.format:
            return self.manifestation_uri()
        if self.expression_date or self.work_component:
            return self.expression_uri()
        return self.work_uri()

    def __repr__(self):
        return f'<FrbrUri({self})>'

    @classmethod
    def parse(cls, s):
        """ Parse a string into an FrbrUri instance.

        :raises ValueError: if parsing fails
        """
        s = s.rstrip('/')
        match = FRBR_URI_RE.match(s)
        if match:
            return cls(**match.groupdict())
        else:
            raise ValueError("Invalid FRBR URI: %s" % s)

    @property
    def year(self):
        """ The year, derived from :data:`date`. Read-only. """
        return self.date.split("-", 1)[0]

    @property
    def place(self):
        """ Full place code, including both country and locality (if present).
        """
        if self.locality:
            return self.country + "-" + self.locality
        return self.country

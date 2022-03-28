from unittest import TestCase
from nose.tools import *  # noqa
from datetime import date

from cobalt import Act, datestring
from cobalt.schemas import assert_validates


class StructuredDocumentTestCase(TestCase):
    # using Act to test StructuredDocument functionality
    # because we need a concrete document (with a default empty_document) to work with
    maxDiff = None

    def test_frbr_uri(self):
        a = Act()
        a.expression_date = '2012-01-01'
        a.frbr_uri = '/zm/act/2007/01'
        today = datestring(date.today())

        assert_equal(a.frbr_uri.work_uri(), '/zm/act/2007/01')

        assert_equal(a.meta.identification.FRBRWork.FRBRthis.get('value'), '/zm/act/2007/01/!main')
        assert_equal(a.meta.identification.FRBRWork.FRBRuri.get('value'), '/zm/act/2007/01')
        assert_equal(a.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm')
        assert_equal(a.meta.identification.FRBRWork.FRBRnumber.get('value'), '01')
        assert_equal(a.meta.identification.FRBRWork.FRBRdate.get('date'), '2007')

        assert_equal(a.meta.identification.FRBRExpression.FRBRthis.get('value'), '/zm/act/2007/01/eng@2012-01-01/!main')
        assert_equal(a.meta.identification.FRBRExpression.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')
        assert_equal(a.meta.identification.FRBRExpression.FRBRdate.get('date'), '2012-01-01')

        assert_equal(a.meta.identification.FRBRManifestation.FRBRthis.get('value'),
                     '/zm/act/2007/01/eng@2012-01-01/!main')
        assert_equal(a.meta.identification.FRBRManifestation.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')
        assert_equal(a.meta.identification.FRBRManifestation.FRBRdate.get('date'), today)

        assert_validates(a)

    def test_frbr_country(self):
        a = Act()
        a.expression_date = '2012-01-01'
        a.frbr_uri = '/zm/act/2007/01'

        assert_equal(a.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm')

        a.frbr_uri = '/zm-abc123/act/2007/01'
        assert_equal(a.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm-abc123')

    def test_title(self):
        a = Act()
        a.title = "a title"
        self.assertEqual(a.title, "a title")

    def test_subtype(self):
        a = Act()
        a.frbr_uri = '/akn/za/act/by-law/2009/1'
        self.assertEqual(a.meta.identification.FRBRWork.FRBRsubtype.get('value'), 'by-law')
        assert_validates(a)

        # clear it
        a.frbr_uri = '/akn/za/act/2009/1'
        with self.assertRaises(AttributeError):
            a.meta.identification.FRBRWork.FRBRsubtype

        assert_validates(a)

    def test_work_date(self):
        """ Work date must be the FRBR date.
        """
        a = Act()
        a.frbr_uri = '/akn/za/act/2012-01-02/5'
        assert_equal(datestring(a.work_date), '2012-01-02')
        assert_is_instance(a.work_date, date)

        a.frbr_uri = '/akn/za/act/2009/5'
        assert_equal(datestring(a.work_date), '2009-01-01')
        assert_is_instance(a.work_date, date)

    def test_expression_date(self):
        a = Act()
        a.expression_date = '2012-01-02'
        assert_equal(datestring(a.expression_date), '2012-01-02')
        assert_is_instance(a.expression_date, date)

    def test_manifestation_date(self):
        a = Act()
        a.manifestation_date = '2012-01-02'
        assert_equal(datestring(a.manifestation_date), '2012-01-02')
        assert_is_instance(a.manifestation_date, date)

    def test_language(self):
        a = Act()
        a.language = 'fre'
        assert_equal(a.language, 'fre')

    def test_namespaces(self):
        # default is now AKN3
        a = Act()
        assert_equal(a.namespace, 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0')

        # prefer AKN3 when both 2 and 3 are listed as namespaces
        a = Act(xml="""<?xml version="1.0"?>
<foo:akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:foo="http://www.akomantoso.org/2.0" xmlns:bar="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <foo:act>
    <meta/>
    <foo:body/>
  </foo:act>
  <bar:act>
    <meta/>
    <bar:body/>
  </bar:act>
</foo:akomaNtoso>""")
        assert_equal(a.namespace, 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0')

        # prefer AKN2 when 2 and something else are listed as namespaces
        a = Act(xml="""<?xml version="1.0"?>
<foo:akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:foo="http://www.akomantoso.org/2.0" xmlns:bar="http://docs.oasis-open.org/legaldocml/ns/akn/5.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <foo:act>
    <meta/>
    <foo:body/>
  </foo:act>
</foo:akomaNtoso>""")
        assert_equal(a.namespace, 'http://www.akomantoso.org/2.0')

        # throw error if neither of AKN2 and AKN3 are listed as namespaces
        with assert_raises(ValueError) as raised:
            Act(xml="""<?xml version="1.0"?>
                <foo:akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:foo="http://www.akomantoso.org/4.0" xmlns:bar="http://docs.oasis-open.org/legaldocml/ns/akn/5.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <foo:act>
    <meta/>
    <body/>
  </foo:act>
</foo:akomaNtoso>""")
        assert_in(
            "Expected to find one of the following Akoma Ntoso XML namespaces: http://docs.oasis-open.org/legaldocml/ns/akn/3.0, http://www.akomantoso.org/2.0. Only these namespaces were found: http://www.w3.org/2001/XMLSchema-instance, http://www.akomantoso.org/4.0, http://docs.oasis-open.org/legaldocml/ns/akn/5.0",
            raised.exception.args)

        # ignore content that isn't in the chosen namespace
        a = Act(xml="""<?xml version="1.0"?>
<bar:akomaNtoso xmlns:foo="http://www.akomantoso.org/2.0" xmlns:bar="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <bar:act>
    <bar:meta/>
    <bar:body>
      <bar:section id="section-1">
        <bar:content>
          <p>This content SHOULD be ignored as it's not using the AKN3 namespace.</p>
          <foo:p>This content should ALSO be ignored as it's using the AKN2 namespace.</foo:p>
          <bar:p>This content should NOT be ignored as it's using the AKN3 namespace.</bar:p>
        </bar:content>
      </bar:section>
    </bar:body>
  </bar:act>
</bar:akomaNtoso>""")
        assert_equal(a.namespace, 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0')
        self.assertEqual("This content should NOT be ignored as it's using the AKN3 namespace.", a.body.section.content.p)
        self.assertNotIn("This content SHOULD be ignored as it's not using the AKN3 namespace.", a.body.section.content.p)
        self.assertNotIn("This content should ALSO be ignored as it's using the AKN2 namespace.", a.body.section.content.p)

    def test_parser(self):
        a = Act()
        # no errors raised by parsing default Act
        a.parse(a.to_xml(), a.document_type)

        # error if root isn't `akomaNtoso`
        with assert_raises(ValueError) as raised:
            a.parse("""<?xml version="1.0"?>
<myBlog xmlns="http://www.akomantoso.org/2.0">
  <p>Whaddup, fam!</p>
</myBlog>""", a.document_type)
        assert_in("XML root element must be akomaNtoso, but got myBlog instead", raised.exception.args)

        # error if root as no children
        with assert_raises(ValueError) as raised:
            a.parse("""<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd">
</akomaNtoso>""", a.document_type)
        assert_in("Expected act as a child of root element", raised.exception.args)

        # error if `act` isn't first child
        with assert_raises(ValueError) as raised:
            a.parse("""<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd">
  <somethingElse>
  </somethingElse>
</akomaNtoso>""", a.document_type)
        assert_in("Expected act as a child of root element", raised.exception.args)

        # allow comments at the top level
        a.parse("""<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <!-- a comment -->
  <act>
    <meta/>
    <body/>
  </act>
</akomaNtoso>""", a.document_type)

    def test_add_number(self):
        """ When adding an FRBRnumber element to a document that doesn't already have one, it
        must come after subtype.
        """
        a = Act(xml="""
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <!-- a comment -->
  <act contains="singleVersion" name="act">
    <meta>
      <identification source="#slaw">
        <FRBRWork>
          <FRBRthis value="/na/act/p/1977/25/!main"/>
          <FRBRuri value="/na/act/p/1977/25"/>
          <FRBRalias value="Livestock Improvement Act, 1977" name="title"/>
          <FRBRdate date="1977-03-23" name="Generation"/>
          <FRBRauthor href="#council"/>
          <FRBRcountry value="na"/>
          <FRBRsubtype value="p"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/na/act/p/1977/25/eng@1993-12-02/!main"/>
          <FRBRuri value="/na/act/p/1977/25/eng@1993-12-02"/>
          <FRBRdate date="1993-12-02" name="Generation"/>
          <FRBRauthor href="#council"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/na/act/p/1977/25/eng@1993-12-02/!main"/>
          <FRBRuri value="/na/act/p/1977/25/eng@1993-12-02"/>
          <FRBRdate date="2020-03-25" name="Generation"/>
          <FRBRauthor href="#slaw"/>
        </FRBRManifestation>
      </identification>
      <publication number="5462" name="South African Government Gazette" showAs="South African Government Gazette" date="1977-03-23"/>
    </meta>
    <body>
      <section eId="section_1">
        <content>
          <p></p>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""")
        a.frbr_uri = '/na/act/p/1997/25/'

        assert_validates(a)

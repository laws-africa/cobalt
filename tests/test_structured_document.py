from unittest import TestCase
from nose.tools import *  # noqa
from datetime import date
import lxml.etree as etree

from cobalt import Act, AmendmentEvent, RepealEvent, Judgment, datestring


class StructuredDocumentTestCase(TestCase):
    # using Act to test StructuredDocument functionality
    # because we need a concrete document (with a default empty_document) to work with
    maxDiff = None

    def test_frbr_uri(self):
        a = Act()
        a.expression_date = '2012-01-01'
        a.frbr_uri = '/zm/act/2007/01'

        assert_equal(a.frbr_uri.work_uri(), '/zm/act/2007/01')
        assert_equal(a.frbr_uri.number, '01')

        assert_equal(a.meta.identification.FRBRWork.FRBRthis.get('value'), '/zm/act/2007/01/!main')
        assert_equal(a.meta.identification.FRBRWork.FRBRuri.get('value'), '/zm/act/2007/01')
        assert_equal(a.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm')

        assert_equal(a.meta.identification.FRBRExpression.FRBRthis.get('value'), '/zm/act/2007/01/eng@2012-01-01/!main')
        assert_equal(a.meta.identification.FRBRExpression.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')

        assert_equal(a.meta.identification.FRBRManifestation.FRBRthis.get('value'),
                     '/zm/act/2007/01/eng@2012-01-01/!main')
        assert_equal(a.meta.identification.FRBRManifestation.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')

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

        a.frbr_uri = '/akn/za/act/2009/1'
        with self.assertRaises(AttributeError):
            a.meta.identification.FRBRWork.FRBRsubtype

    def test_work_date(self):
        a = Act()
        a.work_date = '2012-01-02'
        assert_equal(datestring(a.work_date), '2012-01-02')
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
        assert_in("XML root element must have at least one child", raised.exception.args)

        # error if `act` isn't first child
        with assert_raises(ValueError) as raised:
            a.parse("""<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd">
  <somethingElse>
  </somethingElse>
</akomaNtoso>""", a.document_type)
        assert_in("Expected act as first child of root element, but got somethingElse instead",
                  raised.exception.args)

    def test_components(self):
        a = Act(xml="""<?xml version="1.0" encoding="UTF-8"?>
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <act contains="singleVersion">
    <meta>
      <identification source="#slaw">
        <FRBRWork>
          <FRBRthis value="/na/act/1977/25/!main"/>
          <FRBRuri value="/na/act/1977/25"/>
          <FRBRalias value="Livestock Improvement Act, 1977"/>
          <FRBRdate date="1977-03-23" name="Generation"/>
          <FRBRauthor href="#council"/>
          <FRBRcountry value="na"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!main"/>
          <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
          <FRBRdate date="1993-12-02" name="Generation"/>
          <FRBRauthor href="#council"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!main"/>
          <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
          <FRBRdate date="2020-03-25" name="Generation"/>
          <FRBRauthor href="#slaw"/>
        </FRBRManifestation>
      </identification>
      <publication number="5462" name="South African Government Gazette" showAs="South African Government Gazette" date="1977-03-23"/>
    </meta>
    <body>
      <section id="section-20">
        <content>
          <p></p>
        </content>
      </section>
    </body>
    <attachments>
      <attachment id="att_1">
        <doc name="schedule">
          <meta>
            <identification source="#slaw">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href="#council"/>
                <FRBRcountry value="na"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href="#council"/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href="#slaw"/>
              </FRBRManifestation>
            </identification>
          </meta>
          <mainBody>
            <hcontainer id="schedule" name="schedule">
              <heading>Schedule</heading>
              <paragraph id="schedule.paragraph0">
                <content>
                  <p>This is the content of the Schedule!</p>
                </content>
              </paragraph>
            </hcontainer>
          </mainBody>
        </doc>
      </attachment>
    </attachments>
    <components>
      <component id="comp_1">
        <doc name="schedule">
          <meta>
            <identification source="#slaw">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href="#council"/>
                <FRBRcountry value="na"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href="#council"/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href="#slaw"/>
              </FRBRManifestation>
            </identification>
           </meta>
          <mainBody>
            <hcontainer id="schedule" name="schedule">
              <heading>Schedule</heading>
              <paragraph id="schedule.paragraph0">
                <content>
                  <p>This is the content of the Schedule!</p>
                </content>
              </paragraph>
            </hcontainer>
          </mainBody>
        </doc>
      </component>
    </components>
  </act>
</akomaNtoso>
        """)
        components = a.components()
        self.assertEqual(['main', 'schedule-A', 'schedule-XXX'], sorted(components.keys()))
        self.assertEqual('This is the content of the Schedule!',
                         components['schedule-XXX'].mainBody.hcontainer.paragraph.content.p)


class ActTestCase(TestCase):
    maxDiff = None

    def test_empty_act(self):
        a = Act()
        assert_equal(a.title, "Untitled")
        assert_is_not_none(a.meta)
        assert_is_not_none(a.body)

    def test_empty_body(self):
        a = Act()
        assert_not_equal(a.body.text, '')

    def test_publication_date(self):
        a = Act()
        assert_is_none(a.publication_date)

        a.publication_date = '2012-01-02'
        assert_equal(datestring(a.publication_date), '2012-01-02')
        assert_is_instance(a.publication_date, date)

    def test_publication_number(self):
        a = Act()
        assert_is_none(a.publication_number)

        a.publication_number = '1234'
        assert_equal(a.publication_number, '1234')

    def test_publication_name(self):
        a = Act()
        assert_is_none(a.publication_name)

        a.publication_name = 'Publication'
        assert_equal(a.publication_name, 'Publication')

    def test_set_amendments(self):
        a = Act()
        a.frbr_uri = "/akn/za/act/1900/1"
        a.amendments = [AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/10', amending_title="Foo")]

        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act" contains="singleVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef id="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/>
      </lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        <passiveRef id="amendment-0-source" href="/za/act/1980/10" showAs="Foo"/>
      </references>
    </meta>
    <body/>
  </act>
</akomaNtoso>
""", xml)

        a.amendments = [
            AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/22', amending_title="Corrected"),
            AmendmentEvent(date='2013-03-03', amending_uri='/za/act/1990/5', amending_title="Bar"),
        ]

        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act" contains="singleVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef id="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/>
        <eventRef id="amendment-2013-03-03" date="2013-03-03" type="amendment" source="#amendment-1-source"/>
      </lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        <passiveRef id="amendment-0-source" href="/za/act/1980/22" showAs="Corrected"/>
        <passiveRef id="amendment-1-source" href="/za/act/1990/5" showAs="Bar"/>
      </references>
    </meta>
    <body/>
  </act>
</akomaNtoso>
""", xml)

        amendment = a.amendments[0]
        assert_equal(datestring(amendment.date), '2012-02-01')
        assert_equal(amendment.amending_uri, '/za/act/1980/22')
        assert_equal(amendment.amending_title, 'Corrected')

        amendment = a.amendments[1]
        assert_equal(datestring(amendment.date), '2013-03-03')
        assert_equal(amendment.amending_uri, '/za/act/1990/5')
        assert_equal(amendment.amending_title, 'Bar')

    def test_set_repeal(self):
        a = Act()
        a.frbr_uri = "/akn/za/act/1900/1"
        a.repeal = RepealEvent(date='2012-02-01', repealing_uri='/za/act/1980/10', repealing_title='Foo')
        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act" contains="originalVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef id="repeal-2012-02-01" date="2012-02-01" type="repeal" source="#repeal-source"/>
      </lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        <passiveRef id="repeal-source" href="/za/act/1980/10" showAs="Foo"/>
      </references>
    </meta>
    <body/>
  </act>
</akomaNtoso>
""", xml)

        assert_equal(a.repeal.repealing_uri, '/za/act/1980/10')
        assert_equal(a.repeal.repealing_title, 'Foo')
        assert_equal(datestring(a.repeal.date), '2012-02-01')

        # check that clearing it works
        a.repeal = None
        assert_is_none(a.repeal)

    def test_main(self):
        a = Act()
        self.assertEqual(a.main, a.act)


class JudgmentTestCase(TestCase):
    maxDiff = None

    def test_empty_judgment(self):
        j = Judgment()
        assert_equal(j.title, "Untitled")
        assert_is_not_none(j.meta)
        assert_is_not_none(j.judgmentBody)

    def test_empty_body(self):
        j = Judgment()
        assert_not_equal(j.judgmentBody.text, '')

    def test_main(self):
        j = Judgment()
        self.assertEqual(j.main, j.judgment)

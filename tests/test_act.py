from unittest import TestCase
from nose.tools import *  # noqa
from datetime import date
import lxml.etree as etree

from cobalt.hierarchical import Act, AmendmentEvent, RepealEvent
from cobalt.akn import datestring


class ActTestCase(TestCase):
    maxDiff = None

    def test_empty_act(self):
        a = Act()
        assert_equal(a.title, "Untitled")
        assert_is_not_none(a.meta)
        assert_is_not_none(a.body)

    def test_frbr_uri(self):
        a = Act()
        a.expression_date = '2012-01-01'
        a.frbr_uri = '/zm/act/2007/01'

        assert_equal(a.frbr_uri.work_uri(), '/zm/act/2007/01')
        assert_equal(a.number, '01')

        assert_equal(a.meta.identification.FRBRWork.FRBRthis.get('value'), '/zm/act/2007/01/main')
        assert_equal(a.meta.identification.FRBRWork.FRBRuri.get('value'), '/zm/act/2007/01')
        assert_equal(a.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm')

        assert_equal(a.meta.identification.FRBRExpression.FRBRthis.get('value'), '/zm/act/2007/01/eng@2012-01-01/main')
        assert_equal(a.meta.identification.FRBRExpression.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')

        assert_equal(a.meta.identification.FRBRManifestation.FRBRthis.get('value'), '/zm/act/2007/01/eng@2012-01-01/main')
        assert_equal(a.meta.identification.FRBRManifestation.FRBRuri.get('value'), '/zm/act/2007/01/eng@2012-01-01')
        
    def test_empty_body(self):
        a = Act()
        assert_not_equal(a.body.text, '')

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

    def test_language(self):
        a = Act()
        a.language = 'fre'
        assert_equal(a.language, 'fre')

    def test_set_amendments(self):
        a = Act()
        a.amendments = [AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/10', amending_title="Foo")]

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="singleVersion">
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
      </identification><lifecycle source="#cobalt"><eventRef id="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/></lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
      <passiveRef id="amendment-0-source" href="/za/act/1980/10" showAs="Foo"/></references>
    </meta>
    <body>
      <section id="section-1">
        <content>
          <p/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""",
            etree.tostring(a.root, encoding='utf-8', pretty_print=True).decode('utf-8'))

        a.amendments = [
            AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/22', amending_title="Corrected"),
            AmendmentEvent(date='2013-03-03', amending_uri='/za/act/1990/5', amending_title="Bar"),
        ]

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="singleVersion">
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
      </identification><lifecycle source="#cobalt"><eventRef id="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/><eventRef id="amendment-2013-03-03" date="2013-03-03" type="amendment" source="#amendment-1-source"/></lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
      <passiveRef id="amendment-0-source" href="/za/act/1980/22" showAs="Corrected"/><passiveRef id="amendment-1-source" href="/za/act/1990/5" showAs="Bar"/></references>
    </meta>
    <body>
      <section id="section-1">
        <content>
          <p/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""",
            etree.tostring(a.root, encoding='utf-8', pretty_print=True).decode('utf-8'))

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
        a.repeal = RepealEvent(date='2012-02-01', repealing_uri='/za/act/1980/10', repealing_title='Foo')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
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
      </identification><lifecycle source="#cobalt"><eventRef id="repeal-2012-02-01" date="2012-02-01" type="repeal" source="#repeal-source"/></lifecycle>
      <references>
        <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
      <passiveRef id="repeal-source" href="/za/act/1980/10" showAs="Foo"/></references>
    </meta>
    <body>
      <section id="section-1">
        <content>
          <p/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""",
            etree.tostring(a.root, encoding='utf-8', pretty_print=True).decode('utf-8'))

        assert_equal(a.repeal.repealing_uri, '/za/act/1980/10')
        assert_equal(a.repeal.repealing_title, 'Foo')
        assert_equal(datestring(a.repeal.date), '2012-02-01')

        # check that clearing it works
        a.repeal = None
        assert_is_none(a.repeal)

    def test_namespaces(self):
        # default for the time being is still AKN2
        a = Act()
        assert_equal(a.namespace, 'http://www.akomantoso.org/2.0')

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
        assert_in("Expected to find one of the following Akoma Ntoso XML namespaces: http://docs.oasis-open.org/legaldocml/ns/akn/3.0, http://www.akomantoso.org/2.0. Only these namespaces were found: http://www.w3.org/2001/XMLSchema-instance, http://www.akomantoso.org/4.0, http://docs.oasis-open.org/legaldocml/ns/akn/5.0", raised.exception.args)

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
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
</akomaNtoso>""", a.document_type)
        assert_in("XML root element must have at least one child", raised.exception.args)

        # error if `act` isn't first child
        with assert_raises(ValueError) as raised:
            a.parse("""<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <somethingElse>
  </somethingElse>
</akomaNtoso>""", a.document_type)
        assert_in("Expected act as first child of root element, but got somethingElse instead", raised.exception.args)

    def test_main(self):
        a = Act()
        self.assertEqual(a.main, a.act)

    def test_components(self):
        a = Act(xml="""<?xml version="1.0" encoding="UTF-8"?>
<akomaNtoso xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <act contains="singleVersion">
    <meta>
      <identification source="#slaw">
        <FRBRWork>
          <FRBRthis value="/na/act/1977/25/main"/>
          <FRBRuri value="/na/act/1977/25"/>
          <FRBRalias value="Livestock Improvement Act, 1977"/>
          <FRBRdate date="1977-03-23" name="Generation"/>
          <FRBRauthor href="#council"/>
          <FRBRcountry value="na"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/na/act/1977/25/eng@1993-12-02/main"/>
          <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
          <FRBRdate date="1993-12-02" name="Generation"/>
          <FRBRauthor href="#council"/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/na/act/1977/25/eng@1993-12-02/main"/>
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
  </act>
  <components>
    <component id="component-schedule">
      <doc name="schedule">
        <meta>
          <identification source="#slaw">
            <FRBRWork>
              <FRBRthis value="/na/act/1977/25/schedule-XXX"/>
              <FRBRuri value="/na/act/1977/25"/>
              <FRBRalias value="Schedule"/>
              <FRBRdate date="1980-01-01" name="Generation"/>
              <FRBRauthor href="#council"/>
              <FRBRcountry value="na"/>
            </FRBRWork>
            <FRBRExpression>
              <FRBRthis value="/na/act/1977/25/eng@1993-12-02/schedule"/>
              <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
              <FRBRdate date="1980-01-01" name="Generation"/>
              <FRBRauthor href="#council"/>
              <FRBRlanguage language="eng"/>
            </FRBRExpression>
            <FRBRManifestation>
              <FRBRthis value="/na/act/1977/25/eng@1993-12-02/schedule"/>
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
</akomaNtoso>
        """)
        components = a.components()
        self.assertIn('schedule-XXX', components.keys())
        self.assertEqual('This is the content of the Schedule!',
                         components['schedule-XXX'].mainBody.hcontainer.paragraph.content.p)

def act_fixture(content):
    return """<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <act contains="originalVersion">
    <meta>
      <identification source="">
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
    </meta>
    %s
  </act>
</akomaNtoso>""" % content

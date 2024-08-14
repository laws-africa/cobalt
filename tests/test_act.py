from unittest import TestCase
from datetime import date

from lxml.etree import LxmlSyntaxError

from cobalt import Act, AmendmentEvent, RepealEvent, datestring
from cobalt.schemas import assert_validates


class ActTestCase(TestCase):
    maxDiff = None

    def test_empty_act(self):
        a = Act()
        self.assertEqual(a.title, "Untitled")
        self.assertIsNotNone(a.meta)
        self.assertIsNotNone(a.body)

        assert_validates(a)

    def test_empty_body(self):
        a = Act()
        self.assertNotEqual(a.body.text, '')
        assert_validates(a)

    def test_publication_date(self):
        a = Act()
        self.assertIsNone(a.publication_date)
        assert_validates(a)

        a.publication_date = '2012-01-02'
        self.assertEqual(datestring(a.publication_date), '2012-01-02')
        self.assertIsInstance(a.publication_date, date)
        assert_validates(a)

        a.publication_date = None
        self.assertIsNone(a.publication_date)
        assert_validates(a)

    def test_publication_number(self):
        a = Act()
        self.assertIsNone(a.publication_number)

        a.publication_number = '1234'
        self.assertEqual(a.publication_number, '1234')
        assert_validates(a)

    def test_publication_name(self):
        a = Act()
        self.assertIsNone(a.publication_name)

        a.publication_name = 'Publication'
        self.assertEqual(a.publication_name, 'Publication')
        assert_validates(a)

    def test_set_amendments(self):
        a = Act()
        a.frbr_uri = "/akn/za/act/1900/1"
        a.amendments = [AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/10', amending_title="Foo")]
        assert_validates(a)

        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act" contains="singleVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRdate date="1900" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
          <FRBRnumber value="1"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef eId="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/>
      </lifecycle>
      <references source="#cobalt">
        <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        <passiveRef eId="amendment-0-source" href="/za/act/1980/10" showAs="Foo"/>
      </references>
    </meta>
    <body>
      <section eId="sec_nn_1">
        <content>
          <p eId="sec_nn_1__p_1"/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""", xml)

        a.amendments = [
            AmendmentEvent(date='2012-02-01', amending_uri='/za/act/1980/22', amending_title="Corrected"),
            AmendmentEvent(date='2013-03-03', amending_uri='/za/act/1990/5', amending_title="Bar"),
        ]
        assert_validates(a)

        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act" contains="singleVersion">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRdate date="1900" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
          <FRBRnumber value="1"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef eId="amendment-2012-02-01" date="2012-02-01" type="amendment" source="#amendment-0-source"/>
        <eventRef eId="amendment-2013-03-03" date="2013-03-03" type="amendment" source="#amendment-1-source"/>
      </lifecycle>
      <references source="#cobalt">
        <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        <passiveRef eId="amendment-0-source" href="/za/act/1980/22" showAs="Corrected"/>
        <passiveRef eId="amendment-1-source" href="/za/act/1990/5" showAs="Bar"/>
      </references>
    </meta>
    <body>
      <section eId="sec_nn_1">
        <content>
          <p eId="sec_nn_1__p_1"/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""", xml)

        amendment = a.amendments[0]
        self.assertEqual(datestring(amendment.date), '2012-02-01')
        self.assertEqual(amendment.amending_uri, '/za/act/1980/22')
        self.assertEqual(amendment.amending_title, 'Corrected')

        amendment = a.amendments[1]
        self.assertEqual(datestring(amendment.date), '2013-03-03')
        self.assertEqual(amendment.amending_uri, '/za/act/1990/5')
        self.assertEqual(amendment.amending_title, 'Bar')

        assert_validates(a)

        # clear them
        a.amendments = []
        assert_validates(a)
        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRdate date="1900" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
          <FRBRnumber value="1"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <references source="#cobalt">
        <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
      </references>
    </meta>
    <body>
      <section eId="sec_nn_1">
        <content>
          <p eId="sec_nn_1__p_1"/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""", xml)

    def test_set_repeal(self):
        a = Act()
        a.frbr_uri = "/akn/za/act/1900/1"
        a.repeal = RepealEvent(date='2012-02-01', repealing_uri='/za/act/1980/10', repealing_title='Foo')
        xml = a.to_xml(encoding='unicode', pretty_print=True)
        xml = xml.replace(datestring(date.today()), 'TODAY')

        self.assertMultiLineEqual(
            """<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act name="act">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/akn/za/act/1900/1/!main"/>
          <FRBRuri value="/akn/za/act/1900/1"/>
          <FRBRalias value="Untitled" name="title"/>
          <FRBRdate date="1900" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="za"/>
          <FRBRnumber value="1"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/akn/za/act/1900/1/eng@TODAY/!main"/>
          <FRBRuri value="/akn/za/act/1900/1/eng@TODAY"/>
          <FRBRdate date="TODAY" name="Generation"/>
          <FRBRauthor href=""/>
        </FRBRManifestation>
      </identification>
      <lifecycle source="#cobalt">
        <eventRef eId="repeal-2012-02-01" date="2012-02-01" type="repeal" source="#repeal-source"/>
      </lifecycle>
      <references source="#cobalt">
        <TLCOrganization eId="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
        <passiveRef eId="repeal-source" href="/za/act/1980/10" showAs="Foo"/>
      </references>
    </meta>
    <body>
      <section eId="sec_nn_1">
        <content>
          <p eId="sec_nn_1__p_1"/>
        </content>
      </section>
    </body>
  </act>
</akomaNtoso>
""", xml)

        self.assertEqual(a.repeal.repealing_uri, '/za/act/1980/10')
        self.assertEqual(a.repeal.repealing_title, 'Foo')
        self.assertEqual(datestring(a.repeal.date), '2012-02-01')

        assert_validates(a)

        # check that clearing it works
        a.repeal = None
        self.assertIsNone(a.repeal)

        assert_validates(a)

    def test_main(self):
        a = Act()
        self.assertEqual(a.main, a.act)

    def test_bad_xml(self):
        with self.assertRaises(LxmlSyntaxError):
            Act('badness')

        with self.assertRaises(ValueError):
            Act('<root>no namespace</root>')

        with self.assertRaises(ValueError):
            Act('<akomaNtoso>no first child</akomaNtoso>')

        with self.assertRaises(ValueError):
            Act('<akomaNtoso><child>no namespace</child></akomaNtoso>')

from unittest import TestCase

from lxml import etree

from cobalt import Act
from cobalt.schemas import assert_validates


class AttachmentsTestCase(TestCase):
    maxDiff = None

    def tostring(self, xml):
        return etree.tostring(xml, encoding='unicode').strip()

    def setUp(self):
        self.a = Act(xml="""<?xml version="1.0" encoding="UTF-8"?>
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <act contains="singleVersion" name="act">
    <meta>
      <identification source="#cobalt">
        <FRBRWork>
          <FRBRthis value="/na/act/1977/25/!main"/>
          <FRBRuri value="/na/act/1977/25"/>
          <FRBRalias value="Livestock Improvement Act, 1977" name="title"/>
          <FRBRdate date="1977" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRcountry value="na"/>
          <FRBRnumber value="25"/>
        </FRBRWork>
        <FRBRExpression>
          <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!main"/>
          <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
          <FRBRdate date="1993-12-02" name="Generation"/>
          <FRBRauthor href=""/>
          <FRBRlanguage language="eng"/>
        </FRBRExpression>
        <FRBRManifestation>
          <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!main"/>
          <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
          <FRBRdate date="2020-03-25" name="Generation"/>
          <FRBRauthor href=""/>
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
    <attachments>
      <attachment eId="att_1">
        <heading>Schedule</heading>
        <doc name="schedule">
          <meta>
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1977" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="1993-12-02" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>
          <mainBody>
            <paragraph eId="paragraph_1">
              <content>
                <p>This is the content of the Schedule!</p>
              </content>
            </paragraph>
          </mainBody>
        </doc>
      </attachment>
    </attachments>
    <components>
      <component eId="comp_1">
        <heading>Schedule</heading>
        <doc name="schedule">
          <meta>
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title" />
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>
          <mainBody>
            <paragraph eId="paragraph_1">
              <content>
                <p>This is the content of the Schedule!</p>
              </content>
            </paragraph>
          </mainBody>
        </doc>
      </component>
    </components>
  </act>
</akomaNtoso>
        """)

    def test_component_basics(self):
        components = self.a.components()
        self.assertEqual(['main', 'schedule-A', 'schedule-XXX'], sorted(components.keys()))
        self.assertEqual('This is the content of the Schedule!',
                         components['schedule-XXX'].doc.mainBody.paragraph.content.p)
        assert_validates(self.a)

        # this won't change any component names, because the existing names are used by default
        frbr_uri = self.a.frbr_uri
        frbr_uri.work_component = 'blah'
        self.a.frbr_uri = frbr_uri
        self.assertEqual(['main', 'schedule-A', 'schedule-XXX'], sorted(self.a.components().keys()))

    def test_set_missing_component_with_default(self):
        a = Act(xml="""<?xml version="1.0" encoding="UTF-8"?>
        <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <act contains="singleVersion" name="act">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/na/act/1977/25"/>
                  <FRBRuri value="/na/act/1977/25"/>
                  <FRBRalias value="Livestock Improvement Act, 1977" name="title"/>
                  <FRBRdate date="1977-03-23" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="na"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRdate date="1993-12-02" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRdate date="2020-03-25" name="Generation"/>
                  <FRBRauthor href=""/>
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
        self.assertEqual([None], sorted(a.components().keys()))
        assert_validates(a)

        # change the main component name implicitly
        # should get 'main' as the default
        frbr_uri = a.frbr_uri
        frbr_uri.work_component = None
        a.frbr_uri = frbr_uri
        self.assertEqual(['main'], sorted(a.components().keys()))

    def test_set_missing_component_explicitly(self):
        a = Act(xml="""<?xml version="1.0" encoding="UTF-8"?>
        <akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xsi:schemaLocation="http://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <act contains="singleVersion" name="act">
            <meta>
              <identification source="#cobalt">
                <FRBRWork>
                  <FRBRthis value="/na/act/1977/25"/>
                  <FRBRuri value="/na/act/1977/25"/>
                  <FRBRalias value="Livestock Improvement Act, 1977" name="title"/>
                  <FRBRdate date="1977-03-23" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRcountry value="na"/>
                </FRBRWork>
                <FRBRExpression>
                  <FRBRthis value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRdate date="1993-12-02" name="Generation"/>
                  <FRBRauthor href=""/>
                  <FRBRlanguage language="eng"/>
                </FRBRExpression>
                <FRBRManifestation>
                  <FRBRthis value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                  <FRBRdate date="2020-03-25" name="Generation"/>
                  <FRBRauthor href=""/>
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
        self.assertEqual([None], sorted(a.components().keys()))
        assert_validates(a)

        # change the main component name
        frbr_uri = a.frbr_uri
        frbr_uri.work_component = 'blah'
        a.frbr_uri = frbr_uri
        self.assertEqual(['blah'], sorted(a.components().keys()))

    def test_component_expression_date(self):
        self.a.expression_date = '2021-01-01'

        components = list(self.a.components().values())

        self.assertEqual('''<meta xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1977" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@2021-01-01/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@2021-01-01"/>
                <FRBRdate date="2021-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@2021-01-01/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@2021-01-01"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>''', self.tostring(components[1].doc.meta))

        self.assertEqual('''<meta xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1977" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@2021-01-01/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@2021-01-01"/>
                <FRBRdate date="2021-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@2021-01-01/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@2021-01-01"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>''', self.tostring(components[2].doc.meta))

    def test_component_manifestation_date(self):
        self.a.manifestation_date = '2021-01-01'

        components = list(self.a.components().values())

        self.assertEqual('''<meta xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1977" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="1993-12-02" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="2021-01-01" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>''', self.tostring(components[1].doc.meta))

        self.assertEqual('''<meta xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="eng"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/eng@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/eng@1993-12-02"/>
                <FRBRdate date="2021-01-01" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>''', self.tostring(components[2].doc.meta))

    def test_component_language(self):
        self.a.language = 'swa'

        components = list(self.a.components().values())

        self.assertEqual('''<meta xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1977" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/swa@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/swa@1993-12-02"/>
                <FRBRdate date="1993-12-02" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="swa"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/swa@1993-12-02/!schedule-A"/>
                <FRBRuri value="/na/act/1977/25/swa@1993-12-02"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>''', self.tostring(components[1].doc.meta))

        self.assertEqual('''<meta xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <identification source="#cobalt">
              <FRBRWork>
                <FRBRthis value="/na/act/1977/25/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25"/>
                <FRBRalias value="Schedule" name="title"/>
                <FRBRdate date="1977" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRcountry value="na"/>
                <FRBRnumber value="25"/>
              </FRBRWork>
              <FRBRExpression>
                <FRBRthis value="/na/act/1977/25/swa@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/swa@1993-12-02"/>
                <FRBRdate date="1980-01-01" name="Generation"/>
                <FRBRauthor href=""/>
                <FRBRlanguage language="swa"/>
              </FRBRExpression>
              <FRBRManifestation>
                <FRBRthis value="/na/act/1977/25/swa@1993-12-02/!schedule-XXX"/>
                <FRBRuri value="/na/act/1977/25/swa@1993-12-02"/>
                <FRBRdate date="2020-03-25" name="Generation"/>
                <FRBRauthor href=""/>
              </FRBRManifestation>
            </identification>
          </meta>''', self.tostring(components[2].doc.meta))

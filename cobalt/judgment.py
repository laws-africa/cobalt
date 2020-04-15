from lxml import etree, objectify

from .akn import JudgmentStructure, objectify_parser


class Judgment(JudgmentStructure):
    EMPTY_DOCUMENT = """<?xml version="1.0"?>
    <akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
      <judgment>
        <meta>
          <identification source="#cobalt">
            <FRBRWork>
              <FRBRthis value="/za/judgment/1900/12345/main"/>
              <FRBRuri value="/za/judgment/1900/12345"/>
              <FRBRalias value="Untitled Judgment"/>
              <FRBRdate date="1900-01-01" name="Hearing"/>
              <FRBRauthor href="#scoa" as="#author"/>
              <FRBRcountry value="za"/>
            </FRBRWork>
            <FRBRExpression>
              <FRBRthis value="/za/judgment/1900/12345/eng@/main"/>
              <FRBRuri value="/za/judgment/1900/12345/eng@"/>
              <FRBRdate date="1900-01-01" name="Delivery"/>
              <FRBRauthor href="#scoa" as="#author"/>
              <FRBRlanguage language="eng"/>
            </FRBRExpression>
            <FRBRManifestation>
              <FRBRthis value="/za/judgment/1900/12345/eng@/main"/>
              <FRBRuri value="/za/judgment/1900/12345/eng@"/>
              <FRBRdate date="1900-01-01" name="Conversion"/>
              <FRBRauthor href="#scoa" as="#author"/>
            </FRBRManifestation>
          </identification>
          <references>
            <TLCOrganization id="cobalt" href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
            <TLCOrganization id="scoa" href="/akn/ontology/organization/za.SupremeCourt" showAs="The Supreme Court of Appeal of South Africa"/>
          </references>
        </meta>
        <coverPage/>
        <header/>
        <judgmentBody>
          <introduction/>
          <background/>
          <arguments/>
          <remedies/>
          <motivation/>
          <decision/>
        </judgmentBody>
        <conclusions/>
        <attachments/>
        <components/>
      </judgment>
    </akomaNtoso>
    """

    document_type = "judgment"

    @property
    def body_xml(self):
        """ The raw XML string of the `judgmentBody` element of the document. When
        setting this property, XML must be rooted at a `judgmentBody` element. """
        return etree.tostring(self.judgmentBody, encoding='utf-8')

    @body_xml.setter
    def body_xml(self, xml):
        new_body = objectify.fromstring(xml or EMPTY_BODY, parser=objectify_parser)
        new_body.tag = 'judgmentBody'
        self.judgmentBody.getparent().replace(self.judgmentBody, new_body)
        self.judgmentBody = new_body


EMPTY_BODY = """
<judgmentBody/>
"""

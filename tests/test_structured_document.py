from unittest import TestCase
from nose.tools import *  # noqa
from datetime import date

from cobalt.judgment import Judgment
from cobalt.akn import datestring


class JudgmentTestCase(TestCase):
    maxDiff = None

    def test_empty_judgment(self):
        j = Judgment()
        assert_equal(j.title, "Untitled Judgment")
        assert_is_not_none(j.meta)
        assert_is_not_none(j.judgmentBody)

    def test_frbr_uri(self):
        j = Judgment()
        j.expression_date = '2012-01-01'
        j.frbr_uri = '/zm/judgment/2007/01'

        assert_equal(j.frbr_uri.work_uri(), '/zm/judgment/2007/01')
        assert_equal(j.frbr_uri.number, '01')

        assert_equal(j.meta.identification.FRBRWork.FRBRthis.get('value'), '/zm/judgment/2007/01/main')
        assert_equal(j.meta.identification.FRBRWork.FRBRuri.get('value'), '/zm/judgment/2007/01')
        assert_equal(j.meta.identification.FRBRWork.FRBRcountry.get('value'), 'zm')

        assert_equal(j.meta.identification.FRBRExpression.FRBRthis.get('value'), '/zm/judgment/2007/01/eng@2012-01-01/main')
        assert_equal(j.meta.identification.FRBRExpression.FRBRuri.get('value'), '/zm/judgment/2007/01/eng@2012-01-01')

        assert_equal(j.meta.identification.FRBRManifestation.FRBRthis.get('value'),
                     '/zm/judgment/2007/01/eng@2012-01-01/main')
        assert_equal(j.meta.identification.FRBRManifestation.FRBRuri.get('value'), '/zm/judgment/2007/01/eng@2012-01-01')

    def test_empty_body(self):
        j = Judgment()
        assert_not_equal(j.judgmentBody.text, '')

    def test_work_date(self):
        j = Judgment()
        j.work_date = '2012-01-02'
        assert_equal(datestring(j.work_date), '2012-01-02')
        assert_is_instance(j.work_date, date)

    def test_expression_date(self):
        j = Judgment()
        j.expression_date = '2012-01-02'
        assert_equal(datestring(j.expression_date), '2012-01-02')
        assert_is_instance(j.expression_date, date)

    def test_manifestation_date(self):
        j = Judgment()
        j.manifestation_date = '2012-01-02'
        assert_equal(datestring(j.manifestation_date), '2012-01-02')
        assert_is_instance(j.manifestation_date, date)

    def test_language(self):
        j = Judgment()
        j.language = 'fre'
        assert_equal(j.language, 'fre')

    def test_parser(self):
        j = Judgment()
        # no errors raised by parsing default Judgment
        j.parse(j.to_xml(), j.document_type)

        # error if root isn't `akomaNtoso`
        with assert_raises(ValueError) as raised:
            j.parse("""<?xml version="1.0"?>
<myBlog xmlns="http://www.akomantoso.org/2.0">
  <p>Whaddup, fam!</p>
</myBlog>""", j.document_type)
        assert_in("XML root element must be akomaNtoso, but got myBlog instead", raised.exception.args)

        # error if root as no children
        with assert_raises(ValueError) as raised:
            j.parse("""<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
</akomaNtoso>""", j.document_type)
        assert_in("XML root element must have at least one child", raised.exception.args)

        # error if `judgment` isn't first child
        with assert_raises(ValueError) as raised:
            j.parse("""<?xml version="1.0"?>
<akomaNtoso xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.akomantoso.org/2.0" xsi:schemaLocation="http://www.akomantoso.org/2.0 akomantoso20.xsd">
  <somethingElse>
  </somethingElse>
</akomaNtoso>""", j.document_type)
        assert_in("Expected judgment as first child of root element, but got somethingElse instead", raised.exception.args)

    def test_main(self):
        j = Judgment()
        self.assertEqual(j.main, j.judgment)

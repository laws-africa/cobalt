from unittest import TestCase
from nose.tools import *

from cobalt.uri import FrbrUri


class FrbrUriTestCase(TestCase):
    def test_bad_value(self):
        assert_raises(ValueError, FrbrUri.parse, "/badness")
        assert_raises(ValueError, FrbrUri.parse, "/ukpga/2015/1")

    def test_simple(self):
        uri = FrbrUri.parse("/akn/za/act/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, None)
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.prefix, "akn")

        assert_equal("/akn/za/act/1980/01", uri.work_uri())

    def test_with_subtype(self):
        uri = FrbrUri.parse("/akn/za/act/by-law/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, None)
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "by-law")
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/by-law/1980/01", uri.work_uri())

    def test_with_locality(self):
        uri = FrbrUri.parse("/akn/za-cpt/act/by-law/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, "cpt")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "by-law")
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za-cpt/act/by-law/1980/01", uri.work_uri())

    def test_with_subtype_and_actor(self):
        uri = FrbrUri.parse("/akn/za/act/by-law/actor/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "by-law")
        assert_equal(uri.actor, "actor")
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/by-law/actor/1980/01", uri.work_uri())

    def test_with_long_date(self):
        uri = FrbrUri.parse("/akn/za/act/1980-02-01/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980-02-01")
        assert_equal(uri.year, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/1980-02-01/01", uri.work_uri())

    def test_with_non_numeric_number(self):
        uri = FrbrUri.parse("/akn/za/act/1980/nn")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "nn")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/1980/nn", uri.work_uri())

    def test_with_work_component(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2/!schedule1")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.work_component, "schedule1")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/1980/2", uri.uri())
        assert_equal("/akn/za/act/1980/2/!schedule1", uri.work_uri())
        assert_equal("/akn/za/act/1980/2/eng/!schedule1", uri.expression_uri())

    def test_with_nested_work_components(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2/!schedule1/schedule2/schedule3")
        assert_equal(uri.work_component, "schedule1/schedule2/schedule3")

    def test_with_work_component_legacy(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2/!schedule1")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.work_component, "schedule1")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/1980/2", uri.uri())
        assert_equal("/akn/za/act/1980/2/!schedule1", uri.work_uri())
        assert_equal("/akn/za/act/1980/2/eng/!schedule1", uri.expression_uri())

    def test_with_short_work_component(self):
        uri = FrbrUri.parse("/akn/za-wc/act/pn/2018/46/!6")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, "wc")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "pn")
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "2018")
        assert_equal(uri.number, "46")
        assert_equal(uri.language, "eng")
        assert_equal(uri.work_component, "6")
        assert_equal(uri.expression_date, None)

        uri = FrbrUri.parse("/akn/za-wc/act/2018/46/!6")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, "wc")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "2018")
        assert_equal(uri.number, "46")
        assert_equal(uri.language, "eng")
        assert_equal(uri.work_component, "6")
        assert_equal(uri.expression_date, None)

    def test_with_work_component_and_portion(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2")
        uri.work_component = "main/schedule_1"
        uri.portion = "chp_2"

        assert_equal("/akn/za/act/1980/2", uri.uri())
        assert_equal("/akn/za/act/1980/2/!main/schedule_1", uri.work_uri())
        assert_equal("/akn/za/act/1980/2/eng/!main/schedule_1~chp_2", uri.expression_uri())

    def test_parse_expression2(self):
        uri = FrbrUri.parse("/gh/act/2020/1013/eng@2020-04-03")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@2020-04-03')
        assert_equal(uri.number, '1013')
        assert_is_none(uri.subtype)

    def test_expression_string_no_language(self):
        uri = FrbrUri.parse("/gh/act/2020/1013/")
        assert_equal(uri.language, "eng")
        uri.language = None
        with self.assertRaises(ValueError) as e:
            uri.expression_uri()
        err = e.exception
        assert_equal(str(err), "Expression URI requires a language.")

    def test_parse_expression(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/afr@")
        assert_equal(uri.language, "afr")
        assert_equal(uri.expression_date, '@')
        assert_equal("/akn/za/act/1980/02", uri.work_uri())
        assert_equal("/akn/za/act/1980/02/afr@", uri.expression_uri())

        uri = FrbrUri.parse("/akn/za/act/1980/02/afr@2014-01-01")
        assert_equal(uri.language, "afr")
        assert_equal(uri.expression_date, "@2014-01-01")
        assert_equal("/akn/za/act/1980/02", uri.work_uri())
        assert_equal("/akn/za/act/1980/02/afr@2014-01-01", uri.expression_uri())

        uri = FrbrUri.parse("/akn/za/act/1980/02/afr.html")
        assert_equal(uri.language, "afr")
        assert_equal(uri.format, 'html')

    def test_parse_expression_component_legacy(self):
        """ Legacy components without a ! are no longer supported.
        """
        with self.assertRaises(ValueError):
            FrbrUri.parse("/akn/za/act/1980/02/eng/main")

    def test_parse_work_component(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/eng/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.work_component, "main")

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng/!main~chp_2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.work_component, "main")
        assert_equal(uri.portion, "chp_2")

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng@/!main~chp_2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')
        assert_equal(uri.work_component, "main")
        assert_equal(uri.portion, "chp_2")

    def test_parse_expression_date(self):
        # A dangling @ indicates the very FIRST expression date, which
        # we represent with an empty string ('').
        # A URI without an @ at all, indicates the most recent
        # expression date, which is None.

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_uri(), '/akn/za/act/1980/02/eng')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng@")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')
        assert_equal(uri.expression_uri(), '/akn/za/act/1980/02/eng@')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng@/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng:/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, ':')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng:2012-01-01/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, ':2012-01-01')

    def test_parse_subtype_numeric_number(self):
        # A subtype with a numeric number should not be
        # mistaken for an actor
        uri = FrbrUri.parse("/akn/za-jhb/act/notice/2007/5319/eng@2007-12-05")
        assert_is_none(uri.actor)
        assert_equal(uri.date, "2007")
        assert_equal(uri.language, "eng")
        assert_equal(uri.number, "5319")
        assert_equal(uri.expression_date, "@2007-12-05")

    def test_parse_subtype_and_actor(self):
        uri = FrbrUri.parse("/akn/za-jhb/act/notice/actor/2007/5319/eng@2007-12-05")
        assert_equal(uri.actor, "actor")
        assert_equal(uri.date, "2007")
        assert_equal(uri.number, "5319")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, "@2007-12-05")

    def test_expression_uri(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/eng")
        uri.expression_date = '@2014-01-01'
        uri.work_component = 'main'
        uri.format = 'html'

        assert_equal("/akn/za/act/1980/02/eng@2014-01-01/!main", uri.expression_uri())

    def test_manifestation_uri(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/eng")
        uri.expression_date = '@2014-01-01'
        uri.work_component = 'main'
        uri.format = 'html'

        assert_equal("/akn/za/act/1980/02/eng@2014-01-01/!main.html", uri.manifestation_uri())

    def test_simple_prefix(self):
        # also recognises akn prefix
        uri = FrbrUri.parse("/akn/za/act/1980/01")
        assert_equal(uri.prefix, "akn")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, None)
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/akn/za/act/1980/01", uri.work_uri())

    def test_akn_prefix(self):
        # uses 'akn' prefix as the default when producing one
        uri = FrbrUri(
            country='za',
            locality='ec',
            doctype='act',
            subtype='by-law',
            date='2020',
            number='31',
            actor=None
        )
        assert_equal(uri.prefix, "akn")

        # doesn't use 'akn' prefix if explicitly told not to
        uri = FrbrUri(
            prefix=None,
            country='za',
            locality='ec',
            doctype='act',
            subtype='by-law',
            date='2020',
            number='31',
            actor=None
        )
        assert_is_none(uri.prefix)

    def test_parse_portion_no_component(self):
        uri = FrbrUri.parse("/akn/za/act/2005/5/~sec_5")
        assert_equal(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng/~sec_5")
        assert_equal(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng@2002-03-01/~sec_5")
        assert_equal(uri.portion, "sec_5")
        assert_equal(uri.expression_uri(), "/akn/za/act/2005/5/eng@2002-03-01/~sec_5")

    def test_parse_portion_no_component_format(self):
        uri = FrbrUri.parse("/akn/za/act/2005/5/~sec_5.html")
        assert_equal(uri.portion, "sec_5")
        assert_equal(uri.format, "html")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng/~sec_5.xml")
        assert_equal(uri.portion, "sec_5")
        assert_equal(uri.format, "xml")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng@2002-03-01/~sec_5.xml")
        assert_equal(uri.portion, "sec_5")
        assert_equal(uri.format, "xml")

    def test_parse_portion_component(self):
        uri = FrbrUri.parse("/akn/za/act/2005/5/!main~sec_5")
        assert_equal(uri.work_component, "main")
        assert_equal(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng/!schedule_3~sec_5")
        assert_equal(uri.work_component, "schedule_3")
        assert_equal(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng@2002-03-01/!main~sec_5")
        assert_equal(uri.work_component, "main")
        assert_equal(uri.portion, "sec_5")

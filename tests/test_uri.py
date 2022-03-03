from unittest import TestCase
from nose.tools import *

from cobalt.uri import FrbrUri


class FrbrUriTestCase(TestCase):
    def test_bad_value(self):
        assert_raises(ValueError, FrbrUri.parse, "/badness")
        assert_raises(ValueError, FrbrUri.parse, "/ukpga/2015/1")

    def test_simple(self):
        uri = FrbrUri.parse("/za/act/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, None)
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_is_none(uri.prefix)

        assert_equal("/za/act/1980/01", uri.work_uri())

    def test_with_subtype(self):
        uri = FrbrUri.parse("/za/act/by-law/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, None)
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "by-law")
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/za/act/by-law/1980/01", uri.work_uri())

    def test_with_locality(self):
        uri = FrbrUri.parse("/za-cpt/act/by-law/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.locality, "cpt")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "by-law")
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/za-cpt/act/by-law/1980/01", uri.work_uri())

    def test_with_subtype_and_actor(self):
        uri = FrbrUri.parse("/za/act/by-law/actor/1980/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, "by-law")
        assert_equal(uri.actor, "actor")
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/za/act/by-law/actor/1980/01", uri.work_uri())

    def test_with_long_date(self):
        uri = FrbrUri.parse("/za/act/1980-02-01/01")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980-02-01")
        assert_equal(uri.year, "1980")
        assert_equal(uri.number, "01")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/za/act/1980-02-01/01", uri.work_uri())

    def test_with_non_numeric_number(self):
        uri = FrbrUri.parse("/za/act/1980/nn")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "nn")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        assert_equal("/za/act/1980/nn", uri.work_uri())

    def test_with_work_component(self):
        uri = FrbrUri.parse("/za/act/1980/2/!schedule1")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.work_component, "schedule1")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, None)

        assert_equal("/za/act/1980/2", uri.uri())
        assert_equal("/za/act/1980/2/!schedule1", uri.work_uri())
        assert_equal("/za/act/1980/2/eng/!schedule1", uri.expression_uri())

    def test_with_nested_work_components(self):
        uri = FrbrUri.parse("/za/act/1980/2/!schedule1/schedule2/schedule3")
        assert_equal(uri.work_component, "schedule1/schedule2/schedule3")

    def test_with_work_component_legacy(self):
        uri = FrbrUri.parse("/za/act/1980/2/schedule1")
        assert_equal(uri.country, "za")
        assert_equal(uri.doctype, "act")
        assert_equal(uri.subtype, None)
        assert_equal(uri.actor, None)
        assert_equal(uri.date, "1980")
        assert_equal(uri.number, "2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.work_component, "schedule1")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, None)

        assert_equal("/za/act/1980/2", uri.uri())
        assert_equal("/za/act/1980/2/!schedule1", uri.work_uri())
        assert_equal("/za/act/1980/2/eng/!schedule1", uri.expression_uri())

    def test_with_short_work_component(self):
        uri = FrbrUri.parse("/za-wc/act/pn/2018/46/6")
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
        assert_equal(uri.expression_component, None)

        uri = FrbrUri.parse("/za-wc/act/2018/46/6")
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
        assert_equal(uri.expression_component, None)

    def test_with_work_and_expression_component(self):
        uri = FrbrUri.parse("/za/act/1980/2")
        uri.work_component = "main"
        uri.expression_component = "schedule1"
        uri.expression_subcomponent = "chapter/2"

        assert_equal("/za/act/1980/2", uri.uri())
        assert_equal("/za/act/1980/2/!main", uri.work_uri())
        assert_equal("/za/act/1980/2/eng/!schedule1/chapter/2", uri.expression_uri())

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
        uri = FrbrUri.parse("/za/act/1980/02/afr@")
        assert_equal(uri.language, "afr")
        assert_equal(uri.expression_date, '@')
        assert_equal("/za/act/1980/02", uri.work_uri())
        assert_equal("/za/act/1980/02/afr@", uri.expression_uri())

        uri = FrbrUri.parse("/za/act/1980/02/afr@2014-01-01")
        assert_equal(uri.language, "afr")
        assert_equal(uri.expression_date, "@2014-01-01")
        assert_equal("/za/act/1980/02", uri.work_uri())
        assert_equal("/za/act/1980/02/afr@2014-01-01", uri.expression_uri())

        uri = FrbrUri.parse("/za/act/1980/02/afr.html")
        assert_equal(uri.language, "afr")
        assert_equal(uri.format, 'html')

    def test_parse_expression_component_legacy(self):
        uri = FrbrUri.parse("/za/act/1980/02/eng/main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "main")

        uri = FrbrUri.parse("/za/act/1980/02/eng/main/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "chapter/2")

        uri = FrbrUri.parse("/za/act/1980/02/eng@/main/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "chapter/2")

        uri = FrbrUri.parse("/za/act/1980/02/eng@2014-01-01/main/schedule1")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, "@2014-01-01")
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "schedule1")

        uri = FrbrUri.parse("/za/act/1980/02/eng@2014-01-01/main/schedule1")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, "@2014-01-01")
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "schedule1")

        uri = FrbrUri.parse("/za/act/1980/02/eng/main/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "chapter/2")

        # this is a weird edge case
        uri = FrbrUri.parse("/za/act/1980/02/eng/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "chapter")
        assert_equal(uri.expression_subcomponent, "2")

    def test_parse_expression_component(self):
        uri = FrbrUri.parse("/za/act/1980/02/eng/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "main")

        uri = FrbrUri.parse("/za/act/1980/02/eng/!main/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "chapter/2")

        uri = FrbrUri.parse("/za/act/1980/02/eng@/!main/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "chapter/2")

        uri = FrbrUri.parse("/za/act/1980/02/eng@2014-01-01/!main/schedule1")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, "@2014-01-01")
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "schedule1")

        uri = FrbrUri.parse("/za/act/1980/02/eng@2014-01-01/!main/schedule1")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, "@2014-01-01")
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "schedule1")

        uri = FrbrUri.parse("/za/act/1980/02/eng/!main/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "main")
        assert_equal(uri.expression_subcomponent, "chapter/2")

        # this is a weird edge case
        uri = FrbrUri.parse("/za/act/1980/02/eng/chapter/2")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_component, "chapter")
        assert_equal(uri.expression_subcomponent, "2")

    def test_parse_expression_date(self):
        # A dangling @ indicates the very FIRST expression date, which
        # we represent with an empty string (''). 
        # A URI without an @ at all, indicates the most recent
        # expression date, which is None.

        uri = FrbrUri.parse("/za/act/1980/02/eng")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)
        assert_equal(uri.expression_uri(), '/za/act/1980/02/eng')

        uri = FrbrUri.parse("/za/act/1980/02/eng/main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, None)

        uri = FrbrUri.parse("/za/act/1980/02/eng@")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')
        assert_equal(uri.expression_uri(), '/za/act/1980/02/eng@')

        uri = FrbrUri.parse("/za/act/1980/02/eng@/main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')

        uri = FrbrUri.parse("/za/act/1980/02/eng:/main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, ':')

        uri = FrbrUri.parse("/za/act/1980/02/eng:2012-01-01/main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, ':2012-01-01')

        uri = FrbrUri.parse("/za/act/1980/02/eng@/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, '@')

        uri = FrbrUri.parse("/za/act/1980/02/eng:/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, ':')

        uri = FrbrUri.parse("/za/act/1980/02/eng:2012-01-01/!main")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, ':2012-01-01')

    def test_parse_subtype_numeric_number(self):
        # A subtype with a numeric number should not be
        # mistaken for an actor
        uri = FrbrUri.parse("/za-jhb/act/notice/2007/5319/eng@2007-12-05")
        assert_is_none(uri.actor)
        assert_equal(uri.date, "2007")
        assert_equal(uri.language, "eng")
        assert_equal(uri.number, "5319")
        assert_equal(uri.expression_date, "@2007-12-05")

    def test_parse_subtype_and_actor(self):
        uri = FrbrUri.parse("/za-jhb/act/notice/actor/2007/5319/eng@2007-12-05")
        assert_equal(uri.actor, "actor")
        assert_equal(uri.date, "2007")
        assert_equal(uri.number, "5319")
        assert_equal(uri.language, "eng")
        assert_equal(uri.expression_date, "@2007-12-05")

    def test_expression_uri(self):
        uri = FrbrUri.parse("/za/act/1980/02/eng")
        uri.expression_date = '@2014-01-01'
        uri.expression_component = 'main'
        uri.format = 'html'

        assert_equal("/za/act/1980/02/eng@2014-01-01/!main", uri.expression_uri())

        uri.expression_subcomponent = "chapter/2"
        assert_equal("/za/act/1980/02/eng@2014-01-01/!main/chapter/2", uri.expression_uri())

    def test_manifestation_uri(self):
        uri = FrbrUri.parse("/za/act/1980/02/eng")
        uri.expression_date = '@2014-01-01'
        uri.expression_component = 'main'
        uri.format = 'html'

        assert_equal("/za/act/1980/02/eng@2014-01-01/!main.html", uri.manifestation_uri())

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

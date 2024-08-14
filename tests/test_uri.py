from unittest import TestCase

from cobalt.uri import FrbrUri


class FrbrUriTestCase(TestCase):
    def test_bad_value(self):
        self.assertRaises(ValueError, FrbrUri.parse, "/badness")
        self.assertRaises(ValueError, FrbrUri.parse, "/ukpga/2015/1")

    def test_simple(self):
        uri = FrbrUri.parse("/akn/za/act/1980/01")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.locality, None)
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "01")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)
        self.assertEqual(uri.prefix, "akn")

        self.assertEqual("/akn/za/act/1980/01", uri.work_uri())

    def test_with_subtype(self):
        uri = FrbrUri.parse("/akn/za/act/by-law/1980/01")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.locality, None)
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, "by-law")
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "01")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/by-law/1980/01", uri.work_uri())

    def test_with_locality(self):
        uri = FrbrUri.parse("/akn/za-cpt/act/by-law/1980/01")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.locality, "cpt")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, "by-law")
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "01")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za-cpt/act/by-law/1980/01", uri.work_uri())

    def test_with_subtype_and_actor(self):
        uri = FrbrUri.parse("/akn/za/act/by-law/actor/1980/01")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, "by-law")
        self.assertEqual(uri.actor, "actor")
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "01")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/by-law/actor/1980/01", uri.work_uri())

    def test_with_long_date(self):
        uri = FrbrUri.parse("/akn/za/act/1980-02-01/01")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980-02-01")
        self.assertEqual(uri.year, "1980")
        self.assertEqual(uri.number, "01")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/1980-02-01/01", uri.work_uri())

    def test_with_non_numeric_number(self):
        uri = FrbrUri.parse("/akn/za/act/1980/nn")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "nn")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/1980/nn", uri.work_uri())

    def test_with_work_component(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2/!schedule1")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "2")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.work_component, "schedule1")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/1980/2", uri.uri())
        self.assertEqual("/akn/za/act/1980/2/!schedule1", uri.work_uri())
        self.assertEqual("/akn/za/act/1980/2/eng/!schedule1", uri.expression_uri())

    def test_with_nested_work_components(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2/!schedule1/schedule2/schedule3")
        self.assertEqual(uri.work_component, "schedule1/schedule2/schedule3")

    def test_with_work_component_legacy(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2/!schedule1")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "2")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.work_component, "schedule1")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/1980/2", uri.uri())
        self.assertEqual("/akn/za/act/1980/2/!schedule1", uri.work_uri())
        self.assertEqual("/akn/za/act/1980/2/eng/!schedule1", uri.expression_uri())

    def test_with_short_work_component(self):
        uri = FrbrUri.parse("/akn/za-wc/act/pn/2018/46/!6")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.locality, "wc")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, "pn")
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "2018")
        self.assertEqual(uri.number, "46")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.work_component, "6")
        self.assertEqual(uri.expression_date, None)

        uri = FrbrUri.parse("/akn/za-wc/act/2018/46/!6")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.locality, "wc")
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "2018")
        self.assertEqual(uri.number, "46")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.work_component, "6")
        self.assertEqual(uri.expression_date, None)

    def test_with_work_component_and_portion(self):
        uri = FrbrUri.parse("/akn/za/act/1980/2")
        uri.work_component = "main/schedule_1"
        uri.portion = "chp_2"

        self.assertEqual("/akn/za/act/1980/2", uri.uri())
        self.assertEqual("/akn/za/act/1980/2/!main/schedule_1", uri.work_uri())
        self.assertEqual("/akn/za/act/1980/2/eng/!main/schedule_1~chp_2", uri.expression_uri())

    def test_parse_expression2(self):
        uri = FrbrUri.parse("/gh/act/2020/1013/eng@2020-04-03")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, '@2020-04-03')
        self.assertEqual(uri.number, '1013')
        self.assertIsNone(uri.subtype)

    def test_expression_string_no_language(self):
        uri = FrbrUri.parse("/gh/act/2020/1013/")
        self.assertEqual(uri.language, "eng")
        uri.language = None
        with self.assertRaises(ValueError) as e:
            uri.expression_uri()
        err = e.exception
        self.assertEqual(str(err), "Expression URI requires a language.")

    def test_parse_expression(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/afr@")
        self.assertEqual(uri.language, "afr")
        self.assertEqual(uri.expression_date, '@')
        self.assertEqual("/akn/za/act/1980/02", uri.work_uri())
        self.assertEqual("/akn/za/act/1980/02/afr@", uri.expression_uri())

        uri = FrbrUri.parse("/akn/za/act/1980/02/afr@2014-01-01")
        self.assertEqual(uri.language, "afr")
        self.assertEqual(uri.expression_date, "@2014-01-01")
        self.assertEqual("/akn/za/act/1980/02", uri.work_uri())
        self.assertEqual("/akn/za/act/1980/02/afr@2014-01-01", uri.expression_uri())

        uri = FrbrUri.parse("/akn/za/act/1980/02/afr.html")
        self.assertEqual(uri.language, "afr")
        self.assertEqual(uri.format, 'html')

    def test_parse_expression_component_legacy(self):
        """ Legacy components without a ! are no longer supported.
        """
        with self.assertRaises(ValueError):
            FrbrUri.parse("/akn/za/act/1980/02/eng/main")

    def test_parse_work_component(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/eng/!main")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)
        self.assertEqual(uri.work_component, "main")

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng/!main~chp_2")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)
        self.assertEqual(uri.work_component, "main")
        self.assertEqual(uri.portion, "chp_2")

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng@/!main~chp_2")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, '@')
        self.assertEqual(uri.work_component, "main")
        self.assertEqual(uri.portion, "chp_2")

    def test_parse_expression_date(self):
        # A dangling @ indicates the very FIRST expression date, which
        # we represent with an empty string ('').
        # A URI without an @ at all, indicates the most recent
        # expression date, which is None.

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)
        self.assertEqual(uri.expression_uri(), '/akn/za/act/1980/02/eng')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng/!main")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng@")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, '@')
        self.assertEqual(uri.expression_uri(), '/akn/za/act/1980/02/eng@')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng@/!main")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, '@')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng:/!main")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, ':')

        uri = FrbrUri.parse("/akn/za/act/1980/02/eng:2012-01-01/!main")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, ':2012-01-01')

    def test_parse_subtype_numeric_number(self):
        # A subtype with a numeric number should not be
        # mistaken for an actor
        uri = FrbrUri.parse("/akn/za-jhb/act/notice/2007/5319/eng@2007-12-05")
        self.assertIsNone(uri.actor)
        self.assertEqual(uri.date, "2007")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.number, "5319")
        self.assertEqual(uri.expression_date, "@2007-12-05")

    def test_parse_subtype_and_actor(self):
        uri = FrbrUri.parse("/akn/za-jhb/act/notice/actor/2007/5319/eng@2007-12-05")
        self.assertEqual(uri.actor, "actor")
        self.assertEqual(uri.date, "2007")
        self.assertEqual(uri.number, "5319")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, "@2007-12-05")

    def test_expression_uri(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/eng")
        uri.expression_date = '@2014-01-01'
        uri.work_component = 'main'
        uri.format = 'html'

        self.assertEqual("/akn/za/act/1980/02/eng@2014-01-01/!main", uri.expression_uri())

    def test_manifestation_uri(self):
        uri = FrbrUri.parse("/akn/za/act/1980/02/eng")
        uri.expression_date = '@2014-01-01'
        uri.work_component = 'main'
        uri.format = 'html'

        self.assertEqual("/akn/za/act/1980/02/eng@2014-01-01/!main.html", uri.manifestation_uri())

    def test_simple_prefix(self):
        # also recognises akn prefix
        uri = FrbrUri.parse("/akn/za/act/1980/01")
        self.assertEqual(uri.prefix, "akn")
        self.assertEqual(uri.country, "za")
        self.assertEqual(uri.locality, None)
        self.assertEqual(uri.doctype, "act")
        self.assertEqual(uri.subtype, None)
        self.assertEqual(uri.actor, None)
        self.assertEqual(uri.date, "1980")
        self.assertEqual(uri.number, "01")
        self.assertEqual(uri.language, "eng")
        self.assertEqual(uri.expression_date, None)

        self.assertEqual("/akn/za/act/1980/01", uri.work_uri())

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
        self.assertEqual(uri.prefix, "akn")

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
        self.assertIsNone(uri.prefix)

    def test_parse_portion_no_component(self):
        uri = FrbrUri.parse("/akn/za/act/2005/5/~sec_5")
        self.assertEqual(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng/~sec_5")
        self.assertEqual(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng@2002-03-01/~sec_5")
        self.assertEqual(uri.portion, "sec_5")
        self.assertEqual(uri.expression_uri(), "/akn/za/act/2005/5/eng@2002-03-01/~sec_5")

    def test_parse_portion_no_component_format(self):
        uri = FrbrUri.parse("/akn/za/act/2005/5/~sec_5.html")
        self.assertEqual(uri.portion, "sec_5")
        self.assertEqual(uri.format, "html")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng/~sec_5.xml")
        self.assertEqual(uri.portion, "sec_5")
        self.assertEqual(uri.format, "xml")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng@2002-03-01/~sec_5.xml")
        self.assertEqual(uri.portion, "sec_5")
        self.assertEqual(uri.format, "xml")

    def test_parse_portion_component(self):
        uri = FrbrUri.parse("/akn/za/act/2005/5/!main~sec_5")
        self.assertEqual(uri.work_component, "main")
        self.assertEqual(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng/!schedule_3~sec_5")
        self.assertEqual(uri.work_component, "schedule_3")
        self.assertEqual(uri.portion, "sec_5")

        uri = FrbrUri.parse("/akn/za/act/2005/5/eng@2002-03-01/!main~sec_5")
        self.assertEqual(uri.work_component, "main")
        self.assertEqual(uri.portion, "sec_5")

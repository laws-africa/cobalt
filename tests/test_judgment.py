from unittest import TestCase
from nose.tools import *  # noqa

from cobalt import Judgment


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

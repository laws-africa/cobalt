from unittest import TestCase

from cobalt import Judgment


class JudgmentTestCase(TestCase):
    maxDiff = None

    def test_empty_judgment(self):
        j = Judgment()
        self.assertEqual(j.title, "Untitled")
        self.assertIsNotNone(j.meta)
        self.assertIsNotNone(j.judgmentBody)

    def test_empty_body(self):
        j = Judgment()
        self.assertNotEqual(j.judgmentBody.text, '')

    def test_main(self):
        j = Judgment()
        self.assertEqual(j.main, j.judgment)

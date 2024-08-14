from unittest import TestCase

from cobalt import Debate


class DebateTestCase(TestCase):
    maxDiff = None

    def test_empty_debate(self):
        d = Debate()
        self.assertEqual(d.title, "Untitled")
        self.assertIsNotNone(d.meta)
        self.assertIsNotNone(d.debateBody)

    def test_empty_body(self):
        d = Debate()
        self.assertNotEqual(d.debateBody.text, '')

    def test_main(self):
        d = Debate()
        self.assertEqual(d.main, d.debate)

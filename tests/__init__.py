import os

from lxml import etree


_schema = None


def assert_validates(akn_doc):
    """ Assert that this akn document validates against the AKN schema.
    """
    global _schema

    if not _schema:
        fname = os.path.join(os.path.dirname(__file__), '..', 'cobalt', 'xsd', 'akomantoso30.xsd')
        with open(fname) as f:
            _schema = etree.XMLSchema(etree.parse(f))
    _schema.assertValid(akn_doc.root)

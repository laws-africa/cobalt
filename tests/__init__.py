import os

from lxml import etree


_schema = None

def assertValidates(akn_doc):
    global _schema

    if not _schema:
        fname = os.path.join(os.path.dirname(__file__), '..', 'cobalt', 'xsd', 'akomantoso30.xsd')
        with open(fname) as f:
            _schema = etree.XMLSchema(etree.parse(f))
    _schema.assertValid(akn_doc.root)

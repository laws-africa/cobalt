from cobalt.schemas import get_schema


def assert_validates(akn_doc, strict=False):
    """ Assert that this akn document validates against the AKN schema.
    """
    schema = get_schema(akn_doc.namespace, strict)
    schema.assertValid(akn_doc.root)

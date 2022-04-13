Cobalt
======

.. image:: https://badge.fury.io/py/cobalt.svg
    :target: http://badge.fury.io/py/cobalt

.. image:: https://travis-ci.org/laws-africa/cobalt.svg
    :target: http://travis-ci.org/laws-africa/cobalt

Cobalt is a lightweight Python library for working with `Akoma Ntoso <http://www.akomantoso.org/>`_ documents.
It makes it easy to work with Akoma Ntoso documents, metadata and FRBR URIs.

It is lightweight because most operations are done on the XML document directly without intermediate
objects. You still need to understand how Akoma Ntoso works.

Read the `full documentation at cobalt.readthedocs.io <http://cobalt.readthedocs.io/en/latest/>`_.

Quickstart
----------

Install using::

    $ pip install cobalt

Use it like this::

    >>> from cobalt import Act
    >>> act = Act()
    >>> act.title = "Act 10 of 1980"
    >>> act.frbr_uri = "/za/act/1980-05-03/10"
    >>> act.frbr_uri.year
    '1980'
    >>> act.frbr_uri.date
    '1980-05-03'
    >>> act.frbr_uri.number
    '10'
    >>> act.frbr_uri.doctype
    'act'
    >>> print act.to_xml()
    [ lots of xml ]

Contributing
------------

1. Clone the repo
2. Install development dependencies::

    pip install -e .[dev]

3. Make your changes
4. Run tests::

    nosetests && flake8 cobalt

5. Send a pull request

Releasing a New Version
-----------------------

1. Run the tests!
2. Update VERSION appropriately
3. Update the Change Log section in README.rst
4. Commit and tag::

    git tag vX.X.X
    git push -u origin --tags

5. Build artefacts::

    rm -rf build dist && python setup.py sdist bdist_wheel

6. Upload to PyPI::

    twine upload dist/*

License and Copyright
---------------------

Cobalt is licensed under the LPGL 3.0 license.

Cobalt is Copyright 2015-2020 AfricanLII.

Change Log
----------

5.0.0
-----

- Allow slashes in FRBR URI work component names
- Setting expression and manifestation dates updates attachments and other components
- Don't include Cobalt-specific ``<references>`` element in attachments
- Cascade changes to FRBRlanguage into attachments
- Don't hardcode source
- Don't set ``contains="originalVersion"`` since it is the default value for that attribute.
- Use ``0001-01-01`` as a placeholder date for publication, amendment and repeal events with null dates

4.1.1
.....

- Change eIds of content produced by empty_document_content()

4.1.0
.....

- Allow setting of missing component names

4.0.2
.....

- Better error handling when parsing malformed XML.

4.0.1
.....

(replaced by 4.0.2)

4.0.0
.....

- Support AKN 3.0 namespaces
- Produce URIs with ``akn`` prefix by default (backwards compatibility maintained)
- Support all Akoma Ntoso document types
- Start FRBR URI work component with ``!`` (eg. ``!main``)
- FRBRcountry uses full country code from the FRBR URI
- FRBRnumber uses number portion from FRBR URI
- FRBRdate for FRBRWork contains the date portion of the FRBR URI
- Include AKN 3.0 schema and support for validating against the schema
- The elements returned by ``components()`` are now ``attachment`` or ``component`` elements, not the inner ``doc``

3.1.1
.....

- FIX issue where a four-digit number in an FRBR URI confuses the parser

3.1.0
.....

- Replace arrow with iso8601, avoiding `arrow issue 612 <https://github.com/crsmithdev/arrow/issues/612>`_

3.0.0
.....

- Python 3.6 and 3.7 support
- Drop support for Python 2.x

2.2.0
.....

- FIX don't mistake numbers in uris with subtypes and numeric numbers as actors
- FIX link to GitHub
- Unicode literals when parsing FRBR URIs

2.1.0
.....

- FIX don't strip empty whitespace during objectify.fromstring

2.0.0
.....

- FIX don't pretty-print XML, it introduces meaningful whitespace

1.0.1
.....

- FIX FrbrUri clone bug when a URI had a language.

1.0.0
.....

- Move table of contents, render and other locale (legal tradition) specific functionality out of Cobalt.
- FIX bug that returned the incorrect language when extracting a document's expression URI.

0.3.2
.....

- Inject original img src as data-src

0.3.1
.....

- Support for i18n in XSLT files, including all 11 South African languages from myconstitution.co.za

0.3.0
.....

- Support for images
- Change how XSLT params are passed to the renderer
- Add expression_frbr_uri method to Act class

0.2.1
.....

- When rendering HTML, ensure primary container elements and schedules have appropriate ids

0.2.0
.....

- When rendering HTML, scope component/schedule ids to ensure they're unique

0.1.11
......

- Render ref elements as HTML a elements
- Optionally prepend a resolver URL before a elements

0.1.10
......

- Convert EOL elements to BR when changing XML to HTML

0.1.9
.....

- Support dates before 1900. Contributed by rkunal.

0.1.8
.....

- lifecycle and identification meta elements now have a configurable source attribute

0.1.7
.....

- TOCElement items now include a best-effort title

0.1.6
.....

- Use HTML5 semantic elements section and article when generating HTML for acts

0.1.5
.....

- FIX use schedule FRBRalias as heading

0.1.4
.....

- Transforming XML to HTML now includes all attributes as data- attributes

0.1.3
.....

- Refactor TOC helpers into own file
- Fix .format in FrbrUri

0.1.1
.....

- first release

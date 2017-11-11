Cobalt
======

.. image:: https://badge.fury.io/py/cobalt.svg
    :target: http://badge.fury.io/py/cobalt

.. image:: https://travis-ci.org/OpenUpSA/cobalt.svg
    :target: http://travis-ci.org/OpenUpSA/cobalt

Cobalt is a lightweight Python library for working with `Akoma Ntoso <http://www.akomantoso.org/>`_ Act documents.
It makes it easy to work with Akoma Ntoso metadata, FRBR URIs and generate Tables of Contents for a document.

It is lightweight because most operations are done on the XML document directly without intermediate
objects. You still need to understand how Akoma Ntoso works.

Read the `full documentation at cobalt.readthedocs.org <http://cobalt.readthedocs.org/en/latest/>`_.

Quickstart
----------

Install using::

    $ pip install cobalt

Use it like this::

    >>> from cobalt import Act
    >>> act = Act()
    >>> act.title = "Act 10 of 1980"
    >>> act.frbr_uri = "/za/act/1980/10"
    >>> act.year
    '1980'
    >>> act.number
    '10'
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
4. Commit and push to github
5. Release to PyPI::

    python setup.py sdist bdist_wheel upload
    
License and Copyright
---------------------

Cobalt is licensed under the LPGL 3.0 license.

Cobalt is Copyright 2015-2017 AfricanLII.

Change Log
----------

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

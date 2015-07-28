Cobalt
======

Cobalt is a lightweight Python library for working with `Akoma Ntoso <http://www.akomantoso.org/>`_ Act documents.
It makes it easy to work with Akoma Ntoso metadata, FRBR URIs and generate Tables of Contents for a document.

It is lightweight because most operations are done on the XML document directly without intermediate
objects. You still need to understand how Akoma Ntoso works.

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
    >> act.number
    '10'
    >> print act.to_xml()
    [ lots of xml ]

Contributing
------------

1. Clone the repo
2. Install development dependencies::

    pip install -e .[dev]

3. Make your changes
4. Run tests::

    nosetests && flake8

5. Send a pull request

Change Log
----------

* 0.1.0 - first release

Contents
--------

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

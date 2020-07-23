Cobalt
======

Cobalt is a lightweight Python library for working with `Akoma Ntoso <http://www.akomantoso.org/>`_ documents.
It makes it easy to work with Akoma Ntoso metadata and FRBR URIs.

Cobalt is lightweight because most operations are done on the XML document directly without intermediate
objects. You still need to understand how Akoma Ntoso works.

Contribute to Cobalt on GitHub at `github.com/laws-africa/cobalt <https://github.com/laws-africa/cobalt>`_.

Quickstart
----------

Install using::

    $ pip install cobalt

Use it like this::

    >>> from cobalt import Act
    >>> act = Act()
    >>> act.title = "Act 10 of 1980"
    >>> act.frbr_uri = "/za/act/1980/10"
    >>> act.frbr_uri.year
    '1980'
    >>> act.frbr_uri.date
    '1980-05-03'
    >>> act.number
    '10'
    >>> act.frbr_uri.doctype
    'act'
    >>> print act.to_xml()
    [ lots of xml ]

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

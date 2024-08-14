# Cobalt

![image](https://laws.africa/img/icons/cobalt.png)

[![image](https://badge.fury.io/py/cobalt.svg)](http://badge.fury.io/py/cobalt)

Cobalt is a lightweight Python library for working with [Akoma Ntoso](http://www.akomantoso.org/) documents. It makes it
easy to work with Akoma Ntoso documents, metadata and FRBR URIs.

It is lightweight because most operations are done on the XML document directly without intermediate objects. You still
need to understand how Akoma Ntoso works.

Read the [full documentation at cobalt.readthedocs.io](http://cobalt.readthedocs.io/en/latest/).

## Quickstart

Install using:

    $ pip install cobalt

Use it like this:

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

## Contributing

1.  Clone the repo
2.  Install development dependencies:

        pip install -e .[dev]

3.  Make your changes
4.  Run tests:

        nosetests && flake8 cobalt

5.  Send a pull request

## Releasing a new version

1. Run the tests with `python -m unittest`
2. Update the version by changing the `__version__` variable in [`cobalt/__init__.py`](cobalt/__init__.py)
3. Commit your changes and push to the master branch on GitHub
4. Create a release in GitHub and it will automatically be pushed to PyPi

# License

Cobalt is licensed under the LPGL 3.0 license.

Copyright 2015-2020 AfricanLII.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

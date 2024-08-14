# Change Log

## 9.0.0

-   Dropped support for Python < 3.10 (no other changes)

## 8.0.0

-   Parser now accepts both strings and bytes, and will encode strings to bytes using UTF-8

## 7.0.0

-   Rename `DebateReport` to `Debate`

## 6.1.0

-   Add new schemas.AkomaNtoso30 class with basic schema information

## 6.0.0

-   Add support for portions, such as `~chp_2`
-   Remove non-standard support for expression component and
    subcomponent
-   Remove non-standard legacy support for work components without `!`

## 5.0.0

-   Allow slashes in FRBR URI work component names
-   Setting expression and manifestation dates updates attachments and
    other components
-   Don\'t include Cobalt-specific `<references>` element in attachments
-   Cascade changes to FRBRlanguage into attachments
-   Don\'t hardcode source
-   Don\'t set `contains="originalVersion"` since it is the default
    value for that attribute.
-   Use `0001-01-01` as a placeholder date for publication, amendment
    and repeal events with null dates

## 4.1.1

-   Change eIds of content produced by empty_document_content()

## 4.1.0

-   Allow setting of missing component names

## 4.0.2

-   Better error handling when parsing malformed XML.

## 4.0.1

(replaced by 4.0.2)

## 4.0.0

-   Support AKN 3.0 namespaces
-   Produce URIs with `akn` prefix by default (backwards compatibility
    maintained)
-   Support all Akoma Ntoso document types
-   Start FRBR URI work component with `!` (eg. `!main`)
-   FRBRcountry uses full country code from the FRBR URI
-   FRBRnumber uses number portion from FRBR URI
-   FRBRdate for FRBRWork contains the date portion of the FRBR URI
-   Include AKN 3.0 schema and support for validating against the schema
-   The elements returned by `components()` are now `attachment` or
    `component` elements, not the inner `doc`

## 3.1.1

-   FIX issue where a four-digit number in an FRBR URI confuses the
    parser

## 3.1.0

-   Replace arrow with iso8601, avoiding [arrow issue
    612](https://github.com/crsmithdev/arrow/issues/612)

## 3.0.0

-   Python 3.6 and 3.7 support
-   Drop support for Python 2.x

## 2.2.0

-   FIX don\'t mistake numbers in uris with subtypes and numeric numbers
    as actors
-   FIX link to GitHub
-   Unicode literals when parsing FRBR URIs

## 2.1.0

-   FIX don\'t strip empty whitespace during objectify.fromstring

## 2.0.0

-   FIX don\'t pretty-print XML, it introduces meaningful whitespace

## 1.0.1

-   FIX FrbrUri clone bug when a URI had a language.

## 1.0.0

-   Move table of contents, render and other locale (legal tradition)
    specific functionality out of Cobalt.
-   FIX bug that returned the incorrect language when extracting a
    document\'s expression URI.

## 0.3.2

-   Inject original img src as data-src

## 0.3.1

-   Support for i18n in XSLT files, including all 11 South African
    languages from myconstitution.co.za

## 0.3.0

-   Support for images
-   Change how XSLT params are passed to the renderer
-   Add expression_frbr_uri method to Act class

## 0.2.1

-   When rendering HTML, ensure primary container elements and schedules
    have appropriate ids

## 0.2.0

-   When rendering HTML, scope component/schedule ids to ensure they\'re
    unique

## 0.1.11

-   Render ref elements as HTML a elements
-   Optionally prepend a resolver URL before a elements

## 0.1.10

-   Convert EOL elements to BR when changing XML to HTML

## 0.1.9

-   Support dates before 1900. Contributed by rkunal.

## 0.1.8

-   lifecycle and identification meta elements now have a configurable
    source attribute

## 0.1.7

-   TOCElement items now include a best-effort title

## 0.1.6

-   Use HTML5 semantic elements section and article when generating HTML
    for acts

## 0.1.5

-   FIX use schedule FRBRalias as heading

## 0.1.4

-   Transforming XML to HTML now includes all attributes as data-
    attributes

## 0.1.3

-   Refactor TOC helpers into own file
-   Fix .format in FrbrUri

## 0.1.1

-   first release

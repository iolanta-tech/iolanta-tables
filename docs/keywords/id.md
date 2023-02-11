---
title: "$id"
---

Defines a unique identifier for something. Identifiers are case sensitive. For instance:

Our cats table is now globally identified as `my-cats`. You can render it on any page of the site by this name:

{{ render('my-cats', environments='side-by-side') }}

## Other uses

Unique identifiers can be assigned to rows, columns, and generally to any node of Iolanta graph. For instance:

{{ render('arda-countries', environments='side-by-side') }}

Here, `country-name` becomes a global identifier. Check {{ render('render') }} to see how to use it.

## Prefixes

Identifiers can have prefixes. For instance, `table:columns` is an identifier which has `table:` prefix. That prefix is associated with a URL:

* `table:` = `https://mkdocs.iolanta.tech/tables/`
* and therefore `table:columns` = `https://mkdocs.iolanta.tech/tables/columns`

whence you can find a page describing what `table:columns` really means ;)

This *self-documenting* trait of identifiers is widely used in Iolanta ecosystem.

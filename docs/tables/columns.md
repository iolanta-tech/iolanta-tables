---
title: "table:columns"
hide:
  - toc
---

List columns of a table. Order is preserved.

## Shorthand form

{{ code("samples/simple.yaml", language="yaml", first_line=2, last_line=6) }}

Every column listed in this format is a global identifier (is interpreted as [`$id`](../id/)). However, in this form you cannot define `title` or other properties of a column. For that, the longhand form is required.

## Lengthy form

{{ code("samples/arda-countries.yaml", language="yaml", first_line=2, last_line=5) }}

The nature of `country-name` as a global identifier is now revealed.

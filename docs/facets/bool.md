---
title: Bool
$included:
  $id: bool-table
  table:columns:
    - boolean-value
  table:rows:
    - boolean-value: true
    - boolean-value: false
    - boolean-value: yes
    - boolean-value: no
---

Render boolean values.

{{ render('bool-table', environments='side-by-side') }}

## Code

::: iolanta.facets.html.bool_literal.BoolLiteral

---
title: "table:self"
hide:
  - toc
---

Use this as a column (in {{ render("table:columns") }} and perhaps in {{ render("table:order-by") }}) to render a representation of the whole row instead of a particular column.

{{ render("self", environments="side-by-side") }}

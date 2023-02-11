---
title: "table:rows"
hide:
  - toc
---

Provide data for the table as list of rows, where every row specifies values per column:

{{ code("samples/simple.yaml", language="yaml", first_line=7, last_line=14) }}

If a value for a column is missing, it will be rendered as empty. If an extra column (not listed in `table:columns`) is provided then it will be ignored in this table. (But it can be rendered in other tables or other widgets.)

{{ render("several-planets", environments="side-by-side") }}

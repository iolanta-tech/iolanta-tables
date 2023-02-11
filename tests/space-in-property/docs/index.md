---
title: invalid frontmatter

$id: table
table:columns:
  - title with space
table:rows:
  - title with space: foo
---

{{ render('table') }}

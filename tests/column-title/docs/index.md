---
$id: table

table:columns:
  - $id: foo
    title: FOO

table:rows:
  - foo: bar
---

{{ render('table') }}

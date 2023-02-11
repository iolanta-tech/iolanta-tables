---
$id: table
table:class: Foo
table:columns:
  - table:self
  - name

$included:
  - $type: Foo
    title: Badoom
    name: boo
---

{{ render('table') }}

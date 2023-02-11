---
title: "mkdocs:url"
$included:
  $id: link-table
  table:columns:
    - link
  table:rows:
    - link:
        title: boo
        mkdocs:url: https://boo.com
---

Assign a URL to something and then render it with a clickable link.

{{ render('link-table', environments='side-by-side') }}

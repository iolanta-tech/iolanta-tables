---
$id: render
title: "{{ render(…) }}"
---

Render a link to an MkDocs page, a table, or any other object in `mkdocs-iolanta` ecosystem by its identifier.

```jinja2
{% raw %}
{{ render('country-name') }}
{% endraw %}
```

⇒

{{ render('country-name') }}

The system automatically determines type of the referenced object and the methods to render it with.

## `macros` plugin

`mkdocs-macros-plugin` must be configured at `mkdocs.yml` for `render()` to work. See {{ render('install') }} for details.

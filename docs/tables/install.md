---
title: Installation
$id: install
---

```shell
pip install mkdocs-iolanta-tables
```

## Configuration

```yaml hl_lines="5" title="mkdocs.yml"
# …
plugins:
  - search
  - # … whatever you want
  - mkdocs-iolanta-tables
  - macros:
      on_error_fail: true
      modules:
        - mkdocs_iolanta.macros
```

---
title: mkdocs-iolanta-tables
hide:
  - toc
---

While Markdown is a very readable and lightweight document format, one of its weak points are **tables**. Markdown table formatting is hard, and a table once written is hard to change. Some Markdown users even give up and write their tables in HTML.

This plugin for [MkDocs](https://mkdocs.org) provides facilities to specify table data and formats using simple [YAML](https://yaml.org) markup.

## Demo

I've got two cats.

{{ render("my-cats", environments='side-by-side') }}


Let's look deeper into the code underneath that table.

{{ code("samples/simple.yaml", language="yaml", annotations=[
    "Unique ID of your table. By this ID, you can call the table at any place on the site.",
    "List of columns in its simplest form. Order of columns is preserved.",
    "Data to build the table from. Order is **not** preserved.",
    "Column(s) to order the data by."
]) }}


Want some more? See {{ render('install') }}.

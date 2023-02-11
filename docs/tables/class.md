---
title: "table:class"
---

Just as `{{ render("table:rows") }}`, this keyword permits to specify data for the table, but it does so from a different perspective.

{{ render("jedi", environments="side-by-side") }}

Here, we define several objects of `Jedi` class using `$type` keyword. Having done that, we can instruct the table to render all instances of that class.

Note that we don't have to **define** the class itself anyhow. The system is smart enough to guess that `Jedi` is a class from the fact that we used it for `$type` keyword.

"""MkDocs macros for the documentation site."""
import functools
import textwrap
from pathlib import Path
from typing import List, Optional

from mkdocs_macros.plugin import MacrosPlugin

CODE_TEMPLATE = """
```{language} title="{title}"
{code}
```

{annotations}
"""


def format_annotations(annotations: List[str]) -> str:
    """Format annotations for mkdocs-material to accept them."""
    enumerated_annotations = enumerate(annotations, start=1)

    return '\n\n'.join(
        f'{number}. {annotation}'
        for number, annotation in enumerated_annotations
    )


def code(
    path: str,
    docs_dir: Path,
    language: Optional[str] = None,
    title: Optional[str] = None,
    annotations: Optional[List[str]] = None,
    indent: int = 0,
    first_line: Optional[int] = 0,
    last_line: Optional[int] = -1,
):
    code_content = (docs_dir / path).read_text()

    if first_line or last_line != -1:
        lines = code_content.split('\n')[first_line:last_line]

        if first_line:
            lines.insert(0, '# ✂ ⋯⋯⋯⋯⋯⋯⋯⋯⋯')

        if last_line != '-1':
            lines.append('# ✂ ⋯⋯⋯⋯⋯⋯⋯⋯⋯')

        code_content = '\n'.join(lines)

    rendered_content = CODE_TEMPLATE.format(
        language=language,
        code=code_content,
        title=title or path,
        annotations=format_annotations(annotations or []),
    )

    if indent:
        rendered_content = textwrap.indent(
            rendered_content,
            prefix=' ' * indent,
        )

    return rendered_content


def define_env(env: MacrosPlugin):
    """Hook function."""
    env.macro(
        functools.partial(
            code,
            docs_dir=Path(env.conf['docs_dir']),
        ),
        name='code',
    )

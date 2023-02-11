from pathlib import Path
from typing import Any, Dict

from deepmerge import always_merger
from iolanta.conversions import path_to_url
from mkdocs.config import Config
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs_iolanta.mixins import OctadocsMixin

from iolanta_tables.models import TABLE


class TablesPlugin(OctadocsMixin):
    """Render an HTML table from data presented in the graph."""

    namespaces = {
        'table': TABLE,
    }

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def context_url(self) -> str:
        path = Path(__file__).parent / 'yaml/ctx.yaml'
        return f'file://{path}'

    def on_config(self, config, **kwargs):
        """Adjust configuration."""
        super().on_config(config, **kwargs)

        # Make plugin's templates available to MkDocs
        config['theme'].dirs.append(str(self.templates_path))

    def on_page_context(
        self,
        context: Dict[str, Any],
        page: Page,
        **kwargs,
    ):
        """Make custom functions available to the template."""
        context.update({
            'table': TABLE,
        })

        return context

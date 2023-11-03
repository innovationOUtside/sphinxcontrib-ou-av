"""mol3d extension to embed mol3d in html sphinx output.

Originally based on https://github.com/sphinx-contrib/video/
"""

from typing import Any, Dict, List

import json
import os
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective, SphinxTranslator
from sphinx.util.osutil import copyfile

__author__ = "Raphael Massabot & Tony Hirst"
__version__ = "0.0.2"

logger = logging.getLogger(__name__)

SUPPORTED_OPTIONS: List[str] = [
    "height",
    "width",
    "style",
    "query",
    "src",
]
"List of the supported options attributes"

class ou_mol3d(nodes.General, nodes.Element):
    """mol3d node."""
    pass


class mol3d(SphinxDirective):
    """mol3d directive.

    Wrapper for the html <mol3d> tag embeding all the supported options
    """

    has_content: bool = True
    required_arguments: int = 1
    optional_arguments: int = 1
    option_spec: Dict[str, Any] = {
        "query": directives.unchanged,
        "width": directives.unchanged,
        "height": directives.unchanged,
        "style": directives.unchanged,
        "src": directives.unchanged,
    }

    def run(self) -> List[ou_mol3d]:
        """Return the mol3d node based on the set options."""
        env: BuildEnvironment = self.env
        # check options that need to be specific values
        # TO DO?

        # Get the molecule we want to view
        _query = self.arguments[0]
        # Generate the asset
        import py3Dmol
        view = py3Dmol.view(query=_query)
        filename = f"{_query.replace(':','_')}_generated.html"
        #view.setStyle({'cartoon':{'color':'spectrum'}})
        # Style MUST be valid JSON
        style = self.options.get("style", '{"cartoon":{"color":"spectrum"}}')
        print(f"style {style} was")
        view.setStyle(json.loads(style))
        os.makedirs("_tmp", exist_ok=True)
        tmp_path = os.path.join("_tmp", filename)
        view.write_html(tmp_path)
        # Copy the media asset over to the build directory
        outpath = os.path.join(env.app.builder.outdir, filename)
        dirpath = os.path.dirname(outpath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        copyfile(tmp_path, outpath)
        # TO DO - tidy up and clean _tmp/file
        _ou_mol3d = ou_mol3d(
                query=_query,
                height=self.options.get("height", ""),
                width=self.options.get("width", ""),
                src = tmp_path,
            )
        # TO DO - we need to define a <mol3d> tag handler for HTML
        # TO DO - or tweak this handler to render to everday HTML tags
        # The following is cribbed from Jupyter Book and adds a caption etc
        # https://github.com/executablebooks/MyST-NB/blob/9ddc821933826a7fd2ea9bbda1741f4f3977eb7e/myst_nb/ext/eval/__init__.py#L193C9-L201C39
        if self.content:
            node = nodes.Element()  # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if isinstance(first_node, nodes.paragraph):
                caption = nodes.caption(first_node.rawsource, "", *first_node.children)
                caption.source = first_node.source
                caption.line = first_node.line
                _ou_mol3d += caption
            if len(node) > 1:
                _ou_mol3d += nodes.legend("", *node[1:])
        return [
            _ou_mol3d
        ]


def visit_ou_mol3d_html(translator: SphinxTranslator, node: ou_mol3d) -> None:
    """Entry point of the html mol3d node."""
    # start the mol3d block
    # TO DO - fix need for path hack
    attr: List[str] = [f'{k}="{node[k].replace("_tmp/","")}"' for k in SUPPORTED_OPTIONS if k in node and node[k]]
    html: str = f"<iframe {' '.join(attr)}>"

    translator.body.append(html)


def depart_ou_mol3d_html(translator: SphinxTranslator, node: ou_mol3d) -> None:
    """Exit of the html mol3d node."""
    translator.body.append("</iframe>")


def visit_ou_mol3d_unsupported(translator: SphinxTranslator, node: ou_mol3d) -> None:
    """Entry point of the ignored mol3d node."""
    logger.warning(
        f"mol3d {node['query']}: unsupported output format (node skipped)"
    )
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add mol3d node and parameters to the Sphinx builder."""
    #app.add_config_value("mol3d_enforce_extra_source", False, "html")
    app.add_node(
        ou_mol3d,
        html=(visit_ou_mol3d_html, depart_ou_mol3d_html),
        epub=(visit_ou_mol3d_unsupported, None),
        latex=(visit_ou_mol3d_unsupported, None),
        man=(visit_ou_mol3d_unsupported, None),
        texinfo=(visit_ou_mol3d_unsupported, None),
        text=(visit_ou_mol3d_unsupported, None),
    )
    app.add_directive("ou-mol3d", mol3d)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
"""html5 extension to embed html5 in html sphinx output.

Originally based on https://github.com/sphinx-contrib/video/
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

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

SUPPORTED_MIME_TYPES: Dict[str, str] = {
    ".html": "text/html",
    ".zip": "application/zip",
}
"Supported mime types of the link tag"

SUPPORTED_OPTIONS: List[str] = [
    "height",
    "width",
    "src",
]
"List of the supported options attributes"


def get_html5(src: str, env: BuildEnvironment) -> Tuple[str, str]:
    """Return html5 and suffix.

    Raise a warning if not supported but do not stop the computation.

    Args:
        src: The source of the html5 file (can be local or url)
        env: the build environment

    Returns:
        the src file, the extension suffix
    """

    # TH: what does this do??
    # Does this take a copy of the file so it can then be passed to the build directory?
    #if not bool(urlparse(src).netloc):
    #    env.images.add_file("", src)

    suffix = Path(src).suffix
    if suffix not in SUPPORTED_MIME_TYPES:
        logger.warning(
            f'The provided file type ("{suffix}") is not a supported format. defaulting to ""'
        )
    type = SUPPORTED_MIME_TYPES.get(suffix, "")

    return (src, type)


class ou_html5(nodes.General, nodes.Element):
    """html5 node."""
    pass


class html5(SphinxDirective):
    """html5 directive.

    Wrapper for the html <html5> tag embeding all the supported options
    """

    has_content: bool = True
    required_arguments: int = 1
    optional_arguments: int = 1
    option_spec: Dict[str, Any] = {
        "src": directives.unchanged,
        "width": directives.unchanged,
        "height": directives.unchanged,
    }

    def run(self) -> List[ou_html5]:
        """Return the html5 node based on the set options."""
        env: BuildEnvironment = self.env
        # check options that need to be specific values
        # TO DO?

        # Get the asset location
        _src = get_html5(self.arguments[0], env)
        #Copy the media asset over to the build directory
        # _src[0] is the filename; _src[1] the mime type
        if not bool(urlparse(_src[0]).netloc):
            outpath = os.path.join(env.app.builder.outdir,_src[0])
            dirpath = os.path.dirname(outpath)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            copyfile(_src[0], outpath)
        _ou_html5 = ou_html5(
                src=_src[0],
                height=self.options.get("height", ""),
                width=self.options.get("width",""),
            )
        # THe following is cribbed from Jupyter Book and adds a caption etc
        # https://github.com/executablebooks/MyST-NB/blob/9ddc821933826a7fd2ea9bbda1741f4f3977eb7e/myst_nb/ext/eval/__init__.py#L193C9-L201C39
        if self.content:
            node = nodes.Element()  # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if isinstance(first_node, nodes.paragraph):
                caption = nodes.caption(first_node.rawsource, "", *first_node.children)
                caption.source = first_node.source
                caption.line = first_node.line
                _ou_html5 += caption
            if len(node) > 1:
                _ou_html5 += nodes.legend("", *node[1:])
        return [
            _ou_html5
        ]


def visit_ou_html5_html(translator: SphinxTranslator, node: ou_html5) -> None:
    """Entry point of the html iframe node."""
    # start the html5 block
    # TO DO - if we just have a single html file,
    # or HTML text in the admonition, we could just srcdoc it?
    attr: List[str] = [f'{k}="{node[k]}"' for k in SUPPORTED_OPTIONS if k in node and node[k]]
    html: str = f"<iframe {' '.join(attr)}>"

    translator.body.append(html)


def depart_ou_html5_html(translator: SphinxTranslator, node: ou_html5) -> None:
    """Exit of the html iframe node."""
    translator.body.append("</iframe>")


def visit_ou_html5_unsupported(translator: SphinxTranslator, node: ou_html5) -> None:
    """Entry point of the ignored html5 node."""
    logger.warning(
        f"html5 {node['src']}: unsupported output format (node skipped)"
    )
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add html5 node and parameters to the Sphinx builder."""
    #app.add_config_value("html5_enforce_extra_source", False, "html")
    app.add_node(
        ou_html5,
        html=(visit_ou_html5_html, depart_ou_html5_html),
        epub=(visit_ou_html5_unsupported, None),
        latex=(visit_ou_html5_unsupported, None),
        man=(visit_ou_html5_unsupported, None),
        texinfo=(visit_ou_html5_unsupported, None),
        text=(visit_ou_html5_unsupported, None),
    )
    app.add_directive("ou-html5", html5)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
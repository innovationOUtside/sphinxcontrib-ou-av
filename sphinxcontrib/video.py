"""Video extension to embed video in html sphinx output.

Derived from audio.py in this extrension
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
__version__ = "0.0.1"

logger = logging.getLogger(__name__)

SUPPORTED_MIME_TYPES: Dict[str, str] = {
    ".mp4": "video/mp4",
    #".webm": "video/webm",
}
"Supported mime types of the link tag"

SUPPORTED_OPTIONS: List[str] = [
    "src",
    "autoplay",
    "controls",
    "height",
    "loop",
    "muted",
    "poster",
    "preload",
    "width",
]
"List of the supported options attributes"


def get_video(src: str, env: BuildEnvironment) -> Tuple[str, str]:
    """Return video and suffix.

    Raise a warning if not supported but do not stop the computation.

    Args:
        src: The source of the video file (can be local or url)
        env: the build environment

    Returns:
        the src file, the extension suffix
    """

    suffix = Path(src).suffix
    if suffix not in SUPPORTED_MIME_TYPES:
        logger.warning(
            f'The provided file type ("{suffix}") is not a supported format. defaulting to ""'
        )
    type = SUPPORTED_MIME_TYPES.get(suffix, "")

    return (src, type)


class ou_video(nodes.General, nodes.Element):
    """Video node."""
    pass


class Video(SphinxDirective):
    """Video directive.

    Wrapper for the html <video> tag embeding all the supported options
    """

    has_content: bool = True
    required_arguments: int = 1
    optional_arguments: int = 1
    option_spec: Dict[str, Any] = {
        "alt": directives.unchanged,
        "autoplay": directives.flag,
        "nocontrols": directives.flag,
        "height": directives.unchanged,
        "loop": directives.flag,
        "muted": directives.flag,
        "poster": directives.unchanged,
        "preload": directives.unchanged,
        "width": directives.unchanged,
        "class": directives.unchanged,
    }

    def run(self) -> List[ou_video]:
        """Return the video node based on the set options."""
        env: BuildEnvironment = self.env
        # check options that need to be specific values
        preload: str = self.options.get("preload", "auto")
        valid_preload = ["auto", "metadata", "none"]
        if preload not in valid_preload:
            logger.warning(
                f'The provided preload ("{preload}") is not an accepted value. defaulting to "auto"'
            )
            preload = "auto"

        # Get the asset location
        _src = get_video(self.arguments[0], env)
        #Copy the media asset over to the build directory
        # _src[0] is the filename; _src[1] the mime type
        if not bool(urlparse(_src[0]).netloc):
            outpath = os.path.join(env.app.builder.outdir,_src[0])
            dirpath = os.path.dirname(outpath)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            copyfile(_src[0], outpath)
        _ou_video = ou_video(
                src=_src[0],
                alt=self.options.get("alt", ""),
                autoplay="autoplay" in self.options,
                controls="nocontrols" not in self.options,
                loop="loop" in self.options,
                muted="muted" in self.options,
                poster=self.options.get("poster", ""),
                preload=preload,
                klass=self.options.get("class", ""),
                height=self.options.get("height", ""),
                width=self.options.get("width","")
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
                _ou_video += caption
            if len(node) > 1:
                _ou_video += nodes.legend("", *node[1:])
        return [
            _ou_video
        ]


def visit_ou_video_html(translator: SphinxTranslator, node: ou_video) -> None:
    """Entry point of the html video node."""
    # start the video block
    attr: List[str] = [f'{k}="{node[k]}"' for k in SUPPORTED_OPTIONS if node[k]]
    html: str = f"<video {' '.join(attr)}>"

    translator.body.append(html)


def depart_ou_video_html(translator: SphinxTranslator, node: ou_video) -> None:
    """Exit of the html video node."""
    translator.body.append("</video>")


def visit_ou_video_unsupported(translator: SphinxTranslator, node: ou_video) -> None:
    """Entry point of the ignored video node."""
    logger.warning(
        f"video {node['src']}: unsupported output format (node skipped)"
    )
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add video node and parameters to the Sphinx builder."""
    #app.add_config_value("video_enforce_extra_source", False, "html")
    app.add_node(
        ou_video,
        html=(visit_ou_video_html, depart_ou_video_html),
        epub=(visit_ou_video_unsupported, None),
        latex=(visit_ou_video_unsupported, None),
        man=(visit_ou_video_unsupported, None),
        texinfo=(visit_ou_video_unsupported, None),
        text=(visit_ou_video_unsupported, None),
    )
    app.add_directive("ou-video", Video)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
"""Video extension to embed video in html sphinx output.

Derived from audio.py in this extrension
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse
import urllib

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective, SphinxTranslator
from sphinx.transforms.post_transforms import SphinxPostTransform

__author__ = "Raphael Massabot & Tony Hirst"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)

SUPPORTED_MIME_TYPES: Dict[str, str] = {
    ".mp4": "video/mp4",
    #".webm": "video/webm",
}
"Supported mime types of the link tag"

SUPPORTED_OPTIONS: List[str] = [
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


def get_video(src: str, env: BuildEnvironment) -> Tuple[str, str, bool]:
    """Return video and suffix.

    Raise a warning if not supported but do not stop the computation.

    Args:
        src: The source of the video file (can be local or url)
        env: the build environment

    Returns:
        the src file, the extension suffix and whether file is remote
    """

    suffix = Path(src).suffix
    if suffix not in SUPPORTED_MIME_TYPES:
        logger.warning(
            f'The provided file type ("{suffix}") is not a supported format. defaulting to ""'
        )
    type = SUPPORTED_MIME_TYPES.get(suffix, "")

    is_remote = bool(urlparse(src).netloc)
    if not is_remote:
        # Map video paths to unique names (so that they can be put into a single
        # directory). This copies what is done for images by the process_docs method of
        # sphinx.environment.collectors.asset.ImageCollector.
        src, fullpath = env.relfn2path(src, env.docname)
        env.note_dependency(fullpath)
        env.images.add_file(env.docname, src)

    return (src, type, is_remote)


class ou_video(nodes.General, nodes.Element):
    """Video node."""
    pass


class Video(SphinxDirective):
    """Video directive.

    Wrapper for the html <video> tag embedding all the supported options
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
        sources = [get_video(self.arguments[0], env)]

        _ou_video = ou_video(
            src=sources[0][0],
            sources=sources,
            alt=self.options.get("alt", ""),
            autoplay="autoplay" in self.options,
            controls="nocontrols" not in self.options,
            loop="loop" in self.options,
            muted="muted" in self.options,
            poster=self.options.get("poster", ""),
            preload=preload,
            klass=self.options.get("class", ""),
            height=self.options.get("height", ""),
            width=self.options.get("width", ""),
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


class VideoPostTransform(SphinxPostTransform):
    """Ensure video files are copied to build directory.

    This copies what is done for images in the post_process_image method of
    sphinx.builders.Builder, except as a Transform since we can't hook into that method
    directly.
    """

    default_priority = 200

    def run(self):
        """Add video files to Builder's image tracking.

        Doing so ensures that the builder copies the files to the output directory.
        """
        # TODO: This check can be removed when the minimum supported docutils version
        # is docutils>=0.18.1.
        traverse_or_findall = (
            self.document.findall
            if hasattr(self.document, "findall")
            else self.document.traverse
        )
        for node in traverse_or_findall(ou_video):
            for src, _, is_remote in node["sources"]:
                if not is_remote:
                    self.app.builder.images[src] = self.env.images[src][1]


def visit_ou_video_html(translator: SphinxTranslator, node: ou_video) -> None:
    """Entry point of the html video node."""
    # start the video block
    attr: List[str] = [f'{k}="{node[k]}"' for k in SUPPORTED_OPTIONS if node[k]]
    html: str = f"<video {' '.join(attr)}>"

    # build the sources
    builder = translator.builder
    html_source = '<source src="{}" type="{}">'
    for src, type_, _ in node["sources"]:
        # Rewrite the URI if the environment knows about it, as is done for images in the
        # HTML5 builder, in sphinx.writers.html5.HTML5Translator.visit_image.
        if src in builder.images:
            src = Path(
                builder.imgpath, urllib.parse.quote(builder.images[src])
            ).as_posix()
        html += html_source.format(src, type_)

    # add the alternative message
    # html += node["alt"]

    translator.body.append(html)


def depart_ou_video_html(translator: SphinxTranslator, node: ou_video) -> None:
    """Exit of the html video node."""
    translator.body.append("</video>")


def visit_ou_video_unsupported(translator: SphinxTranslator, node: ou_video) -> None:
    """Entry point of the ignored video node."""
    logger.warning(
        f"video {node['sources'][0][0]}: unsupported output format (node skipped)"
    )
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add video node and parameters to the Sphinx builder."""
    # app.add_config_value("video_enforce_extra_source", False, "html")
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
    app.add_post_transform(VideoPostTransform)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

"""Audio extention to embed audio in html sphinx output.

Originally based on https://github.com/sphinx-contrib/video/
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

__author__ = "Raphael Massabot & Tony Hirst"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)

SUPPORTED_MIME_TYPES: Dict[str, str] = {
    ".mp3": "audio/mpeg",
    #".wav": "audio/wav",
    #".weba": "audio/webm",
}
"Supported mime types of the link tag"

SUPPORTED_OPTIONS: List[str] = [
    "autoplay",
    "controls",
    "loop",
    "muted",
    "preload",
    "src",
]
"List of the supported options attributes"


def get_audio(src: str, env: BuildEnvironment) -> Tuple[str, str]:
    """Return audio and suffix.

    Load the audio to the static directory if necessary and process the suffix. Raise a warning if not supported but do not stop the computation.

    Args:
        src: The source of the audio file (can be local or url)
        env: the build environment

    Returns:
        the src file, the extention suffix
    """

    # TH: what does this do??
    if not bool(urlparse(src).netloc):
        env.images.add_file("", src)

    suffix = Path(src).suffix
    if suffix not in SUPPORTED_MIME_TYPES:
        logger.warning(
            f'The provided file type ("{suffix}") is not a supported format. defaulting to ""'
        )
    type = SUPPORTED_MIME_TYPES.get(suffix, "")

    return (src, type)


class ou_audio(nodes.General, nodes.Element):
    """Audio node."""
    pass


class Audio(SphinxDirective):
    """Audio directive.

    Wrapper for the html <audio> tag embeding all the supported options
    """

    has_content: bool = True
    required_arguments: int = 1
    optional_arguments: int = 1
    option_spec: Dict[str, Any] = {
        "autoplay": directives.flag,
        "nocontrols": directives.flag,
        "loop": directives.flag,
        "muted": directives.flag,
        "preload": directives.unchanged,
        "class": directives.unchanged,
        "src": directives.unchanged,
    }

    def run(self) -> List[ou_audio]:
        """Return the audio node based on the set options."""
        env: BuildEnvironment = self.env

        # check options that need to be specific values
        preload: str = self.options.get("preload", "auto")
        valid_preload = ["auto", "metadata", "none"]
        if preload not in valid_preload:
            logger.warning(
                f'The provided preload ("{preload}") is not an accepted value. defaulting to "auto"'
            )
            preload = "auto"

        # add the audio files as images in the builder
        _src = get_audio(self.arguments[0], env)
        _ou_audio = ou_audio(
                src=_src[0],
                autoplay="autoplay" in self.options,
                controls="nocontrols" not in self.options,
                loop="loop" in self.options,
                muted="muted" in self.options,
                preload=preload,
                klass=self.options.get("class", ""),
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
                _ou_audio += caption
        return [
            _ou_audio
        ]


def visit_ou_audio_html(translator: SphinxTranslator, node: ou_audio) -> None:
    """Entry point of the html audio node."""
    # start the audio block
    attr: List[str] = [f'{k}="{node[k]}"' for k in SUPPORTED_OPTIONS if node[k]]
    if node["klass"]:  # klass need to be special cased
        attr += [f"class=\"{node['klass']}\""]
    html: str = f"<audio {' '.join(attr)}/>"

    translator.body.append(html)


def depart_ou_audio_html(translator: SphinxTranslator, node: ou_audio) -> None:
    """Exit of the html audio node."""
    pass
    #translator.body.append("")


def visit_ou_audio_unsupported(translator: SphinxTranslator, node: ou_audio) -> None:
    """Entry point of the ignored video node."""
    logger.warning(
        f"audio {node['src']}: unsupported output format (node skipped)"
    )
    raise nodes.SkipNode


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add audio node and parameters to the Sphinx builder."""
    app.add_config_value("audio_enforce_extra_source", False, "html")
    app.add_node(
        ou_audio,
        html=(visit_ou_audio_html, depart_ou_audio_html),
        epub=(visit_ou_audio_unsupported, None),
        latex=(visit_ou_audio_unsupported, None),
        man=(visit_ou_audio_unsupported, None),
        texinfo=(visit_ou_audio_unsupported, None),
        text=(visit_ou_audio_unsupported, None),
    )
    app.add_directive("ou-audio", Audio)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
"""Exercise extension to embed exercise in html sphinx output.

Originally based on https://github.com/sphinx-contrib/video/
"""

from typing import Any, Dict, List

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx_design.shared import create_component

__author__ = "Raphael Massabot & Tony Hirst"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)


SUPPORTED_OPTIONS: List[str] = [
    "timing",
]
"List of the supported options attributes"


class discussion(SphinxDirective):
    """The discussion directive is used to generate an activity block."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        discussion = create_component(
            "ou-discussion",
            classes=["ou-discussion"],
            rawtext=self.content,
        )
        self.state.nested_parse(self.content, self.content_offset, discussion)
        return [discussion]


class answer(SphinxDirective):
    """The answer directive is used to generate an answer block."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        answer = create_component(
            "ou-answer",
            classes=["ou-answer"],
            rawtext=self.content,
        )
        self.state.nested_parse(self.content, self.content_offset, answer)
        return [answer]


class exercise(SphinxDirective):
    """exercise directive.

    Wrapper for the <exercise> tag embedding all the supported options
    """

    has_content: bool = True
    required_arguments: int = 1
    optional_arguments: int = 1
    option_spec: Dict[str, Any] = {
        "timing": directives.unchanged,
    }
    final_argument_whitespace = True

    def run(self):
        exercise = create_component("ou-exercise", rawtext=self.content)
        exercise += create_component(
            "ou-title",
            rawtext=self.arguments[0],
            children=[nodes.Text(self.arguments[0], self.arguments[0])],
        )
        timing = self.options.get("timing", None)
        if timing:
            exercise += create_component(
                "ou-time",
                rawtext=timing,
                children=[nodes.Text(timing, timing)],
            )

        self.state.nested_parse(self.content, self.content_offset, exercise)
        return [exercise]


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add exercise node and parameters to the Sphinx builder."""
    app.add_directive("ou-exercise", exercise)
    app.add_directive("ou-answer", answer)
    app.add_directive("ou-discussion", discussion)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

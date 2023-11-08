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


class CustomInternalDirective(SphinxDirective):
    """Generic components..."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        component_name = self.component_name
        component = create_component(
            component_name,
            classes=[component_name],
            rawtext=self.content,
        )
        self.state.nested_parse(self.content, self.content_offset, component)
        return [component]


class discussion(CustomInternalDirective):
    component_name = "ou-discussion"


class answer(CustomInternalDirective):
    component_name = "ou-answer"


class CustomTopDirective(SphinxDirective):
    """Generic top level acitvity/exercise directive.

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
        component_name = self.component_name
        activity = create_component(component_name, rawtext=self.content)
        activity += create_component(
            "ou-title",
            rawtext=self.arguments[0],
            children=[nodes.Text(self.arguments[0], self.arguments[0])],
        )
        timing = self.options.get("timing", None)
        if timing:
            activity += create_component(
                "ou-time",
                rawtext=timing,
                children=[nodes.Text(timing, timing)],
            )

        self.state.nested_parse(self.content, self.content_offset, activity)
        return [activity]


class activity(CustomTopDirective):
    component_name = "ou-activity"


class exercise(CustomTopDirective):
    component_name = "ou-exercise"


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add exercise node and parameters to the Sphinx builder."""
    app.add_directive("ou-activity", activity)
    app.add_directive("ou-exercise", exercise)
    app.add_directive("ou-answer", answer)
    app.add_directive("ou-discussion", discussion)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

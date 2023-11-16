"""Exercise extension to embed exercise in html sphinx output.

Originally based on https://github.com/sphinx-contrib/video/
"""
from sphinx.transforms.post_transforms import SphinxPostTransform

# TO DO - HTML outputs for exercise and activity

from typing import Any, Dict, List
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx_design.shared import create_component, is_component

from sphinxcontrib_ou_media.utils import hack_uuid, handle_css_js_assets

__author__ = "Mark Hall & Tony Hirst"
__version__ = "0.0.1"

# html_static_path = ["_static"]
# html_css_files = ["ou_activities.css"]
# html_js_files = ["ou_activities.js"]

logger = logging.getLogger(__name__)

SUPPORTED_OPTIONS: List[str] = [
    "timing",
]
"List of the supported options attributes"


class OU_CustomInternalDirective(SphinxDirective):
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


class OU_DiscussionDirective(OU_CustomInternalDirective):
    component_name = "ou-discussion"


class OU_AnswerDirective(OU_CustomInternalDirective):
    component_name = "ou-answer"


class OU_InteractionDirective(SphinxDirective):
    """Generic components..."""

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    option_spec: Dict[str, Any] = {
        "type": directives.unchanged,
        "size": directives.unchanged,
        "id": directives.unchanged,  # TO DO - validate id
    }
    final_argument_whitespace = True

    def run(self):
        component_name = "ou-interaction"
        typ = self.options.get("type", "freeresponse")
        size = self.options.get("size", None)
        id = self.options.get("id", hack_uuid())
        # TO DO  - complete options
        if typ == "freeresponse":
            if size not in ["paragraph"]:
                size = "paragraph"
        else:
            typ_ = (
                typ.split()[0]
                .lower()
                .replace("choice", "")
                .replace("_", "")
                .replace("-", "")
            )
            typ = typ_ if typ in ["multiple", "single"] else typ

        component = create_component(
            component_name,
            classes=[component_name],
            rawtext=self.content,
            type=typ,
            size=size,
            id=id,
        )
        if not self.content:
            self.state.nested_parse(self.content, self.content_offset, component)
            return [component]

        if typ in ["multiple", "single"]:
            for item in self.content:
                if not item.strip():
                    continue
                item_ = item.split()
                # Drop the leading T/F
                txt = " ".join(item_[1:]).strip()
                # Get any feedback
                item_ = txt.split("::")
                txt = item_[0].strip()
                feedback = item_[1].strip() if len(item_) == 2 else None
                if item[0].upper() == "T":
                    response = create_component(
                        "Right",
                        rawtext=txt,
                        children=[nodes.Text(txt, txt)],
                    )
                    if feedback:
                        response += create_component(
                            "Feedback",
                            rawtext=feedback,
                            children=[nodes.Text(feedback, feedback)],
                        )
                    component += response
                elif item[0].upper() == "F":
                    response = create_component(
                        "Wrong",
                        rawtext=txt,
                        children=[nodes.Text(txt, txt)],
                    )
                    if feedback:
                        response += create_component(
                            "Feedback",
                            rawtext=feedback,
                            children=[nodes.Text(feedback, feedback)],
                        )
                    component += response
        else:
            self.state.nested_parse(self.content, self.content_offset, component)
        return [component]


class OU_CustomActExDirective(SphinxDirective):
    """Generic top level activity/exercise directive.

    Generates basis for <Activity> and <Exercise> tags, embedding all the supported options
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
        heading = " ".join(self.arguments)
        activity += create_component(
            "ou-title",
            rawtext=heading,
            children=[nodes.Text(heading, heading)],
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


class OU_ActivityDirective(OU_CustomActExDirective):
    component_name = "ou-activity"


class OU_ExerciseDirective(OU_CustomActExDirective):
    component_name = "ou-exercise"


# HtmlTransform classes from Mark Hall's ou-book-theme
class ActivityAnswerHtmlTransform(SphinxPostTransform):
    """Transform activity containers into the HTML specific AST structures."""

    default_priority = 199
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "ou-answer")):
            newnode = create_component(
                "ou-activity-answer",
                classes=["ou-activity-answer"],
            )
            newnode += nodes.raw("", "<hr/>", format="html")
            newnode += nodes.raw(
                "",
                '<button class="sd-btn sd-btn-info ou-toggle ou-toggle-hidden"><span class="ou-toggle-show">Show answer</span><span class="ou-toggle-hide">Hide answer</span></button>',  # noqa: E501
                format="html",
            )
            content_container = create_component(
                "ou-activity-answer-content",
                classes=["ou-activity-answer-content"],
                children=node.children,
            )
            newnode += content_container
            node.replace_self(newnode)


# TO DO - at the moment we treat exercise and activity the same way

class ActivityHtmlTransform(SphinxPostTransform):
    """Transform activity containers into the HTML specific AST structures."""

    default_priority = 198
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(
            lambda node: is_component(node, "ou-activity")
            or is_component(node, "ou-exercise")
        ):
            newnode = create_component(
                "ou-activity",
                classes=["ou-activity"],
            )
            title_node = create_component(
                "ou-activity-title",
                classes=["ou-activity-title"],
                children=node.children[0].children,
            )
            newnode += title_node
            newnode += node.children[1:]
            node.replace_self(newnode)


# TO DO
# right /wrong - SingleChoice, MultipleChoice; variants of a choice type?
"""
```{choice} single
T: this
F: that
```
T and F map on <Right> and <Wrong>
"""


def setup(app: Sphinx) -> Dict[str, bool]:
    """Add exercise node and parameters to the Sphinx builder."""
    app.add_directive("ou-activity", OU_ActivityDirective)
    app.add_directive("ou-exercise", OU_ExerciseDirective)
    app.add_directive("ou-answer", OU_AnswerDirective)
    app.add_directive("ou-discussion", OU_DiscussionDirective)
    app.add_directive("ou-discussion", OU_DiscussionDirective)
    app.add_directive("ou-interaction", OU_InteractionDirective)

    app.add_post_transform(ActivityHtmlTransform)
    app.add_post_transform(ActivityAnswerHtmlTransform)

    # Pass in the stub filename used in static/js/STUB.js etc
    handle_css_js_assets(app, "ou_activities")

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

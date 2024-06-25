from importlib import resources as import_resources
import uuid


def resources_path(path=None):
    """Get path to package resources."""
    path = path if path else "sphinxcontrib_ou_media"
    return import_resources.files(path)


def fetch_template(*args, path=None):
    """Join the path components and fetch the template content."""
    template_path = resources_path(path).joinpath(*args)

    if template_path.is_file():
        with template_path.open() as file:
            return file.read()
    else:
        return None  # Handle the case where the file doesn't exist


def hack_uuid():
    while True:
        # Generate a random UUID
        uid = uuid.uuid4().hex
        # There are conditions...
        # - first character is not a digit
        # - max 20 chars
        if not uid[0].isdigit():
            return uid[:20]


from pathlib import Path
from sphinx.util.fileutil import copy_asset
import os


def handle_css_js_assets(app, stub):
    """Copy over CSS and JS assets to relevant directory
    and add links to HTML page."""

    source_dir = os.path.join(resources_path(), "static")
    build_dir = os.path.join(app.outdir, "_static")

    js_file = f"{stub}.js"
    css_file = f"{stub}.css"

    # Copy JavaScript file
    copy_asset(
        os.path.join(source_dir, "js", js_file),
        build_dir,
        #app.builder,
    )
    # Copy CSS file
    copy_asset(
        os.path.join(source_dir, "css", css_file),
        build_dir,
        #app.builder,
    )
    app.add_css_file(css_file)
    app.add_js_file(js_file)

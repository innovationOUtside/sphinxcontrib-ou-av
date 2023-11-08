import importlib.resources as resources


def resources_path(path):
    """Get path to package resources."""
    path = path if path else "sphinxcontrib_ou_media"
    return resources.files(path)


def fetch_template(*args, path=None):
    """Join the path components and fetch the template content."""
    template_path = resources_path(path).joinpath(*args)

    if template_path.is_file():
        with template_path.open() as file:
            return file.read()
    else:
        return None  # Handle the case where the file doesn't exist

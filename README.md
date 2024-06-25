# sphinxcontrib-ou-xml-tags

*Needs repo name change*

Sphinx is a document publishing framework for converting markdown based source documents to a wide range of output formats, including HTML and XML. Content rendered to Sphinx-generated XML can then be further transformed to other flavouts of XML, such as OU-XML. Sphinx is used as part of the *Jupyter Book* publishing framework.

Sphinx is used as part of the *Jupyter Book* publishing framework.

The `sphinxcontrib-ou-xml-tags` supports a range of markdown admonition blocks that extend the Sphinx XML output in order to simplify the conversion of Sphinx XML to OU-XML. Generation of appropriate HTML tags when using Sphinx to  publish source documents directly to HTML output is also supported. (PDF support may or may not appear at some point in the future...)

The `sphinxcontrib-ou-xml-tags` Python package bundles several Sphinx extensions:

- `ou-audio`: generate approptiate tags for an embedded audio player;
- `ou-video`: generate approptiate tags for an embedded video player;
- `ou-activities`: generate appropriate tags for activities;
- `ou-codestyle`: generate appropriate tags for language-sensitive styled code;
- `ou-mol3d`: generate appropriate tags for embedding a mol3d interactive visualisation;
- `ou-html5`: generate appropriate tags and a zipped HTML5 bundle for deplying an HTML5 asset (e.g. an embedded HTML5 app).

## Usage

Install the package:

`pip install git+https://github.com/innovationOUtside/sphinxcontrib-ou-xml-tags.git`

or:

`pip install https://github.com/innovationOUtside/sphinxcontrib-ou-xml-tags/archive/refs/heads/main.zip`

Include the desired extensions in the Sphinx `_config.yml` file:

```yaml
sphinx:
  extra_extensions:
    - sphinxcontrib.ou-video
    - sphinxcontrib.ou-audio
    - sphinxcontrib.ou-html5
    - sphinxcontrib.ou-mol3d
    - sphinxcontrib.ou-codestyle

    - sphinxcontrib.ou-activities
    - ou_book_theme
```

The `ou_activity` extension also requires: `pip install ou-book-theme`.

For more examples and discussion on how to use these extensions as part of an OU workflow, see [`reusable-content-example`](https://opencomputinglab.github.io/reusable-content-example/media_items.html).

## BUILD and INSTALL

`python3 -m build`

Install as:

`python3 -m pip install .`

## HTML packages

```bash
cd sphinxcontrib_ou_media/packages/shinylite-py
zip -r -X "../../../dist/shinylite-py-01.zip" .
cd ../..
```
cd target_folder; zip -r ../zipped_dir.zip *
# Generating OU-XML

Generating OU-XML is two part process and requires the additional installation of 

The first step is to use Jupyter Book tooling to generate a Sphinx XML version of the Jupyter Book, as defined by the `_toc.yml` and `_config.yml` files:

`jb build PATH_TO_BOOK_SRC --builder custom --custom-builder xml`

This generates XML files in the default `_build/xml` directory.

The second step is to use the `ouseful_obt` command-line tool from the [`ou-xml-validator` package](https://github.com/innovationOUtside/ou-xml-validator/):

`ouseful_obt PATH_TO_BOOK_SRC`

*Note that this currently requires several `ou` parameters to be set, otherwise an error will be raised.

Example `ou` settings in `_config.yml`:

```yaml
ou:
  module_code: OUSEFUL-DEMO-SPHINX
  module_title: sphinxcontrib-ou-xml-tags
  block: 0
  presentation: X
  first_published: 2024
  isbn:
  edition:
  block_title: Examples
  image_path_prefix: https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/
  media_path_prefix: https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/
  codestyle: false
  codelang:
  codesnippet_theme: light # light | dark
  validate: true # validate generated OU-XML in toolchain

```

Generated OU-XML content in the `_build/ouxml` directory can then be validated against an OU-XML schema by running the command:

`ou_xml_validator validate path/to/testme.xml`

See an example of the XML generated for this documentation [here](ouxml/index.xml).
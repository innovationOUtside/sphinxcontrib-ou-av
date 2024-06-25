# Styled code

The OU-XML code rendering does not support style code by default, so we have to use a workaround when rendering styled code to the VLE.

The `{ou-codestyle}` admonition block allows us to individually style code blocks using `prism.js` and is rendered into an HTML page as follows:

```{ou-codestyle} python
# some code

def test():
  """A function."""
  print("hello")
```

Pass the language name in to define the language pack styling.

The result is an HTML5 zipped bundle that renders the styled program listing in an iframe.

Here's an example of the generated OU-XML:

```xml
<MediaContent type="html5" height="400" width="600" src="https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/ouseful-demo-sphinx_b0_p1_x_html0.zip" id="cb78cee0c59f474a98a0"/>
```

The `.zip` file and its contents are automatically generated from based on the contents of the admonition block.
# Styled code

Code can be minimally included in a document using simple fenceposts:

````text
```python
# some code

def test():
  """A function."""
  print("hello")
```
````

In a Sphinxx HTML document, the code styling respects the declared programming laguage type, and the code renders as:

```python
# some code

def test():
  """A function."""
  print("hello")
```

The generated OU-XML is:

```xml
<ProgramListing><Paragraph># some code<br/><br/>def test():<br/>  """A function."""<br/>  print("hello")</Paragraph></ProgramListing>
```

The OU-XML code rendering does not support style code by default, so we have to use a workaround when rendering styled code to the VLE by creating an HTML5 bundle that can pull in a CDN delivered version of [`prism.js`](https://prismjs.com/).

The `{ou-codestyle}` admonition block will generate a standalone HTML page that pulls in the necessary `prism.js` assets from the CDN, and will be rendered into an HTML page using an IFrame as follows:

```{ou-codestyle} python
# some code

def test():
  """A function."""
  print("hello")
```

Pass the language name in to define the language pack styling.

For the generated OU-XML, we created an HTML5 zipped bundle that includes the generated webpage (as `index.html` at the root of the zip archive file) and then call on that. *It is up to the user to ensure that a copy gf the zip file is placed at the desired delivery location.*

```xml
<MediaContent type="html5" height="400" width="600" src="https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/ouseful-demo-sphinx_b0_p1_x_html0.zip" id="cb78cee0c59f474a98a0"/>
```

The `.zip` file and its contents are automatically generated from based on the contents of the admonition block.

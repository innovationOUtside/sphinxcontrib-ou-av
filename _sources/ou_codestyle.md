# Styled code

The OU-XML code rendering does not support style code by default, so we have to use a workaround when rendering styled code to the VLE.

The `{ou-codestyle}` admonition block allows us to individually style code blocks using `prism.js`:

```{ou-codestyle} python
# some code

def test():
  """A function."""
  print("hello")
```

Pass the language name in to define the language pack styling.

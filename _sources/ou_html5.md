# Embedding HTML5 bundles

OU-XML allows HTML5/JS?CSS apps to be embedded in an iframe within a VLE page. The app needs to be provided in tthe form of a zip file and MUST contain an `index.html` file at the root.

````text

```{ou-html5} path/to/html5.zip
:width: 140
:keep: always
```
````

Currently, this does not work with Sphinx rendering to HTML.
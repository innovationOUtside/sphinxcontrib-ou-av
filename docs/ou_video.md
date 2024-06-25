# Embedded video — `ou-video` admonition

Embed a video player capable of playing of a specified video file:

````text
```{ou-video} resources/test.mp4
A caption for a video file.

A line of description.
And continuation of the line.

More description.
```
````

```{ou-video} resources/test.mp4
A caption for a video file.

A line of description.
And continuation of the line.

More description.
```

The block can also be empty of caption and description text. *If there is any text in the body of the admonition, the first line is mapped onto an OU-XML `<Caption>` element.*

The MyST spec also lets you use a video file path in a `{figure}` admonition when generating HTML output, but this is not support for conversion to OU-XML. There is a also a [`sphinx-contrib/youtube`](https://github.com/sphinx-contrib/youtube) extension for embedding videos, but again there is no direct path for generating an appropriate OU-XML media tag.

*TO DO: how does OU-XML recommend YouTube embeds?*

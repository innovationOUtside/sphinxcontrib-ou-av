# Embedded video — `ou-video` admonition

Embed a video player capable of playing of a specified video file:

````text
```{ou-video} resources/test.mp4
```
````

We can also include one or more than one line of text in the body of the admonition.

````text
```{ou-video} resources/test.mp4
A caption for a video file.

A line of description.
And continuation of the line.

More description.
```
````

The first line is mapped to a caption. Any additional lines are mapped to a description. The corresponding OU-XML is:

```xml
<MediaContent type="video" height="" width="" src="https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/ouseful-demo-sphinx_b0_p1_x_media_test.mp4">
    <Caption>Figure 2.1 A caption for a video file.</Caption>
    <Description>
        <Paragraph>A line of description.
            And continuation of the line.</Paragraph>
        <Paragraph>More description.</Paragraph>
    </Description>
</MediaContent>
```

*Including more than one line currently breaks the Sphinx HTML rendering at that point, although the OU-XML is generated correctly.*

The MyST spec also lets you use a video file path in a `{figure}` admonition when generating HTML output, but this is not (yet?) supported for conversion to OU-XML. There is a also a [`sphinx-contrib/youtube`](https://github.com/sphinx-contrib/youtube) extension for embedding videos, but again there is no direct path for generating an appropriate OU-XML media tag.

*TO DO: how does OU-XML recommend YouTube embeds?*

*TO DO: support MyST generated video embeds in conversion to OU-XML.*

Example of code that breaks HTML rendering — the video block shluld be followed by a line that says "made it to here".

```{ou-video} resources/test.mp4
A caption for a video file.

A line of description.
And continuation of the line.

More description.
```

Seems we have *MADE IT TO HERE*

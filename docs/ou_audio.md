# Audio Items — `ou-audio` admonition

Embed an audio player capable of playing a specified audio file:

````text
```{ou-audio} resources/test.mp3
A caption for an audio file.
```
````

This is rendered inside an HTML page as:

```{ou-audio} resources/test.mp3
A caption for an audio file.
```

Renders to the following OU-XML:

```xml
 <MediaContent type="audio" src="https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/ouseful-demo-sphinx_b0_p1_x_media_test.mp3">
        <Caption>Figure 1.1 A caption for an audio file.</Caption>
</MediaContent>
```

As with the `ou-video` element, we can optionally include a caption, or a caption and description elements, by including text inside the admonition block, which renders inside an HTML page (*broken?*) as:

```{ou-audio} resources/test.mp3
A caption for an audio file.

A line of description.
And continuation of the line.

More description.
```

The extended admonition block transforms to the following OU-XML:

```xml
<MediaContent type="audio" src="https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/ouseful-demo-sphinx_b0_p1_x_media_test.mp3">
    <Caption>Figure 1.2 A caption for an audio file.</Caption>
    <Description>
        <Paragraph>A line of description.
            And continuation of the line.</Paragraph>
        <Paragraph>More description.</Paragraph>
    </Description>
</MediaContent>
```

*Currently, there is no native MyST admonition for embedding an audio player.*

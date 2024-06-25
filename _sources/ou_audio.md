# Audio Items — `ou-audio` admonition

Embed an audio player capable of playing a specified audio file:

````text
```{ou-audio} resources/test.mp3
A caption for an audio file.
```
````

```{ou-audio} resources/test.mp3
A caption for an audio file.
```

As with the `ou-video` element, we can optionally include a caption, or a caption and description elements, by including text inside the admonition block.

```{ou-audio} resources/test.mp3
A caption for an audio file.

A line of description.
And continuation of the line.

More description.
```


*Currently, there is no native MyST admonition for embedding an audio player.*


## Visualising molecules — `ou_mol3d`

The [`3dmol.js`](https://3dmol.csb.pitt.edu/) packages provides an interactive 3D viewer for a wide range of molecules.

We can create a simple Sphinx admonition handler that will accept a molecule query code (see the official docs for more info on this) and then render the molecule with desired styling.

We can then use a markdown admonition such as the following to generate an interactive widget that lets us interactively visualise the molecule:

````text
```{ou-mol3d} pdb:1ubq
:style: '{"sphere":{"radius":"0.5"}}'
```
````

to embed an interactive JavaScript powered viewer such as the following (click then drag in the widget below to rotate the rendered molecule; mouse/touchpad controls should also let you zoom in and out):

```{ou-mol3d} pdb:1ubq
:style: '{"sphere":{"radius":"0.5"}}'
:height: 500
:width: 800
:background: '0x222222'
```

*Note that the style information must be presented as a quoted string and take the form of a valid JSON string.*

Renders to the following OU-XML:

```xml
<MediaContent type="html5" height="500" width="600" src="https://raw.githubusercontent.com/innovationoutside/sphinxcontrib-ou-xml-tags/main/vletmp/ouseful-demo-sphinx_b0_p1_x_html1.zip" id="f06b147c75474dcdb6f5"/>
```

The `.zip` file and its contents are automatically generated based on the contents of the admonition block.

*It would perhaps be usedul to try to follow the model of embedded audio and video players and also support captions, additional description text, etc. It may also make sense to automatically number this sort of embedded asset as a figure, or perhaps create an "Interactive Figure" type and associated numbering scheme?*

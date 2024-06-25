# Activities and Exercises — `ou-activity` admonition

OU-XML supports a range of styled activity types, including *activities*, *exercises*, *SAQ*s (self-assessment questions*) and *ITQ*s.

## Activities

*Activity rendering is broken in this extension at the moment due to a collision with the activity admonition handler that is baked into ou-theme. Ideally, that handler would be broken out into its own extension so the rest of the ou-theme can be deployed and the user given free choice over which activity handler to use.*

Activities have two parts - the activity description, and the activity answer.

Activities are defined as:

````text
```{ou-activity} Activity 1
:timing: 1 hour

Do something...
```
````

This currently renders to HTML as:

```{ou-activity} Activity 1
:timing: 1 hour

Do something...
```

This generates the following OU-XML (leaeding and trailing whitespace imside a tag is typically ignored; *but I do need to try to tidy this up...*):

```xml
<Activity>
    <Heading>
Activity 1                </Heading>
    <Timing>
1 hour                </Timing>
    <Question>
        <Paragraph>Do something…</Paragraph>
    </Question>
</Activity>
```

Activities can optionally include an answer:

`````text
````{ou-activity} Activity 2
Do something else...

```{ou-answer}
Here is the second activity answer.

And *more* bits of answer.
```

````
`````

This is currently rednered inside an HTML page as:

````{ou-activity} Activity 2
Do something else...

```{ou-answer}
Here is the second activity answer.

And *more* bits of answer.
```

````


The genereated OU-XML is:

```xml
<Activity>
    <Heading>
Activity 2                </Heading>
    <Question><Paragraph>Do something else…</Paragraph>
    </Question><Answer>
        <Paragraph>Here is the second activity answer.</Paragraph>
        <Paragraph>And <i>more</i> bits of answer.</Paragraph>
    </Answer>
</Activity>
```
Ideally we should also have an identifier associated woth the activity, not least so we can provide a cross-reference link to the activity.

## Exercises

Exercies are also supported, and are distinct fron those supported by the `sphinx-exercise` extension:

````text
```{ou-exercise} Exercise 1
:timing: 1 hour

Do something...
```
````

This is rendered in an HTML page as:

```{ou-exercise} Exercise 1
:timing: 1 hour

Do something...
```

and generates the following OU-XML:

```xml
<Exercise>
    <Heading>
Exercise 1                </Heading>
    <Timing>
1 hour                </Timing>
    <Question><Paragraph>Do something…</Paragraph>
</Question></Exercise>
```

Exercises may also contain answers:

`````text

````{ou-exercise} Exercise 2
:timing: 15 minutes
Do something else...

```{ou-answer}
Here is the second activity answer.

And *more* bits of answer.
```
````
`````

This renders inside an HTML page as:

````{ou-exercise} Exercise 2
:timing: 15 minutes
Do something else...

```{ou-answer}
Here is the second activity answer.

And *more* bits of answer.
```
````

and as is transformed to the following OU-XML:

```xml
<Exercise>
    <Heading>
Exercise 2                </Heading>
    <Timing>
15 minutes                </Timing>
    <Question><Paragraph>Do something else…</Paragraph>
    </Question><Answer>
        <Paragraph>Here is the second activity answer.</Paragraph>
        <Paragraph>And <i>more</i> bits of answer.</Paragraph>
    </Answer>
</Exercise>
```

We can also have a discussion block:

`````text
````{ou-exercise} Exercise 3
:timing: 15 minutes
Do something else...

```{ou-discussion}
Here is the third exercise discussion.

And *more* bits of discussion.
```
````
`````

rendered into an HTML page as follows:

````{ou-exercise} Exercise 3
:timing: 15 minutes
Do something else...

```{ou-discussion}
Here is the third exercise discussion.

And *more* bits of discussion.
```
````

And with corresponding OU-XML:

```xml
<Exercise>
    <Heading>
Exercise 3                </Heading>
    <Timing>
15 minutes                </Timing>
    <Question><Paragraph>Do something else…</Paragraph>
    </Question><Discussion>
        <Paragraph>Here is the third exercise discussion.</Paragraph>
        <Paragraph>And <i>more</i> bits of discussion.</Paragraph>
    </Discussion>
</Exercise>
```

Or an answer and a discussion block:

`````text
````{ou-exercise} Exercise 4
:timing: 1 hour
Do something else...

```{ou-answer}
Here is the fourth exercise answer.

And *more* bits of answer.
```

```{ou-discussion}
Here is the fourth exercise discussion.

And *more* bits of discussion.
```

````
`````

which is rendered into an HTML page as:

````{ou-exercise} Exercise 4
:timing: 1 hour
Do something else...

```{ou-answer}
Here is the fourth exercise answer.

And *more* bits of answer.
```

```{ou-discussion}
Here is the fourth exercise discussion.

And *more* bits of discussion.
```

````

and to the following OU-XML:

```xml
<Exercise>
    <Heading>
Exercise 4                </Heading>
    <Timing>
1 hour                </Timing>
    <Question><Paragraph>Do something else…</Paragraph>
    </Question><Answer>
        <Paragraph>Here is the fourth exercise answer.</Paragraph>
        <Paragraph>And <i>more</i> bits of answer.</Paragraph>
    </Answer>
    <Discussion>
        <Paragraph>Here is the fourth exercise discussion.</Paragraph>
        <Paragraph>And <i>more</i> bits of discussion.</Paragraph>
    </Discussion>
</Exercise>
```

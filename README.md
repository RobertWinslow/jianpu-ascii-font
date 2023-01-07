# Jianpu Ascii Font

This is a font which uses ascii ligatures to display simplified Jianpu 简谱 musical notation.
This is not a specialized font intended for use some musical application,
but rather a very simple way of rendering notation in a word-processor or personal website.

[The font file can can be downloaded from the GitHub repo](https://github.com/RobertWinslow/jianpu-ascii-font/blob/main/JianpuASCII.ttf).

[See here for an editable of the font in use](https://robertwinslow.github.io/jianpu-ascii-font/examples/songs/amazinggrace).

<!--
, and then used in any software that lets the user choose 
TODO: Example with image.
-->




## Syntax

The [wikipedia page for jianpu notation](https://en.wikipedia.org/wiki/Numbered_musical_notation) 
is well-written and describes how the notation works. 
Below is a list of jianpu features implemented in this font and how to use them.

### Basics

- Use digits `1234567` for notes.
- Use `0` for a rest.

<pre>|3 3 4 5|5 4 3 2|1 1 2 3|3 2 2 0|</pre>

![A quick diddy. Ode to Joy.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuBasic.PNG)

- Append `'` to a note to indicate a higher octave by placing a dot above it. `1' 1''`
- Append `,` to a note to indicate a lower octave by placing a dot below it. `1,, 1,,`

<pre>1,,2,,3,,4,,5,,6,,7,,1,2,3,4,5,6,7,12345671'2'3'4'5'6'7'1''2''3''4''5''6''7''</pre>

![A scale spanning three octaves, rendered with this font.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuScale.PNG)



### Timing
- Underline a note either with a `q` (for 'quaver') *before* the note, or a slash `/` *after* it. This halves its length to an eighth note.
- Double-underline a note with an `s` (for 'quaver') *before* it, or two slashes `//` *after* it. This halves the length again to a sixteenth note.
    - If using `/`s together with octave shifts, the order of the modifier characters doesn't matter. They all just come after the digit. But stylistically, the octave marks come before the slashes, to make things consistent with other notational systems.
    - Note that the symbols `0`, `x`, `b`, `#` can be underlined in the same way notes can. For rests `0` and beats `x`, this conveys timing information. For accidentals, it's purely aesthetic.

<pre>s3,,s3,s3s3's3''q3,,q3,q3q3'q3''3,,3,33'3'' 3,,//3,//3//3'//3''//3,,/3,/3/3'/3''/3,,3,33'3''</pre>

![The same note with differing octaves and lengths.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuUnderlines.PNG)



- Place a dash `-` after a note to extend its length by one quarter note. Thus a whole note can be written `1 - - -`.
- Place a dot with `.` to extend a note by half its length. (Two dots means that a note is extended by 3/4 of its length.)
- Chords are indicated by vertically stacking notes. To do this, you'll need to type multiple lines and may need to use spaces ` ` to make sure things properly line up.

<pre>
|1' - 6|5 - 5|1' - 3'/1'/|5..4//1//2//3/|
|4 - 4|3 - 3|3 - 5 |5,- 1,  |
</pre>

![An illustration of ties and slurs and tuplets.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuChords.PNG)


### Other Symbols
- Flats are typed with `b` or `_`, and sharps with `#` or `^`. Naturals are marked with `=` (but naturals are rarely if ever needed in jianpu notation).
    - Place these before the notes. 
    - I couldn't decide how big to make the accidentals, and so I split the difference. `b` and `#` are large standalone characters, while `_`, `^`, and `=` combine with notes into compact ligatures.
    - Place the standalone accidentals before any timing prefixes. EG `#s4` for a sixteenth note F sharp. 

<pre>3#3^3b3_3 3/#/3/^3/b3/_3/</pre>

![An illustration of ties and slurs and tuplets.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuAccident.PNG)

- Bar lines are typed with `|` and `||`
- Repeat symbols are typed with `||:`, `:||:`, and `:||`
- Use `x` for a percussion beat.
- Use `[-]` and `(-)` on the line above the notes to indicate tuplets or ties. 

<pre>
 [-]     (-)
|:1/2/1/ 3 4 5:|:5 - 6 5:|1325,|1231|3125,|5,231||
</pre>

![An illustration of ties and slurs and tuplets.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuTupletsSlurs.PNG)



<!--prepending underscores also works for underlines-->

<!--
- Use `0` for a rest, and `x` for a percussion beat. These follow the same timing rules as notes and can be similarly underlined.o

- Use 0 for a rest
- Use digits 1-7 for notes
- Append `,` to a digit indicate a lower octave.
- Append `'` to indicate a higher octave.
- Append `_` to indicate a shorter note.-->


<!--A digit by itself typically represents a quarter note.-->






## Download

As mentioned above, 
[the font file can can be downloaded from the GitHub repo](https://github.com/RobertWinslow/jianpu-ascii-font/blob/main/JianpuASCII.ttf),
and then installed like any other font.

There's also a [COLRv0 version of the font](https://github.com/RobertWinslow/jianpu-ascii-font/blob/main/colrJianpu.ttf),
which displays notes in different colors.
This was made mostly just to see whether I could, is a bit glitchier, and works in fewer applications,
though it should at least work in every modern internet browser.


![The colored version of the font, all notes demonstrated.](https://robertwinslow.github.io/jianpu-ascii-font/examples/img/jianpuColr.PNG)


## Usage

For local use, like typing up a melody and printing it, you can just install the font,
and then use it like any other (though see below for some settings changes that have to be made in MS Word.)

For use on a website, just host the font file and apply it to a `pre` element using css.

Simple Example:

```html
<style>
@font-face {
    font-family: Jianpu;
    src: url("path/to/JianpuASCII.ttf");
}
.jianpuBlock {
    font-family: Jianpu;
    line-height: 1.5;
    font-size: 25px;
}
</style>
<pre class="jianpuBlock">
|1' - 6|5 - 5|1' - 3'/1'/|
|4 - 4|3 - 3|3 - 5 |
</pre>
```



### What software does this work in?

This method of rendering Jianpu musical scores relies only on basic font-rendering features,
and as such should work basically anywhere.
In my testing, this font renders correctly in the following software with the need for any settings tweaks: All major internet browsers, GIMP, Inkscape, and Libre Office, as well as Notes, Pages, and TextEdit on MacOS. *(QGIS works too, though I can't imagine a situation where you'd want to put this stuff on a map.)*

The only programs I've found in which this font doesn't work 'right out of the box'
are Microsoft Office and MS Paint. 
To get it working properly in Microsoft Word, two changes have to be made:
- First, ligatures must be turned on in the advanced font options. (Highlight the text and open the dialog with ctrl+d).
- Secondly, the "smart quotes" feature must be turned off, lest all the `'` characters be replaced with `‘` or `’`. (This option can be found in `File>Options > Proofing > AutoCorrect Options > AutoFormat As You Type`)













## Example

The following block of text will just look like a mess if viewed as a README on Github,
but if you [view the same page with this font applied](https://robertwinslow.github.io/jianpu-ascii-font/#example),
then you'll see the same [rendition of Amazing Grace as is present on Wikipedia's jianpu article](https://en.wikipedia.org/wiki/Numbered_musical_notation#Examples).

<style>
@font-face {
    font-family: Jianpu;
    src: url("JianpuASCII.ttf");
}
.jianpuBlock {
    font-family: Jianpu;
    line-height: 1.5;
    font-size: 30px;
}
</style>

<pre class="jianpuBlock">
5 |1' - q3'q1'| 3' - 2' |1' - 6|5 - 5|1' - q3'q1'|3' - q2'q3'|5' -
3 |3 - 5 |b7 -b7 |4 - 4|3 - 3|3 - 5 |1' - 5 |5 -
5, |1 - 1 | 1 - 1 |6, - 6,|1 - 1|5, - 5, |1 - 1 |7, -
1, |1, - 5, | 1, - 5, |4, - 4,|1, - 5,|1, - 3, |5, -   |5, -
 
2'/3'/|5' - 3'/1'/| 3' - 3'/2'/|1' - 6|5 - 5|1' - 3'/1'/|3' - 2'|1' - ||
5 |3 - 5 |b7 -b7 |4 - 4|3 - 3|3 - 5 |1' - 4|3 - ||
7, |5, - 1 | 1 - 1 |6, - 6,|1 - 1|5, - 5, |1 - 7,|1 - ||
5, |1, - 5, | 1, - 5, |4, - 4,|1, - 5,|1, - 1, |5, - 5,|1, - ||
</pre>

There are no scripting tricks here. It's just a font.

And here's [a link to the same example in an editable text box](https://robertwinslow.github.io/jianpu-ascii-font/examples/songs/amazinggrace),
if you'd like to play around with it.
Note that the first and second lines deliberately use different syntax for the quarter notes.









## Other Jianpu Typesetting systems.

The advantage of using this font is that the resulting musical notation can be displayed and modified in almost any software.

But of course, there is only so much one can do with font formatting tricks.
And more complex musical notation may require more specialized typesetting software.

- [Simp Erhu](https://simperhu.weebly.com/) is a plugin for Microsoft Word with many specialized symbols for use when playing the erhu. 
- [jianpu-ly](https://github.com/ssb22/jianpu-ly) has its own convention for notating Jianpu in ASCII, but doesn't render the notation itself. Instead it converts the notation into a form which [Lilypond](https://lilypond.org/) can render.
- [Fanqie Jianpu](http://zhipu.lezhi99.com/Zhipu-index.html) is a web interface for typing Jianpu, and can export the result as images.

You may also be interested in [ABC Notation](https://abcnotation.com/wiki/abc:standard:v2.1#the_tune_body),
which is a system of notating scores using ascii text. 
The conventions of using `,` `'` to denote octave shifts comes from ABC notation, (though ABC also uses capital vs lowercase letters,)
as does the use of `/` `//` for note shortening and the prefixes `^` `=` `_` for accidentals.

The use of `s` `q` prefixes for note shortening is something I took from jianpu-ly.

There are several other similarities between these notations and my syntax above, 
but these are cases of convergent evolution rather than direct inspiration.




## License

This font is released under the SIL Open Font License.

Note that this font is a derivative work of the font with Reserved Font Name 'Source', Copyright © Adobe Systems Incorporated 2010, 2012.
In particular, it uses the numerals `0123456789` from "Source Code Pro", by Paul D. Hunt, 
downloaded from Google Fonts here: [https://fonts.google.com/specimen/Source+Code+Pro](https://fonts.google.com/specimen/Source+Code+Pro)

<!--
http://anuccme.com/jianpu
https://github.com/felixhao28/react-jianpu Uses . for sidedot
http://www.jianpu.cn/
https://github.com/journey-ad/jianpu  Very bizarre notation. I don't think I will be trying to copy this.
http://www.jianpu99.net/    Same Fanqie Jianpu in the list above.
https://github.com/lzh9102/musicxml_to_jianpu
http://doc.lezhi99.com/zhipu#152  Fanqie uses slashes for underlining.
https://www.opusonemusic.net/Helpfiles/IPad/pages/CypherNotation.html
-->


<!--https://graphicdesign.stackexchange.com/questions/146896/free-fat-numeral-font-as-used-in-sheet-music-time-signatures/146902#146902
https://abcnotation.com/examples#accidentals  In ABC, flats are represented by prepending an underscore.
https://theocarinanetwork.com/decoding-jianpu-notation-t18028.html
-->



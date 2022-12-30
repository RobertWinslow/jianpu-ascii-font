# Jianpu Ascii Font

This is a font which uses ascii ligatures to display simplified Jianpu 简谱 musical notation.

<!--
TODO: Example with image.
TODO: Test page link in intro.
-->



## What software does this work in?

This method of rendering Jianpu musical scores relies only on basic font-rendering features,
and as such should work basically anywhere.
In my testing, this font renders correctly in the following software with the need for any settings tweaks: All major internet browsers, GIMP, Inkscape, and Libre Office, as well as Notes, Pages, and TextEdit on MacOS.<!--QGIS works too lol-->

The only programs I've found in which this font doesn't work 'right out of the box'
are Microsoft Office and MS Paint. 
To get it working properly in Microsoft Word, two changes have to be made:
- First, ligatures must be turned on in the advanced font options. (Highlight the text and open the dialog with ctrl+d).
- Secondly, the "smart quotes" feature must be turned off, lest all the `'` characters be replaced with `‘` or `’`. (This option can be found in `File>Options > Proofing > AutoCorrect Options > AutoFormat As You Type`)



## Syntax

The [wikipedia page for jianpu notation](https://en.wikipedia.org/wiki/Numbered_musical_notation) 
is well-written and describes how the notation works. 
Below is a list of jianpu features implemented in this font and how to use them.

### Basics

- Use digits `1234567` for notes.
- Use `0` for a rest.
- Append `'` to a note to indicate a higher octave by placing a dot above it. `1' 1''`
- Append `,` to a note to indicate a lower octave by placing a dot below it. `1,, 1,,`
- Chords are indicated by vertically stacking notes. To do this, you'll need to type multiple lines and may need to use spaces ` ` to make sure things properly line up.


### Timing
- Underline a note either with a `q` (for 'quaver') *before* the note, or a slash `/` *after* it. This halves its length to an eighth note.
- Double-underline a note with an `s` (for 'quaver') *before* it, or two slashes `//` *after* it. This halves the length again to a sixteenth note.
    - If using `/`s together with octave shifts, the order of the modifier characters doesn't matter. They all just come after the digit.
    - Note that the symbols `0`, `x`, `b`, `#`, and ` ` (space) can be underlined in the same way notes can. For rests `0` and beats `#`, this conveys timing information. For accidentals and whitespace, it's purely aesthetic.

- Place a dash `-` after after a note to extend its length by one quarter note. Thus a whole note can be written `1 - - -`.
- Place a dot, with `.` or `*`, to extend a note by half its length. (Two dots means that a note is extended by 3/4 of its length.)


### Other Symbols
- Flats are typed with `b`, and sharps with `#`. Place these before the notes. 
    - Place these before the timing prefixes as well. EG `#s4` for a sixteenth note F sharp. 
- Bar lines are typed with `|` and `||`
- Repeat symbols are typed with `||:`, `:||:`, and `:||`
- Use `x` for a percussion beat.



<!--prepending underscores also works for underlines-->

<!--
- Use `0` for a rest, and `x` for a percussion beat. These follow the same timing rules as notes and can be similarly underlined.o

- Use 0 for a rest
- Use digits 1-7 for notes
- Append `,` to a digit indicate a lower octave.
- Append `'` to indicate a higher octave.
- Append `_` to indicate a shorter note.-->


<!--A digit by itself typically represents a quarter note.-->



## Example

<style>
@font-face {
    font-family: Jianpu;
    src: url("../JianpuASCII.ttf ");
}
pre{
    font-family: Jianpu;
    line-height: 1.5 !important;
    font-size: 30px !important;
}
</style>

```
5 |1' - q3'q1'| 3' - 2' |1' - 6|5 - 5|1' - q3'q1'|3' - q2'q3'|5' -
3 |3 - 5 |b7 -b7 |4 - 4|3 - 3|3 - 5 |1' - 5 |5 -
5, |1 - 1 | 1 - 1 |6, - 6,|1 - 1|5, - 5, |1 - 1 |7, -
1, |1, - 5, | 1, - 5, |4, - 4,|1, - 5,|1, - 3, |5, -   |5, -
 
2'/3'/|5' - 3'/1'/| 3' - 3'/2'/|1' - 6|5 - 5|1' - 3'/1'/|3' - 2'|1' - ||
5 |3 - 5 |b7 -b7 |4 - 4|3 - 3|3 - 5 |1' - 4'|3 - ||
7, |5, - 1 | 1 - 1 |6, - 6,|1 - 1|5, - 5, |1 - 7,|1 - ||
5, |1, - 5, | 1, - 5, |4, - 4,|1, - 5,|1, - 1, |5, - 5,|1, - ||
```










## Other Jianpu Typesetting systems.

The advantage of using this font is that the resulting musical notation can be displayed and modified in almost any software.

But of course, there is only so much one can do with font formatting tricks.
And more complex musical notation may require more specialized typesetting software.

- [Simp Erhu](https://simperhu.weebly.com/) is a plugin for Microsoft Word with many specialized symbols for use when playing the erhu. 
- [jianpu-ly](https://github.com/ssb22/jianpu-ly) has its own convention for notating Jianpu in ASCII, but doesn't render the notation itself. Instead it converts the notation into a form which [Lilypond](https://lilypond.org/) can render.
- [Fanqie Jianpu](http://zhipu.lezhi99.com/Zhipu-index.html) is a web interface for typing Jianpu, and can export the result as images.


## License

This font is released under the SIL Open Font License.

Note that this font is a derivative work of the font with Reserved Font Name 'Source', Copyright © Adobe Systems Incorporated 2010, 2012.
In particular, it uses the numerals 0123456789 from "Source Code Pro", by Paul D. Hunt, 
downloaded from Google Fonts here: https://fonts.google.com/specimen/Source+Code+Pro

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



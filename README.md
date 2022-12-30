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

- Use digits `1234567` to represent the notes of the diatonic scale. 
- Dots above the digit represent going up one octave. Type apostrophes after the digit to place dots above: `1' 1''`
- Dots below the digit represent going down one octave. Type commas after the digit to place dots below: `1,, 1,`
- Chords are indicated by typing multiple lines. Notes in the same column are played simultaneously.
- In this font, spaces are whitespace characters, and have no inherent musical meaning, but are important for making sure chords line up properly<!-- and otherwise making things look nice-->. 


### Timing
- Underlining a note halves its length to an eighth note. You can underline a note either by typing a `q` (for 'quaver') *before* the note, or by typing a slash `/` *after* the note. Both `s1` and `1/` indicate an eight note C, and display the same.
- A double underline halves the length again to a sixteenth note. You can double-underline a note either by typing an `s` (for 'semiquaver') before the note, or by typing two slashes `//` after the note.
  - If using `/`s together with octave shifts, the order of the modifier characters doesn't matter. They all just come after the digit.

- A note is extended by a quarter note (crotchet) by placing a dash `-` after it. Thus a whole note can be written `1 - - -`.
- A note is extended by half its length by placing a dot after it. These dots can be typed as `.` or `*`. Two dots, typed with `..` or `**` indicates that a note is extended by 3/4 of its length.
- Use `0` for a rest, and `x` for a percussion beat. These follow the same timing rules as notes and can be similarly underlined.

### Other Symbols
- Flats are typed with `b`, and sharps with `#`. Place these before the notes. These are rendered as seperate characters, and should be placed before the timing prefixes as well. EG `#s4` would be a sixteenth note F sharp. 
- Bar lines are typed with `|` and `||`
- Repeat symbols are typed with `||:`, `:||:`, and `:||`

<!--prepending underscores also works for underlines-->

<!--
- Use `0` for a rest, and `x` for a percussion beat. These follow the same timing rules as notes and can be similarly underlined.o

- Use 0 for a rest
- Use digits 1-7 for notes
- Append `,` to a digit indicate a lower octave.
- Append `'` to indicate a higher octave.
- Append `_` to indicate a shorter note.-->


<!--A digit by itself typically represents a quarter note.-->



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
-->

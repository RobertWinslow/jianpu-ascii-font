# Jianpu Ascii Font

This is a font which uses ascii ligatures to display simplified Jianpu 简谱 musical notation. 简谱

This is a work in progress, but the font file is at least partially functional.

- Use 0 for a rest
- Use digits 1-7 for notes
- Append `,` to a digit indicate a lower octave.
- Append `'` to indicate a higher octave.
- Append `_` to indicate a shorter note.



## What software does this work in?

This method of rendering Jianpu musical scores relies only on basic font-rendering features,
and as such should work basically anywhere.
In my testing, this font renders correctly in the following software with the need for any settings tweaks: All major internet browsers, GIMP, Inkscape, and Libre Office, as well as Notes, Pages, and TextEdit on MacOS.<!--QGIS works too lol-->

The only programs I've found in which this font doesn't work 'right out of the box'
are Microsoft Office and MS Paint. 
To get it working properly in Microsoft Word, two changes have to be made:
- First, ligatures must be turned on in the advanced font options. (Highlight the text and open the dialog with ctrl+d).
- Secondly, the "smart quotes" feature must be turned off, lest all the `'` characters be replaced with `‘` or `’`. (This option can be found in `File>Options > Proofing > AutoCorrect Options > AutoFormat As You Type`)





## Other Jianpu Typesetting systems.

The advantage of using this font is that the resulting musical notation can be displayed and modified in almost any software.

But of course, there is only so much one can do with font formatting tricks.
And more complex musical notation may require more specialized typesetting software.

- [Simp Erhu](https://simperhu.weebly.com/) is a plugin for Microsoft Word with many specialized symbols for use when playing the erhu. 
- [jianpu-ly](https://github.com/ssb22/jianpu-ly) has its own convention for notating Jianpu in ASCII, but doesn't render the notation itself. Instead it converts the notation into a form which [Lilypond](https://lilypond.org/) can render.
- [Fanqie Jianpu](http://zhipu.lezhi99.com/Zhipu-index.html) is a web interface for typing Jianpu, and can export the result as images.



<!--
http://anuccme.com/jianpu
https://github.com/felixhao28/react-jianpu Uses . for sidedot
http://www.jianpu.cn/
https://github.com/journey-ad/jianpu  Very bizarre notation. I don't think I will be trying to copy this.
http://www.jianpu99.net/    Same Fanqie Jianpu in the list above.
https://github.com/lzh9102/musicxml_to_jianpu
http://doc.lezhi99.com/zhipu#152  Fanqie uses slashes for underlining.
-->


<!--https://graphicdesign.stackexchange.com/questions/146896/free-fat-numeral-font-as-used-in-sheet-music-time-signatures/146902#146902-->

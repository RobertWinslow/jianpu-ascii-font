# -*- coding: utf-8 -*-
'''
To Use:
1. Adjust the global parameters in the first section below.
2. type `fontforge -script build_black_font_from_components.py` in the terminal.

Description:
This script uses FontForge to build a very basic monochrome font from a folder of SVG files.
This particular script is specialized to make a Jianpu font using extensive ligatures.
See here for a more generalized script:
https://github.com/RobertWinslow/Simple-SVG-to-Font-with-Fontforge

See here for documentation about FontForge's scripting library:
https://fontforge.org/docs/scripting/python/fontforge.html
'''


#%% SECTION ONE - Imports and parameters
import fontforge
import os

INPUTFOLDER = 'svg/components'
OUTPUTFILENAME = '../JianpuASCII.ttf'

font = fontforge.font()
font.familyname = "Jianpu Ascii"
font.fullname = font.familyname
font.copyright = "SIL OFL. Created 2022 by Robert Martin Winslow" #eg Copyright (c) 2022 Name
font.version = "1.0"

# The following variables are for scaling the imported outlines.
SVGHEIGHT = 150 # units of height of source svg viewbox.
GLYPHHEIGHT = 1500 # font units, default = 1000
#PORTIONABOVEBASELINE = 0.633333 # default is 0.8
UNITSABOVEBASELINE = 950
# If the following parameter is set to a positive integer, all characters are set to that width.
# Set it to 0 or None to make the font non-monospaced.
MONOSPACEWIDTH = 600
# If the following parameter is set to a positive integer, a blank 'space' character is included in the font.
SPACEWIDTH = MONOSPACEWIDTH


#%% SECTION TWO A - Define function for importing outlines.

def importAndCleanOutlines(outlinefile,glyph):
    #print(outlinefile)
    glyph.importOutlines(outlinefile, simplify=False, correctdir=True, accuracy=0.01, scale=False)
    glyph.removeOverlap()
    SCALEFACTOR = GLYPHHEIGHT/SVGHEIGHT
    foregroundlayer = glyph.foreground
    for contour in foregroundlayer:
        for point in contour:
            point.transform((1,0,0,1,0,-800)) # Translate top of glyph down to baseline.
            point.transform((SCALEFACTOR,0,0,SCALEFACTOR,0,0)) # Scale up. Top of glyph will remain at baseline. 
            point.transform((1,0,0,1,0,UNITSABOVEBASELINE)) # translate up to desired cap height
    glyph.setLayer(foregroundlayer,'Fore')



#%% SECTION TWO B - Import basic characters.
def createBasicCharacter(codepoint, glyphname, vectorfilename, width = MONOSPACEWIDTH):
    char = font.createChar(int(codepoint,16), glyphname)
    importAndCleanOutlines(f'{INPUTFOLDER}/{vectorfilename}.svg',char)
    char.width = width
createBasicCharacter('0030','0','0')
createBasicCharacter('0031','1','1')
createBasicCharacter('0032','2','2')
createBasicCharacter('0033','3','3')
createBasicCharacter('0034','4','4')
createBasicCharacter('0035','5','5')
createBasicCharacter('0036','6','6')
createBasicCharacter('0037','7','7')
createBasicCharacter('0078','x','x')
createBasicCharacter('0058','X','x')
createBasicCharacter('002c','comma','downoctave')
createBasicCharacter('0027','prime','upoctave')
createBasicCharacter('002e','period','sidedot')
createBasicCharacter('002a','cdot','sidedot')
createBasicCharacter('0062','b','flat')
createBasicCharacter('0023','hash','sharp')
createBasicCharacter('002d','minus','dash')
createBasicCharacter('007c','bar','bar')
createBasicCharacter('005f','underscore','underscore', width=0)
createBasicCharacter('0071','q','underscore', width=0) # alternate underline. q short for 'quaver', meaning an eighth note
spaceChar = font.createChar(32, 'space')
spaceChar.width = SPACEWIDTH

# TODO: symbols for chord types ala Nashville number system?



#%% SECTION TWO C - Create combination characters with references and ligatures.

# To be quite honest, I don't fully understand what this syntax up front is doing.
# Just treat these next couple of lines as if they are a mystical incantation.
font.addLookup('myLookup','gsub_ligature',None,(("liga",(('DFLT',("dflt")),)),))
font.addLookupSubtable("myLookup", "mySubtable")

# First, some special cases
## The semiquaver / double underline. Base codepoint is the letter s, with '__' as a ligature mapped to it as well.
char = font.createChar(int('0073',16), 'doubleUnderscore')
char.addReference('underscore', (1,0,0,1,0,0)) # -MONOSPACEWIDTH in penultimate value to make it go under the character to the left.
char.addReference('underscore', (1,0,0,1,0,-80))
#char.addPosSub("mySubtable", ('underscore','underscore',))

## Double dot
char = font.createChar(-1, 'doubleDot')
char.addReference('cdot', (1,0,0,1,-50,0)) 
char.addReference('cdot', (1,0,0,1,180,0))
char.addPosSub("mySubtable", ('cdot','cdot',))
char.addPosSub("mySubtable", ('period','period',))

## Slash / for an underline *after* the character
char = font.createChar(int('002f',16), 'slash')
char.addReference('underscore', (1,0,0,1, 0,0)) # -MONOSPACEWIDTH in penultimate value to make it go under the character to the left.

## And a doubleslash likewise.
## This is tricky because I want to be able to type a single _ by itself, but also type a __ by itself.
## I've compromised by only adding the ligature for the slash version.
## TODO: Mabye I should add ligatures via spaces? Or include = as a way to type a double line?
char = font.createChar(-1, 'doubleSlash')
char.addReference('doubleUnderscore', (1,0,0,1, 0,0)) 
char.addPosSub("mySubtable", ('slash','slash',))


GAPBETWEENDOTS = 125
DOTSHIFTFROMLINE = 80

# Here I create some ligatures for each digit. 
# Some of these ligatures could be ignored in favor of zero-width trickery.
# But I'm just not personally a fan of setting a character to be zero width.
# I like how the cursor is rendered part-way through the glyph when in the middle of a ligature sequence.
for digit in ['1','2','3','4','5','6','7',]+['X','x','0','b','hash',]:
    # Single underline for quaver
    char = font.createChar(-1, f'{digit}_Quaver')
    char.addReference(digit)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addPosSub("mySubtable", ('underscore',digit,))
    char.addPosSub("mySubtable", ('q',digit,))
    char.addPosSub("mySubtable", (digit,'slash',))
    
    # double underline for a semiquaver
    char = font.createChar(-1, f'{digit}_Semiquaver')
    char.addReference(digit)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,))
    char.addPosSub("mySubtable", (digit,'slash','slash',))
    

for digit in ['1','2','3','4','5','6','7',]:
    # up an octave
    char = font.createChar(-1, f'{digit}up')
    char.addReference(digit)
    char.addReference('prime', (1,0,0,1,0,0))
    char.addPosSub("mySubtable", (digit,'prime',))
    
    # up two octaves
    char = font.createChar(-1, f'{digit}upTwo')
    char.addReference(digit)
    char.addReference('prime', (1,0,0,1,0,0))
    char.addReference('prime', (1,0,0,1,0,GAPBETWEENDOTS))
    char.addPosSub("mySubtable", (digit,'prime','prime',))
    
    # down one octave
    char = font.createChar(-1, f'{digit}down')
    char.addReference(digit)
    char.addReference('comma', (1,0,0,1,0,0))
    char.addPosSub("mySubtable", (digit,'comma',))
    
    # down two octaves
    char = font.createChar(-1, f'{digit}downTwo')
    char.addReference(digit)
    char.addReference('comma', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-GAPBETWEENDOTS))
    char.addPosSub("mySubtable", (digit,'comma','comma',))
    

    # down one octave with underline for a quaver
    char = font.createChar(-1, f'{digit}downQuaver')
    char.addReference(digit)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    char.addPosSub("mySubtable", ('underscore',digit,'comma',))
    char.addPosSub("mySubtable", ('q',digit,'comma',))
    char.addPosSub("mySubtable", (digit,'comma','slash',))
    char.addPosSub("mySubtable", (digit,'slash','comma',))
    
    # down two octaves with underline for a quaver
    char = font.createChar(-1, f'{digit}downTwoQuaver')
    char.addReference(digit)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    char.addPosSub("mySubtable", ('q',digit,'comma','comma',))
    char.addPosSub("mySubtable", ('underscore',digit,'comma','comma',))
    char.addPosSub("mySubtable", (digit,'comma','comma','slash',))
    char.addPosSub("mySubtable", (digit,'slash','comma','comma',))
    char.addPosSub("mySubtable", (digit,'comma','slash','comma',))
    
    # down one octave with double underlines for a semiquaver
    char = font.createChar(-1, f'{digit}downSemiquaver')
    char.addReference(digit)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,'comma',))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,'comma',))
    char.addPosSub("mySubtable", (digit,'comma','slash','slash',))
    char.addPosSub("mySubtable", (digit,'slash','slash','comma',))
    char.addPosSub("mySubtable", (digit,'slash','comma','slash',))
    
    # down two octaves with double underlines for a semiquaver
    char = font.createChar(-1, f'{digit}downTwoSemiquaver')
    char.addReference(digit)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,'comma','comma',))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,'comma','comma',))
    char.addPosSub("mySubtable", (digit,'comma','comma','slash','slash',))
    char.addPosSub("mySubtable", (digit,'slash','slash','comma','comma',))
    char.addPosSub("mySubtable", (digit,'slash','comma','slash','comma',))
    char.addPosSub("mySubtable", (digit,'slash','comma','comma','slash',))
    char.addPosSub("mySubtable", (digit,'comma','slash','slash','comma',))
    char.addPosSub("mySubtable", (digit,'comma','slash','comma','slash',))
    
    
    # Up one octave with a single underline
    char = font.createChar(-1, f'{digit}upQuaver')
    char.addReference(f'{digit}up')
    char.addReference('underscore')
    char.addPosSub("mySubtable", ('q',digit,'prime',))
    char.addPosSub("mySubtable", ('underscore',digit,'prime',))
    char.addPosSub("mySubtable", (digit,'prime','slash',))
    char.addPosSub("mySubtable", (digit,'slash','prime',))
    
    # Up two octaves with a single underline
    char = font.createChar(-1, f'{digit}upTwoQuaver')
    char.addReference(f'{digit}upTwo')
    char.addReference('underscore')
    char.addPosSub("mySubtable", ('q',digit,'prime','prime',))
    char.addPosSub("mySubtable", ('underscore',digit,'prime','prime',))
    char.addPosSub("mySubtable", (digit,'prime','prime','slash',))
    char.addPosSub("mySubtable", (digit,'slash','prime','prime',))
    char.addPosSub("mySubtable", (digit,'prime','slash','prime',))
    
    # Up one octave with a double underline
    char = font.createChar(-1, f'{digit}upSemiquaver')
    char.addReference(f'{digit}up')
    char.addReference('doubleUnderscore')
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,'prime',))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,'prime',))
    char.addPosSub("mySubtable", (digit,'prime','slash','slash',))
    char.addPosSub("mySubtable", (digit,'slash','slash','prime',))
    char.addPosSub("mySubtable", (digit,'slash','prime','slash',))
    
    # Up two octaves with a double underline
    char = font.createChar(-1, f'{digit}upTwoSemiquaver')
    char.addReference(f'{digit}upTwo')
    char.addReference('doubleUnderscore')
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,'prime','prime',))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,'prime','prime',))
    char.addPosSub("mySubtable", (digit,'prime','prime','slash','slash',))
    char.addPosSub("mySubtable", (digit,'slash','slash','prime','prime',))
    char.addPosSub("mySubtable", (digit,'slash','prime','slash','prime',))
    char.addPosSub("mySubtable", (digit,'slash','prime','prime','slash',))
    char.addPosSub("mySubtable", (digit,'prime','slash','slash','prime',))
    char.addPosSub("mySubtable", (digit,'prime','slash','prime','slash',))




#%% SECTION THREE - Adjust some of the font's global properties.
for char in font.glyphs():
    char.width = MONOSPACEWIDTH


#%% FINALLY - Generate the font
print("Generating black font to", OUTPUTFILENAME)
font.generate(OUTPUTFILENAME)


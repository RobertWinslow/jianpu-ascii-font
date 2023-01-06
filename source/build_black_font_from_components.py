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
font.version = "1.1"

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
def createBasicCharacter(codepoint, glyphname, vectorfilename,):
    char = font.createChar(int(codepoint,16), glyphname)
    importAndCleanOutlines(f'{INPUTFOLDER}/{vectorfilename}.svg',char)
    return char
createBasicCharacter('0030','0','0')
createBasicCharacter('0031','1','1')
createBasicCharacter('0032','2','2')
createBasicCharacter('0033','3','3')
createBasicCharacter('0034','4','4')
createBasicCharacter('0035','5','5')
createBasicCharacter('0036','6','6')
createBasicCharacter('0037','7','7')
createBasicCharacter('0078','x','x')
#createBasicCharacter('0058','X','x')
createBasicCharacter('002c','comma','downoctave')
createBasicCharacter('0027','prime','upoctave')
createBasicCharacter('002e','period','sidedot')
createBasicCharacter('002a','cdot','sidedot')
createBasicCharacter('0062','flat','flat')#b
createBasicCharacter('0023','sharp','sharp')##
createBasicCharacter('002d','minus','dash')
createBasicCharacter('007c','bar','bar')
createBasicCharacter('003a','colon','colon')
createBasicCharacter('005f','underscore','underscore')
createBasicCharacter('0071','q','underscore') # alternate underline. q short for 'quaver', meaning an eighth note
createBasicCharacter('002f','slash','underscore') # appended slash indicates an underline in tomato jianpu
createBasicCharacter('0073','doubleUnderscore','doubleUnderscore') # This is mapped to the letter s, for "semiquaver".
createBasicCharacter('005b','tupletLeft','tupletLeft')
createBasicCharacter('005d','tupletRight','tupletRight')
createBasicCharacter('0028','slurLeft','slurLeft')
createBasicCharacter('0029','slurRight','slurRight')
spaceChar = font.createChar(32, 'space')
spaceChar.width = SPACEWIDTH



#%% SECTION TWO C - Create combination characters with references and ligatures.

# To be quite honest, I don't fully understand what this syntax up front is doing.
# Just treat these next couple of lines as if they are a mystical incantation.
font.addLookup('myLookup','gsub_ligature',None,(("liga",(('DFLT',("dflt")),)),))
font.addLookupSubtable("myLookup", "mySubtable")

# First, some special cases
## Double dot
char = font.createChar(-1, 'doubleDot')
importAndCleanOutlines(f'{INPUTFOLDER}/doubleDot.svg',char)
char.addPosSub("mySubtable", ('cdot','cdot',))
char.addPosSub("mySubtable", ('period','period',))

## Double bar ||
char = font.createChar(-1, 'doubleBar')
importAndCleanOutlines(f'{INPUTFOLDER}/doubleBar.svg',char)
char.addPosSub("mySubtable", ('bar','bar',))
## Repeat signs
# :|
char = font.createChar(-1, 'repeatRight')
importAndCleanOutlines(f'{INPUTFOLDER}/repeatRight.svg',char)
char.addPosSub("mySubtable", ('colon','bar',))
char.addPosSub("mySubtable", ('colon','bar','bar',))
# |:
char = font.createChar(-1, 'repeatLeft')
importAndCleanOutlines(f'{INPUTFOLDER}/repeatLeft.svg',char)
char.addPosSub("mySubtable", ('bar','colon',))
char.addPosSub("mySubtable", ('bar','bar','colon',))
# :|:
char = font.createChar(-1, 'repeatBoth')
importAndCleanOutlines(f'{INPUTFOLDER}/repeatBoth.svg',char)
char.addPosSub("mySubtable", ('colon','bar','colon',))
char.addPosSub("mySubtable", ('colon','bar','bar','colon',))


# Function which means I don't need to manually do all the permutations.
from itertools import permutations
def addSubs(char, digit,before=(),after=()):
    if isinstance(before, str):
        before = (before,)
    if isinstance(after, str):
        after = (after,)
    for prefix in set(permutations(before)):
        for suffix in set(permutations(after)):
            substitutionTuple = prefix+(digit,)+suffix
            char.addPosSub("mySubtable", substitutionTuple)

def createLigBase(basename,namesuffix):
    char = font.createChar(-1, basename+namesuffix)
    char.addReference(basename)
    return char


# parameters for octave dot spacing
GAPBETWEENDOTS = 150
DOTSHIFTFROMLINE = 80

# Here I create some ligatures for each digit. 
# Some of these ligatures could be ignored in favor of zero-width trickery.
# But I'm just not personally a fan of setting a character to be zero width.
# I like how the cursor is rendered part-way through the glyph when in the middle of a ligature sequence.
for digit in ['1','2','3','4','5','6','7',]+['x','0','flat','sharp','space']:
    # Single underline for quaver
    char = createLigBase(digit, '_Quaver')
    char.addReference('underscore', (1,0,0,1,0,0))
    addSubs(char, digit, before=("q"))
    addSubs(char, digit, after=("slash"))
    
    # double underline for a semiquaver
    char = createLigBase(digit, '_Semiquaver')
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    addSubs(char, digit, before=("doubleUnderscore"))
    addSubs(char, digit, after=("slash","slash"))
    

for digit in ['1','2','3','4','5','6','7',]:
    # up an octave
    char = createLigBase(digit, 'up')
    char.addReference('prime', (1,0,0,1,0,0))
    addSubs(char, digit, after=("prime"))
    
    # up two octaves
    char = createLigBase(digit, 'upTwo')
    char.addReference('prime', (1,0,0,1,0,0))
    char.addReference('prime', (1,0,0,1,0,GAPBETWEENDOTS))
    addSubs(char, digit, after=("prime","prime"))
    
    # down one octave
    char = createLigBase(digit, 'down')
    char.addReference('comma', (1,0,0,1,0,0))
    addSubs(char, digit, after=("comma"))
    
    # down two octaves
    char = createLigBase(digit, 'downTwo')
    char.addReference('comma', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-GAPBETWEENDOTS))
    addSubs(char, digit, after=("comma","comma"))
    

    # down one octave with underline for a quaver
    char = createLigBase(digit, 'downQuaver')
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    addSubs(char, digit, before=('q',), after=("comma"))
    addSubs(char, digit, after=("slash","comma"))
    
    # down two octaves with underline for a quaver
    char = createLigBase(digit, 'downTwoQuaver')
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    addSubs(char, digit, before=('q',), after=("comma","comma"))
    addSubs(char, digit, after=("slash","comma","comma"))
    
    # down one octave with double underlines for a semiquaver
    char = createLigBase(digit, 'downSemiquaver')
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    addSubs(char, digit, before=('doubleUnderscore',), after=("comma"))
    addSubs(char, digit, after=("slash","slash","comma"))
    
    # down two octaves with double underlines for a semiquaver
    char = createLigBase(digit, 'downTwoSemiquaver')
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    addSubs(char, digit, before=('doubleUnderscore',), after=("comma","comma"))
    addSubs(char, digit, after=("slash","slash","comma","comma"))
    
    
    # Up one octave with a single underline
    char = createLigBase(digit+'up', 'Quaver')
    char.addReference('underscore')
    addSubs(char, digit, before=('q',), after=("prime"))
    addSubs(char, digit, after=("slash","prime"))
    
    # Up two octaves with a single underline
    char = createLigBase(digit+'upTwo', 'Quaver')
    char.addReference('underscore')
    addSubs(char, digit, before=('q',), after=("prime","prime"))
    addSubs(char, digit, after=("slash","prime","prime"))
    
    # Up one octave with a double underline
    char = createLigBase(digit+'up', 'Semiquaver')
    char.addReference('doubleUnderscore')
    addSubs(char, digit, before=('doubleUnderscore',), after=("prime"))
    addSubs(char, digit, after=("slash","slash","prime"))
    
    # Up two octaves with a double underline
    char = createLigBase(digit+'upTwo', 'Semiquaver')
    char.addReference('doubleUnderscore')
    addSubs(char, digit, before=('doubleUnderscore',), after=("prime","prime"))
    addSubs(char, digit, after=("slash","slash","prime","prime"))




#%% SECTION THREE - Adjust some of the font's global properties.
for char in font.glyphs():
    char.width = MONOSPACEWIDTH


#%% FINALLY - Generate the font
print("Generating black font to", OUTPUTFILENAME)
font.generate(OUTPUTFILENAME)


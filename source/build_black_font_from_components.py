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
def addSubs(char, digit,before=(),after=(), accident=None):
    if isinstance(before, str):
        before = (before,)
    if isinstance(after, str):
        after = (after,)
    if accident:
        before = before+(accident,)
    for prefix in set(permutations(before)):
        for suffix in set(permutations(after)):
            substitutionTuple = prefix+(digit,)+suffix
            char.addPosSub("mySubtable", substitutionTuple)

def createLigBase(basename,namesuffix, accident=''):
    char = font.createChar(-1, basename+accident+namesuffix)
    char.addReference(basename)
    if accident:
        char.addReference(accident, (0.6,0,0,0.8,-250,130))
    return char

for accident in ['flat','sharp']:
    for digit in ['1','2','3','4','5','6','7',]:
        char = createLigBase(digit,'', accident=accident)
        addSubs(char, digit, accident=accident)


# parameters for octave dot spacing
GAPBETWEENDOTS = 150
DOTSHIFTFROMLINE = 80

# Here I create some ligatures for each digit. 
# Some of these ligatures could be ignored in favor of zero-width trickery.
# But I'm just not personally a fan of setting a character to be zero width.
# I like how the cursor is rendered part-way through the glyph when in the middle of a ligature sequence.
for digit in ['x','0','flat','sharp','space', 'period',]:
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
    
for accident in ["","sharp","flat"]:
  for digit in ['1','2','3','4','5','6','7',]:
    # Single underline for quaver
    char = createLigBase(digit, '_Quaver', accident=accident)
    char.addReference('underscore', (1,0,0,1,0,0))
    addSubs(char, digit, before=("q"), accident=accident)
    addSubs(char, digit, after=("slash"), accident=accident)
    
    # double underline for a semiquaver
    char = createLigBase(digit, '_Semiquaver', accident=accident)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    addSubs(char, digit, before=("doubleUnderscore"), accident=accident)
    addSubs(char, digit, after=("slash","slash"), accident=accident)

    # up an octave
    char = createLigBase(digit, 'up', accident=accident)
    char.addReference('prime', (1,0,0,1,0,0))
    addSubs(char, digit, after=("prime"), accident=accident)
    
    # up two octaves
    char = createLigBase(digit, 'upTwo', accident=accident)
    char.addReference('prime', (1,0,0,1,0,0))
    char.addReference('prime', (1,0,0,1,0,GAPBETWEENDOTS))
    addSubs(char, digit, after=("prime","prime"), accident=accident)
    
    # down one octave
    char = createLigBase(digit, 'down', accident=accident)
    char.addReference('comma', (1,0,0,1,0,0))
    addSubs(char, digit, after=("comma"), accident=accident)
    
    # down two octaves
    char = createLigBase(digit, 'downTwo', accident=accident)
    char.addReference('comma', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-GAPBETWEENDOTS))
    addSubs(char, digit, after=("comma","comma"), accident=accident)
    

    # down one octave with underline for a quaver
    char = createLigBase(digit, 'downQuaver', accident=accident)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    addSubs(char, digit, before=('q',), after=("comma"), accident=accident)
    addSubs(char, digit, after=("slash","comma"), accident=accident)
    
    # down two octaves with underline for a quaver
    char = createLigBase(digit, 'downTwoQuaver', accident=accident)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    addSubs(char, digit, before=('q',), after=("comma","comma"), accident=accident)
    addSubs(char, digit, after=("slash","comma","comma"), accident=accident)
    
    # down one octave with double underlines for a semiquaver
    char = createLigBase(digit, 'downSemiquaver', accident=accident)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    addSubs(char, digit, before=('doubleUnderscore',), after=("comma"), accident=accident)
    addSubs(char, digit, after=("slash","slash","comma"), accident=accident)
    
    # down two octaves with double underlines for a semiquaver
    char = createLigBase(digit, 'downTwoSemiquaver', accident=accident)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    addSubs(char, digit, before=('doubleUnderscore',), after=("comma","comma"), accident=accident)
    addSubs(char, digit, after=("slash","slash","comma","comma"), accident=accident)
    
    
    # Up one octave with a single underline
    char = createLigBase(digit+accident+'up', 'Quaver', accident=accident)
    char.addReference('underscore')
    addSubs(char, digit, before=('q',), after=("prime"), accident=accident)
    addSubs(char, digit, after=("slash","prime"), accident=accident)
    
    # Up two octaves with a single underline
    char = createLigBase(digit+accident+'upTwo', 'Quaver', accident=accident)
    char.addReference('underscore')
    addSubs(char, digit, before=('q',), after=("prime","prime"), accident=accident)
    addSubs(char, digit, after=("slash","prime","prime"), accident=accident)
    
    # Up one octave with a double underline
    char = createLigBase(digit+accident+'up', 'Semiquaver', accident=accident)
    char.addReference('doubleUnderscore')
    addSubs(char, digit, before=('doubleUnderscore',), after=("prime"), accident=accident)
    addSubs(char, digit, after=("slash","slash","prime"), accident=accident)
    
    # Up two octaves with a double underline
    char = createLigBase(digit+accident+'upTwo', 'Semiquaver', accident=accident)
    char.addReference('doubleUnderscore')
    addSubs(char, digit, before=('doubleUnderscore',), after=("prime","prime"), accident=accident)
    addSubs(char, digit, after=("slash","slash","prime","prime"), accident=accident)




#%% SECTION THREE - Adjust some of the font's global properties.
for char in font.glyphs():
    char.width = MONOSPACEWIDTH


#%% FINALLY - Generate the font
print("Generating black font to", OUTPUTFILENAME)
font.generate(OUTPUTFILENAME)


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

Script (c) 2026 Robert Winslow. CC BY-SA. See: https://github.com/RobertWinslow/Simple-SVG-to-Font-with-Fontforge
'''


#%% SECTION ONE - Imports and parameters
import fontforge
import os

INPUTFOLDER = 'svg/components'
OUTPUTFILENAME = '../JianpuASCII.ttf'

font = fontforge.font()
font.familyname = "Jianpu Ascii"
font.fullname = font.familyname
font.copyright = "SIL OFL. Created 2026 by Robert Martin Winslow" #eg Copyright (c) 2022 Name
font.version = "3.1"

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

# The following variables are for single-line chords.
# These variables determine the scale and vertical offset of each note in the chord.
COMPACTCHORDSCALE = {2: 0.63, 3: 0.46, 4: 0.36}
COMPACTCHORDPOSITION = {
    2: [440, -390],
    3: [600, 80, -440],
    4: [700, 310, -80, -470],
}




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
createBasicCharacter('0062','b','flat')#b
createBasicCharacter('005f','flat','flatSmall')#_
createBasicCharacter('0023','hash','sharp')##
createBasicCharacter('005e','sharp','sharpSmall')#^
createBasicCharacter('003d','natural','naturalSmall')#=
createBasicCharacter('002d','minus','dash')
createBasicCharacter('007c','bar','bar')
createBasicCharacter('003a','colon','colon')
#createBasicCharacter('005f','underline','underline')
createBasicCharacter('0071','underline','underline') # alternate underline. q short for 'quaver', meaning an eighth note
createBasicCharacter('002f','slash','underline') # appended slash indicates an underline in tomato jianpu
createBasicCharacter('0073','doubleUnderline','doubleUnderline') # This is mapped to the letter s, for "semiquaver".
createBasicCharacter('005b','tupletLeft','tupletLeft')
createBasicCharacter('005d','tupletRight','tupletRight')
createBasicCharacter('0028','slurLeft','slurLeft')
createBasicCharacter('0029','slurRight','slurRight')

createBasicCharacter('0048','fermata','fermata')#H
createBasicCharacter('0054','trill','trill')#T
createBasicCharacter('0074','tremolo','tremolo')#t
createBasicCharacter('007b','arpeggioLeft','arpeggio') #{
arpeggioRight = font.createChar(int('007d', 16), 'arpeggioRight') #}, implemented as a reflected version of the { glyph.
arpeggioRight.addReference('arpeggioLeft', (-1,0,0,1,MONOSPACEWIDTH,0))

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
        char.addReference(accident, (1,0,0,1,0,0))
    return char

for accident in ['flat','sharp','natural']:
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
for digit in ['x','0','period', 'flat','sharp','natural','hash','b','cdot']: #'space',
    # Single underline for quaver
    char = createLigBase(digit, '_Quaver')
    char.addReference('underline', (1,0,0,1,0,0))
    addSubs(char, digit, before=('underline'))
    addSubs(char, digit, after=("slash"))
    
    # double underline for a semiquaver
    char = createLigBase(digit, '_Semiquaver')
    char.addReference('doubleUnderline', (1,0,0,1,0,0))
    addSubs(char, digit, before=("doubleUnderline"))
    addSubs(char, digit, after=("slash","slash"))
    
for accident in ["","sharp","flat","natural"]:
  for digit in ['1','2','3','4','5','6','7',]:
    # Single underline for quaver
    char = createLigBase(digit, '_Quaver', accident=accident)
    char.addReference('underline', (1,0,0,1,0,0))
    addSubs(char, digit, before=('underline'), accident=accident)
    addSubs(char, digit, after=("slash"), accident=accident)
    
    # double underline for a semiquaver
    char = createLigBase(digit, '_Semiquaver', accident=accident)
    char.addReference('doubleUnderline', (1,0,0,1,0,0))
    addSubs(char, digit, before=("doubleUnderline"), accident=accident)
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
    char.addReference('underline', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    addSubs(char, digit, before=('underline',), after=("comma"), accident=accident)
    addSubs(char, digit, after=("slash","comma"), accident=accident)
    
    # down two octaves with underline for a quaver
    char = createLigBase(digit, 'downTwoQuaver', accident=accident)
    char.addReference('underline', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    addSubs(char, digit, before=('underline',), after=("comma","comma"), accident=accident)
    addSubs(char, digit, after=("slash","comma","comma"), accident=accident)
    
    # down one octave with double underlines for a semiquaver
    char = createLigBase(digit, 'downSemiquaver', accident=accident)
    char.addReference('doubleUnderline', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    addSubs(char, digit, before=('doubleUnderline',), after=("comma"), accident=accident)
    addSubs(char, digit, after=("slash","slash","comma"), accident=accident)
    
    # down two octaves with double underlines for a semiquaver
    char = createLigBase(digit, 'downTwoSemiquaver', accident=accident)
    char.addReference('doubleUnderline', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE))
    char.addReference('comma', (1,0,0,1,0,-2*DOTSHIFTFROMLINE-GAPBETWEENDOTS))
    addSubs(char, digit, before=('doubleUnderline',), after=("comma","comma"), accident=accident)
    addSubs(char, digit, after=("slash","slash","comma","comma"), accident=accident)
    
    
    # Up one octave with a single underline
    char = createLigBase(digit+accident+'up', 'Quaver', accident=accident)
    char.addReference('underline')
    addSubs(char, digit, before=('underline',), after=("prime"), accident=accident)
    addSubs(char, digit, after=("slash","prime"), accident=accident)
    
    # Up two octaves with a single underline
    char = createLigBase(digit+accident+'upTwo', 'Quaver', accident=accident)
    char.addReference('underline')
    addSubs(char, digit, before=('underline',), after=("prime","prime"), accident=accident)
    addSubs(char, digit, after=("slash","prime","prime"), accident=accident)
    
    # Up one octave with a double underline
    char = createLigBase(digit+accident+'up', 'Semiquaver', accident=accident)
    char.addReference('doubleUnderline')
    addSubs(char, digit, before=('doubleUnderline',), after=("prime"), accident=accident)
    addSubs(char, digit, after=("slash","slash","prime"), accident=accident)
    
    # Up two octaves with a double underline
    char = createLigBase(digit+accident+'upTwo', 'Semiquaver', accident=accident)
    char.addReference('doubleUnderline')
    addSubs(char, digit, before=('doubleUnderline',), after=("prime","prime"), accident=accident)
    addSubs(char, digit, after=("slash","slash","prime","prime"), accident=accident)




#%% SECTION THREE - Adjust some of the font's global properties.
for char in font.glyphs():
    char.width = MONOSPACEWIDTH


#%% SECTION FOUR - Compact single-line chords using contextual GSUB Lookup Tables.
# This is new to version 3 of the font. 
# If 2-4 notes are written between square brackets, they will be stacked and scaled down to fit in a single line.
# Examples: [123] [1,3,,] [7'52]

chordAtoms = []
for accident in ["", "sharp", "flat", "natural"]:
    for digit in ['1','2','3','4','5','6','7']:
        for suffix in ['','up','upTwo','down','downTwo']:
            chordAtoms.append(digit+accident+suffix)

# This block creates a lookup table for each shrunken position that a note can occupy within a chord.
def addChordSlotLookup(lookupName, glyphSuffix, chordCount, yPosition, advances=False):
    font.addLookup(lookupName, 'gsub_single', None, ())
    subtableName = lookupName + 'Subtable'
    font.addLookupSubtable(lookupName, subtableName)

    scale   = COMPACTCHORDSCALE[chordCount]
    yOffset = COMPACTCHORDPOSITION[chordCount][yPosition]
    xOffset = MONOSPACEWIDTH * (1 - scale) / 2

    for atomName in chordAtoms:
        positionedName = atomName + '_' + glyphSuffix
        positionedGlyph = font.createChar(-1, positionedName)
        positionedGlyph.addReference(atomName, (scale,0,0,scale,xOffset,yOffset))
        positionedGlyph.width = MONOSPACEWIDTH if advances else 0
        font[atomName].addPosSub(subtableName, positionedName)
    return lookupName

addChordSlotLookup('quadChordTop',      'c4Top',    4, 0,)
addChordSlotLookup('quadChordUpperMid', 'c4Upper',  4, 1,)
addChordSlotLookup('quadChordLowerMid', 'c4Lower',  4, 2,)
addChordSlotLookup('quadChordBottom',   'c4Bottom', 4, 3, advances=True)

addChordSlotLookup('tripleChordTop',    'c3Top',    3, 0,)
addChordSlotLookup('tripleChordMiddle', 'c3Middle', 3, 1,)
addChordSlotLookup('tripleChordBottom', 'c3Bottom', 3, 2, advances=True)

addChordSlotLookup('doubleChordTop',    'c2Top',    2, 0,)
addChordSlotLookup('doubleChordBottom', 'c2Bottom', 2, 1, advances=True)

addChordSlotLookup('graceNote',         'grace',    2, 0, advances=True)



# This mystical incantation creates a zero-width character to hide the brackets around chords.
hiddenChordBracket = font.createChar(-1, 'hiddenChordBracket')
hiddenChordBracket.width = 0

arpeggioChordBracket = font.createChar(-1, 'arpeggioChordBracket')
importAndCleanOutlines(f'{INPUTFOLDER}/arpeggio-bar.svg', arpeggioChordBracket)
arpeggioChordBracket.width = 0

font.addLookup('chordBracketsLookup', 'gsub_single', None, (),)
font.addLookupSubtable('chordBracketsLookup', 'chordBracketsSubtable')
font['tupletLeft'].addPosSub('chordBracketsSubtable', 'hiddenChordBracket')
font['tupletRight'].addPosSub('chordBracketsSubtable', 'hiddenChordBracket')
font['arpeggioLeft'].addPosSub('chordBracketsSubtable', 'arpeggioChordBracket')
font['arpeggioRight'].addPosSub('chordBracketsSubtable', 'hiddenChordBracket')

# And here's a second little snippet so that {1} renders as a grace note (shrunken and elevated)
font.addLookup('hideArpeggioLookup', 'gsub_single', None, (),)
font.addLookupSubtable('hideArpeggioLookup', 'hideArpeggioSubtable')
font['arpeggioLeft'].addPosSub('hideArpeggioSubtable', 'hiddenChordBracket')


# This block strings together the above lookup rules 
# to create contextual substitution subtables for each type of chord.
# The last argument is a rule string, which is a succession of [list of glyphs] @<lookupTable> pairs.
# If one item from each list is found in a sequence within the text, then the font applies the lookup tables to each glyph.

font.addLookup(
    'chordContextualLookup', 'gsub_context', None,
    (("liga",(('DFLT',("dflt")),)),), 
    'myLookup' # This is the after_lookup_name parameter. The chordCL needs to happen after the ordinary ligature substitutions.
)
chordAtomCoverageString = '[' + ' '.join(chordAtoms) + ']'

font.addContextualSubtable(
    'chordContextualLookup', 'quadChordCL', 'coverage',
    f'''[tupletLeft arpeggioLeft] @<chordBracketsLookup>
        {chordAtomCoverageString} @<quadChordTop>
        {chordAtomCoverageString} @<quadChordUpperMid>
        {chordAtomCoverageString} @<quadChordLowerMid>
        {chordAtomCoverageString} @<quadChordBottom>
        [tupletRight arpeggioRight] @<chordBracketsLookup>'''
)
font.addContextualSubtable(
    'chordContextualLookup', 'tripleChordCL', 'coverage',
    f'''[tupletLeft arpeggioLeft] @<chordBracketsLookup>
        {chordAtomCoverageString} @<tripleChordTop>
        {chordAtomCoverageString} @<tripleChordMiddle>
        {chordAtomCoverageString} @<tripleChordBottom>
        [tupletRight arpeggioRight] @<chordBracketsLookup>''',
)
font.addContextualSubtable(
    'chordContextualLookup', 'doubleChordCL', 'coverage',
    f'''[tupletLeft arpeggioLeft] @<chordBracketsLookup>
        {chordAtomCoverageString} @<doubleChordTop>
        {chordAtomCoverageString} @<doubleChordBottom>
        [tupletRight arpeggioRight] @<chordBracketsLookup>''',
)
font.addContextualSubtable(
    'chordContextualLookup', 'graceChordCL', 'coverage',
    f'''[arpeggioLeft] @<hideArpeggioLookup>
        {chordAtomCoverageString} @<graceNote>
        [arpeggioRight] @<chordBracketsLookup>''',
)


#%% FINALLY - Generate the font
print("Generating black font to", OUTPUTFILENAME)
font.generate(OUTPUTFILENAME)


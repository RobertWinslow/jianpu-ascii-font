# -*- coding: utf-8 -*-
'''
To Use:
1. Adjust the global parameters in the first section below.
2. type `fontforge -script build_simple_black_font_with_fontforge.py` in the terminal.

Description:
This script uses FontForge to build a very basic monochrome font from a folder of SVG files.
Each SVG file must be named with the codepoint of the unicode character it is to be mapped to. 
    EG `1F94B.svg`
If a glyph maps to a sequence of codepoints, seperate the codepoints with `-` in the SVG file's name.
    EG `1F468-200D-1F9B3.svg`
If there are codepoints which are part of a sequence but lack their own SVG, then placeholder geometry is used.

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
font.fullname = font.familyname + " Serif"
font.copyright = "Created 2022 by Robert Martin Winslow" #eg Copyright (c) 2022 Name
font.version = "0.1"

# The following variables are for scaling the imported outlines.
SVGHEIGHT = 150 # units of height of source svg viewbox.
GLYPHHEIGHT = 1200 # font units, default = 1000
PORTIONABOVEBASELINE = 0.6 # default is 0.8
# The following parameter sets the spacing between characters. 
# It is made redundant by MONOSPACEWIDTH if that parameter is set.
SEPARATION = 0
# If the following parameter is set to a positive integer, all characters are set to that width.
# Set it to 0 or None to make the font non-monospaced.
MONOSPACEWIDTH = 400
# If the following parameter is set to a positive integer, all characters wider than this are scaled down.
# Set it to 0 or None to allow characters to be extra wide.
# If MAXWIDTH is unset, but MONOSPACEWIDTH is set, then some glyphs may have contours outside of their bounding box.
MAXWIDTH = 0
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
            point.transform((1,0,0,1,0,PORTIONABOVEBASELINE*GLYPHHEIGHT)) # translate up to desired cap height
    glyph.setLayer(foregroundlayer,'Fore')


#%% SECTION TWO B - Import basic characters.
# digits
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



#%% SECTION TWO B - Create combination characters with references and ligatures.

# To be quite honest, I don't fully understand what this syntax up front is doing.
# Just treat these next couple of lines as if they are a mystical incantation.
font.addLookup('myLookup','gsub_ligature',None,(("liga",(('DFLT',("dflt")),)),))
font.addLookupSubtable("myLookup", "mySubtable")

# First, some special cases
## The semiquaver / double underline. Base codepoint is the letter s, with '__' as a ligature mapped to it as well.
char = font.createChar(int('0073',16), 'doubleUnderscore')
char.addReference('underscore', (1,0,0,1,0,0)) # -MONOSPACEWIDTH in penultimate value to make it go under the character to the left.
char.addReference('underscore', (1,0,0,1,0,-80))
char.addPosSub("mySubtable", ('underscore','underscore',))
char.width = 0
## Double dot
char = font.createChar(-1, 'doubleDot')
char.addReference('cdot', (1,0,0,1,-100,0)) 
char.addReference('cdot', (1,0,0,1,60,0))
char.addPosSub("mySubtable", ('cdot','cdot',))
char.addPosSub("mySubtable", ('period','period',))
char.width = MONOSPACEWIDTH

for digit in ['1','2','3','4','5','6','7',]:
    # up an octave
    char = font.createChar(-1, f'{digit}up')
    char.addReference(digit)
    char.addReference('prime', (1,0,0,1,0,0))
    char.addPosSub("mySubtable", (digit,'prime',))
    char.width = MONOSPACEWIDTH
    # up two octaves
    char = font.createChar(-1, f'{digit}upTwo')
    char.addReference(digit)
    char.addReference('prime', (1,0,0,1,0,0))
    char.addReference('prime', (1,0,0,1,0,100))
    char.addPosSub("mySubtable", (digit,'prime','prime',))
    char.width = MONOSPACEWIDTH
    # down one octave
    char = font.createChar(-1, f'{digit}down')
    char.addReference(digit)
    char.addReference('comma', (1,0,0,1,0,0))
    char.addPosSub("mySubtable", (digit,'comma',))
    char.width = MONOSPACEWIDTH
    # down two octaves
    char = font.createChar(-1, f'{digit}downTwo')
    char.addReference(digit)
    char.addReference('comma', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-100))
    char.addPosSub("mySubtable", (digit,'comma','comma',))
    char.width = MONOSPACEWIDTH
    # down one octave with underline for a quaver
    char = font.createChar(-1, f'{digit}downQuaver')
    char.addReference(digit)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-75))
    char.addPosSub("mySubtable", ('underscore',digit,'comma',))
    char.addPosSub("mySubtable", ('q',digit,'comma',))
    char.width = MONOSPACEWIDTH
    # down two octaves with underline for a quaver
    char = font.createChar(-1, f'{digit}downTwoQuaver')
    char.addReference(digit)
    char.addReference('underscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-75))
    char.addReference('comma', (1,0,0,1,0,-175))
    char.addPosSub("mySubtable", ('q',digit,'comma','comma',))
    char.addPosSub("mySubtable", ('underscore',digit,'comma','comma',))
    char.width = MONOSPACEWIDTH
    # down one octave with double underlines for a semiquaver
    char = font.createChar(-1, f'{digit}downSemiquaver')
    char.addReference(digit)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-150))
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,'comma',))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,'comma',))
    char.width = MONOSPACEWIDTH
    # down two octaves with double underlines for a semiquaver
    char = font.createChar(-1, f'{digit}downTwoSemiquaver')
    char.addReference(digit)
    char.addReference('doubleUnderscore', (1,0,0,1,0,0))
    char.addReference('comma', (1,0,0,1,0,-150))
    char.addReference('comma', (1,0,0,1,0,-250))
    char.addPosSub("mySubtable", ('doubleUnderscore',digit,'comma','comma',))
    char.addPosSub("mySubtable", ('underscore','underscore',digit,'comma','comma',))
    char.width = MONOSPACEWIDTH

#char = font.createChar(-1, '_'.join(components))
#char.addPosSub("mySubtable", components)
#importAndCleanOutlines(INPUTFOLDER+'/'+filename,char)

# TODO: Seperate underdot positioning when underline is present




#%% SECTION THREE - Adjust some of the font's global properties.
#for g in font.glyphs():
#        g.width = MONOSPACEWIDTH

#%% FINALLY - Generate the font
print("Generating black font to", OUTPUTFILENAME)
font.generate(OUTPUTFILENAME)








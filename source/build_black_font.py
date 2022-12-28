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

INPUTFOLDER = 'svg/combined'
OUTPUTFILENAME = 'JianpuASCII.ttf'
PLACEHOLDERGEOMETRYSVG = 'svg/combined/0030.svg'

font = fontforge.font()
font.familyname = "Jianpu Ascii"
font.fullname = font.familyname + " Serif"
font.copyright = "Created 2022 by Robert Martin Winslow" #eg Copyright (c) 2022 Name
font.version = "0.1"

# The following variables are for scaling the imported outlines.
SVGHEIGHT = 150 # units of height of source svg viewbox.
GLYPHHEIGHT = 1200 # font units, default = 1000
PORTIONABOVEBASELINE = 0.5 # default is 0.8
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
DOUBLEWIDE_CODEPOINTS = ['0030','0031','0032','0033','0034','0035','0036','0037']






#%% SECTION TWO A - Define function for importing outlines.

def importAndCleanOutlines(outlinefile,glyph):
    #print(outlinefile)
    glyph.importOutlines(outlinefile, simplify=True, correctdir=False, accuracy=0.01, scale=False)
    glyph.removeOverlap()
    SCALEFACTOR = GLYPHHEIGHT/SVGHEIGHT
    foregroundlayer = glyph.foreground
    for contour in foregroundlayer:
        for point in contour:
            point.transform((1,0,0,1,0,-800)) # Translate top of glyph down to baseline.
            point.transform((SCALEFACTOR,0,0,SCALEFACTOR,0,0)) # Scale up. Top of glyph will remain at baseline. 
            point.transform((1,0,0,1,0,PORTIONABOVEBASELINE*GLYPHHEIGHT)) # translate up to desired cap height
    glyph.setLayer(foregroundlayer,'Fore')



#%% SECTION TWO B - CREATE GLYPHS FROM THE SVG SOURCE FILES
# Scan the directory of SVG files and make a list of files and codepoints to process
files = os.listdir(INPUTFOLDER)
codetuples = [(tuple(filename[:-4].split('-')), filename) for filename in files if filename.endswith('.svg')]

# Start by loading up all the single codepoint characters.
simplecharacters = [(codepoints[0],filename) for codepoints,filename in codetuples if len(codepoints)==1]
for codepoint, filename in simplecharacters:
    char = font.createChar(int(codepoint,16), 'u'+codepoint)
    importAndCleanOutlines(INPUTFOLDER+'/'+filename,char)

# Manually add 200D (ZWJ), FE0F, and other individual codepoints as glyphs as needed.
# If a codepoint is not present as a glyph, we can't add it into a combined character.
# And if geometry isn't added to a glyph, FontForge will discard it.
# Therefore a placeholder glyph is used. 
presentcomponents = set([g.glyphname for g in font.glyphs()])
missingcodepoints = set()
for codepoints,filename in codetuples:
    for codepoint in codepoints:
        if 'u'+codepoint not in presentcomponents:
            missingcodepoints.add(codepoint)
for codepoint in missingcodepoints:
    char = font.createChar(int(codepoint,16), 'u'+codepoint)
    importAndCleanOutlines(PLACEHOLDERGEOMETRYSVG,char)


# Now make the combination characters via FontForge's ligature feature.
# To be quite honest, I don't fully understand what all this syntax up front is doing.
# Just treat these next couple of lines as if they are a mystical incantation.
font.addLookup('myLookup','gsub_ligature',None,(("liga",(('DFLT',("dflt")),)),))
font.addLookupSubtable("myLookup", "mySubtable")

combocharacters = [(codepoints,filename) for codepoints,filename in codetuples if len(codepoints)>1]

# Imports glyphs for all the non-skintone combination characters. 
for codepoints,filename in combocharacters:
    components = tuple('u'+codepoint for codepoint in codepoints)
    char = font.createChar(-1, '_'.join(components))
    char.addPosSub("mySubtable", components)
    importAndCleanOutlines(INPUTFOLDER+'/'+filename,char)










#%% SECTION THREE - Adjust some of the font's global properties.
# Automagically adjust the horizontal position of the font.
font.selection.all()
font.autoWidth(SEPARATION)

#%% If the parameter is set, scale down the very wide glyphs
# This can make the unusually wide glyphs overlap a bit.
if MAXWIDTH:
    for g in font.glyphs():
        if g.width > MAXWIDTH:
            print(g)
            rescalefactor = MAXWIDTH / g.width
            g.transform((rescalefactor,0,0,rescalefactor,0,0))

font.selection.all()
font.autoWidth(SEPARATION)

# If the parameter is set, standardize the spacing to the right and left
# This can make the unusually wide glyphs overlap a bit.
if MONOSPACEWIDTH:
    for g in font.glyphs():
        bearing = int((MONOSPACEWIDTH-g.width)/2)
        g.left_side_bearing = bearing
        g.right_side_bearing = bearing







#%% FINALLY - Generate the font
print("Generating black font to", OUTPUTFILENAME)
font.generate(OUTPUTFILENAME)








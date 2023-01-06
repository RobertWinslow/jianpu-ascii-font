
# For the sake of making the build 
# For the sake of making the build process as easy as possible,
# I don't use combining diacritics for the dots and underlines in Jianpu notation.
# I simply manually make a glyph for each combination of components.
# In addition to standalone characters, I need to make the following combinatoric characters:
# - 7 characters for notes
# - Three possibilities for underlines (none, one, or two)
# - five possibilities for dots (none, one above, two above, one below, two below)
# That's only 105 total combos. A reasonably small number.
# Also zero width characters for sharps and flats?

#%% 
import os

INPUTFOLDER = 'svg/components'
files = os.listdir(INPUTFOLDER)

OUTPUTFOLDER = 'svg/combined'

#%%

SVGSTART = '<?xml version="1.0" encoding="UTF-8"?><svg version="1.1" viewBox="0 0 60 150" xmlns="http://www.w3.org/2000/svg">'
SVGEND = '</svg>'

## Load up the bits of the svg files which contain the paths
pathDict = {}
for filename in files:
    with open(os.path.join(INPUTFOLDER,filename),'r') as f:
        contents = f.read()
        contents = contents.replace(SVGSTART,'')
        contents = contents.replace(SVGEND,'')
        name = filename[:-4]
        pathDict[name] = contents

#%%

def buildSVG(componentNameList, color='#000'):
    svg = SVGSTART
    svg = svg + ''.join([pathDict[component] for component in componentNameList])
    svg = svg + SVGEND
    svg = svg.replace('#000',color)
    return svg


codepointDict = {
    '0':'0030', '1':'0031', '2':'0032', '3':'0033', 
    '4':'0034', '5':'0035', '6':'0036', '7':'0037', 
    '#':'0023', 'b':'0062', '^':'005e', '_':'005f', '=':'003d',
    ':':'003a', '|':'007c', 'x':'0078', '-':'002d', '.':'002e', '*':'002a',
    ',':'002c', "'":'0027', 's':'0073', 'q':'0071', '/':'002f', 
    '[':'005b', ']':'005d', '(':'0028', ')':'0029', 
}


#%%

def createBasicSVG(character, component):
    svg = buildSVG([component])
    codepoint = codepointDict[character]
    with open(os.path.join(OUTPUTFOLDER,codepoint+'.svg'), 'w') as f:
        f.write(svg)

createBasicSVG('#', 'sharp')
createBasicSVG('b', 'flat')
createBasicSVG('^', 'sharp')
createBasicSVG('_', 'flat')
createBasicSVG('=', 'natural')
createBasicSVG(':', 'colon')
createBasicSVG('|', 'bar')
createBasicSVG('x', 'x')
createBasicSVG('-', 'dash')
createBasicSVG('.', 'sidedot')
createBasicSVG('*', 'sidedot')
createBasicSVG(',', 'downoctave')
createBasicSVG("'", 'upoctave')
createBasicSVG('s', 'doubleUnderline')
createBasicSVG('q', 'underline')
createBasicSVG('/', 'underline')
createBasicSVG('[', 'tupletLeft')
createBasicSVG(']', 'tupletRight')
createBasicSVG('(', 'slurLeft')
createBasicSVG(')', 'slurRight')










# %%

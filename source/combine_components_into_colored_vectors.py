
# This explicitly builds all the combos I need, 
# creating an SVG file for each codepoint.
# Why do this?
# I want to make a colr font using the Nanoemoji tool.
# This accepts as inputs SVG with codepoint ligatures as their filenames.
# By explicitly generating every vector, it becomes really easy to work with nanoemoji.
# (nanoemoji's build process is intelligent enough to reuse shared geometry, so the file size of the end font won't be too large.)

#%% IMPORTS AND PARAMETERS
import os

INPUTFOLDER = 'svg/components'
files = os.listdir(INPUTFOLDER)

OUTPUTFOLDER = 'svg/combined'



COLORS = {
    "0": "#d4d4d4",
    "1": "#bf344b",
    "2": "#ea8127",
    "3": "#d9ae2f",
    "4": "#82a12b",
    "5": "#1385af",
    "6": "#5359b5",
    "7": "#9352a8",
}
COLORS_HIGH = {
    '0': '#d4d4d4',
    '1': '#e66980',
    '2': '#ff9d50',
    '3': '#f7ce50',
    '4': '#87d989',
    '5': '#2dbce2',
    '6': '#8088e2',
    '7': '#ce8ce3'
}
COLORS_LOW = {
    '0': '#d4d4d4',
    '1': '#87122d',
    '2': '#c26012',
    '3': '#a29812',
    '4': '#176a1e',
    '5': '#113074',
    '6': '#2a286f',
    '7': '#652277'
}

BLACKUNDERLINES = False


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

# Null geometry (used to streamline accidental code)
pathDict[''] = ''

#%% DEFINITIONS TO CREATE FILES

codepointDict = {
    '0':'0030', '1':'0031', '2':'0032', '3':'0033', 
    '4':'0034', '5':'0035', '6':'0036', '7':'0037', 
    '#':'0023', 'b':'0062', '^':'005e', '_':'005f', '=':'003d',
    ':':'003a', '|':'007c', 'x':'0078', '-':'002d', '.':'002e', '*':'002a',
    ',':'002c', "'":'0027', 's':'0073', 'q':'0071', '/':'002f', 
    '[':'005b', ']':'005d', '(':'0028', ')':'0029', 
}
basicGeometryMapping = {
    '#': 'sharp',
    'b': 'flat',
    '^': 'sharp',
    '_': 'flat',
    '=': 'natural',
    ':': 'colon',
    '|': 'bar',
    'x': 'x',
    '-': 'dash',
    '.': 'sidedot',
    '*': 'sidedot',
    ',': 'downoctave',
    "'": 'upoctave',
    's': 'doubleUnderline',
    'q': 'underline',
    '/': 'underline',
    '[': 'tupletLeft',
    ']': 'tupletRight',
    '(': 'slurLeft',
    ')': 'slurRight',
}
accidentalMapping = {
    '^': 'sharpSmall',
    '_': 'flatSmall',
    '=': 'naturalSmall',
    '': '',
}

def buildSVG(componentNameList, color='#000'):
    svg = SVGSTART
    svg = svg + ''.join([pathDict[component] for component in componentNameList])
    svg = svg + SVGEND
    svg = svg.replace('#000',color)
    if not BLACKUNDERLINES:
        svg = svg.replace('black',color)
    return svg

def createBasicFile(character, component):
    svg = buildSVG([component])
    codepoint = codepointDict[character]
    with open(os.path.join(OUTPUTFOLDER,codepoint+'.svg'), 'w') as f:
        f.write(svg)

def createBasicComboFile(charSequence,svgContent):
    filename = '-'.join([codepointDict[c] for c in charSequence])
    with open(os.path.join(OUTPUTFOLDER,filename+'.svg'), 'w') as f:
        f.write(svgContent)

# pass in strings of characters to put before, and characters to put after
from itertools import permutations
def createPermutationFiles(svgContent, core,before,after):
    for prefix in set(permutations(before)):
        for suffix in set(permutations(after)):
            charSequence = ''.join(prefix+(core,)+suffix)
            createBasicComboFile(charSequence,svgContent)



### CREATE THE FILES

# Start with simple, non-note single-codepoint glpyhs
for c, shape in basicGeometryMapping.items():
    createBasicFile(c,shape)

# underlines for some characters
for c in ['x','.','#','b','^','_','=','*',]:
    core = basicGeometryMapping[c]
    # Single underline for quaver
    svg = buildSVG([core,'underline'])
    createPermutationFiles(svg,c,'','/')
    createPermutationFiles(svg,c,'q','')
    # double underline for a semiquaver
    svg = buildSVG([core,'doubleUnderline'])
    createPermutationFiles(svg,c,'','//')
    createPermutationFiles(svg,c,'s','')

# special case for 0
# Single underline for quaver
svg = buildSVG(['0','underline'], color=COLORS['0'])
createPermutationFiles(svg,'0','','/')
createPermutationFiles(svg,'0','q','')
# double underline for a semiquaver
svg = buildSVG(['0','doubleUnderline'], color=COLORS['0'])
createPermutationFiles(svg,'0','','//')
createPermutationFiles(svg,'0','s','')


# Other special cases
## Double dot
svg = buildSVG(['doubleDot',])
createBasicComboFile('..',svg)
createBasicComboFile('**',svg)
## Double bar ||
svg = buildSVG(['doubleBar',])
createBasicComboFile('||',svg)
## Repeat signs
# :|
svg = buildSVG(['repeatRight',])
createBasicComboFile(':||',svg)
createBasicComboFile(':|',svg)
# |:
svg = buildSVG(['repeatLeft',])
createBasicComboFile('||:',svg)
createBasicComboFile('|:',svg)
# :|:
svg = buildSVG(['repeatBoth',])
createBasicComboFile(':||:',svg)
createBasicComboFile(':|:',svg)



# DIGIT LIGATURES
for digit in ['1','2','3','4','5','6','7',]:
  for accid in ['','=','^','_']:
    accidComponent = accidentalMapping[accid]

    #Standalone Note
    svg = buildSVG([accidComponent, digit,], color=COLORS[digit])
    createPermutationFiles(svg,digit,accid+'','')

    # Single underline for quaver
    svg = buildSVG([accidComponent, digit,'underline'], color=COLORS[digit])
    createPermutationFiles(svg,digit,accid+'','/')
    createPermutationFiles(svg,digit,accid+'q','')
    # double underline for a semiquaver
    svg = buildSVG([accidComponent, digit,'doubleUnderline'], color=COLORS[digit])
    createPermutationFiles(svg,digit,accid+'','//')
    createPermutationFiles(svg,digit,accid+'s','')
    
    # up an octave
    svg = buildSVG([accidComponent, digit,'upoctave'], color=COLORS_HIGH[digit])
    createPermutationFiles(svg,digit,accid+'',"'")
    # up two octaves
    svg = buildSVG([accidComponent, digit,'upTwo'], color=COLORS_HIGH[digit])
    createPermutationFiles(svg,digit,accid+'',"''")
    # down one octave
    svg = buildSVG([accidComponent, digit,'downoctave'], color=COLORS_LOW[digit])
    createPermutationFiles(svg,digit,accid+'',",")
    # down two octaves
    svg = buildSVG([accidComponent, digit,'downTwo'], color=COLORS_LOW[digit])
    createPermutationFiles(svg,digit,accid+'',",,")
    
    # Up one octave with a single underline
    svg = buildSVG([accidComponent, digit,'upoctave', 'underline'], color=COLORS_HIGH[digit])
    createPermutationFiles(svg,digit,accid+'q',"'")
    createPermutationFiles(svg,digit,accid+'',"'/")
    # Up two octaves with a single underline
    svg = buildSVG([accidComponent, digit,'upTwo', 'underline'], color=COLORS_HIGH[digit])
    createPermutationFiles(svg,digit,accid+'q',"''")
    createPermutationFiles(svg,digit,accid+'',"''/")
    # Up one octave with a double underline
    svg = buildSVG([accidComponent, digit,'upoctave', 'doubleUnderline'], color=COLORS_HIGH[digit])
    createPermutationFiles(svg,digit,accid+'s',"'")
    createPermutationFiles(svg,digit,accid+'',"'//")
    # Up two octaves with a double underline
    svg = buildSVG([accidComponent, digit,'upTwo', 'doubleUnderline'], color=COLORS_HIGH[digit])
    createPermutationFiles(svg,digit,accid+'s',"''")
    createPermutationFiles(svg,digit,accid+'',"''//")

    # down one octave with a single underline
    svg = buildSVG([accidComponent, digit,'downOneUnderline'], color=COLORS_LOW[digit])
    createPermutationFiles(svg,digit,accid+'q',",")
    createPermutationFiles(svg,digit,accid+'',",/")
    # down two octaves with a single underline
    svg = buildSVG([accidComponent, digit,'downTwoUnderline'], color=COLORS_LOW[digit])
    createPermutationFiles(svg,digit,accid+'q',",,")
    createPermutationFiles(svg,digit,accid+'',",,/")
    # down one octave with a double underline
    svg = buildSVG([accidComponent, digit,'downOneDoubleUnderline'], color=COLORS_LOW[digit])
    createPermutationFiles(svg,digit,accid+'s',",")
    createPermutationFiles(svg,digit,accid+'',",//")
    # down two octaves with a double underline
    svg = buildSVG([accidComponent, digit,'downTwoDoubleUnderline'], color=COLORS_LOW[digit])
    createPermutationFiles(svg,digit,accid+'s',",,")
    createPermutationFiles(svg,digit,accid+'',",,//")


# Manually add space character

svg = buildSVG([])
with open(os.path.join(OUTPUTFOLDER,'0020.svg'), 'w') as f:
    f.write(svg)

#%%







# %%

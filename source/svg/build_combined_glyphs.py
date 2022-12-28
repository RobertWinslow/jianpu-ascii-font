
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



#%%

NUMBERPATHSTRINGS = [
    "m25 81.2c-7.1333 0-12.733-2.8667-16.8-8.6-4.0667-5.8-6.1-14.033-6.1-24.7 0-10.733 2.0333-18.9 6.1-24.5 4.0667-5.6 9.6667-8.4 16.8-8.4s12.733 2.8 16.8 8.4 6.1 13.767 6.1 24.5c0 10.667-2.0333 18.9-6.1 24.7-4.0667 5.7333-9.6667 8.6-16.8 8.6zm0-6.6c4.4667 0 8.1-2.1667 10.9-6.5 2.8667-4.3333 4.3-11.067 4.3-20.2 0-4.6-.3667-8.5333-1.1-11.8-.7333-3.3333-1.8-6.0667-3.2-8.2-1.3333-2.2-2.9333-3.8-4.8-4.8s-3.9-1.5-6.1-1.5-4.2333.5-6.1 1.5-3.5 2.6-4.9 4.8c-1.3333 2.1333-2.3667 4.8667-3.1 8.2-.7333 3.2667-1.1 7.2-1.1 11.8 0 9.1333 1.4 15.867 4.2 20.2 2.8667 4.3333 6.5333 6.5 11 6.5zm0-20.7c-1.6667 0-3.1333-.5667-4.4-1.7-1.2-1.2-1.8-2.8667-1.8-5 0-2.0667.6-3.6667 1.8-4.8 1.2667-1.2 2.7333-1.8 4.4-1.8s3.1.6 4.3 1.8c1.2667 1.1333 1.9 2.7333 1.9 4.8 0 2.1333-.6333 3.8-1.9 5-1.2 1.1333-2.6333 1.7-4.3 1.7z",
    "m3.35 80v-6.8h18.4v-47h-14.3v-5.3q5.7-.8 9.5-1.9t6.9-2.8h6.1v57h16.7v6.8z",
    "m2.75 80v-4.9q8.1-7.2 14.3-13 6.3-5.8 10.5-10.6 4.3-4.9 6.5-9.1t2.2-8.2q0-5.5-3.4-9t-10.5-3.5q-4.5 0-8.4 2.3-3.8 2.2-6.9 5.4l-4.7-4.7q4.3-4.4 9.2-7 5-2.7 11.8-2.7 4.8 0 8.6 1.4 3.9 1.3 6.6 3.8 2.7 2.4 4.1 5.9 1.5 3.5 1.5 7.7 0 4.5-2.2 9.1-2.1 4.5-6 9.4-3.9 4.8-9.3 10.1-5.4 5.2-11.9 11.1 3-.2 6-.4t5.9-.2h21v7.1z",
    "m24.95 81.2q-8.3 0-13.9-2.7-5.6-2.8-9.1-6.3l4.2-5.4q3.2 3 7.6 5.3 4.5 2.3 10.7 2.3 3.3 0 6.1-.8 2.8-.9 4.8-2.4 2.1-1.5 3.2-3.6 1.2-2.2 1.2-4.9 0-2.8-1.3-5.1-1.2-2.4-4-4.1t-7.2-2.6-10.7-.9v-6.3q5.7 0 9.6-.9 4-.9 6.5-2.5t3.6-3.8q1.2-2.2 1.2-4.7 0-4.7-3.6-7.4-3.5-2.7-9.4-2.7-4.5 0-8.5 1.8t-7.2 4.7l-4.4-5.2q4-3.5 9.1-5.7 5.1-2.3 11.3-2.3 4.5 0 8.3 1.1 3.9 1.1 6.7 3.2 2.9 2 4.5 5t1.6 6.9q0 5.8-3.8 9.5t-9.8 5.7v.4q3.2.7 6 2.1 2.9 1.3 5.1 3.4 2.2 2 3.4 4.7 1.3 2.7 1.3 6 0 4.2-1.8 7.6t-5 5.8q-3.1 2.3-7.3 3.6-4.2 1.2-9 1.2z",
    "m32.6 80v-17.6h-32.9v-5.5l31.9-40.7h8.8v39.6h9.9v6.6h-9.9v17.6zm-23.8-24.2h23.8v-19.8q.1-2.6.2-5.6.1-3.1.3-5.7h-.5q-1.5 2.3-3.2 4.7-1.7 2.3-3.3 4.6z",
    "m24.171 81.2q-4.3 0-7.8-.8-3.4-.7-6.2-1.9-2.7-1.2-5-2.7-2.2-1.6-4-3.3l4.1-5.4q1.6 1.4 3.4 2.8 1.8 1.3 3.9 2.3 2.2 1 4.8 1.6 2.7.6 5.9.6 3.4 0 6.3-1 3-1.1 5.2-3t3.4-4.6q1.3-2.7 1.3-6 0-6.6-4.3-10.3-4.2-3.7-11.4-3.7-4 0-6.8 1t-6.2 2.9l-4.4-2.8 2.1-30.7h36.1v7.1h-28.8l-1.7 18.9q2.8-1.2 5.4-1.9 2.7-.7 6.4-.7 4.6 0 8.6 1.2t6.9 3.7q3 2.4 4.7 6.2 1.7 3.7 1.7 8.9t-2 9.2q-1.9 4-5.2 6.8-3.3 2.7-7.6 4.2-4.2 1.4-8.8 1.4z",
    "m26.55 81.2q-5.2 0-9.7-1.9-4.4-1.9-7.7-5.7-3.3-3.9-5.2-9.6-1.8-5.8-1.8-13.5 0-9.6 2.2-16.3 2.2-6.8 5.9-11 3.7-4.3 8.5-6.2 4.9-2 10.1-2 5.9 0 10.2 2 4.4 1.9 7.6 4.8l-4.6 5.1q-2.5-2.3-5.8-3.6-3.3-1.4-6.9-1.4-3.8 0-7.3 1.4t-6.2 4.6q-2.6 3.2-4.3 8.5-1.6 5.2-1.7 12.9 3.9-3.8 8.6-6 4.7-2.3 9.5-2.3 4.4 0 8 1.3 3.7 1.2 6.3 3.7 2.7 2.4 4.1 6.1 1.5 3.7 1.5 8.6 0 4.6-1.8 8.4-1.7 3.7-4.6 6.4t-6.8 4.2q-3.8 1.5-8.1 1.5zm0-6.5q2.8 0 5.3-1t4.3-2.8q1.8-1.9 2.8-4.4 1.1-2.6 1.1-5.8 0-6.6-3.5-10-3.5-3.5-10.1-3.5-3.8 0-8.2 2-4.3 2-8.1 6.6.9 9.3 5.1 14.1 4.3 4.8 11.3 4.8z",
    "m17.6 80q.4-9.1 1.7-16.5 1.3-7.5 3.8-14.2t6.3-13q3.9-6.3 9.4-13h-36.8v-7.1h46.2v5.1q-6.3 7.2-10.4 13.8t-6.6 13.5q-2.5 6.8-3.6 14.4t-1.4 17z",
]



LINE1 = "m -2 90 h 54 v 5 h -54 z"
LINE2 = "m -2 100 h 54 v 5 h -54 z"
def dotString(y):
    return f"m 30 {y} a 5 5 0 0 1 -5 5 5 5 0 0 1 -5 -5 5 5 0 0 1 5 -5 5 5 0 0 1 5 5 z"

# d is a dot below, u is a dot above, l is a line below
TOPDECORATORPATHSTRINGS = {
    "": [],
    "u": [dotString(5)],
    "uu": [dotString(5),dotString(-10)],
}

BOTTOMDECORATORPATHSTRINGS = {
    "": [],
    "d": [dotString(95)],
    "dd": [dotString(95),dotString(110)],
    "l": [LINE1],
    "ld": [LINE1,dotString(105)],
    "ldd": [LINE1,dotString(105),dotString(120)],
    "ll": [LINE2,LINE1],
    "lld": [LINE2,LINE1, dotString(115)],
    "lldd": [LINE2,LINE1,dotString(115),dotString(130)],
}

DECORATOR_POSSIBILITIES = [
    ('', ''),
    ('', 'd'),
    ('', 'dd'),
    ('', 'l'),
    ('', 'ld'),
    ('', 'ldd'),
    ('', 'll'),
    ('', 'lld'),
    ('', 'lldd'),
    ('u', ''),
    ('u', 'l'),
    ('u', 'll'),
    ('uu', ''),
    ('uu', 'l'),
    ('uu', 'll'),
]

CODEPOINTS = [
    "0030",
    "0031",
    "0032",
    "0033",
    "0034",
    "0035",
    "0036",
    "0037",
]


COLORS = [
    "#8a8489",
    "#bf344b",
    "#ea8127",
    "#d9ae2f",
    "#82a12b",
    "#1385af",
    "#5359b5",
    "#9352a8",
]
COLORS_HIGH = [
    "#8a8489",
    "#e66980",
    "#ff9d50",
    "#f7ce50",
    "#87d989",
    "#2dbce2",
    "#8088e2",
    "#ce8ce3",
]
COLORS_LOW = [
    "#8a8489",
    "#87122d",
    "#c26012",
    "#a29812",
    "#176a1e",
    "#113074",
    "#2a286f",
    "#652277",
]

def chooseColor(digit,top,bottom):
    if 'u' in top:
        colors = COLORS_HIGH
    elif 'd' in bottom:
        colors = COLORS_LOW
    else:
        colors = COLORS
    return colors[digit]



from itertools import permutations
def generateFilenames(digit,top,bottom):
    snippets = []
    if "ll" in bottom:
        snippets.append("005f-005f")
    elif "l" in bottom:
        snippets.append("005f")
    if "dd" in bottom:
        snippets.append("002c-002c")
    elif "d" in bottom:
        snippets.append("002c")
    if "uu" in top:
        snippets.append("0027-0027")
    elif "u" in top:
        snippets.append("0027")
    filenames = [[str(CODEPOINTS[digit])]+list(perm) for perm in permutations(snippets)]
    filenames = ['-'.join(name) for name in filenames]
    filenames = [name+'.svg' for name in filenames]
    return filenames
    


def createComboSVG(digit, topDecorator, bottomDecorator):
    fill = chooseColor(digit, topDecorator, bottomDecorator)
    svgString = '<?xml version="1.0" encoding="UTF-8"?><svg version="1.1" viewBox="0 -15 50 150" xmlns="http://www.w3.org/2000/svg">\n'
    svgString += f'<path fill="{fill}" d="{NUMBERPATHSTRINGS[digit]}"/>\n'
    for path in TOPDECORATORPATHSTRINGS[topDecorator]:
        svgString += f'<path fill="{fill}" d="{path}"/>\n'
    for path in BOTTOMDECORATORPATHSTRINGS[bottomDecorator]:
        svgString += f'<path fill="{fill}" d="{path}"/>\n'
    svgString += '</svg>'
    for filename in generateFilenames(digit,topDecorator,bottomDecorator):
        with open(f"combined/{filename}", 'w') as f:
            f.write(svgString)





for digit in range(1,8):
    for top,bottom in DECORATOR_POSSIBILITIES:
        createComboSVG(digit, top, bottom, )
createComboSVG(0, '', '')
createComboSVG(0, '', 'l')
createComboSVG(0, '', 'll')



# %%

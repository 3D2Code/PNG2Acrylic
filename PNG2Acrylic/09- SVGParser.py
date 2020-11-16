import os;import time;import json;import math;import re;import random
os.chdir('C:\\Users\\burak\\Google Drive\\Python Files\\PNG2Acrylic')

from xml.dom import minidom

doc = minidom.parse(svg_file)  # parseString also exists
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

#***********************************
from svgpathtools import svg2paths
paths, attributes = svg2paths('some_svg_file.svg')

for k, v in enumerate(attributes):
    print v['d']  # print d-string of k-th path in SVG
    
#************************************
#!/usr/bin/python3
# requires svg.path, install it like this: pip3 install svg.path

# converts a list of path elements of a SVG file to simple line drawing commands
from svg.path import parse_path
from svg.path.path import Line
from xml.dom import minidom

# read the SVG file
doc = minidom.parse('test.svg')
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

# print the line draw commands
for path_string in path_strings:
    path = parse_path(path_string)
    for e in path:
        if isinstance(e, Line):
            x0 = e.start.real
            y0 = e.start.imag
            x1 = e.end.real
            y1 = e.end.imag
            print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
            
            
>>> COMMANDS = set('MmZzLlHhVvCcSsQqTtAa')
									
>>> def _tokenize_path_replace(pathdef):
    # First handle negative exponents:
    pathdef = pathdef.replace('e-', 'NEGEXP').replace('E-', 'NEGEXP')
    # Commas and minus-signs are separators, just like spaces.
    pathdef = pathdef.replace(',', ' ').replace('-', ' -')
    pathdef = pathdef.replace('NEGEXP', 'e-')
    # Commands are allowed without spaces around. Let's insert spaces so it's
    # easier to split later.
    for c in COMMANDS:
        pathdef = pathdef.replace(c, ' %s ' % c)

    # Split the path into elements
    return pathdef.split()

									
>>> collect=[]
									
>>> for k, v in enumerate(attributes):
    collect.append(v['d'])				
>>> collect[0]

#**********************************************
def parse_path0(path_data):
    digit_exp = '0123456789eE'
    comma_wsp = ', \t\n\r\f\v'
    drawto_command = 'MmZzLlHhVvCcSsQqTtAa'
    sign = '+-'
    exponent = 'eE'
    float = False
    entity = ''
    for char in path_data:
        if char in digit_exp:
            entity += char
        elif char in comma_wsp and entity:
            yield entity
            float = False
            entity = ''
        elif char in drawto_command:
            if entity:
                yield entity
                float = False
                entity = ''
            yield char
        elif char == '.':
            if float:
                yield entity
                entity = '.'
            else:
                entity += '.'
                float = True
        elif char in sign:
            if entity and entity[-1] not in exponent:
                yield entity
                float = False
                entity = char
            else:
                entity += char
    if entity:
        yield entity
        
print(list(parse_path0(collect[0])))
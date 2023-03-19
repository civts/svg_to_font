import fontforge

import os
import re
import sys
import xml.etree.ElementTree as ET

# Check that a directory containing SVG files was provided as an argument
if len(sys.argv) != 3:
    print("Please provide a directory containing SVG files as the argument")
    print("and the font name as the second one")
    sys.exit(1)

# Define the input directory containing the SVG files
svg_dir = sys.argv[1]

# Define a regular expression pattern to extract the code point from the SVG filename
pattern = r'([0-9a-fA-F]{4})_(.+)\.svg'

# Create a new FontForge font object
font = fontforge.font()
seen_codepoints = set()

# Loop over all SVG files in the input directory
for root, dirnames, filenames in os.walk(svg_dir):
    for filename in filenames:
        if filename.endswith('.svg'):
            match = re.search(pattern, filename)
            if not match:
                print(f'Error: Invalid filename "{filename}"')
                print(f'It shall be cccc_ddd.svg, where cccc is a')
                print(f'hexadecimal value between e000 and f8ff and')
                print(f'ddd is a description of the glyph (icon).')
                sys.exit(1)

            file_path=os.path.join(root, filename)
            svg_elem = ET.parse(file_path).getroot()

            # Check if the viewBox attribute begins with "0 0"
            if not 'viewBox' in svg_elem.attrib:
                print(f"Error: SVG '{filename}' is missing the viewbox attribute")
                sys.exit(1)
            elif not svg_elem.attrib['viewBox'].startswith('0 0'):
                print(f"Error: SVG '{filename}' has a viewbox that does not start in 0 0: {svg_elem.attrib['viewBox']}")
                print("This most likely leads to nothing being shown, so please fix this")
                sys.exit(1)

            # Extract the code point from the filename using the regular expression pattern
            code_point = int(match.group(1), 16)

            if code_point < 0xe000 or code_point > 0xf8ff:
                print(f"Error: SVG '{filename}' has a code out of the Unicode Private Use Area")
                sys.exit(1)

            if code_point in seen_codepoints:
                print(f"Error: File '{filename}' is trying to use a Unicode code point, {code_point},")
                print(f"which has been already used by another SVG.")
                sys.exit(1)
            else:
                seen_codepoints.add(code_point)

            # Create a new glyph object with the specified code point
            glyph = font.createChar(code_point)

            glyph.importOutlines(file_path)

            description = match.group(2)
            glyph.glyphname = description

            # Center the glyph
            glyph.color = 0
            glyph.left_side_bearing = 0
            glyph.right_side_bearing = 0

fontname = sys.argv[2]

# Set font properties
font.familyname = fontname
font.fontname = f'{fontname}-Regular'
font.fullname = f'{fontname} Regular'
font.weight = 'Regular'
font.version = '0.1'

font.autoWidth(1)
font.autoHint()
font.autoInstr()

# Generate the OpenType font file
font.generate(f'{fontname}.otf')

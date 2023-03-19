# SVG to Font

[![made-with-python](https://img.shields.io/badge/made%20with-Python-1f425f.svg)](https://www.python.org/)
![GitHub](https://img.shields.io/github/license/civts/svg_to_font)

This repo contains a simple python script that can easily convert a bunch of SVG files into a font (`.otf`).

## Dependencies:

- [Fontforge](https://fontforge.org)
- Python 3 (tested on version 3.10.9 on Linux)

## Usage:

Suppose you have the following directory structure:

```
├── svg_to_font.py 🐍
└── svgs 📁
    ├── e000_mercury.svg 🖼️
    ├── e001_venus.svg   🖼️
    ├── e002_earth.svg   🖼️
    ├── e003_mars.svg    🖼️
    ├── e004_jupiter.svg 🖼️
    ├── e005_saturn.svg  🖼️
    ├── e006_uranus.svg  🖼️
    └── e007_neptune.svg 🖼️
```

If you run `python svg_to_font.py ./svgs/ NewFont`, you will get a new file `NewFont.otf` with all the SVGs that were present in `./svgs/` or any of its subdirectories. The name of each SVG file specifies to which glyph (character in the font) it will map.

### SVG file naming:

Each SVG file must be named by specifying its Unicode code point and a description, separated by an underscore.  
The Unicode code point is a hexadecimal number and it shall be in the range `[e000, f8ff]` since this is one Private Use Areas of Unicode. This area can accomodate 6400 glyphs.

The description will be included as the name of the glyph in the font.

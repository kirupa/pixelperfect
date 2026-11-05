# Artwork license

The drawings bundled with this skill are kirupa.com artwork. They are **not** covered by the MIT license in [`LICENSE.txt`](../LICENSE.txt), which covers the skill's code and documentation. They're under the Icon Gallery's free license, below.

This license covers:

- `assets/reference/`: the reference library of approved drawings from the kirupa.com Pixel set, as text sprites at 16 and 24 (`catalog.json` lists them);
- `examples/kirupa-portrait/`: the worked portrait's drawings;
- the drawing grids (`ROWS_…` and `KEYS_…`) in `examples/python-module/tangerine.py`;
- the grids of approved drawings quoted in `references/`: the drawings, not the text around them;
- in the pixelart repository (https://github.com/kirupa/pixelart), the README's showcase images and the drawing grid in the script that makes them.

The templates in `templates/` and the deliberately broken drawings in `examples/lint-failures/` are part of the code, under the MIT license.

The reference library is a small study collection, about 250 drawings at each size, chosen because the skill cites them or because faces depend on them. It isn't the Pixel set, and it mustn't be redistributed as one. The full set is at https://www.kirupa.com/tools/icon_gallery_pixel.htm, with the Icon Gallery at https://www.kirupa.com/tools/icon_gallery.htm and the license and credits at https://www.kirupa.com/design/icons.htm#license.

## The free license

The gallery wrote it for its PNG downloads. It applies the same way to these drawings in any form: text sprites, the PNGs you render from them, and grids quoted in the docs.

```text
KIRUPA ICON GALLERY - FREE LICENSE (PNG)

Copyright (c) kirupa.com.

You may use these PNG icons free of charge in personal and non-commercial
work: your own websites and blogs, slides, school work, and projects you
don't sell or use to promote a business. Please credit kirupa.com, for
example "Icons by kirupa.com".

Commercial use needs an Icon Gallery Pro license. Pro also includes the SVG
source files. Commercial use includes products and apps, client work, ads
and marketing, merchandise, and anything you sell.
https://www.kirupa.com/tools/icon_gallery.htm#pro

You may not resell or redistribute the icons as an icon set, font, or asset
pack, or present them as your own artwork.

The icons are provided as is, without warranty of any kind.
```

So: credit "Icons by kirupa.com" when you use the drawings. For commercial use, or for the SVG source files, get [Icon Gallery Pro](https://www.kirupa.com/tools/icon_gallery.htm#pro).

## Twemoji

The Pixel drawings are redrawn by hand from the Twemoji designs, so they carry Twemoji's credit:

```text
These icons are adapted from the Twemoji designs:
Twemoji graphics Copyright Twitter, Inc. and other contributors,
licensed under CC BY 4.0 https://creativecommons.org/licenses/by/4.0/
https://github.com/jdecked/twemoji (v17.0.3), the maintained fork of https://github.com/twitter/twemoji
These are modified versions, not official Twemoji artwork. No endorsement implied.
```

The original Twemoji project is https://github.com/twitter/twemoji. This repository redistributes no Twemoji files. The skill's `twemoji` and `sheet --twemoji` commands fetch Twemoji SVGs at runtime from jdecked/twemoji v17.0.3 (`https://cdn.jsdelivr.net/gh/jdecked/twemoji@v17.0.3/assets/svg/CODE.svg`) and cache them on your computer, or read them from a folder you name in `PIXEL_EMOJI_TWEMOJI_DIR`. Those SVGs are under CC BY 4.0, as above.

The `emoji` command draws the colour emoji font installed on your computer. Nothing from that font is bundled either.

## Emoji names

The names and file-name slugs in `assets/reference/catalog.json` are derived from Emojibase data v17.0.0:

```text
MIT License

Copyright (c) 2017-2019 Miles Johnson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

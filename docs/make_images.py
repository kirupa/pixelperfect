"""Draw the README's two assortments of icons with the skill's own tool:
docs/images/assortment-24.png and docs/images/assortment-16.png.

Run it from the repository root after changing any drawing they show:

    python docs/make_images.py

Each lays out 98 drawings in rows of 14 on a transparent background, so the pictures read on light and dark pages;
the README shows them at half size. The 24x24 assortment has 97 drawings from the bundled reference library and the
worked portrait of Kirupa, scaled 4x. The 16x16 assortment has 98 other drawings from the library, scaled 6x, so both
pictures share one grid: 96-pixel cells, 24 pixels apart. Scaling is nearest-neighbour. Each order below is fixed:
shuffled once, then arranged so neighbours differ in subject and colour. The pictures are artwork under
skills/pixelperfect/assets/LICENSE.md, like the drawings they show.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "pixelperfect"
sys.path.insert(0, str(SKILL / "scripts"))
import sprite_tool as st   # noqa: E402
from PIL import Image   # noqa: E402

IMAGES = ROOT / "docs" / "images"
PORTRAIT = SKILL / "examples" / "kirupa-portrait"
COLUMNS, CELL, SPACING = 14, 96, 24

# Reference-library codes, row by row. "kirupa" is the worked portrait.
ICONS = {
    24: """
1f600 1f697 1f3c6 1f427 2708 1f975 1f35e 1f680 1f1fa-1f1f8 1f602 1f9b8 1f43c 1f62d 1f381
1f366 1f430 1f1e8-1f1e6 1f607 1f354 1f575 1f44b 1f922 1f9d9 1f4da 1f4aa 1f335 1f382 1f431
1f388 1f929 1f337 1f3a4 1f419 1f525 1f4bb 1f1ef-1f1f5 1f34b 1f98b 2764 1f631 1f3ae 1f3e0
1f436 1f9d1-200d-1f680 1f44d 1f34a 1f923 1f1ec-1f1e7 1f438 kirupa 270f 1f60d 1f333 1f9df 1f918 1f976
1f92a 26bd 1f608 1f435 270c 1f4f7 1f6f8 1f973 1f4a7 1f9db 1f440 1f955 1f422 1f4a1
1f34e 1f41f 2728 1f3c1 267b 1f480 2600 1f444 2705 1f3f4-200d-2620-fe0f 1f42f 1f60e 1f46e 1f355
1f920 1f385 1f511 1fae0 1f477 1f989 1f643 2615 1f451 1f913 1f349 1f3b2 1f319 1f914
""".split(),
    16: """
1f604 1f467 1f635-200d-1f4ab 1f912 1f470 1f632 1f618 1f474 1f642-200d-2194-fe0f 1f486 1f972 1f644 1f475 1f606
1f92f 1f44c 1f970 1f9dd 1f611 1f62a 1f9d4 1f47f 1f64c 1f917 274c 1f471 1fae5 1f624
1f9d1-200d-1f9b2 1f927 1f37e 1f91e 1f971 1f9d5 1f448 1f92b 1f645 1f924 1f469 1f64f 1f928 1f47c
1fae8 1f926 1f925 1f9d0 1f9d1-200d-2695-fe0f 1f97a 1f636-200d-1f32b-fe0f 1f9d1-200d-1f393 1f60a 1f43e 1f915 1f974 1f5e3 1f61c
1f637 1f44f 1fae3 1f646 1f590 1f978 1f9d2 1f615 1f44a 1f9d1-200d-1f4bb 1f60f 1f9d1-200d-1f9b0 270d 1f910
1f9d1-200d-1f9b1 1f616 1f30a 1f92d 1f92e 1f468-200d-1f373 1f44e 1f635 2622 1f621 261d 1f453 1f609 1f937
1f633 1f628 1f476 1f622 1f473 1f60b 1fae1 1f935 1f62e-200d-1f4a8 1faea 1f478 1f62c 1f605 1f629
""".split(),
}


def drawing(code, size):
    sprite = st.parse_sprite(PORTRAIT / f"kirupa-{size}.sprite") if code == "kirupa" else st.set_sprite(size, code)
    image = sprite.image()
    if image.size != (size, size):
        sys.exit(f"{code}: expected {size}x{size}, got {image.width}x{image.height}")
    return image


def assortment(size):
    icons = ICONS[size]
    rows = -(-len(icons) // COLUMNS)
    step = CELL + SPACING
    board = Image.new("RGBA", (COLUMNS * step - SPACING, rows * step - SPACING), (0, 0, 0, 0))
    for i, code in enumerate(icons):
        board.alpha_composite(st.scaled(drawing(code, size), CELL // size), ((i % COLUMNS) * step, (i // COLUMNS) * step))
    return board


def main():
    shared = set(ICONS[24]) & set(ICONS[16])
    if shared:
        sys.exit(f"the assortments should differ, but both show {' '.join(sorted(shared))}")
    IMAGES.mkdir(parents=True, exist_ok=True)
    for size in ICONS:
        out = IMAGES / f"assortment-{size}.png"
        assortment(size).save(str(out), optimize=True)
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()

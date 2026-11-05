"""Draw the README's assortment of icons, docs/images/assortment.png, with the skill's own tool.

Run it from the repository root after changing any drawing it shows:

    python docs/make_images.py

It lays out 98 drawings at 24x24 in rows of 14: 97 from the bundled reference library and the worked portrait of
Kirupa. Each is scaled 4x, nearest-neighbour, on a transparent background, so the picture reads on light and dark
pages; the README shows it at half size. The order below is fixed: shuffled once, then arranged so neighbours differ
in subject and colour. The picture is artwork under skills/pixel-emoji/assets/LICENSE.md, like the drawings it shows.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "pixel-emoji"
sys.path.insert(0, str(SKILL / "scripts"))
import sprite_tool as st   # noqa: E402
from PIL import Image   # noqa: E402

OUT = ROOT / "docs" / "images" / "assortment.png"
PORTRAIT = SKILL / "examples" / "kirupa-portrait" / "kirupa-24.sprite"
SIZE, SCALE, GAP, COLUMNS = 24, 4, 6, 14

# Reference-library codes, row by row. "kirupa" is the worked portrait.
ICONS = """
1f600 1f697 1f3c6 1f427 2708 1f975 1f35e 1f680 1f1fa-1f1f8 1f602 1f9b8 1f43c 1f62d 1f381
1f366 1f430 1f1e8-1f1e6 1f607 1f354 1f575 1f44b 1f922 1f9d9 1f4da 1f4aa 1f335 1f382 1f431
1f388 1f929 1f337 1f3a4 1f419 1f525 1f4bb 1f1ef-1f1f5 1f34b 1f98b 2764 1f631 1f3ae 1f3e0
1f436 1f9d1-200d-1f680 1f44d 1f34a 1f923 1f1ec-1f1e7 1f438 kirupa 270f 1f60d 1f333 1f9df 1f918 1f976
1f92a 26bd 1f608 1f435 270c 1f4f7 1f6f8 1f973 1f4a7 1f9db 1f440 1f955 1f422 1f4a1
1f34e 1f41f 2728 1f3c1 267b 1f480 2600 1f444 2705 1f3f4-200d-2620-fe0f 1f42f 1f60e 1f46e 1f355
1f920 1f385 1f511 1fae0 1f477 1f989 1f643 2615 1f451 1f913 1f349 1f3b2 1f319 1f914
""".split()


def drawing(code):
    sprite = st.parse_sprite(PORTRAIT) if code == "kirupa" else st.set_sprite(SIZE, code)
    image = sprite.image()
    if image.size != (SIZE, SIZE):
        sys.exit(f"{code}: expected {SIZE}x{SIZE}, got {image.width}x{image.height}")
    return image


def assortment():
    rows = -(-len(ICONS) // COLUMNS)
    step = (SIZE + GAP) * SCALE
    board = Image.new("RGBA", (COLUMNS * step - GAP * SCALE, rows * step - GAP * SCALE), (0, 0, 0, 0))
    for i, code in enumerate(ICONS):
        board.alpha_composite(st.scaled(drawing(code), SCALE), ((i % COLUMNS) * step, (i // COLUMNS) * step))
    return board


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assortment().save(str(OUT), optimize=True)
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

"""Draw the README's showcase images in docs/images/ with the skill's own tool.

Run it from the repository root after changing the drawings it shows:

    python docs/make_images.py

Every sprite is scaled 8x, nearest-neighbour, onto a checkered canvas that marks its 16x16 or 24x24 grid. The
pictures are artwork under skills/pixel-emoji/assets/LICENSE.md, like the drawings they show.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "pixel-emoji"
sys.path.insert(0, str(SKILL / "scripts"))
import sprite_tool as st   # noqa: E402
from PIL import Image, ImageDraw   # noqa: E402

OUT = ROOT / "docs" / "images"
SCALE = 8
PAPER, CHECK, EDGE = (246, 248, 250, 255), (234, 238, 242, 255), (208, 215, 222, 255)
INK, GREY = (36, 41, 47, 255), (87, 96, 106, 255)
MARGIN = 32

EXEMPLARS = ["1f600", "1f34a", "2615", "1f989", "1f3a4", "1f6f8"]

# The first 16px tangerine, before Kirupa's "Make the 16x16 orange look less squished" (references/worked-examples.md
# section 4 tells the story). It uses the approved tangerine's palette.
TANGERINE_BEFORE = """\
..........####..
.........#ffc#..
.......a#fcc#...
.....##aa###....
...##gggeee##...
..#ghhgeeeeed#..
.#ghihgeeeeedd#.
#gghigeeeeeeddb#
#gggeeeeeeeeddb#
#egeeeeeeeeddbb#
#eeeeeeeeeddbbb#
#eeeeeeeeddbbbb#
.#deeeeeddbbbb#.
..#ddeeddbbbb#..
...##dddbbb##...
.....######.....
"""


def canvas(sprite):
    """The sprite at 8x on a checkerboard with one square per grid cell."""
    image = sprite.image()
    side = image.width * SCALE
    board = Image.new("RGBA", (side, side), PAPER)
    draw = ImageDraw.Draw(board)
    for y in range(image.height):
        for x in range(image.width):
            if (x + y) % 2:
                draw.rectangle([x * SCALE, y * SCALE, (x + 1) * SCALE - 1, (y + 1) * SCALE - 1], fill=CHECK)
    board.alpha_composite(st.scaled(image, SCALE))
    draw.rectangle([0, 0, side - 1, side - 1], outline=EDGE)
    return board


def centred(draw, text, x, y, size, color):
    face = st.font(size)
    width = draw.textlength(text, font=face) if hasattr(draw, "textlength") else face.getsize(text)[0]
    draw.text((x - width / 2, y), text, font=face, fill=color)


def exemplars():
    pair_w, gap, gutter, row_h = 128 + 16 + 192, 16, 48, 28 + 192 + 26 + 30
    rows = (len(EXEMPLARS) + 1) // 2
    board = Image.new("RGBA", (MARGIN * 2 + pair_w * 2 + gutter, MARGIN * 2 + rows * row_h - 30), PAPER)
    draw = ImageDraw.Draw(board)
    for i, code in enumerate(EXEMPLARS):
        x0, y0 = MARGIN + (i % 2) * (pair_w + gutter), MARGIN + (i // 2) * row_h
        small, big = st.set_sprite(16, code), st.set_sprite(24, code)
        name = st.reference_item(code)["name"]
        centred(draw, name[:1].upper() + name[1:], x0 + pair_w / 2, y0, 17, INK)
        base = y0 + 28 + 192
        board.alpha_composite(canvas(small), (x0, base - 128))
        board.alpha_composite(canvas(big), (x0 + 128 + gap, base - 192))
        centred(draw, "16\u00d716", x0 + 64, base + 6, 13, GREY)
        centred(draw, "24\u00d724", x0 + 128 + gap + 96, base + 6, 13, GREY)
    return board


def portrait():
    folder = SKILL / "examples" / "kirupa-portrait"
    parts = [("kirupa-16.sprite", "16\u00d716"), ("kirupa-24.sprite", "24\u00d724"),
             ("kirupa-16-yellow.sprite", "16\u00d716"), ("kirupa-24-yellow.sprite", "24\u00d724")]
    widths, gaps = [128, 192, 128, 192], [16, 48, 16]
    width = MARGIN * 2 + sum(widths) + sum(gaps)
    board = Image.new("RGBA", (width, MARGIN * 2 + 28 + 192 + 26), PAPER)
    draw = ImageDraw.Draw(board)
    x, base, starts = MARGIN, MARGIN + 28 + 192, []
    for (name, label), w, gap in zip(parts, widths, gaps + [0]):
        board.alpha_composite(canvas(st.parse_sprite(folder / name)), (x, base - w))
        centred(draw, label, x + w / 2, base + 6, 13, GREY)
        starts.append(x)
        x += w + gap
    centred(draw, "Real skin tone", (starts[0] + starts[1] + 192) / 2, MARGIN, 17, INK)
    centred(draw, "Set yellow", (starts[2] + starts[3] + 192) / 2, MARGIN, 17, INK)
    return board


def before_after():
    after = st.set_sprite(16, "1f34a")
    before = st.Sprite("tangerine, before", TANGERINE_BEFORE.split(), after.palette)
    panel, arrow = 240, 72
    board = Image.new("RGBA", (MARGIN * 2 + panel * 2 + arrow, MARGIN * 2 + 128 + 54), PAPER)
    draw = ImageDraw.Draw(board)
    labels = [("Before", "a squat body, 14\u00d711"), ("After", "a true circle, 12\u00d712")]
    for i, (sprite, (title, note)) in enumerate(zip((before, after), labels)):
        x = MARGIN + i * (panel + arrow)
        board.alpha_composite(canvas(sprite), (x + (panel - 128) // 2, MARGIN))
        centred(draw, title, x + panel / 2, MARGIN + 128 + 8, 17, INK)
        centred(draw, note, x + panel / 2, MARGIN + 128 + 32, 13, GREY)
    mid_x, mid_y = MARGIN + panel + arrow / 2, MARGIN + 64
    draw.line([mid_x - 22, mid_y, mid_x + 18, mid_y], fill=GREY, width=4)
    draw.polygon([(mid_x + 24, mid_y), (mid_x + 10, mid_y - 10), (mid_x + 10, mid_y + 10)], fill=GREY)
    return board


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, make in (("exemplars.png", exemplars), ("portrait.png", portrait),
                       ("before-after.png", before_after)):
        path = OUT / name
        make().convert("RGB").save(str(path), optimize=True)
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()

# Worked examples

Eleven drawings from kirupa.com's published Pixel sets, each at 16 and 24, with the reasoning behind every pixel that matters. I chose them because almost every one failed first, and each failure taught a rule you'll need for other subjects:

- reinterpreting a 3D emoji;
- three-quarter views and materials;
- true circles;
- straight diagonals;
- symmetric light;
- emitted light;
- accidental faces;
- flags;
- flat marks.

Faces and people have their own long reference, `faces.md`; here they get a short pointer at the end.

How to use this file:

- **Print any approved grid yourself:** `python3 scripts/sprite_tool.py text set:16:2615` (or `set:24:2615`). `text` keys the palette by brightness: `a` is the darkest colour after ink. So the same letter means different colours in different sprites. The role written after each colour is mine.
- **Look at it, don't just read it:**

  ```bash
  python3 scripts/sprite_tool.py zoom set:16:2615 set:24:2615 --out 2615-zoom.png
  python3 scripts/sprite_tool.py sheet set:16:2615 set:24:2615 --twemoji 2615 --emoji 2615 --out 2615-board.png
  ```

  `zoom` puts both on a numbered grid. `sheet` sets them beside Twemoji and the system emoji, at real size on light and dark. Do this for every example before you read my notes on it.
- **Lint it:** `python3 scripts/sprite_tool.py check set:16:2615 set:24:2615`. The `check` output below is verbatim.
  - The mirror figure compares only the silhouette (which pixels are opaque), not colours. So a sphere lit from the upper left can still score `0 off`.
  - Warnings on approved art are explained where they appear. A warning asks you to look, not to change.
- **Grids marked wrong** are earlier versions I rebuilt from my notes. They aren't bundled, so their `check` output names them `old/NAME.sprite` and you can't re-run it.
- **Coordinates** are `(x, y)` counted from 0 at the top left, as in `construction.md`. "Rows 3–7" means y = 3 to 7.

Each example opens with the brief, the header lines of SKILL.md Step 2. Where kirupa.com's drawing module for the sprite records one, I quote it, so the brief is the one that produced the approved art. Then come:

- what Kirupa said;
- the approved sprites;
- my decisions;
- what went wrong first;
- the lint result;
- the rule to take away.

Contents:

1. Slightly smiling face (1f642): the baseline head
2. Hot beverage (2615): a 3D emoji redrawn as a side profile
3. Bread (1f35e): three-quarter view, material and texture
4. Tangerine (1f34a): a true circle first, accessories outside it
5. Microphone (1f3a4): a diagonal that stays straight
6. Skull and crossbones (2620): symmetry and where the light comes from
7. Flying saucer (1f6f8) and floating saucer (e6f8): reimagining, and light that stays flat
8. Radioactive (2622): a symbol, and the face nobody asked for
9. Flag: United States (1f1fa-1f1f8): stripes and stars by count
10. Paw prints (1f43e): one big flat mark
11. Faces and people: where to look
12. The patterns in one table

## 1. Slightly smiling face (1f642): the baseline head

```text
essence: a friendly yellow face with a small smile
keep: the round head, two eyes, one smile line
drop: Twemoji's soft shading, eye highlights and blush
view: front, mirror-symmetric
```

The 16px module's note is shorter: "eyes and a shallow smile, nothing else".

**What Kirupa said:**

- "For the smileys, match the yellow tone of the darkproject yellow smilies."
- "For the smileys, notice that the darkproject smileys for the vertical eyes are just one pixel thick. Mimic that so that these look harmonious when placed SxS to them."

```text
1f642                      1f642
......#####.....           ........................
....##ddddc##...           ........########........
...#ddccccccc#..           ......##ddddddcc##......
..#deccccccccc#.           .....#ddcccccccccb#.....
..#dcc#ccc#ccc#.           ....#dcccccccccccbb#....
.#dccc#ccc#cccb#           ...#dcceecccccccccbb#...
.#dccc#ccc#cccb#           ..#dcccec#cccc#ccccbb#..
.#dcccccccccccb#           ..#dccccc#cccc#ccccbb#..
.#dccccccccccba#           .#dcccccc#cccc#cccccbb#.
.#ccc#ccccc#cba#           .#dcccccc#cccc#cccccbb#.
..#ccc#####cba#.           .#dcccccc#cccc#cccccbb#.
..#ccccccccbba#.           .#dcccccccccccccccccba#.
...#cccccbbaa#..           .#dcccccccccccccccccba#.
....##bbbaa##...           .#dcccccccccccccccccba#.
......#####.....           .#dcccc#cccccccc#cccba#.
................           .#dccccc#cccccc#ccccba#.
                           ..#cccccc######ccccba#..
                           ..#ccccccccccccccccba#..
                           ...#ccccccccccccccba#...
                           ....#bbbccccccccbbb#....
                           .....#bbbbbbbbbbaa#.....
                           ......##bbbbbaaa##......
                           ........########........
                           ........................
```

Both sizes use the same five yellows: `a` #f08e00, `b` #ffbf00, `c` #ffe600, `d` #ffff93, `e` #ffffcf. In order, those are:

1. the deep shade;
2. the shade rim;
3. the base;
4. the light rim;
5. the glint.

**Decisions:**

- **The head fills the canvas.** It's 15×15 at 16, columns 1–15 with axis 16, so it has a one-pixel centre column at x 8. At 24 it's 22×22, columns 1–22 with axis 23, so its centre is a two-column seam. These are the templates `smiley-16` and `smiley-24`. Start every round face from them.
- **The eyes are 1px wide and solid ink.** At 16 each is 1×3, at x 6 and x 10 on rows 4–6. At 24 each is 1×5, at x 9 and x 14 on rows 6–10.
  - The 24's eyes are taller, not wider. Doubling the 16 would give 2px eyes and break the harmony Kirupa asked for.
- **The mouth is one line with lifted corners.**
  - At 16, the corners at (5, 9) and (11, 9) sit one row above the line, which runs x 6–10 on row 10.
  - At 24, each corner is a two-pixel step, (7, 14) and (8, 15) on the left, (16, 14) and (15, 15) on the right. The line runs x 9–14 on row 16.
  - The corners are the expression. Move them and the face changes mood.
- **Light from the upper left, round the rim only.**
  - The light rim hugs the outline at the upper left, and the two shade rims hug it at the lower right.
  - The glint is one pixel at (4, 3) at 16. At 24 it's three pixels, (7, 5), (8, 5) and (7, 6).
  - The middle of the face stays flat base yellow, so the features sit on a clean field.

**What went wrong first:** my first smileys were Twemoji shrunk onto the grid. The eyes were several pixels wide, with whites and highlights, and at 1x they read as mush. Kirupa: "The eyes in all of your smileys are uncannily bad."

```text
set:16:1f642 (16px): ok  inner 7%  colours 6  span 15x15  mirror x+x'=16 (0 off)
set:24:1f642 (24px): ok  inner 5%  colours 6  span 22x22  mirror x+x'=23 (0 off)
```

**Take away:** a face is read from about twenty pixels, so each one is a decision. Everything else about faces is in `faces.md`:

- the 16px and 24px face kits;
- every published smiley as a recipe;
- hands, people and hair;
- portraits from a photo.

## 2. Hot beverage (2615): a 3D emoji redrawn as a side profile

```text
essence: a mug of hot coffee, steaming
keep: a white mug in side profile, the coffee's surface, a handle, two wisps of steam
drop: Twemoji's saucer, its 3D tilt and its soft gradients
view: side profile
```

The modules' own words:

- **16:** "a side-profile mug, steam as two pale wisps". The steam is in fact dark slate; see below.
- **24:** "a classic white mug of coffee with two wisps of steam, instead of Twemoji's cup and saucer, which turn to mush at 24px."

**What Kirupa said:**

- "Look at the icons now. The coffee one looks really bad. Compare it to darkproject's version of coffee (see attached). Notice the cleaner lines."
- "It is ok to reinterpret the intent, kind of like coffee. fully 3D is hard in pixel art."
- He later made this mug the model for everything: "The best example is the coffee emoji. In the original Twemoji, it is a 3D version, which works when you have antialiased lines. In the darkproject version, it is simplified to a 2D side profile view, which translates very nicely to pixel art. The colors are subtly different to indicate a curvature."

### 16px

```text
name: hot beverage (2615)
size: 16

[palette]
a #4a2414 coffee in shadow under the far rim
b #7a3e20 coffee
c #4b4f5c steam, flat slate, no outline
d #a65a2e the one lit coffee pixel
e #7f8799 darkest mug band, right edge
f #a7aebd mug shade band and handle shade
g #cfd4de mug edge tone and handle
h #eceef3 mug base white
i #ffffff highlight band and the front lip

[grid]
......c..c......
.....c..c.......
......c..c......
..##########....
.#haaaaaaaag#...
.#hdbbbbbbbg#...
.#hiiiiiiigf#...
.#giihhhhgfe###.
.#giihhhhgfe#hg#
.#giihhhhgfe##f#
.#giihhhhgfe##f#
.#giihhhhgfe#gf#
.#giihhhhgfe###.
.#giihhhhgfe#...
.#giihhhhgfe#...
..##########....
```

**Decisions at 16:**

- **The view does the work.** The mug is a rectangle: the outline runs x 1–12 by rows 3–15, with the four corner pixels left off so it reads rounded. There's no saucer; at 16 a saucer is a grey line that adds nothing.
- **The cylinder is vertical bands, not a gradient.** Rows 7–14 read `g ii hhhh g f e`, left to right:
  - `g`, an edge tone;
  - `ii`, a two-pixel highlight band;
  - `hhhh`, the base white;
  - `g f e`, three steps of shade toward the right.

  That's what Kirupa meant by "The colors are subtly different to indicate a curvature." The highlight sits one pixel in from the left edge, not on it, because a cylinder's edge turns away from you. The bands run the full height, so the mug reads round at 1x.
- **The coffee is two rows.**
  - Row 4 is the coffee in shadow under the far rim (`a`, the darkest colour).
  - Row 5 is the coffee itself (`b`), with one lit pixel `d` at (3, 5).
  - Row 6 is the near lip in white (`i`), the brightest row on the mug. The lip separates coffee from mug with no ink at all.
- **Ink closes the opening.** Row 3 is ink from x 2 to 11; the coffee sits under it.
- **The handle's hole is ink.** The handle is x 12–15, rows 7–12, and its hole is ink at x 13 on rows 9–10. A hole narrower than 3px can't be transparent, because the outline round it would fill it (see `construction.md`, section 5).
- **The steam is flat and unoutlined.** It's two three-pixel zigzags of dark slate, (6, 0), (5, 1), (6, 2) and (9, 0), (8, 1), (9, 2).
  - An outline round a one-pixel wisp makes a black worm.
  - Mid-dark slate reads on both white and dark pages.
  - Steam is an effect, not a solid, so it takes no light.

### 24px

```text
name: hot beverage (2615)
size: 24

[palette]
a #4f2410 coffee in shadow under the back lip
b #74391a coffee, sides of the oval
c #9a5428 coffee
d #6b7690 deepest mug shade, bottom-right corners
e #9aa3bd mug shade band
f #e6ad72 crema glint
g #c7cde0 mug mid-shade
h #e6e9f2 mug base white
i #f7f8fc mug light
j #ffffff highlight band, lip and steam wisps

[grid]
......#.....#...........
.....#j#...#j#..........
.....#j#...#j#..........
......#j#.#j#...........
......#j#.#j#...........
.......#...#............
........................
.....#########..........
...##jjiiiiihh##........
..#jjaaaaaaaaahh#.......
.#jbbcccccccccbbg#......
.#jbcffcccccccbbg#####..
.#ijjccccccccbhhg#ihhg#.
.#hijjjjjiiiihgee####ge#
.#hijjiiihhhhggee#..#ge#
.#hijjiiihhhhggee#..#ge#
.#hijjiiihhhhggee#..#ge#
.#hijjiiihhhhggee#..#ge#
.#hijjiiihhhhggee####ge#
.#hijjiiihhhhggee#geed#.
.#hijjiiihhhhggee#####..
..#hhhhhggggeeed#.......
...#############........
........................
```

**Decisions at 24:**

- **Redrawn, not scaled.** I drew the 24 from the brief, not from the 16, and used the extra room for things the 16 couldn't hold.
- **The rim becomes an oval.** At 24 the eye sits a little above the rim:
  - Row 8 is the back lip (`j`, `i`, `h`).
  - The coffee is an oval on rows 9–12. Its far edge is in shadow (`a`, row 9), its sides are darker (`b`), and a two-pixel crema glint (`f`) sits at x 5–6 on row 11.
  - The front lip (`j`) closes it on rows 12–13.

  The module: "a white ceramic mug lit from the upper left, an oval of coffee with a light rim, a squared handle and two wisps of steam."
- **The body keeps the same band logic.**
  - Rows 14–20 read `h i jj iii hhhh gg ee` from x 2 to 16.
  - Row 21 darkens to `hhhhh gggg eee d`, because the bottom turns away from the light.
  - The deepest tone `d` appears only at the bottom-right corners of the mug and the handle.
- **The handle hole is real now.** At 24 there's room for a 2×4 hole (x 18–19, rows 14–17) with ink round it, so it's transparent and the page shows through.
- **The steam becomes outlined white wisps.** They're (6, 1), (6, 2), (7, 3), (7, 4) and (12, 1), (12, 2), (11, 3), (11, 4), and they lean apart as they rise.
  - At 24 there's room for ink on both sides of a 1px line, and outlined white reads better than slate.
  - The steam is flat at both sizes. The 16 just can't afford to outline it.
- **Ten colours at 16, eleven at 24.** The extra 24 colours went to the crema and a deeper shade, not to texture.

**What went wrong first:** my earlier cup followed Twemoji: a cup on a saucer seen from above, filled with Twemoji's flat colours, with black lines between the parts. The fix wasn't better shading; it was a different view.

```text
set:16:2615 (16px): ok  inner 6%  colours 10  span 15x16  mirror x+x'=15 (20 off)
   warn  6 pixels of unoutlined 1px lines (x,y): (6,0), (9,0), (5,1), (8,1), (6,2), (9,2) -- right only for flat effects (steam, rays, sparkles, motion) in a mid tone that reads on white and dark
   warn  2x2 black block inside the shape at (x,y): (12,9) -- right for a hole, an open mouth, an eye socket or a dark lens; otherwise it's a blotch
set:24:2615 (24px): ok  inner 2%  colours 11  span 23x23  mirror x+x'=22 (65 off)
```

Both 16px warnings are explainable:

- The unoutlined pixels are the steam, an effect.
- The 2×2 black block at (12, 9) is the handle's ink hole beside the mug's own outline.

The 24 has no warnings.

**Take away:**

- When the emoji is drawn in 3D, find the view in which the object is a clean silhouette: side, front or plan.
- Show the third dimension with bands of tone, not with perspective.
- Effects such as steam stay flat. They get ink only when there's room for it on both sides.

## 3. Bread (1f35e): three-quarter view, material and texture

The module's brief:

> 1f35e bread -- essence: a golden loaf in three-quarter view, a domed crust behind a pale cut end; keep: the crust rising to a rounded top lit at the upper left and darkening down the long right side, the cut face on the left in cream crumb tones inside a darker crust rim; drop: Twemoji's pinkish tan (golden crust as in the 24px reference)

Twemoji's bread is a front-on slice. Three-quarter view is the exception in this set: use it only when the 3D is the essence. Here it is, because bread is crust and crumb, and you can see both only from three-quarters.

**What Kirupa said:** "Don't use the outlines as an excuse for doing a shoddy job. Focus on bread. For bread, look at this attached example that looks very nice. Tell me why yours looks terrible." Then, after my answer: "Generalize your learnings for all emojis. Not just the bread themed ones."

My answer became rules for every subject, so here it is in full:

1. **Flat fills, no light.** I'd copied Twemoji's one or two flat tones per part. The reference used one light and a 4–6-tone, hue-shifted ramp per material.
   - Bread runs from near-black brown through red-brown, orange and gold to cream.
   - Highlights go warm and yellow; shadows go red-brown.
2. **Narrow value range.** Pastels go muddy at pixel scale. The reference spans almost black to almost white within one object.
3. **Black lines between every part: stained glass.** Ink belongs on the silhouette and on real holes. Crust against crumb, scoring and seams are drawn with a darker local tone.
4. **The wrong view.** A front-on slice is one flat shape. A three-quarter view shows top, side and cut face: three planes for three tones.
5. **No material.** The reference had sparse 1px holes in the crumb and 2–3px highlight clusters on the crust.
6. **Silhouettes not designed for the grid.** Good sprites fill the canvas with clean stair-steps and readable negative space, not a lumpy blob.
7. **Copying the source when it fails.** Reimagine instead: Twemoji's flying saucer beam reads as a lamp or a pedestal at pixel size (example 7).

### 16px

```text
name: bread (1f35e)
size: 16

[palette]
a #9c4416 deepest crust, bottom and lower right
b #c4651f crust side, in shade
c #de8a2e crust mid and the cut face's crust rim
d #f0b148 lit top crust
e #e4b679 crumb shade where the face meets the side
f #f3d39d crumb mid and the one hole
g #f9d67f crust highlight
h #fbe6c0 crumb
i #fff6e2 lightest crumb and crust glints

[grid]
........#####...
......##ggddd#..
....##giggdddc#.
...#gigggdddcbb#
..#ccccdddcbbbb#
.#ciiihccbbbbb#.
#ciihhhfbbbbba#.
#chhhffebbbbba#.
.#chhfebbbbbba#.
.#chfhebbbbbaa#.
.#chhfebbbbaaa#.
.#chffebbbaaa#..
.#cfffebaaaa#...
.#aaaaaaaa##....
..########......
................
```

**Decisions at 16:**

- **Three planes, three lights.**
  - The dome (rows 0–4) is lit gold (`g`, `d`), with two glint pixels `i` at (7, 2) and (5, 3).
  - The cut face (rows 5–12, left of x 7) is pale crumb inside a crust rim (`c`) down its left edge, lightest at its upper left.
  - The long side (x 7–13) is in shade (`b`) and darkens to `a` at the lower right.
- **No ink inside: 0%.**
  - A row of crust tone separates the cut face from the dome: `c` at x 3–6 on row 4 is the crust's rim round the face.
  - A column of crumb shade separates the face from the side: `e` at x 6–7.

  Tone does the work of the line.
- **One hole.** A single `f` pixel at (4, 9). At 16 one hole says "crumb"; a pattern of them says "noise".
- **A dark base.** The bottom crust (row 13, `a` at x 2–9) is the darkest band, so the loaf sits on something.
- **Two ramps.** Crust is `a b c d g` and crumb is `e f h i`, sharing the lightest tone for glints. That's 9 colours plus ink.

### 24px

```text
name: bread (1f35e)
size: 24

[palette]
a #6e2c10 deepest crust, lower right
b #9c4416 shaded crust: face-to-side edge, bottom, far side
c #c4651f crust side and the cut face's top rim
d #de8a2e crust mid and the cut face's left rim
e #c98f52 crumb holes
f #f0b148 lit top crust
g #e4b679 crumb shade along the face's right edge and bottom
h #f3d39d crumb
i #f9d67f crust highlight
j #fbe6c0 light crumb
k #fff0c4 crust glints
l #fff6e2 lightest crumb, upper left

[grid]
........................
........................
.............######.....
...........##iiffff#....
.........##iiiiffffd#...
.......##ikkiffffdddd#..
.....##ikkiffffddddccb#.
....#cccccfffddddccbba#.
...#clljjjcddddccbbcb#..
..#dljjjhjhcdccbbcccb#..
.#djjjehhhhgbbbcccccb#..
.#djhhhhhhegbcccccccb#..
..#djhhhhegbccccccccb#..
..#dhhehhhgbccccccccb#..
..#dhhhehggbcccccccbb#..
..#dhehhhggbcccccbbbb#..
..#dhhhhhhgbcccbbbbaa#..
..#dhhhehhgbcbbbbaa##...
..#dhhhhehgbbbbaa##.....
..#bgggggggbbaa##.......
..#bbbbbbbbbb##.........
...##########...........
........................
........................
```

**Decisions at 24:**

- **The same three planes, given room.** The dome is rows 2–7, the cut face is a tall rounded panel at x 3–10 on rows 8–19, and the side is x 11–20.
- **Crumb texture.** There are eight hole pixels (`e`), single or in diagonal pairs:
  - (6, 10)
  - (10, 11) and (9, 12)
  - (6, 13) and (7, 14)
  - (5, 15)
  - (7, 17) and (8, 18)

  There's never a 2×2 block and never a regular pattern; holes in a grid read as a waffle.
- **The cut face has a crust frame without ink.**
  - A crust tone tops it (`c` at x 5–9 on row 7).
  - A lit crust rim runs down its left (`d`, x 2–3).
  - The bottom crust is shaded (`b`, rows 19–20).
  - A crumb shade (`g`) marks where the face turns into the side.
- **Glints are a cluster, not a line.** Two pairs of `k` at x 10–11 on row 5 and x 8–9 on row 6 make a small diagonal highlight on the dome.
- **13 colours, inside the 24px limit of 18.** The 24 earned a deeper crust, a hole tone and glints; it didn't earn a third ramp.

**What went wrong first:** my first bread was Twemoji's slice, flat-filled, with black lines between crust and crumb. It had every fault in the list above.

```text
set:16:1f35e (16px): ok  inner 0%  colours 10  span 16x15  mirror x+x'=15 (29 off)
set:24:1f35e (24px): ok  inner 0%  colours 13  span 22x20  mirror x+x'=23 (58 off)
```

**Take away:**

- The right view gives you planes. The planes give you tones. The tones replace lines.
- Texture is a few deliberate pixels, never a pattern.

## 4. Tangerine (1f34a): a true circle first, accessories outside it

The module's brief:

> 1f34a tangerine -- essence: a round orange fruit with a twig and a leaf; keep: a true 14px circle lit from the upper left, the 24px layout of a twig up-left and a long leaf up-right above it; drop: peel dimples

**What Kirupa said:**

- "Make the 16x16 orange look less squished". He offered the site's logo as a starting point: "The site's logo is an orange. Use that as an inspiration if needed."
- My next version still wasn't right. He asked for it to be "more round and less squishy".

Here are the three 16s in order: the original, my first fix (B5) and the approved drawing (R5).

```text
tangerine-16-old   tangerine-16-b5    1f34a
..........####..   ....##....#####.   ....##....#####.
.........#ffc#..   ....#a#..#fffc#.   ....#a#..#fffc#.
.......a#fcc#...   .....#a##ffcc#..   .....#a##ccc##..
.....##aa###....   ....##a#ccc##...   ....##ggge##....
...##gggeee##...   ...#ghhggeee#...   ...#ghhggeee#...
..#ghhgeeeeed#..   ..#ghhhhggeee#..   ..#ghhhhggeee#..
.#ghihgeeeeedd#.   ..#hhiihggeee#..   ..#hhiihggeee#..
#gghigeeeeeeddb#   .#ghhihhggeeee#.   .#ghhihhggeeee#.
#gggeeeeeeeeddb#   .#gghhhgggeeee#.   .#gghhhgggeeee#.
#egeeeeeeeeddbb#   .#gggggggeeeed#.   .#gggggggeeeed#.
#eeeeeeeeeddbbb#   .#eeggggeeeedd#.   .#eeggggeeeedd#.
#eeeeeeeeddbbbb#   ..#eeeeeeeedd#..   ..#eeeeeeeedd#..
.#deeeeeddbbbb#.   ..#eeeeeeeddb#..   ..#eeeeeeeddb#..
..#ddeeddbbbb#..   ...#eeeeeddb#...   ...#eeeeeddb#...
...##dddbbb##...   ....##eedd##....   ....##eedd##....
.....######.....   ......####......   ......####......
```

**The original (wrong).** Its brief said "a squat round orange fruit with a stem and one leaf", so I drew a squat fruit. The body inside the outline is 14 wide and 11 tall. The drawing did exactly what the brief asked; the brief was wrong. **Words in a brief become pixels**, so choose the adjectives as carefully as the colours.

**B5 (still wrong).** I replaced the flat top with the twig and leaf. It looked taller, because the accessories took the top rows. But the body itself was still 12 wide and 11 tall. Measure the body, not the bounding box.

I also tried the logo's crown of leaves. At 16 it read as a bow tied on top, so I dropped it.

**R5 (approved).** I drew a true circle first, then put the twig and leaf outside it.

- **The ring:** a 14px outline circle, x 1–14 by rows 2–15.
- **The body:** 12×12, with row widths 4, 8, 10, 10, 12, 12, 12, 12, 10, 10, 8, 4. That's the same top to bottom, so the fruit is as tall as it is wide.
- **The twig and the leaf:** the twig (`a`) is at (5, 1) and (6, 2), and the two-tone leaf (`f`, `c`) is at x 9–13 on rows 1–2. Both sit on top of the ring and touch the outline only where they join it.
- **The light:** a diagonal ramp from the white glint at (5, 6), (6, 6) and (5, 7) at the upper left, through lit, base and shade, to the deepest shade at the lower right.

```text
name: tangerine (1f34a)
size: 16

[palette]
a #5b3417 twig
b #a54806 deepest peel shade, lower right
c #3f9a25 leaf shade
d #d4690a peel shade
e #f58f0c peel base
f #7ccf3a leaf light
g #ffae3d lit peel
h #ffd28c peel light
i #ffffff glint

[grid]
....##....#####.
....#a#..#fffc#.
.....#a##ccc##..
....##ggge##....
...#ghhggeee#...
..#ghhhhggeee#..
..#hhiihggeee#..
.#ghhihhggeeee#.
.#gghhhgggeeee#.
.#gggggggeeeed#.
.#eeggggeeeedd#.
..#eeeeeeeedd#..
..#eeeeeeeddb#..
...#eeeeeddb#...
....##eedd##....
......####......
```

The 24 already had the layout the 16 needed, which is why the brief says "the 24px layout":

- **The body:** a 20×20 outline circle, x 2–21 by rows 4–23.
- **The twig:** (8, 1), (9, 2) and (10, 3), running up and to the left.
- **The leaf:** three tones, running up and to the right from (12, 4) to (20, 1).

```text
name: tangerine (1f34a)
size: 24

[palette]
a #2f7a35 leaf, deepest
b #b8430a deepest peel shade
c #965c34 twig
d #4f9e3a leaf shade
e #e2660c peel shade
f #f4900c peel base
g #86c44a leaf light
h #ffb03a lit peel
i #ffd47a peel light
j #fff4d6 glint

[grid]
........#.......#####...
.......#c#....##ggggg#..
........#c#..#ggggdddd#.
.........#c##ggddddaa#..
........####dddaaaa##...
......##hhhh#######.....
.....#hhhiihhfffff#.....
....#hhhiiiihhfffff#....
...#hhhijjiihfffffff#...
...#hhhijiihfffffffe#...
..#hhhhiiiihfffffffee#..
..#hhhhhiihffffffffee#..
..#fhhhhhhfffffffffee#..
..#ffhhhhfffffffffeee#..
..#fffhhffffffffffeeb#..
..#ffffffffffffffeeeb#..
..#fffffffffffffeeebb#..
..#ffffffffffffeeebbb#..
...#fffffffffeeeeebb#...
...#efffffffeeeeebbb#...
....#eefffffeeeeebb#....
.....#eeeeeeeeebbb#.....
......##eeeeeebb##......
........########........
```

```text
old/tangerine-16-old.sprite (16px): ok  inner 2%  colours 10  span 16x16  mirror x+x'=15 (14 off)
   essence: a squat round orange fruit with a stem and one leaf
   warn  1 dark pixels are their own edge (x,y): (7,2) -- right for a thin dark stem, leaf tip, strand of hair or whisker; otherwise outline it
old/tangerine-16-b5.sprite (16px): ok  inner 2%  colours 10  span 14x16  mirror x+x'=15 (10 off)
   essence: a round orange fruit with a twig and a leaf
set:16:1f34a (16px): ok  inner 1%  colours 10  span 14x16  mirror x+x'=15 (9 off)
set:24:1f34a (24px): ok  inner 2%  colours 11  span 21x24  mirror x+x'=23 (31 off)
```

**Lint passed all three 16s.** The squat one's only warning is about a twig pixel. Lint can't see "squished". You can, if you measure: count the body's width and height inside the outline, and compare them with the subject's real proportions, before anyone else sees it.

**Take away:**

- Draw the whole body first, using the circle tables in `construction.md`. Accessories go outside it.
- Measure the body, not the bounding box.
- Read your brief's adjectives back to yourself.

## 5. Microphone (1f3a4): a diagonal that stays straight

The module's brief:

> 1f3a4 microphone -- essence: a handheld mic: a round silver grille head on a dark handle; keep: ball head with grille dots, blue collar, a straight tapered handle at 45 degrees, one blue note; drop: the second note

**What Kirupa said:** "the microphone doesn't look good. It looks curved. Make it better and feel free to explore different microphone styles if that would be easier to represent in 16x16."

Here are the wrong 16 and the approved one:

```text
mic-16-old         1f3a4
.........####...   ...##....####...
........#jjii#..   ..#ff#..#jijg#..
.......#jkjiig#.   ..#f#c##kkjiii#.
......#jkkiiiig#   .##f###jkjgiggd#
......#jkiiiiig#   #ffc#.#jjiiiggg#
......#jiiiiiig#   #cc#..#jgiggdgb#
.....#hiiiiiigg#   .##...#iiigggdd#
.....#hfiiiigg#.   .....#hhggdgbd#.
....#aefcgggd#..   ....#eefcggdd#..
...#ebbacc###...   ...#eebac####...
..#ebba###......   ..#eebaa#.......
.#ebba#.........   ..#ebaa#........
.#eba#..........   .#eba##.........
#eba#...........   #eba#...........
#ba#............   .#a#............
.##.............   ..#.............
```

**Why the old one looked curved.** Its handle's edges disagreed:

- The right ink stepped exactly one column per row: x 7, 6, 5, 4, 3 on rows 10–14.
- The left ink went x 3, 2, 1, 1, 0, 0 on rows 9–14.
- The light stripe inside went x 4, 3, 2, 2, 1, stalling at row 12.

A line that stalls bends. When the edges and the stripes of a long shape step at different rates, the eye reads a curve.

**What I tried before the fix.** Kirupa invited other styles, so I tried several:

- A thin handle read as a magnifier or a spoon.
- Upright mics read as a light bulb or an ice-cream cone.
- A wide collar read as a cone or a flashlight.

The handheld ball mic, laid on the 45° diagonal, was the only one that read as a microphone at 16.

### 16px

```text
name: microphone (1f3a4)
size: 16

[palette]
a #323d4f handle, dark side
b #4f5d73 handle mid stripe and the ball's darkest pixels
c #2f7fd6 collar and note shade
d #66757f grille dots and ball deep shade
e #76869c handle light edge
f #5dadec collar and note
g #99aab5 ball shade
h #a6d6ff collar light
i #ccd6dd ball mid
j #e1e8ed ball light
k #f5f8fa ball highlight

[grid]
...##....####...
..#ff#..#jijg#..
..#f#c##kkjiii#.
.##f###jkjgiggd#
#ffc#.#jjiiiggg#
#cc#..#jgiggdgb#
.##...#iiigggdd#
.....#hhggdgbd#.
....#eefcggdd#..
...#eebac####...
..#eebaa#.......
..#ebaa#........
.#eba##.........
#eba#...........
.#a#............
..#.............
```

**Decisions at 16:**

- **Every internal boundary in the handle is a perfect 1:1 diagonal.** On rows 9–13:
  - the middle stripe `b` runs x 6, 5, 4, 3, 2;
  - the right edge of the light `e` runs x 5, 4, 3, 2, 1;
  - the left edge of the dark `a` runs x 7, 6, 5, 4, 3.

  The taper happens only at the outer outline. Taper inside the shape and the stripes kink.
- **The ball is a lit sphere with a texture.** It fills x 6–15 on rows 0–9 and is lit from the upper left; the highlight is at (8, 2), (9, 2) and (8, 3). The grille is a scatter of single dark dots (`d`) in the shaded half. At 16 a full mesh is noise; a few dots say "grille".
- **The collar is a blue band across the diagonal,** in three tones: `h` at (6, 7) and (7, 7), `f` at (7, 8), and `c` at (8, 8) and (8, 9). It separates head from handle with colour instead of a black line.
- **One note, top left.** It has a stem at x 3 on rows 1–3, a flag at (4, 1) and (5, 2), and a head at x 1–3 on row 4 and x 1–2 on row 5. It fills the empty corner the diagonal leaves, and it says "music". The second note in Twemoji was dropped.

### 24px

```text
name: microphone (1f3a4)
size: 24

[palette]
a #323d4f handle, dark side
b #3b4650 dark grille dots
c #4f5d73 handle mid stripe
d #2f7fd6 collar and note shade
e #66757f ball deep shade and grille dots
f #76869c handle light edge
g #5dadec collar and note
h #99aab5 ball shade
i #a6d6ff collar light
j #ccd6dd ball mid
k #e1e8ed ball light
l #f5f8fa ball highlight

[grid]
........................
.....##........###......
....#ig#.....##khj##....
....#igg#...#lllkkjh#...
....#i#gd#.#jljlhkehb#..
...##i##d#.#lllkkkjhe#..
..#gii#.#.#khkhkhjehbe#.
..#ggd#...#jkkkjjjheee#.
...#d#....#jejejehbebe#.
....#.....##jjhhheeee#..
.........#i#bhbebebeb#..
........#fig#eeeeeee#...
........#fcgg##ebe##....
.......#ffcadd####......
......#ffcaaa#..........
.....#ffcaa##...........
....#ffcaa#.............
....#fcaa#..............
...#fcaa#...............
..#fca##................
..#ca#..................
...##...................
........................
........................
```

**Decisions at 24:**

- **The same design, with the extra room spent on the grille.** The ball is x 10–22 on rows 1–12, with a checker mesh on rows 4, 6, 8 and 10.
- **The note** fills the corner at x 2–9 on rows 1–8.
- **The collar** runs diagonally from (10, 10) to (13, 13).
- **The rule still holds:** the handle's middle stripe `c` runs x 10 on rows 12–13, then x 9, 8, 7, 6, 5, 4, 3 on rows 14–20, exactly one column per row.

```text
old/mic-16-old.sprite (16px): ok  inner 0%  colours 12  span 16x16  mirror x+x'=16 (65 off)
   essence: a handheld mic: a round silver grille head on a dark handle
set:16:1f3a4 (16px): ok  inner 3%  colours 12  span 16x16  mirror x+x'=15 (45 off)
   warn  26 single-pixel tone specks: noisy or dithered. Merge them into clean areas
set:24:1f3a4 (24px): ok  inner 4%  colours 13  span 21x21  mirror x+x'=24 (88 off)
   warn  44 single-pixel tone specks: noisy or dithered. Merge them into clean areas
```

Notice that **lint passed the curved one**. On the approved art, the speck warnings are the grille dots and the mesh. Isolated single pixels are noise unless they're the point, and on a grille they're the point.

**Take away:**

- A diagonal is straight only if every edge and every internal boundary steps at the same rate.
- Taper at the outline, never inside.
- If a style won't read, change the style. Kirupa expects you to explore.

## 6. Skull and crossbones (2620): symmetry and where the light comes from

The 16's brief:

> 2620 skull and crossbones -- essence: a small skull with two bones crossed behind it, knobs at the corners; keep: four round bone ends, the skull's own outline where bone tucks behind; drop: the hidden shafts

**What Kirupa said:**

- On symmetry in general: "Also, keep symmetry in mind."
- On my 24: "make the skull and cross bones 24x24 one be more symmetrical. Right now, the skull is very lopsided compared to the bones."

### 16px

```text
name: skull and crossbones (2620)
size: 16

[palette]
a #39424c socket far wall
b #8696a4 deepest bone shade
c #b3c1cc bone shade
d #e1e8ed bone base
e #ffffff bone light, upper left

[grid]
..##........##..
.#ee#......#ed#.
#edd#......#ddc#
.##dd######dc##.
...##eedddc##...
...#eedddddc#...
...#eddddddc#...
...#d##dd##c#...
...#d#add#ac#...
...#ddd##dcc#...
...#ddddddcc#...
...##ddddcc##...
.##d#d#dd#c#c##.
#ddc#d#dd#c#ccb#
.#dc########cb#.
..##........##..
```

**Decisions at 16:**

- **The bones are only their ends.** The shafts would hide behind the skull anyway, so I dropped them. Four knobs stick out at the corners, and each one tucks into the skull's outline. The silhouette mirrors exactly (axis 15, 0 off).
- **Lit from the upper left, like everything solid.**
  - White `e` covers the cranium's upper left, at (5, 4), (6, 4), (4, 5), (5, 5) and (4, 6).
  - Shade `c` runs down the right side at x 10–11.
  - Every knob is lit on its own upper left, and the lower-right knob is the darkest.
- **The sockets are holes, and holes light in reverse.** Each socket is three ink pixels and one dark slate pixel: ink at (5, 7), (6, 7) and (5, 8), with `a` at (6, 8).
  - Inside a hole, the wall that faces the light is the far, lower-right one, so that's where the one lighter pixel goes.
  - The right socket is the same shape translated, not mirrored: ink at (9, 7), (10, 7) and (9, 8), with `a` at (10, 8). Both catch the light from the same side.
- **The nose and teeth are ink, too.**
  - The nose is ink at x 7–8 on row 9.
  - The teeth are light pixels separated by ink on rows 12–13: bone at x 5, x 7–8 and x 10, with ink between them.
  - The jaw closes with ink on row 14, x 4–11.

### 24px

```text
name: skull and crossbones (2620)
size: 24

[palette]
a #8696a4 knob undersides
b #aab8c2 bone shade
c #b3c1cc skull side shade and teeth
d #ccd6dd lit knob tops
e #e1e8ed skull base
f #ffffff top light band

[grid]
....###..........###....
...#ddd#........#ddd#...
...#bbb#........#bbb#...
.##dbba#........#abbd##.
#ddbbb#.########.#bbbdd#
#bbbabd#ffffffff#dbabbb#
#aaa#a#feeeeeeeef#a#aaa#
.###.#feeeeeeeeeef#.###.
....#eeeeeeeeeeeeee#....
....#eee##eeee##eee#....
....#ee####ee####ee#....
....#ee####ee####ee#....
....#eee##eeee##eee#....
....#ceeeee##eeeeec#....
.....#ceeee##eeeec#.....
......#ceeeeeeeec#......
.###.#d#eeeeeeee#d#.###.
#ddd#db#eeeeeeee#bd#ddd#
#bbbdba#cc#cc#cc#abdbbb#
#aabbb#.##.##.##.#bbbaa#
.##abbd#........#dbba##.
...#bbb#........#bbb#...
...#aaa#........#aaa#...
....###..........###....
```

**What went wrong first:** the old 24 was shaded procedurally, lit from the left with six or seven tones, and its sockets merged into one black band. The light on one side made the skull look lopsided against bones that were perfectly symmetric. That's the drawing Kirupa called lopsided.

**Decisions at 24:** I tried several variants and chose E, lit from the top.

- **A top light band, mirrored.** White `f` runs across row 5 at x 8–15 and wraps down at (7, 6), (16, 6), (6, 7) and (17, 7).
- **Mirrored shade.** Shade `c` runs down the lower sides, at (5, 13), (6, 14) and (7, 15), and their mirror images. The skull is now symmetric in colour as well as shape.
- **The sockets** are 4×4 with their corners off, at x 7–10 and x 13–16 on rows 9–12.
- **The nose** is 2×2, at x 11–12 on rows 13–14.
- **The teeth and jaw:** teeth on row 18, then a scalloped jaw on row 19, with gaps at x 7, 10, 13 and 16.
- **The bones are lit from the top too:** the knob tops `d`, the bone `b` and the knob undersides `a`.

This is a deliberate exception to upper-left light. When a symmetric emblem must look symmetric, and the shading is big enough to see, light it from the top. At 16 the upper-left light is small enough that the skull still reads as level.

```text
set:16:2620 (16px): ok  inner 12%  colours 6  span 16x16  mirror x+x'=15 (0 off)
   warn  12% inner black (approved 16px icons stay under 12%): name the reason for every inner ink pixel or repaint it with the part's darkest tone
   warn  8 inner black pixels sit right inside the outline (x,y): (4,4), (11,4), (4,11), (11,11), (4,13), (6,13) ... -- a doubled outline or a black seam? Use the material's dark tone instead
set:24:2620 (24px): ok  inner 9%  colours 7  span 24x24  mirror x+x'=23 (0 off)
```

At 16 the warnings are the sockets, nose and teeth: 12% inner ink is high, but it's all holes, which is what ink inside a silhouette is for. The inner pixels beside the outline are where the bones tuck under the skull, and where the teeth meet the jaw line.

**Take away:**

- Holes are ink, and inside a hole the lit wall is the far one.
- Copy lit shapes by translation, not mirroring.
- Symmetric subjects need symmetric light once the shading is large.

## 7. Flying saucer (1f6f8) and floating saucer (e6f8): reimagining, and light that stays flat

The module's brief for 1f6f8:

> 1f6f8 flying saucer -- essence: a flying saucer beaming down a cone of yellow light; keep: a level side profile, a blue dome lit at the upper left, a grey lens hull lit on top with a band of white rim lights, a beam that steps wider with a checker under the hull and a row of dots; drop: Twemoji's tilt and the beam's gradient

**What Kirupa said:**

- "Remember to reimagine them as needed if the emoji version doesn't make sense. For example, for alien spaceship or plants…"
- "As an add-on. The beveled look only makes sense if the underlying shape is 3d. For example, the beam from the UFO is not and shouldn't be beveled."
- Showing me reference saucers from a pixel pack: "For UFO, if you are showing the beam, go with a more side-profile version similar to the one in the bottom row. Provide an additional UFO that looks like the one in the top row that is just floating without a beam."

So one emoji became two drawings. e6f8 is a private-use code that kirupa.com added for the floating saucer; it isn't a Twemoji.

**What went wrong first:**

- Twemoji's saucer is tilted, with a yellow beam that read as a lamp or a pedestal at pixel size.
- My first redraw ringed the hull with bands of tone, and it read as a striped lampshade.
- I also gave the beam the same bevel as the hull, and Kirupa stopped me.

### 1f6f8 at 16px

```text
name: flying saucer (1f6f8)
size: 16

[palette]
a #4b5761 underside, darkest
b #67757f underside
c #3b88c3 dome shade
d #5dadec dome
e #9aaab4 hull shade and the band between the lights
f #ffac33 beam dashes
g #8ccaf7 dome light
h #ccd6dd hull
i #ffd983 beam
j #e1e8ed hull light
k #e3f4ff dome glint
l #f5f8fa hull highlight
m #f2fbff rim lights

[grid]
......####......
.....#kgdd#.....
...##gddddc##...
.##ljjjhhhhee##.
#emememeemememe#
.##bbbbbbbbbb##.
...##aaaaaa##...
....#ifiifi#....
....#fiffif#....
...#iiiiiiii#...
...#fifiifif#...
...#iiiiiiii#...
..#iiiiiiiiii#..
..#iiiiiiiiii#..
..#iiiiiiiiii#..
...##########...
```

**Decisions at 16:**

- **A level side profile.** A saucer seen side-on is the widest silhouette that fits, and it can't be mistaken for anything else.
- **The solid parts take the light.**
  - The glass dome (rows 0–2) is a blue ramp lit at the upper left.
  - The hull on row 3 reads `l jjj hhhh ee`, from highlight to shade, left to right.
  - The underside is darker, in two steps: `b` on row 5 and `a` on row 6.
- **The rim lights are a rhythm.** Single `m` pixels sit at x 2, 4, 6, 9, 11 and 13 on row 4, mirrored about the centre seam, with hull shade between them.
- **The beam is flat.** It's a separate shape, so it has its own outline. It widens in three steps: x 5–10 on rows 7–8, x 4–11 on rows 9–11, then x 3–12 on rows 12–14, with ink on row 15. Inside are two flat yellows only:
  - a checker of `f` dashes under the hull;
  - a row of `f` dots on row 10.

  No light, no bevel: the beam is light itself. The 24px module puts it in one line: "Emitted light (beam, rim lamps) stays flat; the hull and dome take the light."

### 1f6f8 at 24px

```text
name: flying saucer (1f6f8)
size: 24

[palette]
a #4b5761 underside, darkest
b #67757f underside
c #3b88c3 dome shade
d #5dadec dome
e #9aaab4 hull shade and the band between the lights
f #ffac33 beam dashes
g #8ccaf7 dome light
h #ccd6dd hull
i #ffd983 beam
j #e1e8ed hull light
k #e3f4ff dome glint
l #f5f8fa hull highlight
m #f2fbff rim lights

[grid]
.........######.........
........#kkgddd#........
.......#kggddddc#.......
....###ggdddddddc###....
..##lljjjjjjhhhhhhee##..
.#jjhhhhhhhhhhhhhhheee#.
#eemmeemmeemmeemmeemmee#
.#bbbbbbbbbbbbbbbbbbbb#.
..###aaaaaaaaaaaaaa###..
.....###aaaaaaaa###.....
.......#ifififif#.......
.......#fifififi#.......
......##iiiiiiii##......
.....#iiiiiiiiiiii#.....
.....#iiiiiiiiiiii#.....
.....#ifiifiifiifi#.....
.....#iiiiiiiiiiii#.....
....##iiiiiiiiiiii##....
...#iiiiiiiiiiiiiiii#...
...#iiiiiiiiiiiiiiii#...
...#iiiiiiiiiiiiiiii#...
...#iiiiiiiiiiiiiiii#...
...#iiiiiiiiiiiiiiii#...
....################....
```

**Decisions at 24:** the same drawing, with the same thirteen colours.

- **Bigger parts:** the dome is rows 0–3 and the hull rows 4–5.
- **Rim lights in pairs:** x 3–4, 7–8, 11–12, 15–16 and 19–20 on row 6.
- **The beam:** 8, then 12, then 16 pixels wide on rows 10–22, with dots on row 15 at x 7, 10, 13 and 16.

One flaw to avoid copying: the checker at the top of the beam is mirror-symmetric in shape but not in colour. Make yours symmetric.

### e6f8, the floating saucer

The module's brief:

> e6f8 floating flying saucer -- essence: the flying saucer hovering with no beam; keep: a front-on level saucer, a tall blue glass dome lit at the upper left, amber lamps where the dome meets the hull, a grey lens hull with two white portholes and a dark underside; drop: the beam

```text
name: floating flying saucer (e6f8)
size: 16

[palette]
a #4b5761 underside, darkest
b #67757f hull band
c #3b88c3 dome shade
d #5dadec dome
e #9aaab4 hull shade
f #8ccaf7 dome light
g #ffcc4d amber lamps
h #ccd6dd hull
i #e1e8ed hull light
j #e3f4ff dome glint
k #f2fbff portholes

[grid]
................
................
................
......####......
.....#jjff#.....
....#jjfffd#....
.###jfffdddc###.
#iih#fdddcc#hhe#
#eeeg######geeb#
.#bbbkbbbbkbbb#.
..##aaaaaaaa##..
....########....
................
................
................
................
```

**Decisions at 16:**

- **Fill the long side.** The saucer is 16 wide and only 9 tall (rows 3–11), centred on the canvas. A saucer is flat; "fill the canvas" means the long side, and lint measures it that way.
- **The dome** (rows 3–7) is the same blue ramp as 1f6f8, so the two read as one family.
- **A line of ink** at x 5–10 on row 8 separates the dome from the hull. It's an important inner shape, so it gets ink, not tone.
- **Two amber lamps** at (4, 8) and (11, 8) mark where the dome meets the hull. They're emitted light, so they're one flat colour.
- **The hull** is lit from the left (`i`, `h`) and shaded on the right (`e`, `b`). Two white portholes (`k`) sit at (5, 9) and (10, 9), and the underside `a` is at x 4–11 on row 10.

```text
name: floating flying saucer (e6f8)
size: 24

[palette]
a #4b5761 underside, darkest
b #67757f hull band
c #3b88c3 dome shade
d #5dadec dome
e #9aaab4 hull shade
f #8ccaf7 dome light
g #ffcc4d amber lamps
h #ccd6dd hull
i #e1e8ed hull light
j #e3f4ff dome glint
k #f5f8fa hull highlight
l #f2fbff portholes

[grid]
........................
........................
........................
........................
........................
........................
.........######.........
.......##jjjffd##.......
......#jjjjffffdd#......
.....#jjjffffffddc#.....
.####jjffffffffdddc####.
#kkii#ffffffffdddc#hhee#
#iihhg############ghhee#
#eeeelleeeelleeeelleeeb#
.##bbbbbbbbbbbbbbbbbb##.
...####aaaaaaaaaa####...
.......##########.......
........................
........................
........................
........................
........................
........................
........................
```

**Decisions at 24:** the saucer is 24×11, on rows 6–16.

- **Amber lamps** at (5, 12) and (18, 12), either side of the ink line at x 6–17.
- **Three portholes** (`l`) in pairs at x 5–6, 11–12 and 17–18 on row 13.
- **The underside** is a band of `b` on row 14 and `a` at x 7–16 on row 15.

```text
set:16:1f6f8 (16px): ok  inner 1%  colours 14  span 16x16  mirror x+x'=15 (0 off)
   warn  26 single-pixel tone specks: noisy or dithered. Merge them into clean areas
set:24:1f6f8 (24px): ok  inner 2%  colours 14  span 24x24  mirror x+x'=23 (0 off)
set:16:e6f8 (16px): ok  inner 8%  colours 12  span 16x9  mirror x+x'=15 (0 off)
set:24:e6f8 (24px): ok  inner 8%  colours 13  span 24x11  mirror x+x'=23 (0 off)
```

The 16px speck warning lists the rim lights and the beam's dots: deliberate single pixels.

**Take away:**

- Choose the view that makes the silhouette unmistakable, even when the emoji chose another.
- Light belongs to solid things. Light sources, beams, lamps and glows stay flat.
- A flat subject fills the long side and leaves the short side short.

## 8. Radioactive (2622): a symbol, and the face nobody asked for

The module's brief:

> 2622 radioactive -- essence: radiation trefoil; keep: three 60-degree blades, separate hub; drop: round hub (square at 16px)

**What went wrong first:** this one wasn't Kirupa's catch. A reviewer checking my draft wrote: "at 1x the rounded blobs + center dot read as a FACE (two eyes, nose, mouth)". Two round blobs over a third, with a dot between them, is a face to every human eye. The fix was in the shapes:

- wedge blades with straight sides, which widen outward;
- a hub that stands apart from the blades;
- a one-pixel gap all round the hub.

### 16px

```text
name: radioactive (2622)
size: 16

[palette]
a #f4900c disc
b #ffffff trefoil

[grid]
......#####.....
....##aaaaa##...
...#aaaaaaaaa#..
..#abbaaaaabba#.
..#abbbaaabbba#.
.#abbbbaaabbbba#
.#abbbabbbabbba#
.#abbbabbbabbba#
.#aaaaabbbaaaaa#
.#aaaaaaaaaaaaa#
..#aaaabbbaaaa#.
..#aaabbbbbaaa#.
...#aabbbbbaa#..
....##aaaaa##...
......#####.....
................
```

**Decisions at 16:**

- **Three colours: ink, orange and white.** A symbol is print, so it's flat. No light, no shading.
- **The disc is 15×15,** columns 1–15 on rows 0–14, with axis 16 and a one-pixel centre column.
- **The upper blades are wedges.** The left one widens from 2px on row 3 to 4px on row 5; it covers row 3 at x 4–5, row 4 at x 4–6, row 5 at x 3–6, and rows 6–7 at x 3–5. The right blade mirrors it.
- **The hub is a 3×3 square** at x 7–9 on rows 6–8. A round hub needs more pixels than 16 has, so the module says "square at 16px". Orange surrounds it on every side: at x 6 and x 10, on row 5 above and on row 9 below.
- **The bottom blade** is x 7–9 on row 10 and x 6–10 on rows 11–12.

### 24px

```text
name: radioactive (2622)
size: 24

[palette]
a #f4900c disc
b #ffffff trefoil

[grid]
........................
........########........
......##aaaaaaaa##......
.....#aaaaaaaaaaaa#.....
....#aaaaaaaaaaaaaa#....
...#aabbaaaaaaaabbaa#...
..#aabbbbaaaaaabbbbaa#..
..#abbbbbaaaaaabbbbba#..
.#aabbbbbbaaaabbbbbbaa#.
.#abbbbbbbaaaabbbbbbba#.
.#abbbbbbaabbaabbbbbba#.
.#abbbbbbabbbbabbbbbba#.
.#aaaaaaaabbbbaaaaaaaa#.
.#aaaaaaaaabbaaaaaaaaa#.
.#aaaaaaaaaaaaaaaaaaaa#.
.#aaaaaaaabbbbaaaaaaaa#.
..#aaaaaabbbbbbaaaaaa#..
..#aaaaaabbbbbbaaaaaa#..
...#aaaabbbbbbbbaaaa#...
....#aaabbbbbbbbaaa#....
.....#aaabbbbbbaaa#.....
......##aaaaaaaa##......
........########........
........................
```

**Decisions at 24:** the disc covers rows 1–22.

- **The upper blades** run rows 5–11.
- **The hub** is round now: x 10–13 on rows 10–13, with the corners off.
- **The bottom blade** is rows 15–20, with the gap on row 14.

```text
set:16:2622 (16px): ok  inner 0%  colours 3  span 15x15  mirror x+x'=16 (0 off)
set:24:2622 (24px): ok  inner 0%  colours 3  span 22x22  mirror x+x'=23 (0 off)
```

**Take away:**

- Do the pareidolia check at 1x on every drawing: does anything read as a face? Two dots over a line or a blob will.
- Fix an accidental face by changing the shapes and the gaps, not the colours.
- Symbols and print stay flat.

## 9. Flag: United States (1f1fa-1f1f8): stripes and stars by count

```text
essence: the flag of the United States
keep: a navy canton with a regular field of stars, red and white stripes starting and ending red
drop: the true counts (13 stripes, 50 stars), which the grid can't hold
view: a flat card with clipped corners
```

**What Kirupa said:** "The country flags are really bad as well. Fix them."

**What went wrong first:** my first flags were a majority vote of the Twemoji artwork, one colour per cell. Stars vanished and emblems became mush.

The 24px flag module now says what replaced that: "Fields start from a majority vote of the Twemoji artwork, one colour per cell and no blends, then are cleaned up by hand". Its rules:

- "flags are printed cloth, not solid forms, so the field is flat (no light) and has no ink inside the card";
- "stripes split the rows and columns evenly and mirror wherever the real flag does";
- "stars, crescents, discs, the Union Jack and coats of arms are redrawn as a few clean pixel shapes in the flag's own colours";
- "shared charges, such as the Union Jack canton and the star stamps, are identical wherever they appear."

### 16px

```text
name: flag: United States (1f1fa-1f1f8)
size: 16

[palette]
a #3c3b6e navy canton
b #b22334 red stripes
c #eeeeee white stripes and stars

[grid]
................
................
.##############.
##aaaaaabbbbbb##
#acacacabbbbbbb#
#aacacaaccccccc#
#acacacabbbbbbb#
#aaaaaaaccccccc#
#bbbbbbbbbbbbbb#
#cccccccccccccc#
#bbbbbbbbbbbbbb#
#cccccccccccccc#
##bbbbbbbbbbbb##
.##############.
................
................
```

**Decisions at 16:**

- **One card for every flag.** It's 16×12 on rows 2–13, a 14×10 field inside the outline. The corner pixels are clipped: the field's own corner cells are ink, and the card's corners are transparent.
- **Stars by pattern, not by count.**
  - The canton is x 1–7 on rows 3–7.
  - It holds 8 stars in a 3-2-3 checker: x 2, 4 and 6 on row 4; x 3 and 5 on row 5; x 2, 4 and 6 on row 6.
  - The module calls it a "checker of star dots". A regular pattern of the wrong count reads as the US flag. An irregular one of the right count reads as noise.
- **Stripes by rows.**
  - Ten field rows can't hold 13 stripes. They can hold 9 bands that start and end red, if one band is doubled.
  - The doubled band is the top red (rows 3–4), mostly behind the canton.
  - Then the bands alternate one row each, down to red on row 12.
  - Other flags reuse the trick: Liberia's "eleven stripes become ten, doubling the top red as on the gold US flag."

### 24px

```text
name: flag: United States (1f1fa-1f1f8)
size: 24

[palette]
a #3c3b6e navy canton
b #b22334 red stripes
c #eeeeee white stripes and stars

[grid]
........................
........................
........................
.######################.
##aaaaaaaaaabbbbbbbbbb##
#acacacacacabbbbbbbbbbb#
#aacacacacaaccccccccccc#
#acacacacacabbbbbbbbbbb#
#aacacacacaaccccccccccc#
#acacacacacabbbbbbbbbbb#
#aacacacacaaccccccccccc#
#aaaaaaaaaaabbbbbbbbbbb#
#cccccccccccccccccccccc#
#bbbbbbbbbbbbbbbbbbbbbb#
#cccccccccccccccccccccc#
#bbbbbbbbbbbbbbbbbbbbbb#
#cccccccccccccccccccccc#
#bbbbbbbbbbbbbbbbbbbbbb#
#cccccccccccccccccccccc#
##bbbbbbbbbbbbbbbbbbbb##
.######################.
........................
........................
........................
```

**Decisions at 24:** the same card at 24: "a 22x16 field inside a 1px black outline with clipped corners (rows 3-20)".

- **The canton** is x 1–11 on rows 4–11.
- **27 stars:** 5 on rows 5, 7 and 9, and 4 on rows 6, 8 and 10.
- **15 bands,** with the top red doubled on rows 4–5.

```text
set:16:1f1fa-1f1f8 (16px): ok  inner 2%  colours 4  span 16x12  mirror x+x'=15 (0 off)
set:24:1f1fa-1f1f8 (24px): ok  inner 1%  colours 4  span 24x18  mirror x+x'=23 (0 off)
```

The 1–2% inner ink is the four clipped corner cells of the field, nothing else.

**Take away:**

- Count what the grid can hold, keep the pattern regular, and start and end on the right colour.
- Flags are flat cloth: no light, and no ink inside the card.
- See `construction.md`, section 10, for the general flag method.

## 10. Paw prints (1f43e): one big flat mark

```text
essence: an animal's paw print
keep: four toes round a big pad, mirror-symmetric
drop: Twemoji's second print
view: flat, from above
```

The 24px module's docstring explains the change: "one big, mirror-symmetric print (four toes and a lobed pad) instead of two small ones, which can't be read at 24px. A print is a flat mark, so it takes no light."

**What Kirupa said:** "the paw prints, you can't even tell they are paw prints."

### 16px

```text
name: paw prints (1f43e)
size: 16

[palette]
a #6b2716 print
b #93412a light pixels at each part's upper left

[grid]
....##....##....
...#ba#..#ba#...
...#aa#..#aa#...
...#aa#..#aa#...
.##.##....##.##.
#ba#........#ba#
#aa#........#aa#
#aa#..####..#aa#
.##..#bbba#..##.
....#bbaaaa#....
...#baaaaaaa#...
...#aaaaaaaa#...
...#aaaaaaaa#...
....#aaaaaa#....
.....######.....
................
```

**Decisions at 16:**

- **One print, not two.** Twemoji shows two small prints. At 16 each would be a cluster of 1px dots, and the result is noise.
- **Every part is outlined on its own.** The toes and the pad are separate shapes with ink round each, so they never merge:
  - two main toes, 2×3, at x 4–5 and x 10–11 on rows 1–3;
  - two side toes, at x 1–2 and x 13–14 on rows 5–7;
  - the pad on rows 8–13.
- **The silhouette mirrors** about axis 15.
- **One flaw to avoid copying.** The 16 is two-tone: each toe has one lighter pixel at its upper left, and the pad has a short diagonal of them, copied by translation. That's light on a flat mark, and the module's comment is stale. Follow the 24 for new work.

### 24px

```text
name: paw prints (1f43e)
size: 24

[palette]
a #8c3b22 print, flat

[grid]
........................
.......##......##.......
......#aa#....#aa#......
.....#aaaa#..#aaaa#.....
.....#aaaa#..#aaaa#.....
.....#aaaa#..#aaaa#.....
..##.#aaaa#..#aaaa#.##..
.#aa#.#aa#....#aa#.#aa#.
#aaaa#.##......##.#aaaa#
#aaaa#............#aaaa#
#aaaa#...######...#aaaa#
.#aa#..##aaaaaa##..#aa#.
..##..#aaaaaaaaaa#..##..
.....#aaaaaaaaaaaa#.....
....#aaaaaaaaaaaaaa#....
...#aaaaaaaaaaaaaaaa#...
...#aaaaaaaaaaaaaaaa#...
...#aaaaaaaaaaaaaaaa#...
...#aaaaaaaaaaaaaaaa#...
...#aaaaaaaaaaaaaaaa#...
....#aaaaaaaaaaaaaa#....
.....#aaaaa##aaaaa#.....
......#####..#####......
........................
```

**Decisions at 24:**

- **One flat colour.** A print takes no light.
- **The toes:** the main toes are 4×6 ovals at x 6–9 and x 14–17 on rows 2–7, and the side toes are 4×5 at x 1–4 and x 19–22 on rows 7–11.
- **The pad** is x 4–19 on rows 11–21, with a notch at the bottom centre: ink at (11, 21) and (12, 21), and transparency at (11, 22) and (12, 22). The notch gives the pad its lobes.

```text
set:16:1f43e (16px): ok  inner 0%  colours 3  span 16x15  mirror x+x'=15 (0 off)
set:24:1f43e (24px): ok  inner 0%  colours 2  span 24x22  mirror x+x'=23 (0 off)
```

**Take away:**

- When the emoji shows two small copies, draw one big one.
- Outline separate parts separately.
- Marks, prints, stamps and silhouettes are flat.

## 11. Faces and people: where to look

These have their own long walk-throughs in `faces.md`:

- **Rolling on the floor laughing (1f923),** `faces.md` sections 4 and 7.
  - It shows a tilted head, eyes squeezed into L shapes, and tears that fly outward.
  - Kirupa, on my first version: "the tear drops should be going outward like in the original source version. The shouldn't be going straight down. It looks like an earring right now."
- **Person (1f9d1),** `faces.md` section 10. It covers the head template, hair as a cap with its own ink, the skin ramp and 1×2 eyes.
- **Portraits of a real person from a photo,** `faces.md` sections 13 and 14.

## 12. The patterns in one table

| When you see this | Example | Do this |
| --- | --- | --- |
| The emoji is drawn in 3D or tilted | 2615, 1f6f8 | Pick the view with the clearest silhouette (side, front or plan); show depth with bands of tone |
| The subject is about a material, such as crust and crumb | 1f35e | Three-quarter view; one ramp per material; tone, not ink, between materials |
| The subject is round | 1f34a | Draw a true circle from the tables; accessories go outside it; measure the body |
| The subject is long and thin | 1f3a4 | Lay it on the 45° diagonal; every edge and stripe steps 1:1; taper only at the outline |
| The subject is symmetric | 2620, 2622, 1f43e | Mirror the silhouette; copy lit details by translation; light from the top if one-sided light looks lopsided |
| A hole or socket | 2615, 2620 | Under 3px it's ink. Inside a bigger hole, the lit wall is the far one |
| Light sources: beams, lamps, glows | 1f6f8, e6f8 | Flat colours, no bevel; only solid parts take light |
| Symbols, print and flags | 2622, 1f1fa-1f1f8 | Flat; regular patterns; check for accidental faces at 1x |
| The emoji repeats a small thing | 1f43e | Draw one big one |
| Steam, rays, sparkles | 2615 | Flat effects. Unoutlined mid-tone at 16; outlined at 24 when there's room |
| Lint passes but it looks wrong | 1f34a, 1f3a4 | Trust your eyes. Lint can't see squished, curved or a face that shouldn't be there |

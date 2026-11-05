# Construction: grid, line, colour and light

This is the craft under every drawing: how I place the outline, step a curve, decide when black belongs inside, build a ramp and light a form. Grids marked **approved** are copied from kirupa.com's published set; print any of them with `python3 scripts/sprite_tool.py text set:16:CODE`. Grids marked **wrong** show mistakes I made, so you can recognise them.

Contents:

1. The canvas and its coordinates
2. The outline
3. Curves and circle tables
4. Diagonals and long thin things
5. Black inside the silhouette
6. Colour: budgets, ramps and value
7. Light on solid forms
8. Flat things, glows and fire
9. Small features, text and tiles
10. Flags
11. Groups, figures and composition

## 1. The canvas and its coordinates

- Coordinates are `(x, y)`: x is the column counted from 0 at the left, y is the row counted from 0 at the top. Lint prints positions the same way.
- A 16px sprite has columns and rows 0–15; a 24px sprite has 0–23. The canvas edge counts as transparency, so a coloured pixel on row 0 or column 15 needs ink beyond it, which can't exist. Keep colour off the edge rows and columns; only `#` may sit there.
- **Fill the canvas.** The long side, outline included, should span 14–16px at 16 and 20–23px at 24. `check` errors under 13px (16) and 17px (24), and warns under 14px and 20px. The only waiver is a subject that is small by meaning: a `scale: small` header line, or "small … square" or "small … diamond" in the name. Kirupa's set grades its small squares and diamonds by size on purpose.
- **Mirror axes.** A symmetric subject mirrors pixel `x` onto `x' = axis − x`:

  | Subject | Columns | Axis | Centre |
  | --- | --- | --- | --- |
  | 16px smiley or person head (15px wide) | 1–15 | 16 | one column, x 8 |
  | 16px card, tile or 16-wide body | 0–15 | 15 | two columns, x 7 and 8 |
  | 16px 13px head (`smiley-head13-16`) | 2–14 | 16 | one column, x 8 |
  | 24px smiley or person head (22px wide) | 1–22 | 23 | two columns, x 11 and 12 |
  | 24px card or 24-wide body | 0–23 | 23 | two columns |

  An odd width gives a one-pixel centre column, for a nose, a tie or a candle wick. An even width gives a two-pixel centre seam. Choose before drawing; a subject that needs a centre pixel can't be centred on an even width. `check` reports the best axis it finds (`mirror x+x'=16 (0 off)`), and lists the pixels that break it when only a few do.

## 2. The outline

**Ink is `#`, pure #000000, one pixel thick, round the whole silhouette.** Every opaque pixel that touches transparency on a side (left, right, up or down) is ink. Pixels that touch the background only at a corner don't need ink, and shouldn't get any.

Right: corners touch diagonally, and every ink pixel has exactly two ink neighbours along the line.

```text
..####..
.#oooo#.
#oooooo#
#oooooo#
.#oooo#.
..####..
```

Wrong: doubled corners. The extra pixel at each corner touches only ink. It thickens the line and squares off the curve.

```text
.######.
##oooo##
#oooooo#
#oooooo#
##oooo##
.######.
```

Wrong: a hug, a black seam just inside the outline. It reads as a heavy double border. That edge belongs to the material's darkest tone:

```text
......#####.....
....##SSSSs##...
...##Sssssss##..
..##Wssssssss##.
```

Lint stops the hug at 16px:

```text
ERROR 22 inner black pixels sit right inside the outline (x,y): (4,2), (12,2), (3,3), (13,3), (3,4), (13,4) ... -- a doubled outline. The outline is one pixel thick; repaint the inner ring with the material's dark tone
```

Wrong: no outline. Without ink, a yellow face dissolves on a white page:

```text
ERROR 29 light pixels touch transparency or the canvas edge (x,y): (6,1), (7,1), (8,1), (9,1), (10,1), (4,2) ... -- the silhouette needs its 1px '#' outline
```

### Separate pieces get their own outline

Kirupa: "when the shape has individual pieces (like this falling rock), each individual shape should have a black outline as well. The black outlines aren't optional." Rocks, toes, bones, drops, tears, a leaf beside a fruit, the note beside a microphone: each is a closed ink shape.

- **Where two pieces touch, they share one ink line.** Never put two ink lines side by side.
- **Where they don't touch, leave at least one background pixel between them.** The approved 16px paw keeps a gap between every toe (row 4: `.##.##....##.##.`), so each toe reads as its own pad.
- **At 24px, every important piece gets ink,** including pieces inside the silhouette: the dome of a saucer against its hull, a mug's handle, each eye.
- **At 16px, pieces inside the silhouette are usually split by tone,** because a 1px ink line costs a sixteenth of the canvas. See section 5.

### The two 16px exceptions

Both produce warnings, so you confirm each one was deliberate:

- **Thin effect lines.** A 1px line in a mid tone can float unoutlined when it is clear on both sides: steam, rays, sparkles, motion lines. The approved 16px mug's steam is `c #4b4f5c`, a mid slate that reads on white and on dark:

  ```text
  ......c..c......
  .....c..c.......
  ......c..c......
  ```

  Each wisp is a clean diagonal whose pixels touch only at corners. An L-join (a pixel with neighbours both beside it and above or below it) isn't thin. Lint then treats it as a light pixel against transparency, and errors.

- **Dark edges.** A pixel darker than luminance 70 may be its own edge: a thin dark stem, a leaf tip, a strand of hair, a whisker. The approved tangerine's twig is `a #5b3417` with ink beside it.

At 24px there are no exceptions. Steam, rays, drips, tears and spikes all get ink. The approved 24px mug's steam is two outlined white wisps:

```text
......#.....#...........
.....#j#...#j#..........
.....#j#...#j#..........
......#j#.#j#...........
......#j#.#j#...........
.......#...#............
```

## 3. Curves and circle tables

A curve is a sequence of runs. Walk round a quadrant from the top centre to the side centre, and write down how many pixels each step stays on one row (near the top) or one column (near the side). **The runs must shrink toward the 45° point and grow again after it, and the list must read the same backwards.** The 15px smiley head is 5-2-1-2-5: a 5px flat top, a 2px step, one corner pixel, a 2px step and a 5px flat side.

Wrong: runs of 1-1-1 make a straight 45° edge, so the circle reads as an octagon. A reviewer caught exactly this on a computer disk: "the gold disc reads octagonal."

```text
.....####.....
....#oooo#....
...#oooooo#...
..#oooooooo#..
.#oooooooooo#.
#oooooooooooo#
```

Wrong: a run grows before the 45° point (1, then 2), so the curve bulges and reads as a potato or an onion.

```text
....####....
...#oooo#...
.##oooooo##.
#oooooooooo#
```

Don't invent circles; copy these. Every one is outline-clean under `check`. Fill the `o` area with your base, then light it.

### 16px circles

15px, runs 5-2-1-2-5: the smiley and person head (`smiley-head-16`). It sits on columns 1–15 with axis 16.

```text
.....#####.....
...##ooooo##...
..#ooooooooo#..
.#ooooooooooo#.
.#ooooooooooo#.
#ooooooooooooo#
#ooooooooooooo#
#ooooooooooooo#
#ooooooooooooo#
#ooooooooooooo#
.#ooooooooooo#.
.#ooooooooooo#.
..#ooooooooo#..
...##ooooo##...
.....#####.....
```

14px, runs 4-2-1-2-4: the tangerine's body, a ball, a coin. It sits on columns 1–14, axis 15.

```text
.....####.....
...##oooo##...
..#oooooooo#..
.#oooooooooo#.
.#oooooooooo#.
#oooooooooooo#
#oooooooooooo#
#oooooooooooo#
#oooooooooooo#
.#oooooooooo#.
.#oooooooooo#.
..#oooooooo#..
...##oooo##...
.....####.....
```

13px, runs 5-2-2-5: the head under a hat or halo (`smiley-head13-16`, rows 3–15).

```text
....#####....
..##ooooo##..
.#ooooooooo#.
.#ooooooooo#.
#ooooooooooo#
#ooooooooooo#
#ooooooooooo#
#ooooooooooo#
#ooooooooooo#
.#ooooooooo#.
.#ooooooooo#.
..##ooooo##..
....#####....
```

12px, runs 4-2-2-4: a round part inside a bigger drawing, such as a clock face with feet or a pot belly. On its own it's too small (lint errors under 13px).

```text
....####....
..##oooo##..
.#oooooooo#.
.#oooooooo#.
#oooooooooo#
#oooooooooo#
#oooooooooo#
#oooooooooo#
.#oooooooo#.
.#oooooooo#.
..##oooo##..
....####....
```

### 24px circles

kirupa.com's 24px faces come from a half-width table. Each number is the half-width of one row, from the top row to the middle; the bottom half mirrors it. A row with half-width `h` fills columns `centre − h` to `centre + h − 1`, where `centre` is the left edge plus half the size. The edge pixels become ink.

| Diameter | Half-widths, top row to middle | Runs |
| --- | --- | --- |
| 22 | 4 6 7 8 9 10 10 11 11 11 11 | 8-2-1-1-1-2-8 |
| 20 | 3 5 6 7 8 9 9 10 10 10 | 6-2-1-1-1-2-6 |
| 18 | 3 5 6 7 8 8 9 9 9 | 6-2-1-1-2-6 |
| 16 | 2 4 5 6 7 7 8 8 | 4-2-1-1-2-4 |
| 14 | 2 4 5 6 6 7 7 | 4-2-1-2-4 |

The 22px head (`smiley-head-24`, columns 1–22, axis 23):

```text
.......########.......
.....##oooooooo##.....
....#oooooooooooo#....
...#oooooooooooooo#...
..#oooooooooooooooo#..
.#oooooooooooooooooo#.
.#oooooooooooooooooo#.
#oooooooooooooooooooo#
#oooooooooooooooooooo#
#oooooooooooooooooooo#
#oooooooooooooooooooo#
#oooooooooooooooooooo#
#oooooooooooooooooooo#
#oooooooooooooooooooo#
#oooooooooooooooooooo#
.#oooooooooooooooooo#.
.#oooooooooooooooooo#.
..#oooooooooooooooo#..
...#oooooooooooooo#...
....#oooooooooooo#....
.....##oooooooo##.....
.......########.......
```

The 20px circle, for a body that leaves room for a stem or ears:

```text
.......######.......
.....##oooooo##.....
....#oooooooooo#....
...#oooooooooooo#...
..#oooooooooooooo#..
.#oooooooooooooooo#.
.#oooooooooooooooo#.
#oooooooooooooooooo#
#oooooooooooooooooo#
#oooooooooooooooooo#
#oooooooooooooooooo#
#oooooooooooooooooo#
#oooooooooooooooooo#
.#oooooooooooooooo#.
.#oooooooooooooooo#.
..#oooooooooooooo#..
...#oooooooooooo#...
....#oooooooooo#....
.....##oooooo##.....
.......######.......
```

The approved 24px tangerine uses a fuller 20px circle with runs 8-2-1-1-2-8: longer flats make a plumper fruit. Any monotonic, palindromic profile is fine. Ovals follow the same rules, with longer flats on the long axis.

## 4. Diagonals and long thin things

Right: a 1:1 diagonal touches only at corners.

```text
#.....
.#....
..#...
...#..
```

Wrong: L-joins. Filling the inside of each step doubles the line's weight and makes it jagged.

```text
##....
.##...
..##..
...##.
```

Right: a 2:1 slope uses equal runs.

```text
##......
..##....
....##..
......##
```

Wrong: uneven runs (3-1-2) wobble.

```text
###.....
...#....
....##..
......##
```

Lint can't see a jaggy outline; the zoom board can. Kirupa's standard is "sharper straight lines and minimizing extraneous details."

**Lay long, thin subjects on the 45° diagonal.** A pencil, sword, carrot, rocket, wand or microphone is longer than the canvas is wide, and the diagonal is the longest line in a square. The approved 16px microphone's handle runs from the ball head at the upper right down to the lower left as a 2–3px band with clean steps on both sides:

```text
...#eebac####...
..#eebaa#.......
..#ebaa#........
.#eba##.........
#eba#...........
.#a#............
..#.............
```

The band is lit like a cylinder: light `e` on the upper-left edge, mid `b`, and dark `a` on the lower-right edge. Kirupa said the previous 16px microphone "looks curved": its handle bent like a ladle. Four rounds of variants read as a spoon, a bulb, a cone and a flashlight before this straight, tapered 45° handle under a dotted ball won. Upright, the same parts read as a bulb or an ice-cream cone.

## 5. Black inside the silhouette

At 16px a black line inside the silhouette costs as much as a feature. Kirupa: "notice from darkproject when dark outlines are used inside the visual vs. just being on the outline." Black goes inside **only** for these five reasons:

1. **Holes and openings.** A handle hole, an open mouth, a keyhole, a doorway, a nostril. The approved 16px mug's handle hole is a 1×2 column of ink at x 13, rows 9–10. Lint's `2x2 black block at (12,9)` warning is that hole plus the mug wall beside it, and the drawing is right.
2. **Deep crevices and undersides.** Under a mushroom cap, between two wheels, the shadowed gap under a lid.
3. **Face features.** Eyes, mouth lines, brows, the sockets and nose of a skull.
4. **Overlaps of similar values.** Where two parts are the same colour and only a line can split them: fingers, a book's cover over its pages, white bones behind a white skull. The approved 16px skull keeps its own outline where the bones tuck behind it (rows 3–4 and 12–14) and drops the hidden shafts.
5. **Line art that is the symbol itself.** Clock hands, a card's suit marks, the letters on a sign.

**The test:** point at every black pixel inside the silhouette and name its reason. If you can't, recolour it with the darkest tone of the part it belongs to. If deleting an inner line makes the icon cleaner at 1x, delete it.

Wrong: a mouth drawn as a solid black slab. It's 34% inner black.

```text
.#Sssssssssssst#
.#S##########tu#
.#s##########tu#
..###########u#.
..###########u#.
...###########..
```

```text
ERROR 34% of the drawing is black inside the silhouette: blotchy. Separate parts with tones and keep inner ink for holes, crevices, face features, overlaps of similar values and line-art symbols
```

**Ink vs. muddle at 24px.** At 24px each important piece gets its own ink: the lid, the handle, the wheel, each eye. Small repeated parts still split by their own dark tone, not ink: piano keys, card-file tabs, roof shingles, a tight cluster of petals, a row of buttons. Ink round each one turns the area into black mesh.

**Value does the separating.** Two neighbouring parts must differ in value (lightness), not just hue. Lint warns when different hues of nearly equal value touch in several places (`different colours of nearly equal value touch`). The greyscale panel on the zoom board shows it at a glance.

## 6. Colour: budgets, ramps and value

### Budgets

| | 16px | 24px |
| --- | --- | --- |
| Tones per solid material | 3–4 | 3–5 |
| Total colours, ink included | about 4–10; approved median 7; lint warns above 14 | about 6–16; approved median 8; lint warns above 18 |

Reuse one ramp for every part made of the same material. A brown that appears in the twig and the handle should be the same brown. More tones don't make a better sprite; more value contrast does.

### Hue-shifted ramps

A ramp is three to five tones of one material. Shadows shift hue toward cooler and richer, and highlights toward warmer and paler. Darkening by adding black, or lightening by adding white, makes grey mud.

```bash
python3 scripts/sprite_tool.py ramp "#f58f0c"
```

```text
  #b33b00  luminance  88.2  deep shadow
  #d45e00  luminance 118.6  shadow
  #f58f0c  luminance 158.6  base
  #ffb71e  luminance 187.1  light
  #ffd530  luminance 206.7  highlight
Shadows turn cooler and richer, highlights warmer and paler. Use 3-4 tones at 16px, 3-5 at 24px.
```

Treat the output as a starting point, then adjust by eye. The approved tangerine's peel runs `#a54806` deep shade, `#d4690a` shade, `#f58f0c` base, `#ffae3d` light and `#ffd28c` highlight, with a `#ffffff` glint. Its highlights are paler than the generated ones, so the light area reads as sheen and not as a yellow patch. `ramp --hue H --value V --up N --down N` controls the hue step, the value step and the number of tones. For skin, use a gentle ramp: `ramp '#c68642' --hue 3 --value 0.09 --up 1`.

### Ramps kirupa.com uses

| Material | Tones, dark to light |
| --- | --- |
| Smiley yellow (Darkproject-matched) | `#f08e00` `#ffbf00` `#ffe600` `#ffff93` `#ffffcf` |
| Golden hair (people) | `#8a3a00` `#a04a06` `#e07f16` `#ffb23a` |
| Leaf (24px kit) | `#10362a` `#1e5631` `#2f7a35` `#4f9e3a` `#86c44a` `#c9e86e` |
| Metal (24px kit) | `#1c2330` `#323d4f` `#4f5d73` `#76869c` `#a8b6c8` `#e4ecf5` |
| Ash and bone (24px kit) | `#3b4650` `#66757f` `#99aab5` `#ccd6dd` `#e1e8ed` `#f5f8fa` |
| White ceramic (16px mug) | `#7f8799` `#a7aebd` `#cfd4de` `#eceef3` `#ffffff` |
| Black material (slate) | `#262b30` `#30363c` `#3a4148` `#66717c` |

The 24px kit ramps have six tones because they serve many subjects; one sprite uses three to five of them.

### Black, navy and other dark materials

Anything darker than luminance 40 reads as ink, and lint counts it as ink. A black hat, a black cat or dark hair drawn in black vanishes into its own outline. Draw black materials in **slate**: `#262b30` deep (luminance 42), `#30363c` shade (53), `#3a4148` base (64), `#66717c` light (111). On the person templates these are the four hair keys `k`, `d`, `h` and `H`. The approved 16px top hat's crown is slate, lit from the left:

```text
...##########...
...#egccccba#...
```

There, `e #5d6679` and `g #8792a8` are the lit side, `c #414858` the base, and `b #343a48` and `a #2b303c` the shaded side. Dark hair sits at luminance 55–65 with an ink outline. Navy is a trap: `#00247d` has luminance 35 and reads as ink at 16px, so the approved Union Jack uses `#12328c` (51) and the US flag uses `#3c3b6e` (65). `ramp` flags tones that would read as ink and prints the slate advice for dark bases.

### Keep the subject's colour identity

A red apple stays red, a tangerine stays orange, and a blue car stays blue. Sample Twemoji or the system emoji (`sample IMAGE --box …`) and build ramps round those bases. Kirupa wanted his smileys to "match the yellow tone of the darkproject yellow smilies", and the set's yellow ramp above is that match.

## 7. Light on solid forms

One light, from the upper left, on solid forms only: fruit, balls, pots, bottles, cups, animals, vehicles, buildings, tools, and also leaves, petals and stems. The style notes put it plainly: "leaves, petals and stems are solid forms and keep the shading you've given them."

**Spheres** get a light area and glint at the upper left and a dark crescent at the lower right. Here is the approved 16px tangerine as a tone map (`L` light, `W` glint, `o` base, `S` shade, `t` twig, `f` leaf):

```text
....##....#####.
....#t#..#ffff#.
.....#t##fff##..
....##LLLo##....
...#LLLLLooo#...
..#LLLLLLLooo#..
..#LLWWLLLooo#..
.#LLLWLLLLoooo#.
.#LLLLLLLLoooo#.
.#LLLLLLLooooS#.
.#ooLLLLooooSS#.
..#ooooooooSS#..
..#oooooooSSS#..
...#oooooSSS#...
....##ooSS##....
......####......
```

The light is a broad soft area, not a ring. The shade is a crescent that hugs the lower-right rim. The glint is a few pixels inside the light area, never on the rim.

**Cylinders** (mugs, cans, bottles, trunks, a diagonal handle) get vertical bands. The approved 16px mug's body is the same row repeated: a rim tone, a two-pixel white highlight band near the left, the base, then three darker bands toward the right.

```text
.#giihhhhgfe#
```

The 24px mug spreads the same idea over more pixels: `.#hijjiiihhhhggee#`.

**Boxes** get a light top, a mid face and a dark face. **Thin forms** (leaf blades, petals, ribbons, paper wraps) get a lit half and a shaded half across the midrib or fold. The tangerine's leaf is light `f` on its upper rows and shade `c` below.

**Faces are lit on the rim only.** A light rim at the upper left (`S`), a shade rim at the lower right (`t`, then `u` deepest), one glint (`W`), and a single flat base everywhere else, so the features read. See `faces.md`.

**Symmetry can outrank the light.** Kirupa asked for the 24px skull and crossbones to be "more symmetrical." The approved version is lit from the top and mirrored exactly about axis 23. Use this for icons whose identity is symmetry (a skull, a trophy, a shield); everything else stays upper-left.

Right: light edge at the upper left, dark edge at the lower right.

```text
#######
#hhhhb#
#hbbbd#
#hbbbd#
#bdddd#
#######
```

Wrong: pillow shading. Darkening every edge equally makes a puffy blob with no light direction.

```text
#######
#ddddd#
#dbbbd#
#dbbbd#
#ddddd#
#######
```

Also wrong: concentric bands (rings of tone that follow the outline), dithering (checkerboards of two tones), and single-pixel tone specks. At 16px a 1px tone band hugging the rim beats a gradient. Lint warns when more than 15% of the pixels are lone tone specks.

**Glints.** Glossy things get a white or near-white glint: 1–2px at 16 and a 2–3px cluster at 24. The 16px smiley's glint is one pixel at (4,3); the 24px glint is three pixels at (7,5), (8,5) and (7,6).

## 8. Flat things, glows and fire

Kirupa: "The beveled look only makes sense if the underlying shape is 3d. For example, the beam from the UFO is not and shouldn't be beveled."

**Keep these flat** (one or two tones, no bevel, no rim light): symbols, signs, arrows, letters and numbers, flags, printed marks (labels, icing lines), paper and wrappers, beams and rays, glows and sparkles, sprinkles and 1–2px dots, and screens. The approved flying saucer's beam is a flat pale yellow `i #ffd983` with a few darker `f #ffac33` dashes for motion. It has no light direction.

**Emissive things use colour zones, not light.** A flame is brightest in its core and coolest at its edges. The approved 16px fire has an orange body `b #f4900c`, a yellow core `c #ffcc4d`, a pale heart `d #fff1b8` low in the centre, and a deeper orange `a #d9620b` on the outer lower edge:

```text
#bbbccccccccaaa#
#bbbccdddcccaaa#
#bbbccddddccaaa#
.#bbbccddccbaa#.
..#aaaccccaaa#..
```

Water, gems, glass and screens likewise use flat zones of colour with one hard highlight, not a light ramp.

## 9. Small features, text and tiles

- **The 2px rule.** A part under 2px at 16 (3px at 24) either becomes one highlight pixel or goes. Peel dimples, seeds smaller than a pixel, stitching and fine print go. Write them in `drop:`.
- **Exaggerate what you keep.** Handles, ears, eyes, wheels and the identifying feature get a little bigger than life. The tangerine's leaf is longer than a real leaf, because the leaf is what separates it from an orange ball.
- **Text.** Letters at 16px are 3×5 with 1px strokes, flat white on a flat tile, with no ink of their own; round letters leave their corner pixels out. In the approved 16px "OK" button (`text set:16:1f197`) the `O` covers x 5–7 and the `K` x 9–11, on rows 5–9. At 24px letters grow to 2px strokes, 8 wide and 12 tall, and each gets its own ink outline:

  ```text
  #cbbb####bbbb##bbbb##ba#
  #cbb#dddd#bb#dd#bb#dd#a#
  #cb##dddd##b#dd#b##dd#a#
  #c#dd####dd##dd##dd##ba#
  #c#dd#bb#dd##dd##dd#bba#
  #c#dd#bb#dd##dddd##bbba#
  ```

  Those are the top rows of the approved 24px "OK". Its button also has a 1px light edge `c` on the top and left and a dark edge `a` on the right and bottom, because a button is a raised object.
- **Tiles.** Signs, buttons and squared symbols sit on a flat coloured tile with an ink outline and stepped corners. The approved 16px tile fills rows 0–14 and columns 1–15:

  ```text
  ...###########..
  ..#aaaaaaaaaaa#.
  .#aaaaaaaaaaaaa#
  ```

  The approved 24px tile fills rows 1–22 and columns 1–22:

  ```text
  ....################....
  ..##aaaaaaaaaaaaaaaa##..
  ..#aaaaaaaaaaaaaaaaaa#..
  .#aaaaaaaaaaaaaaaaaaaa#.
  ```

  On the approved restroom tiles (`1f6b9`, both sizes) the white figure is flat and has no ink; the tile's colour is its outline. Simplify the symbol to bold shapes. A reviewer rejected the passport-control sign as "too busy at 1x (the diagonal striped booklet reads as a stripy box)". The fix was "two bold white shapes on the blue tile": an officer's bust beside a plain booklet.

## 10. Flags

Kirupa: "The country flags are really bad as well. Fix them." The fix was a fixed card and flat fields.

- **The card.** At 16px a flag is a 16×12 card on rows 2–13: an ink outline, a 14×10 flat field inside it (rows 3–12, columns 1–14) and clipped corners (the field's first and last rows start and end with `##`). At 24px it's 24×18 on rows 3–20, with a 22×16 field.
- **Flat colour only.** No light, no wave, no gloss and no ink inside the field. The colours are the flag's own, at full strength, with every dark colour above luminance 40.
- **Simplify the emblem to blocks.** Stars become dots in a checker; a disc follows a circle table; crosses become 2px bands, with white edges where the real flag has them; fine emblems (coats of arms, text) become a block of their main colour.
- **Stripes are 1px at 16.** The count needn't match; the pattern must. The 16px US flag has nine bands of red and white and eight star dots on a navy canton:

  ```text
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
  ```

  Japan's flag at 16 is a 6×6 red disc (`aaaa` caps over four `aaaaaa` rows) centred on the white field. The Union Jack's diagonals are 1px, and its red cross is 2px with white edges, on navy `#12328c`.

## 11. Groups, figures and composition

- **One dominant shape.** A 16px icon holds one big readable shape plus one or two secondary features. When a subject is a scene (a family, a sport, a place), choose the one or two figures or objects that say it.
- **Front to back.** Draw the back object first and let the front one overlap it. Ink only where the overlap joins two similar values.
- **Gaps between figures.** Keep at least one background pixel between separate figures or objects, so their outlines don't merge into a blob.
- **Heads in groups.** A reviewer found that families "read as crosses or a churchyard. The plus-shaped 3×3 heads look like crosses at 8×." Adults get 4×4 heads with only the four corners trimmed, so they read as round, and bodies with rounded shoulders. Children get 3×3 or 2×2 solid square heads; a small square reads as a round dot, but a plus reads as a cross.
- **Choose the view that shows the action.** A front-on bow "still reads as a dome or helmet at x1, because a front view of a bow hides everything that says 'bowing'." The fix was a side profile of a kneeling bow. A sport is drawn by its equipment or one figure mid-action, in profile.
- **Reinterpret when the source fails at pixel size.** Kirupa: "Remember to reimagine them as needed if the emoji version doesn't make sense." The flying saucer's beam became a level side profile with a flat beam, and a second, beamless saucer floats front-on.

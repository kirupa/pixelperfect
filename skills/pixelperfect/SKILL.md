---
name: pixelperfect
description: How to hand-draw proper 16x16 and 24x24 pixel-art emoji for any subject (objects, animals, food, plants, smileys and faces, people, a portrait of a real person from a photo, symbols, signs and flags) in the style of kirupa.com's 1,948 hand-drawn Pixel emoji. Use it to draw, redraw, fix, review, grade or critique pixel emoji, icons or sprites at 16px or 24px, and to turn a photo of someone into a pixel emoji of their face. Its scripts/sprite_tool.py starts sprites from face and bust templates, lints them against the house rules, renders zoom, review and blind-test boards beside Twemoji and the system emoji, finds approved reference sprites, samples photo and skin colours, builds hue-shifted ramps, mirrors halves and exports Python rows.
license: MIT (LICENSE.txt); bundled artwork is under assets/LICENSE.md
compatibility: Python 3.9+ with Pillow and numpy. Optional - resvg_py (Twemoji renders), fontTools (Apple joined-emoji glyphs) and internet access (Twemoji SVGs and photo URLs, cached). Works offline with the bundled reference library.
metadata:
  author: Kirupa Chinnathambi (kirupa.com)
  version: "1.0.0"
---

# Pixel emoji: 16×16 and 24×24

I draw the pixel emoji on kirupa.com: 1,948 subjects, each drawn by hand twice, once on a 16×16 grid and once on a 24×24 grid. They're at https://www.kirupa.com/tools/icon_gallery_pixel.htm. People call me a world-famous pixel artist now. I didn't start as one.

My first set was terrible. I shrank Twemoji's vector art onto the grid and called it pixel art. Kirupa looked at it and wrote, "The designs look comically bad." The eyes in my smileys were "uncannily bad". My coffee cup was a smear of "blotchy black lines that muddle the image", you "can't even tell they are paw prints", the flags were mud, and one round of feedback ended, "You have failed me for the last time."

He didn't hand me a style guide. He taught me from first principles, one critique at a time:

- **Think in the grid.** "Think of yourself as a world famous pixel artist who hand-crafts every pixel on a 16x16 grid. The goal is to simplify complex ideas into a form that can be represented as pixel art."
- **Find the essence.** "Ask 'What is the essence of what I want to highlight?' … Simplify and enhance is the key."
- **Spend pixels on what matters.** "You need to be careful about what pixel is important and what isn't."
- **Outline in black, and make contrast carry the detail.** Darkproject "maximizes contrast to ensure legibility of detail".
- **Know when black belongs inside.** "Notice from darkproject when dark outlines are used inside the visual vs. just being on the outline."
- **Prefer clean, sharp lines.** "8-bit pixel art tends to go more for sharper straight lines and minimizing extraneous details."
- **Shade only what is solid.** "The beveled look only makes sense if the underlying shape is 3d."
- **Respect symmetry.** "There are two eyes and they should look identical unless there is an expression being shown."
- **Judge it at real size.** "Make sure the icons look clear in 16x16 before blowing it up."
- **Grade yourself honestly.** "If you will give anything less than an A+, regenerate it."

This skill turns that teaching into a procedure. Follow it and you'll draw an emoji that sits comfortably beside Darkproject icons and Nintendo item sprites, for any subject. His exact words, and the rule each one produced, are in `references/lessons.md`.

## How to use this skill

1. Read this file once, top to bottom. Then, for each subject, follow the 14 steps in order. Steps 1–4 happen before you place a pixel. Almost every bad drawing I made started with drawing before deciding.
2. Open the references when a step points to them:

   | Reference | Read it for |
   | --- | --- |
   | `references/lessons.md` | Kirupa's critiques, verbatim, grouped by principle, with the rule each one produced |
   | `references/construction.md` | Grid, outline, circles, diagonals, inner ink, ramps, light and flats, with right-and-wrong grids |
   | `references/faces.md` | Smileys, expressions, hands, people, hair, glasses, beards, and portraits of real people from a photo |
   | `references/worked-examples.md` | Eleven approved drawings at both sizes, with every decision explained |
   | `references/review.md` | The rubric, critique questions, review boards, every lint rule, and failures with their fixes |
   | `examples/kirupa-portrait/README.md` | A finished portrait from a photo, at both sizes, with every step, grade and caveat |
   | `assets/reference/` | About 250 approved drawings at both sizes, as `.sprite` text; `catalog.json` lists them |

   If a `references/*-pipeline.md` file sits beside this skill, it describes the host project's file locations, build and publish steps; follow it.

3. **Set up once.** The tool needs Python 3.9+ with Pillow and numpy: `python3 -m pip install -r scripts/requirements.txt`. `resvg_py` renders Twemoji SVGs and `fontTools` finds Apple's pictures of joined (ZWJ) emoji; both are optional. Run every command from this skill's folder (the one holding this file), exactly as written: `python3 scripts/sprite_tool.py …`. From anywhere else, give the script's full path. On Windows, type `py` instead of `python3`. `python3 scripts/sprite_tool.py --help` and `python3 scripts/sprite_tool.py COMMAND --help` explain everything.

   A bare `--out` name (no folder in it) goes to your work folder, `PIXELPERFECT_WORK`, which defaults to `~/pixelperfect-work`, so drafts never land in a repository. Write `./NAME` to use the current folder instead. Bare input names are read from the current folder, then from the work folder. Quote every argument that holds a comma, `@` or `#`. These settings are all optional:

   | Setting | What it does |
   | --- | --- |
   | `PIXELPERFECT_WORK` | Where bare `--out` names go (default `~/pixelperfect-work`) |
   | `PIXELPERFECT_SET_DIR` | Folders or zips of a full Pixel set's PNGs, named by code or file name, read by `set:` and `find` before the bundled library. Separate several with `:` (`;` on Windows). `--set-dir PATH` does the same for one command |
   | `PIXELPERFECT_TWEMOJI_DIR` | Folders or zips of Twemoji `<code>.svg` files, read before the cache and the pinned CDN copy (jdecked/twemoji v17.0.3) |
   | `PIXELPERFECT_CACHE` | Where downloads are kept (default `~/.cache/pixelperfect`, `~/Library/Caches/pixelperfect` on macOS, `%LOCALAPPDATA%\pixelperfect` on Windows) |
   | `PIXELPERFECT_OFFLINE` | `1` means never download, like `--offline`; cached files still work |
   | `PIXELPERFECT_FONT` | A colour emoji font file for `emoji`, when the system's isn't found |

   Set one for a session in bash or zsh, or in PowerShell:

   ```bash
   export PIXELPERFECT_WORK="$HOME/pixelperfect-work"
   ```

   ```powershell
   $env:PIXELPERFECT_WORK = "$HOME\pixelperfect-work"
   ```

   `set:SIZE:CODE` names an approved drawing, such as `set:16:1f34a` or `set:24:tangerine`. The skill bundles about 250 subjects at both sizes (`find` lists them). For all 1,948, download the free PNG zips from the Pixel gallery, https://www.kirupa.com/tools/icon_gallery_pixel.htm, and pass a zip or its folder with `--set-dir` or `PIXELPERFECT_SET_DIR`.

4. **Look at every PNG you make.** Open it with your image viewer (an agent's `view` tool shows images). Lint is a gate, not a judge. Give every board a new file name (`-r2`, `-r3`), because viewers cache by path.

### The `.sprite` file

You draw by typing rows of keys into a text file. This is kirupa.com's approved 16px tangerine:

```text
name: tangerine
size: 16
essence: a round orange fruit with a leafy twig
keep: a full round body lit from the upper left, the twig, one leaf
drop: peel dimples, the navel, a second leaf
view: front, the twig and leaf above the body
rev: 5

[palette]
a #5b3417 twig
c #3f9a25 leaf shade
f #7ccf3a leaf light
b #a54806 peel deep shade
d #d4690a peel shade
e #f58f0c peel base
g #ffae3d peel light
h #ffd28c peel highlight
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

`#` is always ink (#000000) and `.` is always clear. Every other key is one character defined in `[palette]` as `KEY #rrggbb what it is`. `//` starts a comment. A 24px sprite has 24 rows of 24 keys. `new` writes the skeleton for you, blank or from a template.

## The house style at a glance

| | 16×16 | 24×24 |
| --- | --- | --- |
| Long side, outline included | 14–16px (lint errors under 13) | 20–23px (errors under 17, warns under 20) |
| Black outline | One 1px line round the whole silhouette | Round the silhouette and every important piece |
| Black inside | Only holes, crevices and undersides, face features, overlaps of similar values, and line-art symbols. Inner black is usually under 12% of the pixels; 22% fails. | Each important piece gets ink, but small repeated parts are split by tone ("ink vs. muddle") |
| Colours, ink included | About 4–10, median 7; lint warns above 14 | About 6–16, median 8; lint warns above 18 |
| Tones per solid material | 3–4 | 3–5 |
| Light | From the upper left, on solid forms only | The same |
| Flat (no light) | Symbols, signs, letters, flags, print, paper, beams, rays, glows, sparkles, screens. Fire, water and gems use colour zones. | The same |
| Black materials | The slate ramp `#66717c` light, `#3a4148` base, `#30363c` shade, `#262b30` deep; never pure black | The same |
| Smiley eyes | 1×3 at x 6 and 10 | 1×5 bars at x 9 and 14 |
| Person eyes | 1×2 on heads and busts (1×1 on tiny full figures) | 2×3 on big heads, 2×2 on busts and behind glasses (1×2 on tiny full figures) |
| Curves | Monotonic runs (5-2-1-2-5 for the 15px head) | Monotonic runs (8-2-1-1-1-2-8 for the 22px head) |

The two sizes are two drawings of one design. Never make one by resizing the other.

## The method

### Step 1. Gather references, and study them

Look before you draw. Collect three kinds of reference and open each one:

```bash
python3 scripts/sprite_tool.py twemoji 1f34a --out tangerine-twemoji.png
python3 scripts/sprite_tool.py emoji 1f34a --out tangerine-apple.png
python3 scripts/sprite_tool.py find tangerine
python3 scripts/sprite_tool.py text set:16:1f34a
```

- **The emoji itself:** `twemoji CODE` renders Twemoji, the design kirupa.com's set follows. `emoji CODE` renders the system's colour emoji (Apple, Noto or Segoe). It also takes the character itself, and combined (ZWJ) codes like `1f468-200d-1f373`. Find a code with `find WORD`, which searches the approved drawings by name, keyword and category. A subject outside the reference library still has a Twemoji code: its code points in lowercase hex, joined by `-`.
- **The subject in real life,** if the emoji isn't enough. For a portrait, use photos of the person; see Step 12.
- **The masters.** Approved neighbours in kirupa.com's set (`find`, then `text set:16:CODE`) show how a similar subject was solved, pixel by pixel. Darkproject's 16px icons, the emoji.gg pixel pack, and Game Boy, NES and SNES item sprites (Zelda: A Link to the Past) set the bar. If you keep your own collection of reference icons as PNG or GIF files, `text`, `zoom` and `sheet --neighbor` read them too. Study them; never copy, trace or ship them.

While you look, write down the silhouette, the two or three colour families, and the one thing that makes this subject itself and not its neighbour (a tangerine's leaf, a lime's wheel, a mug's handle).

### Step 2. Decide the essence: what to keep, exaggerate and drop

This is the most important step. Kirupa: "Not every detail will make sense, so you shouldn't try to crowd the grid with every thing that would fit. Simplify and enhance is the key."

Fill in four header lines before drawing (lint warns while `essence:` is empty):

- `essence:` the subject in one line, as a child would say it ("a round orange fruit with a leafy twig").
- `keep:` the two or three features that identify it. A 16px icon holds **one big readable shape plus one or two secondary features**. At 24px you can afford one or two more.
- Exaggerate the features you keep: chunky handles, big eyes and ears, wheels, separate toe pads, a leaf a little larger than life.
- `drop:` everything else: texture, small text, fine patterns, reflections, background scenery, second copies, saucers and props. A part under 2px at 16px (3px at 24px) either becomes a single highlight pixel or goes.

Then ask, "If someone saw only this at 16px, what would they call it?" If the answer isn't the subject, the essence is wrong, not the pixels.

### Step 3. Choose the view and the silhouette

Reinterpret freely; "It is ok to reinterpret the intent." Twemoji's 3D cup on a saucer became a 2D mug in side profile, because "fully 3D is hard in pixel art". Pick the view pixel art does best:

| View | For |
| --- | --- |
| Side profile | Mugs, cups, bottles, vehicles, shoes, most animals, fish, tools, instruments, a UFO with a beam |
| Front | Faces, people, buildings, robots, symmetric objects (vases, bells, trophies, skulls) |
| Top | Flat things: pizza, cookie, plate, coin, clock |
| Three-quarter | Only where 3D is the essence: an ice cube, a gift box, dice |
| 45° diagonal | Long thin things (a pencil, sword, carrot, rocket, microphone), because a diagonal fills the square |

Keep the subject's colour identity: a red apple stays red. Write the choice in `view:`. If the obvious view reads as something else at 1x, change the view. A front-on bow read as a dome until it became a side profile; a front-on microphone read as a bulb or an ice-cream cone until it was laid on the diagonal.

### Step 4. Plan the grid

Decide where every big mass goes before drawing:

- **Fill the canvas.** The long side, outline included, spans 14–16px at 16 and 20–23px at 24. Centre the subject. Coloured pixels never touch the canvas edge, which counts as transparency.
- **Budget the pixels.** Give the body most of the grid, then place the secondary features. Never shrink the body to make room for a prop: the tangerine read as "squished" until its stem and leaf stopped eating the top of the circle.
- **Choose the symmetry axis.** A subject 16 pixels wide mirrors x onto 15 − x; one 15 pixels wide on columns 1–15 mirrors onto 16 − x; at 24px the usual axis is 23. An even width has a two-pixel centre seam, and an odd width has a one-pixel centre column. Decide which your subject needs; a nose or a tie wants an odd width.
- **Use standard shapes.** Round bodies use the circle tables in `references/construction.md`; faces and people start from templates (Step 10).

To see where the masses fall, make a proportion draft, view it, then throw it away:

```bash
python3 scripts/sprite_tool.py draft tangerine-twemoji.png --size 16 --colors 4 --out tangerine-16-draft.sprite
python3 scripts/sprite_tool.py zoom tangerine-16-draft.sprite --out tangerine-16-draft.png
```

The draft is mush by design: no outline, no light, ragged edges. Never trace it. Read off the proportions, then start your own file:

```bash
python3 scripts/sprite_tool.py new tangerine --size 16 --out tangerine-16-r1.sprite
```

### Step 5. Block the silhouette and its one black outline

1. Fill the whole silhouette with the base colour key, including parts that stick out (a handle, an ear, a leaf).
2. Put a 1px `#` outline on every clear pixel that touches the fill on a side. That's the line lint checks for. Corners touching only diagonally don't need ink.
3. Never double the outline. A black seam inside the outline (a "hug") reads as a heavy border; that edge belongs to the material's dark tone.
4. Black outlines aren't optional: "Each individual shape should have a black outline as well." At 24px, every important separate piece gets its own ink: a lid, a handle, a wheel, a leaf, each eye. At 16px, pieces inside the silhouette are usually split by tone (Step 7).
5. Thin, unoutlined 1px lines are allowed at 16px for things like steam, rays and sparkles, and a thin dark stem, whisker or hair strand can be its own edge. Lint warns about these so you'll confirm each one was deliberate. At 24px, everything is outlined.

### Step 6. Make curves and diagonals clean

- **Curves step monotonically.** Going round a quadrant, runs shrink toward the 45° point and grow again after it. The 15px smiley head goes 5-2-1-2-5: a 5px flat top, a 2px step, one corner pixel, then a 2px and a 5px run down the side. Never 1-3-1-2. A good circle's horizontal runs mirror its vertical runs. Lumpy runs read as octagons and potatoes. Copy the circle profiles in `references/construction.md` rather than inventing them.
- **Diagonals are 1:1 or 2:1,** with steps that touch only at corners. An L-join (an extra pixel filling the inside of a step) makes a line look thick and jagged.
- **No doubled corners and no orphans.** Each pixel of an outline touches exactly two neighbours along the line.
- Kirupa's standard: "sharper straight lines and minimizing extraneous details."

### Step 7. Separate the inside by tone, not by ink

At 16px, parts inside the silhouette are split by colour and value: green leaf against orange peel, brown coffee in a white mug, a hat on a head. Black goes inside **only** for these five reasons:

1. Holes and openings: a handle hole, an open mouth, a keyhole, a doorway.
2. Deep crevices and undersides: under a mushroom cap, between two wheels.
3. Face features: 1px eyes, mouth lines, nostrils.
4. Overlaps of similar values, where only a line can split them: fingers, a book's cover over its pages, two grapes.
5. Line art that is the symbol itself: clock hands, a card's suit marks, a music note.

**The test:** for every black pixel inside the silhouette, name its reason. If you can't, recolour it with the darkest tone of the part it belongs to. At 24px, ink each important piece, but split small repeated parts (keys, tabs, shingles, petals in a tight cluster) with their own dark tone. If removing an inner line makes the icon cleaner at 1x, remove it. Adjacent parts must differ in **value**, not just hue; the greyscale panel in `zoom` shows whether they do.

### Step 8. Build colour ramps

- **Start from the reference's colours.** Sample them (`sample` works on any image), then build a hue-shifted ramp round each base: shadows shift cooler and richer, and highlights warmer and paler. That's never grey mud.

  ```bash
  python3 scripts/sprite_tool.py sample tangerine-twemoji.png --box "40,50,120,140" --colors 4
  python3 scripts/sprite_tool.py ramp "#f58f0c"
  ```

- **Spend colour like money:** 3–4 tones per solid material at 16px and 3–5 at 24px, about 4–10 colours in total at 16 and 6–16 at 24. Reuse one ramp for every part made of the same stuff.
- **Maximise contrast between parts.** Darkproject "maximizes contrast to ensure legibility of detail": make neighbouring parts clearly lighter or darker than each other.
- **Black materials are slate,** so the black outline still shows: `#66717c` light, `#3a4148` base, `#30363c` shade, `#262b30` deep. On the person templates those are the hair keys `H h d k`, in that order. Dark hair sits at luminance 55–65. No palette colour should be darker than luminance 40: it reads as ink, and lint counts it as ink. Even navy `#00247d` reads as ink at 16px; use `#12328c`.
- **Smiley yellow** is the Darkproject-matched ramp `#ffffcf` glint, `#ffff93` light, `#ffe600` base, `#ffbf00` rim, `#f08e00` deep. Kirupa: "match the yellow tone of the darkproject yellow smilies."

### Step 9. Light solid forms; keep flat things flat

- **One light, from the upper left,** on solid forms only: fruit, balls, pots, bottles, animals, vehicles, buildings, tools, leaves, petals and stems. Spheres get a light crescent and glint at the upper left and a dark crescent at the lower right. Cylinders get vertical bands, like the 16px mug's body row `g i i h h h h g f e`: a rim tone, a white highlight band near the left, the base, then three darker bands toward the right. Boxes get a light top, a mid face and a dark face. Faces are lit on the rim only.
- **Flat things stay flat** (1–2 tones, no bevel): symbols, signs, arrows, letters, flags, print, paper, beams, rays, glows, sparkles and screens. Fire, water and gems use colour zones, not shading. Kirupa: "the beam from the UFO is not and shouldn't be beveled."
- **No pillow shading** (darkening every edge equally), no concentric bands, no dithering and no single-pixel tone noise. At 16px, a 1px tone band hugging the rim beats a gradient.
- Glossy things get a white glint: 1–2px at 16 and a 2–3px cluster at 24.

### Step 10. Features and faces

Faces are read from a few pixels, so those pixels must be perfect. Start smileys and people from a template instead of drawing a head:

```bash
python3 scripts/sprite_tool.py new grinning --template smiley-head-16 --out grinning-16-r1.sprite
```

Templates: `smiley-head-16`, `smiley-head13-16` (a 13px head leaving three rows for a hat or halo), `smiley-16`, `smiley-head-24`, `smiley-24`, `person-head-16`, `person-head-24` and `bust-16`. Each prints a hint about its geometry.

- **Eyes are 1px wide on smileys and on 16px people** (1×3 smiley and 1×2 person at 16; 1×5 smiley at 24); **24px people use 2×3** (2×2 in a bust or behind glasses). They're vertical, solid black and identical by translation. Only an expression changes them (a wink, squeezed `> <`, hearts, stars). Two different eyes read as broken, not expressive. Never use a 2×2 blob eye on a 16px head.
- **A mouth is one line:** a smile is two corner pixels plus a short line one row lower. An open mouth is an outlined hole with one colour inside (dark, red tongue or white teeth), at most two rows.
- **Extras are separate objects:** tears stream outward from a squeezed eye, never hang straight down like earrings. Hearts, sweat, hats and halos get ink only where they meet transparency or a similar value.
- **Draw one half and mirror it** when the face is symmetric:

  ```bash
  python3 scripts/sprite_tool.py mirror grinning-16-r1.sprite --axis 16 --swap "S=t,W=t" --out grinning-16-r2.sprite
  ```

  `--swap` turns the copied lit-side keys into shade keys, because light still comes from the upper left.

`references/faces.md` has the full face kit: coordinates for every eye and mouth at both sizes, brows, tears, blush, hands, animal faces and people.

### Step 11. Draw the 24×24 natively

Draw the 24px version from the same essence, view and palette families, on a fresh grid. Never scale the 16 up or the 24 down; Kirupa wanted "a clean 16x16 and 24x24 version", each designed for its grid. The extra pixels pay for:

- Ink round each important piece, not just the silhouette.
- One or two more tones per material, and real glints of 2–3px.
- Proper features: 1×5 smiley eyes, 2×3 person eyes, 2×2 ink eye sockets on a skull, finger lines in a darker skin tone (never black).
- Outlined steam, rays and tears, which are thin 1px lines at 16.
- One or two more identifying details from your `keep:` list. Don't add new clutter.

Then put both sizes on one board and check that they read as the same emoji (Step 13).

### Step 12. People, and portraits from a photo

kirupa.com's set draws generic people with smiley-yellow skin, golden-orange hair separated from the face by value (an ink fringe at 24), 1×2 eyes at 16 and 2×3 eyes at 24, and one profession cue (a toque, a helmet, a stethoscope). Start from `person-head-16`, `person-head-24` or `bust-16`.

A portrait of a real person is a likeness built from a few true traits. `examples/kirupa-portrait/README.md` walks through a finished one, from a public photo to both grids, with every command, grade and caveat.

1. **Use photos the person has published,** or ones you were given: front-facing, evenly lit, the face large. A photo's URL works anywhere a file name does; the tool downloads it once into its cache. Enlarge the face to study it and to find the pixel boxes you'll need:

   ```bash
   python3 scripts/sprite_tool.py crop "https://www.kirupa.com/about/kirupa_bio_pic_png.png@265,225,470,480" --scale 2 --out face-crop.png
   ```

2. **Pick three to five traits you can see** that survive at 16px: hair shape and colour, hairline, glasses, facial hair, face shape (a round, oval or long jaw), expression, clothing colour. Write them in `keep:`, most important first, phrased as things a stranger could name at 1x: "dark hair", "a toothy grin", "glasses". Strangers name colours and shapes, not lengths or styles. At 24px, add one or two more. Strong brows are a 24-only trait, for photos that plainly show them.
3. **Sample the skin mechanically.** Box one clean patch of skin as the skin box `SX0,SY0,SX1,SY1`: the cheeks and nose between the eyes and the mouth, or the forehead. Keep hair, brows, eyes, lips, glasses and background out; brows and eyes drag the average darker. Run `sample PHOTO --box "SX0,SY0,SX1,SY1" --face`. It lists every colour cluster with its hex, luminance, saturation and share, flags the palest, least saturated cluster (flash or shine) and the darkest (shadow), and recommends the base. `ramp` that base onto `S s t u`. When photos disagree, sample the most evenly lit one, never a flash photo. Use the person's own tone, lightened or darkened by nothing. Sample the hair and shirt with plain `sample`; black hair is the slate ramp.
4. **Build on the template:** change the hair silhouette first, then the jaw (round, oval or long, at most 1px per side from the template), then add glasses, facial hair or brows, then the expression. A kit grin's width is a house shape, not an enlarged feature: a big smile is the kit's grin at the kit's width, never a wider or deeper one. The 16px person-head grin is four rows (an ink lip, white teeth, a grey lower-teeth row, an ink base) and needs the eyes on rows 6–7 and a hair cap that ends on row 3; `references/faces.md` §10 has it. With facial hair at 16, keep the hair and a small mouth and leave the grin to the 24. Never raise a person-head's mouth corners: they read as a moustache.
5. **Respect the person.** No caricature: exaggerate the chosen traits' shapes (a hair silhouette, a beard, the frames), never anatomy. Draw only what the photo shows. Never infer or add anything about ethnicity, age, gender, religion or health that isn't plainly visible, and don't "correct" a face toward a default.
6. **Review it against the photo, then blind.** `sheet --ref "PHOTO@X0,Y0,X1,Y1"` puts the cropped face beside your drawing, and `check SPRITE --skin "S,s,t,u" --face "PHOTO@SX0,SY0,SX1,SY1"` (the same skin box) fails if the sprite's average skin is more than 15 luminance from the photo face's. Put the 16 and the 24 on one board: same palette, hairline shape, mouth type and extras; the 24 adds detail and never contradicts the 16. Then run the blind test in Step 13. If the portrait must sit in the set, deliver a smiley-yellow variant too by swapping only the skin keys (don't use `--skin` on it). Where dark hair reaches the eye rows, the yellow variant can read as sunglasses: trim or lighten the hair there, and blind-test the yellow version too.

`references/faces.md` §13 has the full procedure; §10 has the jaw, grin and brow grids; §12 has glasses and beards at both sizes; §14 is the portrait addendum to the acceptance rubric, with the respect checklist.

### Step 13. The review loop

Every drawing goes round this loop until it's an A+. Two to four passes is normal.

```bash
python3 scripts/sprite_tool.py check tangerine-16-r1.sprite
python3 scripts/sprite_tool.py zoom tangerine-16-r1.sprite --out tangerine-16-r1-zoom.png
python3 scripts/sprite_tool.py sheet tangerine-16-r1.sprite --twemoji 1f34a --emoji 1f34a --neighbor set:16:1f34b --neighbor set:16:1f34e --out tangerine-16-r1-sheet.png
```

1. **`check`:** fix every ERROR. For every warning, fix it or write the reason it's deliberate in a `note:` line (a steam wisp, a thin stem).
2. **`zoom`:** open it. On the numbered grid, inspect the outline, every curve, the mirror axes and stray pixels. In the greyscale panel, make sure neighbouring parts differ in value.
3. **`sheet`:** open it. First look at the 1x row on light and dark. Can you name the subject in half a second? Then compare it with Twemoji and the system emoji (same subject, same colour identity) and with its neighbours (same outline weight, saturation, canvas fill and amount of detail).
4. **Grade it honestly** against the best pixel art you know. Below A+, fix the biggest problem first and save the result as the next rev (`-r2`). Don't polish an A+.
5. **When you're stuck, branch.** Draw two or three different designs (A, B, C) and compare them on one sheet: `sheet A.sprite B.sprite C.sprite --twemoji CODE --out …`. The microphone took four rounds of variants before the diagonal design won.
6. **Blind-test anything that must be recognised:** faces, people, portraits, and any subject you hesitated over. `blind` writes anonymised 1x, 2x and gridless 4x renders, shuffled with at least one approved neighbour as an unlabelled control, plus a `key.txt` that says which is which:

   ```bash
   python3 scripts/sprite_tool.py blind tangerine-16-r1.sprite --control set:16:1f34b --out tangerine-blind-r1
   ```

   Give only the `show/` folder and the fixed prompt it prints to three fresh reviewers (people, or new agents with no context). It passes when 2 of the 3 name your top two traits unprompted: for a person, the first two in `keep:`; for anything else, what it is and its key cue. Ignore any misread the control also gets: dark hair on every person-head reads as a "helmet", and that's the house style, not your drawing. One round is noisy, so pass two rounds running (new reviewers, a new `--seed`) or 5 of 9 reads over three rounds. For a portrait in a real skin tone, add a skin-matched control: reviewer models misread darker skin, and you never change a sampled skin tone because of it. `references/review.md` §2 has the full protocol.

Ask yourself:

- What does it read as at 1x? If anything other than the subject, it isn't done.
- Where does my eye land first? Is that the essence?
- Which pixel can I delete without losing anything?
- Can every inner black pixel name one of the five reasons?
- Is every curve monotonic, every diagonal clean, and the symmetry exact?
- Is every solid part lit from the upper left, and every flat part flat?
- Do the 16 and the 24 read as one emoji?

Grade it with the acceptance rubric below. `references/review.md` shows how I check each rubric line, and lists every lint rule.

### Step 14. Hand off

- **Show proposals; don't silently replace.** Kirupa's rule for revisions: "Create the proposals but don't make the change to the main list. Show me for evaluation first." Present the candidates side by side (`sheet` with every rev and the references), say which you'd pick and why, and let the owner choose.
- **Deliver** the `.sprite` files plus PNGs at 1x and 8x for each size:

  ```bash
  python3 scripts/sprite_tool.py render tangerine-16-r1.sprite --out tangerine-16.png
  python3 scripts/sprite_tool.py render tangerine-16-r1.sprite --scale 8 --out tangerine-16-8x.png
  ```

- **If your project keeps its art in Python,** `export` writes the drawing as `ROWS_NAME` and `KEYS_NAME` lists, and `MODULE.py:NAME` reads them back; `examples/python-module/tangerine.py` shows the format. If a `references/*-pipeline.md` file sits beside this skill, follow it to add the art to the host project. Never publish anything without the owner's explicit go-ahead.

  ```bash
  python3 scripts/sprite_tool.py export tangerine-16-r1.sprite --name TANGERINE16 --out tangerine16.py
  ```

## Failure catalogue

These are the mistakes I made, and what fixed each one. `references/review.md` has more.

| You see | Why it happens | Fix |
| --- | --- | --- |
| Mush, smeared detail, broken 1px slivers | The art was traced, downsampled or converted | Redraw from the essence. A draft is for proportions only. |
| Blotchy black lines muddling the inside | 24px habit: ink between every pair of parts | Use the five-reasons test, and recolour the rest with dark tones |
| A heavy double border | A black seam inside the outline | Use the material's dark tone instead (lint: "hug") |
| Colour touching transparency | A missing outline pixel | Ink every clear pixel beside colour |
| A lumpy circle or an octagon | Non-monotonic runs | Use a circle profile from `construction.md` |
| A jaggy, thick diagonal | L-joins, irregular steps | Use 1:1 or 2:1 steps that touch at corners only |
| Uncanny or mismatched eyes | 2×2 blobs, different sizes | Use the house eye: 1px wide on smileys and 16px people, 2×3 on 24px people (2×2 in a bust or behind glasses); identical, mirrored |
| A lopsided symmetric subject | Both halves placed by hand | Draw half and `mirror` it; `check` lists the breaking pixels |
| Squished or shrunken body | Props ate the body's pixels | Keep the full body and fit props round it |
| It reads as something else | Wrong view, or the key cue is missing | Change the view, exaggerate the identifying feature, try variants |
| A bevel on a beam, flag or sign | Light applied to everything | Keep the flat list flat |
| A flat, lifeless solid | No light ramp | Light it from the upper left: crescent, bands or faces |
| Grey mud, or too many colours | Unshifted ramps, one ramp per part | Use hue-shifted `ramp`s, shared across one material, within the budget |
| A black hat or cat vanishes | Pure-black fill against the black outline | Use the slate ramp |
| Speckled noise | Dithering, single-pixel tone specks | Use runs of 2px or more per tone |
| Tears like earrings | Drops hanging straight down | Stream them outward from the squeezed eye |
| Paw prints nobody recognises | Toes merged into the pad | Use separate, fully outlined toe pads above a big pad |
| A portrait's skin lighter than the person's | It was sampled from a flash highlight or shine | `sample --face` the most evenly lit photo, then pass `check --skin --face` |
| A portrait's big grin that nobody reads | The grin was enlarged, or squeezed into rows the head doesn't have | Use the kit grin at the kit's width (`faces.md` §10); if the 16 can't fit it, move the eyes up, shorten the hair, or keep the grin for the 24 and give the 16 a wide calm smile |
| Busier, darker or smaller than its neighbours | No harmony check | Simplify, brighten or enlarge it until it matches the set |

## Acceptance rubric

An emoji is **A+** and ready when every line is true:

- [ ] Anyone would name it at 1x, on light and on dark, in half a second.
- [ ] `check` shows no ERRORS, and every warning has a stated reason.
- [ ] It fills the canvas (14–16 or 20–23px) and is centred.
- [ ] One clean outline; every inner black pixel has one of the five reasons (16px), or every important piece is inked (24px).
- [ ] Every curve is monotonic, every diagonal clean; no orphans and no doubled corners.
- [ ] Symmetric subjects are exactly symmetric in shape, and the two eyes are identical unless the expression differs.
- [ ] Hue-shifted ramps within the colour budget, and neighbouring parts clearly differ in value.
- [ ] Solid forms are lit from the upper left; flat things are flat.
- [ ] It keeps the subject's colour identity and essence when compared with Twemoji and the system emoji.
- [ ] It sits among approved neighbours with the same weight, saturation, fill and level of detail.
- [ ] The 16 and the 24 read as the same emoji, and neither is a resize of the other.

A **portrait of a real person** must also meet these:

- [ ] Blind, 2 of 3 fresh reviewers name its top two traits unprompted, in two rounds running (Step 13, item 6).
- [ ] Someone who knows the person recognises them. Until then, hand it off marked "unverified".
- [ ] Every trait is visible in the person's published photos: nothing inferred, nothing caricatured.
- [ ] The real-tone version passes `check --skin --face`. Judge it against neighbours on weight, fill and detail only; its smiley-yellow variant carries the set's colour harmony.

This rubric is the single source of truth; `references/review.md` shows how I check each line. Grade **A** means one fix away: make it and go round the loop again. Grade **B** means the view, silhouette or grid is wrong: go back to Step 3 or 4. Grade **C** or below means the essence is wrong: go back to Step 2.

## Commands

| Command | Does |
| --- | --- |
| `python3 scripts/sprite_tool.py find WORD... [--size 24]` | Finds approved sprites by name, keyword or category, in the reference library and any `--set-dir` set; every WORD must match, so search one word at a time when unsure |
| `python3 scripts/sprite_tool.py text SPRITE... [--out FILE]` | Prints any sprite as `.sprite` text to study it (`set:16:CODE`, a PNG or GIF, or `MODULE.py:NAME`) |
| `python3 scripts/sprite_tool.py twemoji CODE --out PNG` | Renders Twemoji (from `PIXELPERFECT_TWEMOJI_DIR`, then the cache, then the pinned CDN copy; needs `resvg_py`) |
| `python3 scripts/sprite_tool.py emoji CODE --out PNG` | Renders the system colour emoji (also a character or a ZWJ code) |
| `python3 scripts/sprite_tool.py crop "IMAGE@X0,Y0,X1,Y1" --scale 3 --out PNG` | Crops and enlarges part of a photo to study it |
| `python3 scripts/sprite_tool.py draft IMAGE --size 16 --out FILE` | Makes a proportion draft; `"IMAGE@X0,Y0,X1,Y1"` crops first |
| `python3 scripts/sprite_tool.py sample IMAGE --box "X0,Y0,X1,Y1"` | Lists the dominant colours in an area |
| `python3 scripts/sprite_tool.py sample IMAGE --box "SX0,SY0,SX1,SY1" --face` | On a skin box (one clean patch of cheek or forehead): skin clusters with luminance, saturation and share; flags flash/shine and shadow; recommends the base |
| `python3 scripts/sprite_tool.py ramp "#hex"` | Builds a hue-shifted ramp, with slate advice for dark bases |
| `python3 scripts/sprite_tool.py new NAME --size 16 [--template T] --out FILE` | Starts a `.sprite`, blank or from a template |
| `python3 scripts/sprite_tool.py mirror FILE --out FILE [--axis 15] [--swap "S=t"] [--only "#."]` | Copies one half onto the other |
| `python3 scripts/sprite_tool.py check SPRITE...` | Lints against the house rules; exits 1 on errors |
| `python3 scripts/sprite_tool.py check SPRITE --skin "S,s,t,u" --face "IMAGE@SX0,SY0,SX1,SY1"` | Also fails if the sprite's average skin, over those keys, is more than 15 luminance from the skin box's face average |
| `python3 scripts/sprite_tool.py zoom SPRITE... --out PNG` | Shows a numbered big grid, mirror axes, 1x–3x on light and dark, and greyscale |
| `python3 scripts/sprite_tool.py sheet SPRITE... --out PNG [--ref IMG] [--twemoji C] [--emoji C] [--neighbor S]` | Makes the review board |
| `python3 scripts/sprite_tool.py blind SPRITE... --control S --out DIR` | Writes a shuffled, unlabelled blind test (`DIR/show/`) and its answer key (`DIR/key.txt`) |
| `python3 scripts/sprite_tool.py render SPRITE --out PNG [--scale 8]` | Writes the deliverable PNG |
| `python3 scripts/sprite_tool.py export SPRITE --name NAME [--out FILE]` | Writes the drawing as Python `ROWS_NAME` and `KEYS_NAME` lists |

Every command that writes a file refuses to replace an existing one unless you add `--force`. IMAGE and PHOTO can be a file or an http(s) URL. Add `--offline` to any command (or set `PIXELPERFECT_OFFLINE=1`) to never download.

To practise the loop on approved art, copy an approved drawing into your work folder and review it as if it were yours:

```bash
python3 scripts/sprite_tool.py text set:16:1f34a --out study-tangerine-16.sprite
python3 scripts/sprite_tool.py check study-tangerine-16.sprite
```

## Folder map

```text
pixelperfect/
├── SKILL.md                       this procedure
├── LICENSE.txt                    MIT, for the code and docs
├── references/
│   ├── lessons.md                 Kirupa's teaching, verbatim, and the rule each lesson produced
│   ├── construction.md            grid, outline, circles, diagonals, inner ink, ramps, light, flats, flags
│   ├── faces.md                   smileys, expressions, people, glasses, beards, portraits from a photo
│   ├── worked-examples.md         eleven approved drawings, both sizes, every decision explained
│   └── review.md                  rubric, critique questions, boards, lint rules, failures and fixes
├── scripts/
│   ├── sprite_tool.py             the tool behind every command above
│   └── requirements.txt           Pillow and numpy; resvg_py and fontTools optional
├── templates/*.sprite             smiley, smiley head, person head and bust starting points
├── assets/
│   ├── LICENSE.md                 the artwork's free non-commercial license and the Twemoji credit
│   └── reference/                 about 250 approved drawings at 16 and 24, as .sprite text, plus catalog.json
└── examples/
    ├── kirupa-portrait/           a portrait from a public photo, both sizes, real tone and yellow
    ├── lint-failures/             four broken smileys that check rejects, for testing the lint
    └── python-module/             the ROWS_/KEYS_ format that export writes and MODULE.py:NAME reads
```

The bundled drawings are a study library, not the icon set: they're under the free license in `assets/LICENSE.md`, which doesn't allow redistributing them as a set. The full set is at https://www.kirupa.com/tools/icon_gallery_pixel.htm.

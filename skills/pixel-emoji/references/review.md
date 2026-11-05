# Review: how I judge a drawing

I didn't get good by drawing better first. I got good by looking better. My early sprites passed my own eye because I judged them at 8x, alone, against nothing. Kirupa judged them at 1x, beside Darkproject's icons, and he was right every time. This file is how I look now: the loop, the views, the questions, the rubric, every lint rule, and the failures I made with the fix for each.

The commands assume SKILL.md's setup: run them from the skill's folder (from anywhere else, give the script's full path), and bare `--out` names land in your work folder.

Contents:

1. The loop
2. Five ways to look
3. Questions I ask every drawing
4. The rubric and the grades
5. Comparison boards
6. The lint, rule by rule
7. The lint on approved art
8. What the lint can't see
9. Failures and their fixes
10. Revisions, proposals and hand-off

## 1. The loop

Every drawing goes round this loop until it earns an A+. Two to four passes is normal. The microphone took four rounds of variants before one design won.

```bash
python3 scripts/sprite_tool.py check tangerine-16-r1.sprite
python3 scripts/sprite_tool.py zoom tangerine-16-r1.sprite --out tangerine-16-r1-zoom.png
python3 scripts/sprite_tool.py sheet tangerine-16-r1.sprite --twemoji 1f34a --emoji 1f34a --neighbor set:16:1f34b --neighbor set:16:1f34e --out tangerine-16-r1-sheet.png
```

1. **Lint it** with `check`. Fix every ERROR. Read every warning, then fix it or write why it's deliberate in a `note:` line.
2. **Inspect the pixels** with `zoom`: the outline, every curve and diagonal, the symmetry, stray pixels and the greyscale panel.
3. **Judge the read** with `sheet`: 1x on light and dark first, then the references, then the neighbours.
4. **Grade it** (section 4). Below A+, name the single biggest problem, fix only that, save the result as the next rev (`-r2`), and go round again.
5. **Branch when you're stuck.** If two passes fail on the same problem, the design is wrong, not the pixels. Draw two or three different designs and compare them on one board (section 5).

This is still Kirupa's standard, and now it's mine: "For every pixel art visual you created, ask yourself what grade you will give it compared to the various other pixel art that you have seen. If you will give anything less than an A+, regenerate it."

## 2. Five ways to look

Each view catches mistakes the others hide. Use all five on every pass.

| View | Where to find it | What it catches |
| --- | --- | --- |
| 1x on light and on dark | `sheet` real-size rows; the `zoom` 1x–3x strip | Whether it reads at all; mush; accidental faces and letters; an outline that vanishes on dark |
| 2x and 3x | the `zoom` strip | Lumpy curves, jaggy diagonals, strays you can't quite see at 1x |
| The 8x numbered grid | `zoom`, with its mirror axes | Exact coordinates: broken symmetry, L-joins, doubled corners, orphans, a missing outline pixel |
| Greyscale (the squint test) | the `zoom` greyscale panel | Parts of equal value that merge; light that isn't from the upper left; a ramp that's really one value |
| Beside references and neighbours | `sheet` | Lost colour identity or essence; the wrong weight, saturation, size or level of detail for the set |

How I look:

- **Judge at 1x first.** Kirupa: "Make sure the icons look clear in 16x16 before blowing it up." At 8x everything looks deliberate. At 1x only the essence survives.
- **Name it in half a second.** Look at the 1x sprite with the label covered and say what it is. If you hesitate, or say something else, it isn't done.
- **Run the blind test** on anything that must be recognised: faces, people, portraits, and any subject you hesitated over. A fresh reviewer's first answer is honest, but one reviewer, or one round of three, is noisy, so the protocol is fixed:
  1. **Make the cards with `blind`,** with at least one approved neighbour as a control. It renders every sprite at 1x, 2x and a gridless 4x on white, shuffles them under letters, and writes which letter is which, with each drawing's `essence:` and `keep:`, to `key.txt`:

     ```bash
     python3 scripts/sprite_tool.py blind tangerine-16-r2.sprite --control set:16:1f34b --control set:16:1f34e --out tangerine-blind-r2
     ```

     For a portrait in a real skin tone, add a skin-matched control too: an approved shape, such as `set:16:1f9d1` or `set:16:1f600`, saved with `text --out` and with only its skin keys changed to your sampled tones.
  2. **Show three fresh reviewers** only the `show/` folder: people, or new agents with no other context. Never the key, the file names or your notes.
  3. **Send the fixed prompt** word for word. `blind` prints it, and `key.txt` keeps a copy:

     ```text
     Open only the images in this folder. Each letter is one tiny icon, shown at real size (LETTER-1x.png), at 2x and
     at 4x. For EACH letter, from the pictures alone, answer in a line or two:
     1. What is this?
     2. What can you tell about the person or subject?
     3. Its two most distinctive traits.
     4. Possible misreads: what could someone mistake it, or any part of it, for?
     Don't guess who anyone is, and don't compare the letters with each other.
     ```

  4. **Decide the scoring before you read.** Write down what counts as naming each trait. For teeth: "teeth", "toothy" or a white mouth; "big smile" alone is a different trait. For hair: "dark" or "black", not "brown". Save every prompt and answer word for word.
  5. **Pass rule:** 2 of the 3 reviewers name the drawing's top two traits unprompted. For a person, those are the first two in its `keep:` line, phrased as things a stranger can name at 1x (dark hair, a toothy grin, glasses, a beard); for anything else, what it is and its key cue. One round is noisy, so pass two rounds running, each reshuffled with a new `--seed` and new reviewers, or 5 of 9 reads over three rounds.
  6. **Judge each trait against the controls.** Ignore any misread a control also gets: dark hair on the person-head template reads as a "helmet", "hat" or "beard" even on the approved `set:16:1f9d1`. That's the house style, not your drawing. Once your drawing names a trait as often as the approved shape does, stop redrawing it.
  7. **Know the reviewers' bias.** Agent reviewers misread darker skin, even as an animal face, and a skin-matched control draws the same misread. The read follows the skin, not the drawing. Never lighten or change a sampled skin tone because of it. A person makes the respect and likeness call.
  8. **On a fail,** exaggerate the missing trait's shape (never its size), save a new rev, and test it in a new `--out` folder with new reviewers: a reviewer who has seen it isn't blind any more.

  `examples/kirupa-portrait/README.md` has a real record: ten rounds on one portrait, with the controls' scores beside it.
- **Squint.** In the greyscale panel the big shapes should still separate, and the light should still come from the upper left.
- **Look for what isn't there.** At 1x the eye finds patterns everywhere:
  - two dark dots over a line read as a face;
  - hollow ink loops read as letters;
  - a plus shape reads as a cross;
  - a square body under a head reads as a headstone.

  Check the 1x read for anything the subject isn't. `worked-examples.md` §8 shows a radioactive sign that grew a face.

## 3. Questions I ask every drawing

**Reading and essence**

- What does it read as at 1x? If it's anything other than the subject, it isn't done.
- Where does my eye land first? Is that the essence I wrote in the header?
- Which pixel can I delete without losing anything? Delete it.
- Did I keep any detail because it fits rather than because it says something? Kirupa: "Not every detail will make sense, so you shouldn't try to crowd the grid with every thing that would fit."
- Would another view read better: a side profile, a front elevation, or one item instead of a pair?

**Silhouette and outline**

- Does it fill the canvas (14–16px on the long side at 16, 20–24px at 24) and sit centred?
- Is there exactly one black outline, one pixel thick, all the way round, and round every separate piece?
- Is every curve monotonic, with runs that only grow and then shrink? Is every diagonal a clean 1:1 or 2:1 step whose pixels touch only at corners?
- If the subject is symmetric, does `check` report `0 off`?

**Inside**

- Can every inner black pixel name one of the five reasons: a hole or opening, a crevice, a face feature, an overlap of two parts with similar values, or a line-art symbol? At 24, is every important piece inked?
- Do neighbouring parts clearly differ in value in the greyscale panel?
- Are the tones in runs of two or more, with no dithering and no single-pixel specks?

**Colour and light**

- Is the colour count within the budget, with one shared ramp per material?
- Are the ramps hue-shifted (warmer and lighter going up, cooler and darker going down), not just darker greys?
- Is every solid form lit from the upper left? Is every flat thing flat: symbols, flags, print, paper, beams, glows, fire, water and screens?
- Are black materials drawn in slate, so they don't vanish into the outline?

**Faces and people**

- Are the two eyes identical, unless the expression says otherwise?
- Are the eyes the house size? Eyes are 1px wide on smileys and on 16px people (1×3 smiley and 1×2 person at 16; 1×5 smiley at 24); 24px people use 2×3 (2×2 in a bust or behind glasses).
- Do the mouth and its corners carry the expression? Is a grin the kit's grin at the kit's width?
- For a portrait: are the three to five chosen traits visible at 1x, with nothing exaggerated into caricature? Does the real-tone version pass `check --skin --face`, and does the blind test name the first two traits in `keep:`?

**16 and 24**

- Is the 24 drawn natively, not resized from the 16, with the same design, colours and light?
- Did the 24 spend its extra pixels on the essence (cleaner curves, one more ramp step, a feature the 16 had to drop) rather than on noise?

**The set**

- Beside its neighbours, does it have the same outline weight, saturation, canvas fill and level of detail?
- Beside Twemoji and the system emoji, does it keep the same colour identity and the same idea?

## 4. The rubric and the grades

SKILL.md's acceptance rubric is the single source of truth. This table repeats its lines in the same order, and adds how I check each one and when it fails. An emoji is A+ when every row passes; a portrait of a real person must also pass P1–P4.

| # | SKILL.md rubric line | How I check | It fails when |
| --- | --- | --- | --- |
| 1 | Anyone would name it at 1x, on light and on dark, in half a second | `sheet` real-size rows; `blind` (section 2) | You hesitate, name something else, or see a face that isn't there |
| 2 | `check` shows no ERRORS, and every warning has a stated reason | `check` (section 6) | Any ERROR, or a warning with no fix and no reason in `note:` |
| 3 | It fills the canvas (14–16 or 20–23px) and is centred | `check` span; `zoom` | Span warnings; off-centre by more than a pixel without a reason |
| 4 | One clean outline; every inner black pixel has one of the five reasons (16px), or every important piece is inked (24px) | `zoom` 8x; `check` edge, hug and inner-ink rules | It's doubled, broken, or missing round a separate piece; an inner black pixel can't name its reason |
| 5 | Every curve is monotonic, every diagonal clean; no orphans and no doubled corners | `zoom` 2x–3x and 8x | Lumps, octagons, L-joins, uneven steps, strays, a straight line that reads curved |
| 6 | Symmetric subjects are exactly symmetric in shape, and the two eyes are identical unless the expression differs | `check` mirror figure; `zoom` axes | `n off` on a symmetric subject; eyes that differ for no reason |
| 7 | Hue-shifted ramps within the colour budget, and neighbouring parts clearly differ in value | `check` colours and equal value; greyscale panel | Over the budget, unshifted grey ramps, or parts that merge in greyscale |
| 8 | Solid forms are lit from the upper left; flat things are flat | the `zoom` greyscale panel | Light from another side, a bevel on a flat thing, or a solid left flat |
| 9 | It keeps the subject's colour identity and essence beside Twemoji and the system emoji | `sheet` with `--twemoji` and `--emoji` | The wrong colour family, or the key cue is lost |
| 10 | It sits among approved neighbours with the same weight, saturation, fill and level of detail | `sheet` with `--neighbor` | Heavier, busier, more saturated or smaller than its neighbours, or darker without a reason. A real-tone portrait is judged on weight, fill and detail only (P4). |
| 11 | The 16 and the 24 read as the same emoji, and neither is a resize of the other | a pair board (section 5) | One is a resize of the other, or the designs disagree |
| P1 | Blind, 2 of 3 fresh reviewers name its top two traits unprompted, in two rounds running | `blind` and the protocol in section 2 | Fewer than 2 of 3 name the first two traits in `keep:` in either round, not counting misreads the controls also get |
| P2 | Someone who knows the person recognises them; until then it's marked "unverified" | Show it to the person, or someone who knows them | Nobody who knows them has seen it, and the hand-off doesn't say "unverified" |
| P3 | Every trait is visible in the person's published photos: nothing inferred, nothing caricatured | `sheet --ref`; `faces.md` §14 | A trait no photo shows, anything inferred about identity, or an enlarged feature |
| P4 | The real-tone version passes `check --skin --face`; its smiley-yellow variant carries the set's colour harmony | `check SPRITE --skin "S,s,t,u" --face "PHOTO@SX0,SY0,SX1,SY1"` | The skin is more than 15 luminance from the photo's face average |

Grades:

- **A+:** every row passes. Stop polishing and present it.
- **A:** one fix away: a pixel, a run, a tone. Make that fix and go round the loop again.
- **B:** it reads, but the view, silhouette or grid is wrong (proportions, a key cue too small). Go back to SKILL.md Step 3 or 4 and redraw.
- **C or below:** it doesn't read, or it reads as something else: the essence is wrong. Go back to Step 2, rethink the essence and try two or three designs.

Grade against the best pixel art you know (Darkproject, and NES, SNES and Game Boy sprites), not against your previous rev. A rev that's better than the last one can still be a C.

## 5. Comparison boards

`zoom` shows each sprite on a big numbered grid with its mirror axes, at 1x–3x on light and dark, and in greyscale. `sheet` puts the references beside each sprite, then shows the sprites at real size among the `--neighbor` sprites, on light and dark.

The boards I build:

- **The standard board** for every rev: the three commands in section 1.
- **The variants board**, when I'm stuck. Draw designs A, B and C and judge them together:

  ```bash
  python3 scripts/sprite_tool.py sheet tangerine-16-a.sprite tangerine-16-b.sprite tangerine-16-c.sprite --twemoji 1f34a --emoji 1f34a --out tangerine-16-abc.png
  ```

- **The progression board:** every rev so far, to check that each one really is better and that nothing good was lost on the way:

  ```bash
  python3 scripts/sprite_tool.py sheet tangerine-16-r1.sprite tangerine-16-r2.sprite --twemoji 1f34a --out tangerine-16-revs.png
  ```

- **The pair board:** the 16 and the 24 side by side, to check they're one emoji:

  ```bash
  python3 scripts/sprite_tool.py zoom tangerine-16-r2.sprite tangerine-24-r1.sprite --out tangerine-pair-zoom.png
  ```

  Check that they share the palette, the outline of the silhouette, the view, and every identifying feature. For a face, that's also the hairline's shape (arched, straight, M or parted), the mouth type and the extras. The 24 may add a trait or two, but it never contradicts the 16.

- **The portrait board:** add `--ref "PHOTO@X0,Y0,X1,Y1"` to `sheet` to put the cropped photo beside the sprite. `faces.md` §13 covers it.
- **The set board:** find neighbours with `find`, then pass two to four of them with `--neighbor`. It matches names, codes and categories (and keywords, when a `--set-dir` catalog has them), so a category such as `food` lists a whole shelf:

  ```bash
  python3 scripts/sprite_tool.py find food
  ```

  Choose neighbours of the same kind and a similar shape: other fruit for a fruit, other smileys for a face, `set:16:1f9d1` (person) and its man and woman variants for a portrait. More than four neighbours turns into noise.

Read a board in this order:

1. The real-size rows, on light and then on dark. Name it.
2. Your sprite beside Twemoji and the system emoji: the colour identity, the key cue and the view.
3. Your sprite among its neighbours: outline weight, saturation, fill and detail. If it looks heavier, darker, busier or smaller, it is.

## 6. The lint, rule by rule

`check` lints `.sprite` files, PNGs, `set:SIZE:CODE` and `MODULE.py:CODE` sources. It prints one summary line per sprite, then each `ERROR` and `warn`. It exits with status 1 if any sprite has an error. As its help says, lint is a gate, not a quality judgment.

The summary line reads `inner 7%  colours 6  span 15x15  mirror x+x'=16 (0 off)`:

- `inner` is the share of the silhouette that is inner ink.
- `colours` counts every distinct colour, including black.
- `span` is the width and height of the opaque area.
- `mirror` names the best left-right mirror axis and how many silhouette pixels break it.

Definitions the rules use:

- **Luminance** is 0.299 R + 0.587 G + 0.114 B.
- **Ink** is any opaque pixel with luminance under 40. So a near-black like #111111 still counts as ink, while the slate #262b30 (about 42) doesn't. That's why black materials use slate.
- **Outline ink** is ink that touches transparency or the canvas edge, counting the four side neighbours. **Inner ink** is all other ink.
- **The silhouette** is the set of opaque pixels.

### Errors: these must be fixed

| Rule | 16px | 24px | It means |
| --- | --- | --- | --- |
| Colour at the edge | A light pixel (luminance 70 or more) that isn't pure black touches transparency or the canvas edge, and isn't a 1px-thin line | Any pixel that isn't pure #000000 touches transparency or the canvas edge, including spikes, drips and tears | A gap in the outline. Ink every clear pixel beside colour. |
| Too small | The long side spans under 13px | The long side spans under 17px | It doesn't fill the canvas |
| Blotchy | Inner ink is over 22% of the silhouette | — | Black lines are muddling the inside |
| Doubled outline | 16 or more inner ink pixels sit right inside the outline | — | A second black ring. Repaint it with the material's dark tone. |
| A file that isn't a sprite | Partial transparency, or colour stored in transparent pixels | The same | Pixel art is binary. Every pixel is fully clear or fully opaque. |
| Skin far from the photo (only with `--skin` and `--face`) | The pixel-weighted average of the `--skin` keys is more than 15 luminance from the face average that `sample --face` prints for the same skin box | The same | The base came from a flash highlight or a shadow, or the ramp went onto the wrong keys. Rebuild the ramp from the base `sample --face` recommends. Never run it on a smiley-yellow variant. |

`check` also refuses to load a file with a malformed palette line, a key defined twice, `#` or `.` redefined, a row of the wrong width, an unknown key, a grid that isn't 16 or 24 rows, or an image with so many colours it's a photo. The message names the line.

### Warnings: look, then fix or explain

| Rule | 16px | 24px | It flags | It's right for |
| --- | --- | --- | --- | --- |
| Unoutlined 1px lines | Light edge pixels that are 1px thin (clear on both sides) | — | Bare 1px strokes | Flat effects (steam, rays, sparkles, motion) in a mid tone that reads on white and on dark |
| Dark pixels as their own edge | Non-black edge pixels darker than luminance 70 | — | A dark tone standing in for the outline | A thin dark stem, a leaf tip, a strand of hair, a whisker |
| Nearly too small | The long side spans 13px | 17 to 19px | Approved icons span 14–16 or 20–24 | A subject that's small by meaning (next row) |
| Small by meaning | Under 14px, with `scale: small` in the header or "small … square" or "small … diamond" in the name | Under 20px, the same | The size is deliberate | The set's graded small squares and diamonds |
| Inner ink | Over 12% | Over 22% | Too much black inside | Open mouths, dark lenses, eye sockets, line-art symbols |
| Hug | 7 to 15 inner ink pixels right inside the outline | 24 or more | A doubled outline or a black seam | Ink that separates two parts of similar value; dark-bodied objects at 24 |
| Black block | Any 2×2 block of inner ink | Any 3×3 block | A blotch | A hole, an open mouth, an eye socket, a dark lens |
| Lone specks | More than 2 ink pixels with no ink among their eight neighbours | The same | Noise | A pair of 1×1 eyes, a pupil, a nostril |
| Colours | More than 14 | More than 18 | Too many colours | Busy people with props; merge ramps where you can |
| Tone specks | More than 15% of the silhouette is single-pixel islands of a tone | The same | Dithering or noise | A deliberate dot pattern, such as a microphone grille |
| Equal value | 4 or more places where two saturated colours (saturation over 0.3, hues over 35° apart) with luminance within 14 touch | 6 or more | Colours that blur together at 1x and in greyscale. Make one lighter or darker, or ink the border. | Rarely right; look first |
| Nearly symmetric | 1 to 4 silhouette pixels break the best mirror | 1 to 6 | A symmetric subject placed by hand | A deliberately asymmetric subject; ignore it then |
| Palette notes | No `essence:` line; unused keys; a key darker than luminance 40; two keys with one colour | The same | `.sprite` housekeeping | — |

Notes on the mirror rule:

- It tries the axes x + x' = 14, 15 and 16 at 16px (22, 23 and 24 at 24px) and reports the best. An even sum has a one-pixel centre column (16 has its centre at x 8); an odd sum has a two-column seam (15 pairs x 7 with x 8).
- It compares the silhouette only, never colours, so upper-left light doesn't break it. A lit sphere can score `0 off`.
- It stays silent at `0 off` and above its limit, where it assumes the subject is meant to be asymmetric. Read the figure in the summary line yourself.

The bad files in `examples/lint-failures/` are for testing the lint. Each is the 16px smiley with one mistake. Check them all (the command exits 1, because they have errors):

```bash
python3 scripts/sprite_tool.py check "examples/lint-failures/*.sprite"
```

The output, verbatim:

```text
examples/lint-failures/blotch-16.sprite (16px): ERRORS  inner 34%  colours 6  span 15x15  mirror x+x'=16 (1 off)
   essence: 1f642 slightly smiling face: calm, friendly, the reference for every 16px face
   ERROR 34% of the drawing is black inside the silhouette: blotchy. Separate parts with tones and keep inner ink for holes, crevices, face features, overlaps of similar values and line-art symbols
   warn  11 inner black pixels sit right inside the outline (x,y): (3,10), (3,11), (4,12), (5,12), (11,12), (12,12) ... -- a doubled outline or a black seam? Use the material's dark tone instead
   warn  2x2 black block inside the shape at (x,y): (3,8), (4,8), (5,8) ... -- right for a hole, an open mouth, an eye socket or a dark lens; otherwise it's a blotch
   warn  nearly mirror-symmetric (axis x + x' = 16) but 1 pixel breaks it ((3,13)/(13,13)); fix it if the subject is symmetric, or name the reason in an 'asymmetric:' header line
examples/lint-failures/double-outline-16.sprite (16px): ERRORS  inner 20%  colours 6  span 15x15  mirror x+x'=16 (0 off)
   essence: 1f642 slightly smiling face: calm, friendly, the reference for every 16px face
   ERROR 22 inner black pixels sit right inside the outline (x,y): (4,2), (12,2), (3,3), (13,3), (3,4), (13,4) ... -- a doubled outline. The outline is one pixel thick; repaint the inner ring with the material's dark tone
   warn  20% inner black (about 95% of approved 16px icons stay under 12%): name the reason for every inner ink pixel or repaint it with the part's darkest tone
examples/lint-failures/no-outline-16.sprite (16px): ERRORS  inner 9%  colours 6  span 13x14  mirror x+x'=16 (0 off)
   essence: 1f642 slightly smiling face: calm, friendly, the reference for every 16px face
   ERROR 29 light pixels touch transparency or the canvas edge (x,y): (6,1), (7,1), (8,1), (9,1), (10,1), (4,2) ... -- the silhouette needs its 1px '#' outline
   warn  4 lone black specks (x,y): (5,1), (11,1), (5,13), (11,13) -- a pair of 1x1 eyes, a pupil or a nostril is fine; more is noise
examples/lint-failures/tiny-16.sprite (16px): ERRORS  inner 0%  colours 2  span 9x9  mirror x+x'=16 (0 off)
   essence: 1f642 slightly smiling face: calm, friendly, the reference for every 16px face
   ERROR the subject spans only 9x9px; fill the canvas (14-16px on the long side)
   warn  palette keys never used: S W t u
```

Look at `no-outline-16`: it lost its outline, and the four ink pixels left over from it now stand alone as specks. One mistake can raise several messages. Fix the ERROR first and run `check` again.

## 7. The lint on approved art

I calibrated every threshold on kirupa.com's 1,948 approved drawings at each size. If approved art fails, the lint is wrong, not the art.

| | 16px | 24px |
| --- | --- | --- |
| Drawings that raise an error | 0 | 0 |
| Drawings with no warning at all | 1,439 (73.9%) | 1,616 (83.0%) |
| Colours: median, 95th percentile, max | 7, 14, 20 | 8, 17, 22 |
| Inner ink: median, 95th percentile, max | 2%, 12%, 22% | 4%, 20%, 73% |
| Long-side span: 5th percentile, median | 15, 16 | 22, 23 |

How often each warning fires on approved art (out of 1,948):

| Warning | 16px | 24px |
| --- | --- | --- |
| Tone specks | 95 | 68 |
| Inner ink | 87 | 81 |
| Equal value | 85 | 83 |
| Hug | 79 | 85 |
| Colours | 78 | 7 |
| Black block | 57 | 113 |
| Nearly symmetric | 43 | 32 |
| Dark pixels as their own edge | 41 | — |
| Unoutlined 1px lines | 39 | — |
| Lone specks | 23 | 7 |
| Span (including small by meaning) | 9 | 10 |

So a warning on its own isn't a verdict. Here are approved drawings that warn, with `check` output verbatim, and the reason each warning is right:

```text
set:16:1f600 (16px): ok  inner 14%  colours 8  span 15x15  mirror x+x'=16 (0 off)
   warn  14% inner black (approved 16px icons stay under 12%): name the reason for every inner ink pixel or repaint it with the part's darkest tone
set:16:1f60e (16px): ok  inner 20%  colours 7  span 15x15  mirror x+x'=16 (0 off)
   warn  20% inner black (approved 16px icons stay under 12%): name the reason for every inner ink pixel or repaint it with the part's darkest tone
   warn  2x2 black block inside the shape at (x,y): (4,4), (5,4), (6,4) ... -- right for a hole, an open mouth, an eye socket or a dark lens; otherwise it's a blotch
set:16:1f973 (16px): ok  inner 7%  colours 13  span 16x16  mirror x+x'=16 (25 off)
   warn  2 pixels of unoutlined 1px lines (x,y): (13,0), (1,15) -- right only for flat effects (steam, rays, sparkles, motion) in a mid tone that reads on white and dark
set:16:25aa (16px): ok  inner 0%  colours 2  span 7x7  mirror x+x'=16 (0 off)
   warn  the subject spans 7x7px, allowed because it is small by meaning ('small' in its name or 'scale: small'); keep the set's graded sizes
set:16:1f92a (16px): ok  inner 21%  colours 10  span 15x16  mirror x+x'=16 (3 off)
   warn  21% inner black (approved 16px icons stay under 12%): name the reason for every inner ink pixel or repaint it with the part's darkest tone
   warn  nearly mirror-symmetric (axis x + x' = 16) but 3 pixels break it ((5,14)/(11,14), (6,15)/(10,15), (7,15)/(9,15)); fix them if the subject is symmetric
set:16:2620 (16px): ok  inner 12%  colours 6  span 16x16  mirror x+x'=15 (0 off)
   warn  12% inner black (approved 16px icons stay under 12%): name the reason for every inner ink pixel or repaint it with the part's darkest tone
   warn  8 inner black pixels sit right inside the outline (x,y): (4,4), (11,4), (4,11), (11,11), (4,13), (6,13) ... -- a doubled outline or a black seam? Use the material's dark tone instead
set:16:1f646 (16px): ok  inner 8%  colours 14  span 16x16  mirror x+x'=15 (0 off)
   warn  20 dark pixels are their own edge (x,y): (3,3), (4,3), (11,3), (12,3), (2,4), (13,4) ... -- right for a thin dark stem, leaf tip, strand of hair or whisker; otherwise outline it
set:24:1f480 (24px): ok  inner 20%  colours 6  span 22x21  mirror x+x'=23 (0 off)
   warn  3x3 black block inside the shape at (x,y): (5,8), (6,8), (15,8) ... -- right for a hole, an open mouth, an eye socket or a dark lens; otherwise it's a blotch
set:16:1f9d1-200d-1f393 (16px): ok  inner 9%  colours 15  span 16x16  mirror x+x'=16 (7 off)
   warn  15 colours; nearly all approved 16px icons use 14 or fewer (median 7). Merge ramps
```

- **1f600, grinning face:** the open mouth is drawn in ink round its teeth, a face feature.
- **1f60e, sunglasses:** the lenses are dark glass, so a black block is right.
- **1f973, partying face:** the two bare pixels are confetti, a flat effect. The hat and confetti make it asymmetric, so the mirror stays silent.
- **25aa, small black square:** small by meaning. It belongs to a graded series of squares.
- **1f92a, zany face:** the wild eye and the tongue make it asymmetric on purpose. The 3 mirror breaks are the tongue.
- **2620, skull and crossbones:** the inner ink separates white bone from the white skull (an overlap of similar values) and draws the teeth.
- **1f646, person gesturing OK:** the raised arms leave 1px gaps beside the head. Ink there would close the gaps, so the arms' dark shade is their edge.
- **1f480 at 24, skull:** the eye sockets are holes.
- **The graduate, 1f9d1-200d-1f393:** skin, hair, gown, cap and tassel need a 15th colour.

The microphone shows the other side. The approved 16px mic warns `26 single-pixel tone specks`: its grille is a deliberate dot pattern. The old mic it replaced, which looked curved, passed with no warnings at all (`worked-examples.md` §5).

To study any approved drawing, copy it into your work folder and lint it as if it were yours:

```bash
python3 scripts/sprite_tool.py text set:16:2620 --out study-skull-16.sprite
python3 scripts/sprite_tool.py check study-skull-16.sprite
```

## 8. What the lint can't see

Every one of these passed `check`. Only looking caught them.

- **Whether it reads as the subject,** or as a face, letters, a cross or a crown.
- **Squished proportions.** The tangerine's first body was 14 wide and 11 tall. Lint passed it; Kirupa asked for it "more round and less squishy".
- **A straight line that reads curved.** The old microphone passed with no warnings. Kirupa: "the microphone doesn't look good. It looks curved."
- **Lumpy curves.** Lint doesn't check that runs grow and shrink monotonically. Count them on the 8x grid.
- **Light direction, and bevels on flat things.** Lint doesn't know where the light is or which parts are flat.
- **Colour identity and essence** compared with Twemoji and the system emoji.
- **Harmony with the set.**
- **Expression and likeness.** `check --skin --face` checks only the skin's tone. The blind test and someone who knows the person check the likeness.
- **Whether the 16 and the 24 agree.**
- **Whether an inner black pixel's reason is real.** Lint counts inner ink; you have to name each pixel's reason.

## 9. Failures and their fixes

Every row here is a mistake I made. Where Kirupa named it, his words are in `lessons.md`. Rows marked "review note" came from my own review passes, not from Kirupa.

### Reading and essence

| You see | Why it happens | Fix |
| --- | --- | --- |
| Mush, smeared detail, broken 1px slivers | The art was converted, traced or downsampled from Twemoji | Redraw by hand from the essence. A `draft` is for proportions only. |
| Every detail squeezed in, nothing readable | Detail kept because it fits | Write essence, keep and drop first, then delete everything that doesn't serve the essence |
| A 3D emoji turned to mud | Perspective and soft shading can't survive the grid | Reinterpret it: a side profile like the coffee mug, or a front elevation |
| It reads as something else: letters, a crown, a comb | Hollow ink loops, or upright shapes in a row (review notes) | Use solid shapes, change the pose or view, and re-check at 1x |
| People read as crosses and headstones | Plus-shaped heads and square bodies (review note) | Use solid square heads, trimmed only at the corners when larger, and rounded shoulders |
| A face that nobody drew | Two dark blobs over a centre dot or a line (review note on the radioactive sign) | Break the pattern: square up the blades, change the spacing or the value |
| A pose that reads as a dome or a helmet | A front view hides the action (review note on the bowing person) | Turn it to a side profile that shows the action |
| Two small things that read as nothing | Twemoji shows a pair; at 16 each is too small | Show one big item (one paw print, one microphone) |

### Silhouette and outline

| You see | Why it happens | Fix |
| --- | --- | --- |
| Colour touching transparency | A missing outline pixel | Ink every clear pixel beside colour (lint: "touch transparency") |
| A separate piece that bleeds into its neighbour | Only the outer silhouette was outlined | Give every important piece its own full outline |
| A heavy double border | A black ring inside the outline | Use the material's dark tone instead (lint: "hug") |
| A clean outline round a messy inside | The outline was treated as the whole job | Draw the inside with the same care: tones, not lines |
| A lumpy circle or an octagon | Runs that don't grow and shrink monotonically | Use a circle profile from `construction.md` |
| A squished or shrunken body | Accessories (stems, leaves, hands, props) took the body's pixels | Draw the full body first; put accessories outside it; measure the body alone |
| A straight part that reads curved | Uneven steps, or a diagonal mixed with straight runs | Use one consistent 1:1 or 2:1 diagonal that touches only at corners; widen the shape so it reads as a solid bar |
| A jaggy, thick diagonal | L-joins and doubled corners | Remove the extra corner pixel so steps touch diagonally |
| A lopsided symmetric subject | Both halves placed by hand | Draw one half and `mirror` it; `check` lists the breaking pixels |
| Square, boxy torsos | Rectangles for bodies (review note) | Slope the shoulders and round the bottom corners |
| It's smaller or lighter than its neighbours | No set check | Fill the canvas; compare on a set board |

### Inside, colour and light

| You see | Why it happens | Fix |
| --- | --- | --- |
| Blotchy black lines muddling the inside | The 24px habit of inking between every pair of parts | Apply the five-reasons test; recolour the rest with dark tones |
| Parts that merge into each other | Equal values (lint: "equal value") | Make one clearly lighter or darker, or ink the border if it's an overlap |
| Low contrast; detail you can't read | Timid ramps | Maximise contrast between neighbouring parts, as Darkproject does |
| Grey mud, or too many colours | Unshifted ramps, one ramp per part | Use hue-shifted `ramp`s shared across one material, within the budget |
| A black hat, cat or camera vanishes | Pure black fill against the black outline | Use the slate ramp: #66717c light, #3a4148 base, #30363c shade, #262b30 deep (hair keys `H h d k`) |
| Speckled noise | Dithering, single-pixel tone specks | Use runs of two pixels or more for each tone |
| A bevel on a beam, flag, sign or screen | Light applied to everything | Keep the flat list flat |
| A flat, lifeless solid | No light ramp | Light it from the upper left: a crescent, bands or faces |
| Flattened leaves and petals | Over-applying the flat rule | Leaves, petals and stems are solid: a lit half and a shaded half along the midrib |
| A smiley that looks off-colour beside Darkproject's | The wrong yellow | Use the house yellows from the templates |

### Faces and people

| You see | Why it happens | Fix |
| --- | --- | --- |
| Uncanny eyes | 2×2 blobs, whites and highlights squeezed in | Use the house eyes. Eyes are 1px wide on smileys and on 16px people (1×3 smiley and 1×2 person at 16; 1×5 smiley at 24); 24px people use 2×3 (2×2 in a bust or behind glasses). |
| Mismatched eyes | Each eye drawn by hand | Make them identical, mirrored, unless the expression differs |
| Eyes thicker than the set's | Doubling the 16 to make the 24 | Use the 24px house size above: a smiley's eyes grow taller (1×5), never wider |
| Tears like earrings, or drooping | Drops hanging straight down from the eye | Stream them outward from the squeezed eyes, as in the source emoji |
| A wild eye that doesn't read | Two different eye styles muddled | Give the odd eye a white with a black pupil |
| A portrait that's generic | No distinguishing traits chosen | Pick three to five traits visible in the photo, most important first in `keep:`, and give them pixels |
| A portrait that mocks | Traits exaggerated past the photo | Keep proportions true; use the respect checklist in `faces.md` §14 |
| A portrait's skin lighter than the person's | The base was sampled from a flash highlight or shine | `sample --face` on the most evenly lit photo, ramp its base onto `S s t u`, then pass `check --skin --face` |
| A portrait's big grin that nobody reads | The grin was enlarged, or squeezed into rows the head doesn't have | Use the kit grin at the kit's width (`faces.md` §10). A kit grin's width is a house shape, not an enlarged feature. |
| A portrait whose face is the wrong shape | The template's jaw kept, or reshaped by eye | Use a round, oval or long jaw from `faces.md` §10, at most 1px per side from the template |
| A blind reviewer says "helmet" | Dark hair on the person-head template | Expected: the approved control reads the same way. Ignore it when the control gets it too (section 2). |

### Flags and marks

| You see | Why it happens | Fix |
| --- | --- | --- |
| Paw prints nobody recognises | Toes merged into the pad, two small prints | One big print: four separate, fully outlined toes above a big lobed pad |
| Flags that look wrong | Stripes and stars eyeballed, shading on cloth | Count the stripes and stars, keep the field flat, use the shared stamps (`construction.md`) |

### Process

| You see | Why it happens | Fix |
| --- | --- | --- |
| It looked fine at 8x and fails at 1x | Judging zoomed in | Judge at 1x first, every pass |
| Rev 5 is worse than rev 2 | Polishing without comparing | Put every rev on a progression board |
| The owner is surprised by a change | Shipping without approval | Present proposals and let the owner choose |

## 10. Revisions, proposals and hand-off

- **Name every rev and keep it:** `NAME-SIZE-r1.sprite`, `-r2`, and so on. Never overwrite a rev. Kirupa: "Keep incrementing the rev for those versions so that we can see the progression." Name branches `-a`, `-b`, `-c`.
- **Show proposals; don't replace silently.** Kirupa: "Create the proposals but don't make the change to the main list. Show me for evaluation first."
- **Present a board, not a description.** Show every candidate with Twemoji, the system emoji and the neighbours, at 1x on light and dark. Say which one you'd pick, in one sentence why, and what `check` says about it.
- **Take feedback at 1x literally.** When Kirupa said the microphone "looks curved", the grid said it was straight. At 1x it looked curved, and 1x is what people see. Fix what the viewer sees, not what the grid says.
- **Fix the whole class, not the one sprite.** When a critique names one drawing, find every drawing with the same mistake. Kirupa: "Generalize your learnings for all emojis. Not just the bread themed ones."
- **Deliver** the `.sprite` files, plus `render` PNGs at 1x and 8x for each size, as SKILL.md Step 14 shows.
- **Label a portrait honestly.** Say which file is the real-tone likeness and which is the smiley-yellow variant, give the blind result (how many of three reviewers named which traits), and mark it "unverified" until someone who knows the person has recognised it.

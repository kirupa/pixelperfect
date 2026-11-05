# Worked portrait: Kirupa Chinnathambi

Kirupa taught me pixel art from first principles, so his face became this skill's acceptance test. An agent that had never seen my lessons drew it by following only `SKILL.md` and its references. These are its final drawings, with the commands to repeat every step for anyone whose photos are public.

| File | What it is |
| --- | --- |
| `kirupa-16.sprite` | 16px in his sampled skin tone: round 11 ("G2"), the version promoted |
| `kirupa-24.sprite` | 24px in his sampled skin tone: round 3 |
| `kirupa-16-yellow.sprite`, `kirupa-24-yellow.sprite` | The set variants: only the skin keys `S s t u` are swapped to smiley yellow |

The grids and palettes are in the `.sprite` files. Each file's `note:` line records what changed in every round and why the failed rounds failed. These drawings are artwork under the free license in [`assets/LICENSE.md`](../../assets/LICENSE.md), not the MIT license that covers the code.

## The photos

Both are published on kirupa.com and referenced by URL; no photo is stored in this repository. The tool downloads each one once into its cache (`PIXELPERFECT_CACHE`).

| Photo | What it shows | Face box | Skin box |
| --- | --- | --- | --- |
| https://www.kirupa.com/about/kirupa_bio_pic_png.png (703×808) | A large, front-facing face: the dipped fringe, the short sides at ear level, the oval jaw. Flash-lit, with a surprised expression | `265,225,470,480` | `300,375,445,410` |
| https://www.kirupa.com/images/kirupa_headshot.png (378×154) | The grin with teeth and the volume of hair on top | `10,0,90,95` | not used |

The skill says to sample the most evenly lit photo and never a flash photo. The bio photo is flash-lit, but it's the only large, front-facing one. That's the case `sample --face` exists for: it flags the flash cluster and leaves it out of the face average.

## The steps

Run these from the skill folder (the one that holds `SKILL.md`). Bare `--out` names go to the work folder, `PIXELPERFECT_WORK` (default `~/pixelperfect-work`). On Windows, type `py` instead of `python3`.

1. **Study the faces.** Crop each photo to the face and look at it, as SKILL.md Step 12 asks:

   ```bash
   python3 scripts/sprite_tool.py crop "https://www.kirupa.com/about/kirupa_bio_pic_png.png@265,225,470,480" --scale 2 --out kirupa-face.png
   python3 scripts/sprite_tool.py crop "https://www.kirupa.com/images/kirupa_headshot.png@10,0,90,95" --scale 4 --out kirupa-headshot.png
   ```

2. **Choose the traits a stranger can name at 1x.** The `keep:` lines put them first: short dark hair and a big toothy grin. The 24 adds his thick, straight brows. Everything else is dropped, including the nose, the stubble, the surprised moment and the flash lighting.

3. **Sample the skin and build the ramp.**

   ```bash
   python3 scripts/sprite_tool.py sample "https://www.kirupa.com/about/kirupa_bio_pic_png.png" --box "300,375,445,410" --face
   python3 scripts/sprite_tool.py ramp "#c28164" --hue 3 --value 0.09 --up 1
   ```

   On this box, `sample --face` prints a face average of `#b87a5f` (luminance 137.4) and recommends the base `#c28164`. The drawings' base, `#cb8d71`, was picked by hand from a larger box before `--face` existed. Both drawings still pass the skin check below. For a new portrait, take the tool's base.

4. **Start each size from its own person-head template.** Never resize one size into the other.

   ```bash
   python3 scripts/sprite_tool.py new kirupa-16 --size 16 --template person-head-16 --out kirupa-16-r1.sprite
   python3 scripts/sprite_tool.py new kirupa-24 --size 24 --template person-head-24 --out kirupa-24-r1.sprite
   ```

5. **Lint, with the skin check.** The drawn skin must average within 15 luminance of the photo's face:

   ```bash
   python3 scripts/sprite_tool.py check examples/kirupa-portrait/kirupa-16.sprite examples/kirupa-portrait/kirupa-24.sprite --skin "S,s,t,u" --face "https://www.kirupa.com/about/kirupa_bio_pic_png.png@300,375,445,410"
   ```

   Both pass. The 16's skin is 12.2 lighter than the face average and the 24's is 13.4 lighter. The 16's one mirror break is the notch at (7,0), accepted by its `asymmetric:` header.

6. **Review against the photos and the approved neighbours.**

   ```bash
   python3 scripts/sprite_tool.py zoom examples/kirupa-portrait/kirupa-16.sprite examples/kirupa-portrait/kirupa-24.sprite --out kirupa-zoom.png
   python3 scripts/sprite_tool.py sheet examples/kirupa-portrait/kirupa-16.sprite examples/kirupa-portrait/kirupa-24.sprite --ref "https://www.kirupa.com/about/kirupa_bio_pic_png.png@265,225,470,480" --ref "https://www.kirupa.com/images/kirupa_headshot.png@10,0,90,95" --neighbor set:16:1f9d1 --neighbor set:16:1f600 --neighbor set:24:1f9d1 --neighbor set:24:1f600 --out kirupa-board.png
   ```

7. **Run the blind test** with approved controls shuffled in, as in [`review.md`](../../references/review.md) section 2:

   ```bash
   python3 scripts/sprite_tool.py blind examples/kirupa-portrait/kirupa-16.sprite --control set:16:1f9d1 --control set:16:1f600 --out kirupa-blind-r1
   ```

   For a real skin tone, also add a skin-matched control. Copy an approved shape with `text set:16:1f600 --out ctrl-1f600.sprite`, then change only its skin colours to yours.

8. **Make the set variants** by swapping only `S s t u` to smiley yellow: `#ffff93 #ffe600 #ffbf00 #f08e00`.

The full procedure is in SKILL.md Step 12 and [`faces.md`](../../references/faces.md) section 13.

## What the final drawings do

- **16 (round 11).**
  - **Hair:** short, in lit slate clumps, with sideburns running down to the ears.
  - **Notch:** the one at (7,0) splits the top into two clumps for the volume in the headshot.
  - **Eyes:** 1×2, at x6 and x10 on rows 6–7.
  - **Grin:** the house four-row grin from approved 1f601, one row lower than on the smiley head:
    - an ink lip at x4–12 on row 9;
    - white upper teeth at x5–11 on row 10;
    - light-grey lower teeth `#cfd6e6` at x6–10 on row 11;
    - an ink base at x6–10 on row 12.
  - **What failed:**
    - Rounds 2–5 used 1f600's dark mouth interior, and reviewers didn't read it as teeth.
    - Round 8's 2px cheeks made the grin read neutral.
- **24 (round 3).**
  - **Fringe:** the ink rises to row 7.
  - **Brows:** 4×1 in the deepest hair slate, on row 10 at x7–10 and x13–16, with one skin row above the 2×3 eyes on rows 12–14.
  - **Jaw:** oval; it narrows below the mouth on rows 19–22.
  - **Grin:** a crescent:
    - ink corners at x7 and x16 on row 17;
    - teeth at x9–14 on row 18;
    - an ink base at x9–14 on row 19.

## Grades and caveats

| Drawing | Grade | Notes |
| --- | --- | --- |
| 16, real tone | **A+ on the rubric, with a caveat** | It met the blind pass rule in two rounds running: rounds 6–7 named the dark hair 3 of 3 and the toothy grin 2 of 3. In rounds 8–10 the teeth were named 1 of 3, the same as an approved 1f600 control recoloured to his skin. So the grin reads as well as the house shape does in this skin, and no better. |
| 24, real tone | **A+ on the rubric** | A blind reviewer called it "a smiling person with dark hair" and named a "very broad toothy smile" and a "blunt dark hairline". In a blind pair test, 3 of 3 reviewers said the 16 and the 24 are the same emoji. |
| 16, yellow | **A** | Over two rounds, 5 of 6 reviewers read it as wearing sunglasses or glasses. The slate sideburns beside the eyes make a dark band at eye level on yellow. The fix, trimming or lightening the hair at eye level on the yellow only, is in faces.md section 13 step 13. It isn't applied here, so the variant stays in sync with the real-tone file. |
| 24, yellow | graded with the real-tone 24 | Only the skin keys differ. |

Over 15 blind reads of the final 16, reviewers named dark hair 13 times, a big grin 12 times and teeth 7 times.

- **Reviewer bias.** Some reviewer models misread darker skin, even as an animal face. Skin-matched controls drew the same misread, so it follows the skin, not the drawing. Never change a sampled skin tone because of it; a person makes the respect and likeness call.
- **Likeness: unverified.** Strangers name the traits, but nobody who knows Kirupa has yet confirmed that the drawing reads as him. The traits are true to him but common, so expect it to read as Kirupa in context, next to his name, rather than on its own.

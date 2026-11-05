# Faces, people and portraits

Faces are where I failed hardest. My first smileys were shrunken Twemoji with mushy eyes, and Kirupa put it bluntly: "The eyes in all of your smileys are uncannily bad." He sent me a zoomed-in Darkproject smiley and pointed at what I'd missed: "Notice the clean outlines in black that are noticeable." A face is read from fewer than twenty pixels, so every one of them has to be deliberate.

This file is the whole face kit: the rules, the 16px and 24px heads, every eye, brow and mouth stamp with its coordinates, the published smileys as recipes, animals, people, hair, skin, glasses, beards, and the procedure for drawing a real person from a photo. Grids marked **approved** are copied from kirupa.com's published set; print any of them with `python3 scripts/sprite_tool.py text set:16:CODE` or `set:24:CODE`.

Contents:

1. Rules every face follows
2. The 16px head
3. The 16px face kit
4. Approved 16px smileys, read closely
5. Hats, halos and props
6. The 24px head and kit
7. Approved 24px smileys, read closely
8. Hands on faces
9. Animal faces, and faces on things
10. People: heads, busts and hair
11. Skin
12. Facial hair and glasses
13. Portraits of a real person from a photo
14. The portrait addendum
15. The face checklist
16. Appendix: every published smiley as a recipe

## 1. Rules every face follows

- **Eyes are 1px wide on smileys and on 16px people** (1×3 smiley and 1×2 person at 16; 1×5 smiley at 24); **24px people use 2×3** (2×2 in a bust or behind glasses, such as 1f935 and the nerd's pupils). They're vertical and solid black. Kirupa: "For the smileys, notice that the darkproject smileys for the vertical eyes are just one pixel thick. Mimic that so that these look harmonious when placed SxS to them." Tiny full figures, whose heads are only a few pixels, use 1×1 at 16 and 1×2 at 24. No whites, irises or highlights at 16px, except where the expression is the eye (round shocked eyes, pleading eyes, the zany face).
- **The two eyes are identical.** Kirupa: "For faces, there are two eyes and they should look identical unless there is an expression being shown." Of an octopus I drew: "It looks unnecessarily bad because both the eyes are off." Plain bars are symmetric, so mirroring and copying give the same result. Shapes with a lit side are *translated* copies, so both eyes are lit from the same side: hearts (1f60d) and stars (1f929) at both sizes, and the catch-lights of 1f97a, the cat and the dog at 24px. The one mirrored exception in the published set is 1f97a at 16px, whose two catch-light pixels face the nose.
- **Only an expression changes an eye,** and then it changes on purpose: a wink, squeezed `> <` eyes, hearts, stars, crosses, a raised brow. Two eyes that differ by accident read as broken, not expressive.
- **When one eye gets a white, both do.** Kirupa, on the zany face: "wouldn't it be better to have the left eye also have a white background with a black eye?" Mismatched eye sizes are fine when that's the expression; mismatched construction isn't.
- **A mouth is one line.** A smile is two corner pixels and a short line one row lower. An open mouth is an outlined hole: at 16px it holds at most two rows inside (white teeth over a dark mouth, or a dark mouth over a red tongue). At 24px it can hold three or four.
- **No nose, no ears on smileys, and no brows unless the expression needs them** (worry, anger, a raised brow, surprise), or, at 24 only, a portrait whose photos plainly show strong brows (section 10). People get ears only where the hair leaves room: 1px bumps in the silhouette at 16, rim-tone ears boxed by ink at 24.
- **The head is lit on the rim, not shaded across.** The upper-left rim is the light tone, the lower-right rim is one or two shade tones, and everything else is the flat base. A glint is one pixel at 16 and three at 24, at the upper left. No gradients across a face, no cheek shading.
- **Smiley yellow is the Darkproject ramp.** Kirupa: "For the smileys, match the yellow tone of the darkproject yellow smilies." Use `#ffffcf` glint, `#ffff93` light, `#ffe600` base, `#ffbf00` rim shade and `#f08e00` deep shade, and nothing else on the head.
- **Extras are separate objects** with their own small ramps. Tears, sweat, hearts, hands, hats and halos carry ink where they meet transparency. Against the face, use ink when the two values are close (an orange hand at 24, a hat brim) and a tone change when they're far apart: red hearts and blue tears on yellow need no ink at 16. They never share the head's shading.
- **Tears fly outward.** Kirupa, on rolling on the floor laughing: "the tear drops should be going outward like in the original source version. The shouldn't be going straight down. It looks like an earring right now." And at 24px: "fix the 24x24 similarly to ensure the tears don't look like they are drooping." A tear leaves the corner of the eye and travels away from the face, along the direction of the tilt or the force of the laugh.
- **Reinterpret rather than render.** Kirupa: "It is ok to reinterpret the intent, kind of like coffee. fully 3D is hard in pixel art. But that doesn't mean the ice cube has to look bad either." A tilted, laughing head is a rotated silhouette with pixel-clean features, not a 3D render.
- **Accidental faces are a bug.** Any two level dark dots with something below them read as a face. A review note on a radioactive sign: "at 1x the rounded blobs + center dot read as a FACE (two eyes, nose, mouth)." When a subject isn't a face, break that read.

## 2. The 16px head

Every 16px smiley starts here. The head is a 15px stepped circle on columns 1–15 and rows 0–14, so a symmetric face mirrors on axis 16 (`x' = 16 − x`), and column 8 is the centre. Row 15 stays empty; tears, tongues and hands may break into it.

```text
name: smiley-head-16
size: 16
essence: a round yellow head lit from the upper left: the base every 16px smiley starts from
keep: the 15px stepped circle, S rim upper left, t and u rim lower right, one W glint
drop: everything else; eyes, mouth and extras go on per subject
view: front
note: the 15px round head on columns 1-15 (mirror axis x + x' = 16); features go on with ink

[palette]
u #f08e00 skin deep shade
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)
W #ffffcf glint (one pixel)

[grid]
......#####.....
....##SSSSs##...
...#SSsssssss#..
..#SWsssssssss#.
..#Sssssssssss#.
.#Sssssssssssst#
.#Sssssssssssst#
.#Sssssssssssst#
.#Ssssssssssstu#
.#ssssssssssstu#
..#ssssssssstu#.
..#ssssssssttu#.
...#sssssttuu#..
....##tttuu##...
......#####.....
................
```

```bash
python3 scripts/sprite_tool.py new grinning --template smiley-head-16 --out grinning-16-r1.sprite
```

Then stamp the features from the kit below. Leave the rim exactly as it is: the published smileys all share it, so a face drawn on this head sits beside them without a seam.

## 3. The 16px face kit

These are the stamps the published smileys are built from, copied from kirupa.com's drawing modules. Each one lists the columns and rows it covers on the 16px head, and the colours it uses besides ink. Inside a stamp, `.` means "leave the head pixel as it is", not transparency. Copy a stamp's rows into your grid starting at its first column and row.

**Eyes.** `FACE_EYES` is the default: two 1×3 bars on columns 6 and 10. Everything else is an expression.

```text
FACE_EYES: x 6-10, rows 4-6
    #...#
    #...#
    #...#
EYES_BIG: x 6-10, rows 3-6
    #...#
    #...#
    #...#
    #...#
EYES_LOW: x 6-10, rows 5-6
    #...#
    #...#
EYES_HAPPY: x 4-12, rows 4-5
    .##...##.
    #..#.#..#
EYES_SHUT: x 4-12, rows 5-6
    #..#.#..#
    .##...##.
EYES_SQUINT: x 5-11, rows 4-6
    #.....#
    .##.##.
    #.....#
EYE_WINK: x 9-12, rows 4-5
    .##.
    #..#
EYE_WINK_LEFT: x 4-7, rows 4-5
    .##.
    #..#
EYES_ROUND: x 3-13, rows 4-8  (w #ffffff)
    .###...###.
    #www#.#www#
    #w#w#.#w#w#
    #www#.#www#
    .###...###.
EYES_PUPPY: x 3-13, rows 5-8
    .##.....##.
    ####...####
    ####...####
    .##.....##.
EYES_X: x 5-11, rows 4-6
    #.#.#.#
    .#...#.
    #.#.#.#
GLARE: x 5-11, rows 3-6
    ##...##
    .##.##.
    .#...#.
    .#...#.
HEART_EYES: x 3-13, rows 3-6  (p #ff8f8f, R #c8283a, r #ef3349)
    pr.rr.pr.rr
    rrrrr.rrrrr
    .rrR...rrR.
    ..R.....R..
STAR_EYES: x 3-13, rows 2-6  (O #c9452a, o #f4683a)
    ..o.....o..
    ..o.....o..
    ooooo.ooooo
    .ooO...ooO.
    .o.O...o.O.
```

- `EYES_HAPPY` (`^ ^`) is the smiling, closed eye; `EYES_SHUT` is the same shape flipped, for sleep and calm.
- `EYES_SQUINT` is the squeezed `> <` of laughing and wincing.
- `EYES_ROUND` gives both eyes whites with a pupil (1f633, flushed). `EYES_PUPPY` is two rounded 4×4 ink blobs; 1f97a adds two white catch-light pixels to each. They are the only blob eyes in the set, and they exist because the expression is the eye.
- Hearts and stars are translated copies, so both eyes are lit from the same side.

**Brows.** Only when the expression needs them. They sit one or two rows above the eyes and never touch them.

```text
BROWS_WORRIED: x 5-11, rows 2-3
    .##.##.
    #.....#
BROWS_ANGRY: x 5-11, rows 3-4
    ##...##
    .##.##.
BROWS_ARCHED: x 4-12, rows 3-4
    .##...##.
    #..#.#..#
BROWS_UP: x 4-12, rows 3-4
    .##...##.
    #.......#
```

**Mouths.** `MOUTH_SLIGHT` is the default calm smile. Count the rows inside every open mouth: one or two, never more.

```text
MOUTH_SLIGHT: x 5-11, rows 9-10
    #.....#
    .#####.
MOUTH_SMILE: x 4-12, rows 8-10
    #.......#
    .#.....#.
    ..#####..
MOUTH_FLAT: x 6-10, row 10
    #####
MOUTH_FROWN: x 5-11, rows 9-10
    .#####.
    #.....#
SMALL_FROWN: x 6-10, rows 10-11
    .###.
    #...#
MOUTH_O_SMALL: x 7-9, rows 9-11  (m #8a2c1a)
    .#.
    #m#
    .#.
MOUTH_O: x 6-10, rows 9-12  (m #8a2c1a)
    .###.
    #mmm#
    #mmm#
    .###.
MOUTH_GRIN: x 4-12, rows 8-11  (m #8a2c1a, w #ffffff)
    #########
    #wwwwwww#
    .#mmmmm#.
    ..#####..
MOUTH_TEETH: x 4-12, rows 8-11  (e #cfd6e6, w #ffffff)
    #########
    #wwwwwww#
    .#eeeee#.
    ..#####..
TEETH_CLENCHED: x 4-12, rows 8-11  (e #cfd6e6, w #ffffff)
    .#######.
    #w#w#w#w#
    #e#e#e#e#
    .#######.
MOUTH_TONGUE: x 4-12, rows 8-12  (R #c8283a, r #ef3349)
    #########
    ..#rrr#..
    ..#rRr#..
    ..#rrr#..
    ...###...
MOUTH_KISS: x 7-9, rows 8-12
    ##.
    ..#
    ##.
    ..#
    ##.
MOUTH_WAVY: x 4-12, rows 10-11
    .##...##.
    #..###..#
GROAN: x 5-11, rows 8-11  (m #8a2c1a, w #ffffff)
    ..###..
    .#www#.
    #mmmmm#
    #######
NERD_TEETH: x 5-11, rows 9-11  (G #9aa6b4, w #ffffff)
    #.....#
    .#wGw#.
    ..###..
```

**Extras.** Tears, sweat, blush, halos and hands. Each carries its own ink where it leaves the head.

```text
TEAR: x 11-14, rows 7-11  (B #3fa9f0, b #b8e6ff, N #2273c3)
    b...
    .b..
    .BB.
    ..BB
    ..NN
TEAR_STREAK: x 9-15, rows 0-4  (B #3fa9f0, b #b8e6ff, N #2273c3)
    ...##..
    ...bb#.
    bbbBBB#
    .BBBBN#
    ...BN#.
TEARS_JOY: x 1-15, rows 6-14  (B #3fa9f0, b #b8e6ff, N #2273c3)
    ..bb.......bb..
    .bB.........Bb.
    .bB.........Bb.
    .bB.........Bb.
    #bB.........Bb#
    #bBB.......BBb#
    #BBN.......NBB#
    .#N.........N#.
    ..#.........#..
STREAMS: x 4-12, rows 7-12  (B #3fa9f0, b #b8e6ff, N #2273c3)
    bB.....Bb
    bB.....Bb
    bB.....Bb
    bB.....Bb
    bB.....Bb
    BN.....NB
SWEAT: x 12-15, rows 0-4  (B #3fa9f0, b #b8e6ff, N #2273c3)
    .#..
    .b#.
    bBB#
    BBN#
    .N..
BLUSH: x 3-13, row 7  (p #ff8f8f)
    pp.......pp
HALO: x 3-13, rows 0-2  (a #fff4c4, G #d8a038, g #f8d878)
    .#########.
    #aagggggGG#
    .#########.
HANDS_CHEEKS: x 1-15, rows 8-14  (H #f4900c, J #c86400, j #ffb547)
    ##...........##
    #jJ.........Jj#
    #jHJ.......JHj#
    #jHJ.......JHj#
    #jHJ.......JHj#
    #HJJ.......JJH#
    .###.......###.
Z_SIGN: x 10-15, rows 0-5  (B #3fa9f0, b #b8e6ff, N #2273c3)
    .####.
    #bbbB#
    .##B#.
    .#B##.
    .BBNN#
    ....#.
DROOL: x 9-11, rows 11-15  (B #3fa9f0, b #b8e6ff)
    b..
    b..
    bb.
    BB#
    ##.
STEAM: x 1-7, rows 11-15  (w #ffffff, z #e2e8ed)
    .##....
    #ww##..
    #wwwz#.
    #zwwzz#
    .#####.
```

- `BLUSH` is two 2px pink dashes (`#ff8f8f`) under the eyes, never a round patch.
- `TEARS_JOY` runs down both rims and leaves the jaw as two drops; `STREAMS` runs straight down the cheeks for wailing. Both are light-blue channels (`#b8e6ff`) edged in mid blue (`#3fa9f0`) and ending in deep blue (`#2273c3`): a tiny water ramp, no gradients.
- `HANDS_CHEEKS` uses the orange hand ramp (`#ffb547`, `#f4900c`, `#c86400`; section 8), so the hands never melt into the yellow head.

## 4. Approved 16px smileys, read closely

**Approved.** The calm four: slight smile, grin, grin with happy eyes, and a wink.

```text
1f642              1f600              1f604              1f609
......#####.....   ......#####.....   ......#####.....   ......#####.....
....##ddddc##...   ....##eeeed##...   ....##eeeed##...   ....##ddddc##...
...#ddccccccc#..   ...#eeddddddd#..   ...#eeddddddd#..   ...#ddccccccc#..
..#deccccccccc#.   ..#efddddddddd#.   ..#efddddddddd#.   ..#deccccccccc#.
..#dcc#ccc#ccc#.   ..#edd#ddd#ddd#.   ..#ed##ddd##dd#.   ..#dcc#ccc##cc#.
.#dccc#ccc#cccb#   .#eddd#ddd#dddc#   .#ed#dd#d#dd#dc#   .#dccc#cc#cc#cb#
.#dccc#ccc#cccb#   .#eddd#ddd#dddc#   .#edddddddddddc#   .#dccc#cccccccb#
.#dcccccccccccb#   .#edddddddddddc#   .#edddddddddddc#   .#dcccccccccccb#
.#dccccccccccba#   .#ed#########cb#   .#ed#########cb#   .#dc#ccccccc#ba#
.#ccc#ccccc#cba#   .#dd#ggggggg#cb#   .#dd#ggggggg#cb#   .#ccc#ccccc#cba#
..#ccc#####cba#.   ..#dd#aaaaa#cb#.   ..#dd#aaaaa#cb#.   ..#ccc#####cba#.
..#ccccccccbba#.   ..#ddd#####ccb#.   ..#ddd#####ccb#.   ..#ccccccccbba#.
...#cccccbbaa#..   ...#dddddccbb#..   ...#dddddccbb#..   ...#cccccbbaa#..
....##bbbaa##...   ....##cccbb##...   ....##cccbb##...   ....##bbbaa##...
......#####.....   ......#####.....   ......#####.....   ......#####.....
................   ................   ................   ................
```

- **1f642** is `FACE_EYES` plus `MOUTH_SLIGHT`: corners at x 5 and 11 on row 9, the line on row 10. That's the whole face. Every other face in the set is measured against it.
- **1f600** swaps in `MOUTH_GRIN`: a 9px top lip on row 8, one row of white teeth, one row of dark-red mouth (`#8a2c1a`), and a 5px bottom line. Two rows inside, as the rule says.
- **1f604** changes only the eyes, to `EYES_HAPPY`. The mouth is byte-identical to 1f600's. Reuse is what makes a set.
- **1f609** keeps the left eye and replaces the right with the `EYE_WINK` arch, and uses the wider `MOUTH_SMILE`. A wink is one changed eye; nothing else moves.

**Approved.** Blush, tears of joy, one tear, and wailing.

```text
1f60a              1f602              1f622              1f62d
......#####.....   ......#####.....   ......#####.....   ......#####.....
....##eeeed##...   ....##hhhhf##...   ....##gggge##...   ....##iiiig##...
...#eeddddddd#..   ...#hhfffffff#..   ...#ggeeeeeee#..   ...#ii##g##gg#..
..#efddddddddd#.   ..#hifffffffff#.   ..#gheeeeeeeee#.   ..#ij#ggggg#gg#.
..#ed##ddd##dd#.   ..#hf##fff##ff#.   ..#gee#eee#eee#.   ..#igggggggggg#.
.#ed#dd#d#dd#dc#   .#hf#ff#f#ff#fe#   .#geee#eee#eeed#   .#igg##ggg##ggf#
.#edddddddddddc#   .#hggfffffffgge#   .#geee#eee#eeed#   .#ig#gg#g#gg#gf#
.#ebbdddddddbbc#   .#gcfffffffffcg#   .#geefeeeeeeeed#   .#ighdgggggdhgf#
.#ed#ddddddd#ca#   .#gc#########cg#   .#gefeeeeeeeedc#   .#ighdgggggdhfe#
.#ddd#ddddd#dca#   .#gc#jjjjjjj#cg#   .#ebbe#####eedc#   .#gghdg###gdhfe#
..#ddd#####dca#.   .#gcf#aaaaa#ecg#   .#bbe#eeeee#dc#.   ..#ghd#aaa#dhe#.
..#ddddddddcca#.   .#gccf#####eccg#   .#aaeeeeeeeddc#.   ..#ghd#ccc#dhe#.
...#dddddccaa#..   .#ccbffffeedbcc#   ..##eeeeeddcc#..   ...#dbg###fbd#..
....##cccaa##...   ..#b##eeedd##b#.   ....##dddcc##...   ....##fffee##...
......#####.....   ...#..#####..#..   ......#####.....   ......#####.....
................   ................   ................   ................
```

- **1f60a**: happy eyes, `BLUSH` on row 7 at x 3–4 and 12–13, and `MOUTH_SMILE`.
- **1f602**: happy eyes, the grin, and `TEARS_JOY`: light-blue streams hug both rims from row 6 and leave the jaw as two inked drops at x 3 and 13 on rows 13–14. The tears break the head's outline on purpose.
- **1f622**: plain eyes, a frown, and one tear running from under the left eye down to the rim. One tear, one side.
- **1f62d**: worried brows (`##` at x 6–7 and 9–10 on row 2, dropping to x 5 and 11 on row 3, the same brows as 1f97a), the `^` of `EYES_HAPPY` on rows 5–6 squeezed shut, two streams straight down the cheeks at x 4–5 and 11–12 on rows 7–12 (light blue on the outer side, mid blue inside, deep blue where they end on row 12), and a wailing mouth only 3px wide (x 7–9): a dark `#8a2c1a` row over a red `#ef3349` tongue row, between ink on rows 9 and 12.

**Approved.** Halo, sunglasses, thinking and a cowboy hat.

```text
1f607              1f60e              1f914              1f920
....#########...   ......#####.....   ......#####.....   ......##.##.....
...#ffeeeeebb#..   ....##eeeed##...   ....##ggggf##...   .##..#dc#cb#..##
....#########...   ...#eeddddddd#..   ...#ggfffffff#..   .#d#.#dcccb#.#b#
................   ..#efddddddddd#.   ..#gh###f###ff#.   .#cd#aaaaaaa#cb#
......#####.....   .###############   ..#g#fffffffff#.   .#cffffffffffcb#
....##ggggd##...   .#ea####c####ac#   .#gfff#fff#fffd#   ..#ccccccccccb#.
...#ggddddddd#..   .#ed###ddd###dc#   .#gfff#fff#fffd#   ...###########..
...#ghddddddd#..   .#edddddddddddc#   .#g##f#fff#fffd#   ..#ihhhhhhhhhg#.
..#gd##ddd##dc#.   .#ed#ddddddd#cb#   .#gcaffffffffdb#   ..#ihh#hhh#hhg#.
..#g#dd#d#dd#c#.   .#ddd#ddddd#dcb#   .#fcafff####fdb#   ..#ihh#hhh#hhg#.
..#gddddddddca#.   ..#ddd#####dcb#.   .#cceeeeea#fdb#.   ..#ihh#hhh#hge#.
..#dd#ddddd#ca#.   ..#ddddddddccb#.   .#ccccccca#ddb#.   ..#h#hhhhhhh#e#.
...#dd#####aa#..   ...#dddddccbb#..   .#cc######dbb#..   ...#h#hhhhg#e#..
...#dddddccaa#..   ....##cccbb##...   ..#cccca#bb##...   ...#hh#####ee#..
....##cccaa##...   ......#####.....   ...#caa####.....   ....##gggee##...
......#####.....   ................   ....###.........   ......#####.....
```

- **1f607** uses a 13×12 head on rows 4–15, so the halo gets rows 0–2 to itself with row 3 empty below it. The halo is an inked ring seen edge-on: ink at x 4–12 on rows 0 and 2, and on row 1 ink caps at x 3 and 13 round a gold ramp lit from the left (`#fff4c4` at x 4–5, `#f8d878` at x 6–10, `#d8a038` at x 11–12). The happy eyes sit on rows 8–9 and the slight smile on rows 11–12. Kirupa named this face, along with tears of joy, rolling on the floor laughing and the cowboy, as faces that "don't look good". The published halo has rows of its own instead of sitting on the head.
- **1f60e**: the frame is one full ink row (row 4, x 1–15) that runs a pixel past the head's outline on both sides as the temples. The lenses are solid ink, x 4–7 and 9–12 on row 5, narrowing to x 4–6 and 10–12 on row 6 so their bottoms round off, with skin showing at x 8 between them. One slate pixel (`#56626e`) sits at each lens's outer top corner (x 3 and 13 on row 5). Black material that must read as glass gets a slate highlight, never a white blob. `check` warns about 20% inner ink and 2×2 ink blocks here, and both are right for dark lenses.
- **1f914**: an arched left brow (x 5–7 on row 3, bending down to x 4 on row 4) beside a flat right brow (x 9–11 on row 3), 1×3 eyes at x 6 and 10 on rows 5–7, and a flat mouth line pushed to the right (x 8–11 on row 9). The orange hand breaks out of the head at the lower left: the index finger (x 3–4, rows 7–9) touches the chin with a dark-orange edge instead of ink, and the fist fills rows 10–15.
- **1f920**: the hat takes rows 0–6 in a brown ramp (`#4e2c0a` to `#e0a85a`): a crown with tops at x 6–7 and 9–10 round a dent at x 8, a band at x 5–11 on row 3, and a brim whose tips curl up at x 1–2 and 14–15. The brim's bottom ink (row 6, x 3–13) is also the face's top outline: one shared row. The face fills rows 7–15, with 1×3 eyes at x 6 and 10 on rows 8–10 and a big U smile (x 4 and 12 on row 11, x 5 and 11 on row 12, the line at x 6–10 on row 13).

**Approved.** Zany, rolling on the floor laughing, heart eyes, and pleading.

```text
1f92a              1f923              1f60d              1f97a
......#####.....   ......#####.##..   ......#####.....   ......#####.....
....##ggggf##...   ....##hhhhf#gg#.   ....##hhhhg##...   ....##ddddc##...
...#ggfffffff#..   ...#hhf#fgggccc#   ...#hhggggggg#..   ...#dd##c##cc#..
..#ghffff###ff#.   ..#hiff#ffccccb#   ..#ecgccgecgcc#.   ..#de#ccccc#cc#.
..#g##ff#iii#f#.   ..#hfff###ffcb#.   ..#cccccgccccc#.   ..#dcccccccccc#.
.#g#ii#f#i#i#fe#   .#hffffffff##fe#   .#hgccbgggccbgf#   .#dc##ccccc##cb#
.#g##i#f#iii#fe#   .#h###ffff#j#fe#   .#hggbgggggbggf#   .#d#f##ccc##f#b#
.#gf##fff###ffe#   .#hff#fff#ja#fe#   .#hgggggggggggf#   .#d##f#ccc#f##b#
.#gffffffffffed#   .#hgf#ff#jaa#ed#   .#hg#########fd#   .#dc##ccccc##ba#
.#fff#######eed#   .#fgcff#jaaa#ed#   .#gg#iiiiiii#fd#   .#cccccccccccba#
..#f#iiiiiii#d#.   ..#gcf#jaaa#ed#.   ..#gg#aaaaa#fd#.   ..#cccc###ccba#.
..#ff#ccca##ed#.   .#gccc#####eed#.   ..#ggg#####ffd#.   ..#ccc#ccc#bba#.
...#f#cbc#edd#..   .#gccbfffeedd#..   ...#gggggffdd#..   ...#cccccbbaa#..
....##cbc#d##...   ..#cb#eeedd##...   ....##fffdd##...   ....##bbbaa##...
.....#cbc##.....   ...##.#####.....   ......#####.....   ......#####.....
......###.......   ................   ................   ................
```

- **1f92a**: two different eyes, both white with a black pupil, which is the zany fix Kirupa asked for. The left is small: a rounded outline (x 4–5 on rows 4 and 7, x 3 and 6 on rows 5–6) round three white pixels and a pupil at (4, 6). The right is big: a 3×3 white at x 9–11 on rows 4–6 with the pupil at (10, 5). The grin shows white teeth on row 10 (x 5–11), and a red tongue (`#ef3349`, with `#c8283a` down its middle) hangs out off-centre at x 6–8 on rows 11–14, breaking the outline with its own ink on row 15.
- **1f923**: the whole head is tilted. Both eyes are squeezed into L shapes, (7, rows 2–4) + (8–9, row 4) and (3–5, row 6) + (5, row 7); the tilted D mouth shows teeth along its upper-left edge; and two tears fly outward, one off the upper right (x 9–14, rows 0–4) and one off the lower left (x 2–5, rows 8–14). My first version dropped the tears straight down, and Kirupa said it looked like an earring.
- **1f60d**: `HEART_EYES` at x 3–7 and 9–13 on rows 3–6, translated copies with no ink: pink `#ff8f8f` at each heart's upper left, red `#ef3349`, and dark red `#c8283a` at its lower right. Red on yellow is already a big jump in hue and value, so at 16 the hearts need no outline. Plus the grin. 1f929 does the same with orange stars (`#f4683a`, shaded `#c9452a` on the right) at x 3–7 and 9–13 on rows 2–6.
- **1f97a**: `EYES_PUPPY`, two rounded 4×4 ink eyes, plus two white catch-light pixels in each: (4, 6) and (5, 7) on the left, mirrored to (12, 6) and (11, 7). Worried brows and a small pout. This is the one face where a blob eye is right, because big glossy eyes are the expression.

## 5. Hats, halos and props

Anything worn on top of the head needs rows of its own. Start from the 13px head, which leaves rows 0–2 free, and move every feature down 2 rows.

```text
name: smiley-head13-16
size: 16
essence: a 13px round head on rows 3-15 that leaves rows 0-2 for a hat, halo or horns
keep: the stepped circle and its rim light; features move down 2 rows
drop: everything else; the span warning goes away once the hat, halo or horns are on
view: front
note: a 13px head on rows 3-15 that leaves rows 0-2 for a hat, halo or horns; move features down 2 rows

[palette]
u #f08e00 skin deep shade
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)
W #ffffcf glint (one pixel)

[grid]
................
................
................
......#####.....
....##SSSSs##...
...#SSsssssss#..
...#SWsssssss#..
..#Sssssssssst#.
..#Sssssssssst#.
..#Sssssssssst#.
..#Ssssssssstu#.
..#ssssssssstu#.
...#sssssstuu#..
...#sssssttuu#..
....##tttuu##...
......#####.....
```

- **Halo:** 1f607's edge-on ring above: an ink-capped gold bar on rows of its own, never painted onto the head.
- **Hats** keep their brim wider than the head and their own ink all round. Sit the brim's bottom outline on the head's top outline; one shared ink row, never two.
- **Horns, a party hat, a crown:** same rule. If a prop needs more than three rows, shrink the face as 1f920 does rather than squash the prop.
- **Props held in front** (a hand, a thermometer, a mask) cover the face and keep their own outline where they meet it at a similar value.

## 6. The 24px head and kit

The 24px head is a 22px stepped circle on columns 1–22 and rows 1–22, mirrored on axis 23 (`x' = 23 − x`), with a 3-pixel glint at the upper left.

```text
name: smiley-head-24
size: 24
essence: a round yellow head lit from the upper left: the base every 24px smiley starts from
keep: the 22px stepped circle, S rim upper left, t and u rim lower right, a 3-pixel W glint
drop: everything else; eyes, mouth and extras go on per subject
view: front
note: the 22px head on columns 1-22 (mirror axis x + x' = 23); features go on with ink

[palette]
u #f08e00 skin deep shade
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)
W #ffffcf glint (3 pixels, upper left)

[grid]
........................
........########........
......##SSSSSSss##......
.....#SSssssssssst#.....
....#Sssssssssssstt#....
...#SssWWssssssssstt#...
..#SsssWssssssssssstt#..
..#Sssssssssssssssstt#..
.#Sssssssssssssssssstt#.
.#Sssssssssssssssssstt#.
.#Sssssssssssssssssstt#.
.#Sssssssssssssssssstu#.
.#Sssssssssssssssssstu#.
.#Sssssssssssssssssstu#.
.#Sssssssssssssssssstu#.
.#Sssssssssssssssssstu#.
..#sssssssssssssssstu#..
..#sssssssssssssssstu#..
...#sssssssssssssstu#...
....#tttssssssssttt#....
.....#ttttttttttuu#.....
......##tttttuuu##......
........########........
........................
```

The 24px kit is a different set of stamps, drawn natively. Never scale the 16px features up. Each eye or brow below gives the left one's top-left corner and size; the right one goes at `x = 24 − x − width`, the same row. That keeps both eyes identical and the face symmetric about axis 23.

**Eyes** (the left one's top-left corner; the right one is placed for you):

```text
bar at (9,6), 1x5  right at x 14
    #
    #
    #
    #
    #
short at (9,8), 1x4  right at x 14
    #
    #
    #
    #
low at (9,8), 1x5  right at x 14
    #
    #
    #
    #
    #
tall at (9,5), 1x6  right at x 14
    #
    #
    #
    #
    #
    #
dot at (9,9), 1x2  right at x 14
    #
    #
arch at (4,7), 6x3  right at x 14
    .####.
    #....#
    #....#
caret at (4,7), 6x3  right at x 14
    ..##..
    .#..#.
    #....#
closed at (4,9), 6x2  right at x 14
    #....#
    .####.
lid at (4,9), 6x2  right at x 14
    .####.
    #....#
squint at (5,6), 4x5  right at x 15
    #...
    ##..
    .###
    ##..
    #...
line at (5,9), 6x1  right at x 13
    ######
white at (4,5), 6x6  right at x 14
    .####.
    #wwww#
    #w##w#
    #w##w#
    #wwww#
    .####.
roll at (4,5), 6x6  right at x 14
    .####.
    #w##w#
    #w##w#
    #wwww#
    #wwww#
    .####.
heart at (3,6), 7x6  right at x 14 (copied, not mirrored)
    .##.##.
    #qr#rr#
    #rrrrr#
    .#rrr#.
    ..#r#..
    ...#...
star at (2,3), 9x9  right at x 13 (copied, not mirrored)
    ....#....
    ...#o#...
    ...#O#...
    ####O####
    #oOOOOOO#
    .#OOOOO#.
    ..#OOO#..
    .#OO#OO#.
    .##...##.
cross at (4,7), 6x5  right at x 14
    ##..##
    .####.
    ..##..
    .####.
    ##..##
spiral at (4,5), 6x6  right at x 14
    ######
    #....#
    #.##.#
    #.#..#
    #.####
    #.....
plead at (4,6), 6x6  right at x 14 (copied, not mirrored)
    .####.
    #ww###
    #ww###
    ######
    ####w#
    .####.
half at (5,8), 6x3  right at x 13 (copied, not mirrored)
    ######
    ...#..
    ...#..
dollar at (5,5), 5x7  right at x 14 (copied, not mirrored)
    ..E..
    .EEEE
    E.E..
    .EEE.
    ..E.E
    EEEE.
    ..E..
```

**Brows** (the left one's top-left corner; the right one is placed for you):

```text
angry at (4,3), 7x4  right at x 13
    ###....
    .####..
    ...####
    .....##
worried at (4,3), 6x3  right at x 14
    ....##
    ..##..
    ##....
arc at (4,3), 6x2  right at x 14
    .####.
    #....#
flat at (5,4), 5x1  right at x 14
    #####
```

**Mouths** (the left one's top-left corner; mouths are placed once):

```text
smile at (6,13), 12x4
    #..........#
    #..........#
    .#........#.
    ..########..
smile_s at (7,14), 10x3
    #........#
    .#......#.
    ..######..
grin at (6,13), 12x6
    ############
    #wwwwwwwwww#
    #RRRRRRRRRR#
    .#RRRRRRRR#.
    ..#RRRRRR#..
    ...######...
grin_t at (6,13), 12x6
    ############
    #wwwwwwwwww#
    #RRRRRRRRRR#
    .#RRPPPPRR#.
    ..#PPkPPP#..
    ...######...
beam at (5,13), 14x5
    ##############
    #wwwwwwwwwwww#
    ##############
    .#wwwwwwwwww#.
    ..##########..
laugh at (5,12), 14x7
    ##############
    #wwwwwwwwwwww#
    #RRRRRRRRRRRR#
    #RRRRRRRRRRRR#
    .#RRRPPPPRRR#.
    ..#PPPkPPPP#..
    ...########...
o at (10,15), 4x4
    .##.
    #RR#
    #RR#
    .##.
O at (9,14), 6x5
    .####.
    #RRRR#
    #RRRR#
    #RRRR#
    .####.
OO at (8,13), 8x7
    ..####..
    .#RRRR#.
    #RRRRRR#
    #RRRRRR#
    #RRRRRR#
    .#RRRR#.
    ..####..
frown_s at (8,15), 8x3
    ..####..
    .#....#.
    #......#
frown at (6,15), 12x3
    ...######...
    .##......##.
    #..........#
flat at (8,16), 8x1
    ########
flat_s at (9,16), 6x1
    ######
kiss at (10,13), 3x5
    ##.
    ..#
    .#.
    ..#
    ##.
tongue at (6,13), 12x6
    ############
    #RRRRRRRRRR#
    .##PPPPPP##.
    ..#PkPPPP#..
    ..#PPPPPP#..
    ...######...
grimace at (5,14), 13x5
    #############
    #ww#ww#ww#ww#
    #############
    #ww#ww#ww#ww#
    #############
wavy at (6,16), 12x2
    .##..##..##.
    #..##..##..#
zigzag at (6,15), 12x3
    ..#...#...#.
    .#.#.#.#.#.#
    #...#...#...
sad_open at (8,14), 8x4
    ..####..
    .#RRRR#.
    #RRRRRR#
    ########
wail at (6,13), 12x5
    ....####....
    ..##RRRR##..
    .#RRRRRRRR#.
    #wwwwwwwwww#
    ############
smirk at (9,14), 9x4
    ........#
    .......#.
    #.....#..
    .#####...
diag at (7,14), 10x4
    .......###
    ....###...
    .###......
    #.........
```

Letters inside the stamps: `#` ink, `w` white `#ffffff`, `r` red `#ef3349`, `R` dark red `#c8283a`, `c` pink `#ff8f8f`, `P` `#ff6f8a`, `k` `#ffb8c6`, `q` `#ff98a6`, `B` blue `#3fa9f0`, `b` light blue `#b8e6ff`, `N` deep blue `#2273c3`, `g` `#e2e8ed`, `G` `#9aa7b2`, `D` slate `#56626e`, `o` `#ffa230`, `O` `#e0661c`, `y` `#fff3a0`, `Y` `#ffd43b`, and the hand ramp `H` `#f4900c`, `j` `#ffb547`, `J` `#c86400`, `K` `#8a3c00`.

What 24px earns over 16px:

- **Eyes:** 1×5 bars (`bar`), 1×6 tall eyes, 6×3 `^` arches and carets, 6×6 whites and pleading eyes. There are no 2px-wide smiley eyes; 2×3 is for people.
- **Mouths:** an open grin can hold a row of teeth and three rows of mouth; a smile gets stepped corners.
- **Extras get outlines.** At 16, hearts and stars have no ink and tears are 1–2px channels. At 24, hearts and stars are inked shapes with a highlight (1f60d's hearts have a pink `#ff98a6` highlight and an ink notch on top), and tears and streams become drops and channels with ink where they meet transparency.
- **Hands get separated fingers.** Tilted hands use 2px fingers split by 1px dark-orange lines (1f92d), open hands use 2px fingers split by 1px ink gaps (1f917), and a fist's curled fingers are separated by ink rows (1f914). Section 8 has the details.

## 7. Approved 24px smileys, read closely

**Approved.**

```text
1f642                      1f600                      1f604
........................   ........................   ........................
........########........   ........########........   ........########........
......##ddddddcc##......   ......##eeeeeedd##......   ......##eeeeeedd##......
.....#ddcccccccccb#.....   .....#eedddddddddc#.....   .....#eedddddddddc#.....
....#dcccccccccccbb#....   ....#edddddddddddcc#....   ....#edddddddddddcc#....
...#dcceecccccccccbb#...   ...#eddffdddddddddcc#...   ...#eddffdddddddddcc#...
..#dcccec#cccc#ccccbb#..   ..#edddfd#dddd#ddddcc#..   ..#edddfdddddddddddcc#..
..#dccccc#cccc#ccccbb#..   ..#eddddd#dddd#ddddcc#..   ..#ed####dddddd####cc#..
.#dcccccc#cccc#cccccbb#.   .#edddddd#dddd#dddddcc#.   .#ed#dddd#dddd#dddd#cc#.
.#dcccccc#cccc#cccccbb#.   .#edddddd#dddd#dddddcc#.   .#ed#dddd#dddd#dddd#cc#.
.#dcccccc#cccc#cccccbb#.   .#edddddd#dddd#dddddcc#.   .#edddddddddddddddddcc#.
.#dcccccccccccccccccba#.   .#edddddddddddddddddcb#.   .#edddddddddddddddddcb#.
.#dcccccccccccccccccba#.   .#edddddddddddddddddcb#.   .#edddddddddddddddddcb#.
.#dcccccccccccccccccba#.   .#eddd############ddcb#.   .#eddd############ddcb#.
.#dcccc#cccccccc#cccba#.   .#eddd#gggggggggg#ddcb#.   .#eddd#gggggggggg#ddcb#.
.#dccccc#cccccc#ccccba#.   .#eddd#aaaaaaaaaa#ddcb#.   .#eddd#aaaaaaaaaa#ddcb#.
..#cccccc######ccccba#..   ..#dddd#aaaaaaaa#ddcb#..   ..#dddd#aaaaaaaa#ddcb#..
..#ccccccccccccccccba#..   ..#ddddd#aaaaaa#dddcb#..   ..#ddddd#aaaaaa#dddcb#..
...#ccccccccccccccba#...   ...#ddddd######dddcb#...   ...#ddddd######dddcb#...
....#bbbccccccccbbb#....   ....#cccddddddddccc#....   ....#cccddddddddccc#....
.....#bbbbbbbbbbaa#.....   .....#ccccccccccbb#.....   .....#ccccccccccbb#.....
......##bbbbbaaa##......   ......##cccccbbb##......   ......##cccccbbb##......
........########........   ........########........   ........########........
........................   ........................   ........................
```

- **1f642**: 1×5 eyes at x 9 and 14 on rows 6–10, and a two-step smile: corners at x 7 and 16 on row 14, then x 8 and 15, then the 6px line on row 16.
- **1f600**: a 12px top lip on row 13, a row of teeth, then three rows of dark mouth tapering 10, 8, 6, and a bottom line.
- **1f604**: squared arches for happy eyes (a 4px top bar at x 5–8 on row 7, legs at x 4 and 9 on rows 8–9; the right eye at x 14–19) and the same grin.

**Approved.**

```text
1f609                      1f602                      1f62d
........................   ........................   ........................
........########........   ........########........   ........########........
......##ddddddcc##......   ......##jjjjjjhh##......   ......##iiiiiigg##......
.....#ddcccccccccb#.....   .....####hhhhhh####.....   .....#iiggggggggge#.....
....#dcccccccccccbb#....   ....#jhhh#hhhh#hhff#....   ....#igg##gggg##gee#....
...#dcceecccccccccbb#...   ...#jhhkkhhhhhhhhhff#...   ...#ig##jggggggg##ee#...
..#dcccec#cccccccccbb#..   ..#jhhhkhhhhhhhhhhhff#..   ..#i##gjgggggggggg##e#..
..#dccccc#cccccc##cbb#..   ..#jh####hhhhhh####ff#..   ..#ig####gggggg####ee#..
.#dcccccc#ccccc#cc#cbb#.   .#jh#hhhh#hhhh#hhhh#ff#.   .#ig#gggg#gggg#gggg#ee#.
.#dcccccc#cccc#cccc#bb#.   .#jh#hhhh#hhhh#hhhh#ff#.   .#ig####g#gggg#g####ee#.
.#dcccccc#ccccccccccbb#.   .#jhhhhhhhhhhhhhhhhhff#.   .#ig#hb#gggggggg#hb#ee#.
.#dcccccccccccccccccba#.   .#jhhhhhhhhhhhhhhhhhfd#.   .#ig#hb#gggggggg#hb#ec#.
.#dcccccccccccccccccba#.   .#jhh##############hfd#.   .#ig#hb#gggggggg#hb#ec#.
.#dcccccccccccccccccba#.   .#jhh#llllllllllll#hfd#.   .#ig#hb#gg####gg#hb#ec#.
.#dcccc#cccccccc#cccba#.   .#jhh#aaaaaaaaaaaa#hfd#.   .#ig#hb#g#aaaa#g#hb#ec#.
.#dccccc#cccccc#ccccba#.   .#j#h#aaaaaaaaaaaa#h#d#.   .#ig#hb##aaaaaa##hb#ec#.
..#cccccc######ccccba#..   ..#i#h#aaaeeeeaaa#h#i#..   ..#g#hb##adddda##hb#c#..
..#ccccccccccccccccba#..   ..#c#hh#eeegeeee#hh#c#..   ..#g#hb#g#dfdd#g#hb#c#..
...#ccccccccccccccba#...   .#icc#hh########hh#icc#.   ...##hb#gg####gg#hb##...
....#bbbccccccccbbb#....   #icccc#fhhhhhhhhf#icccc#   ....###egggggggge###....
.....#bbbbbbbbbbaa#.....   #ccccb#fffffffffd#ccccb#   .....#eeeeeeeeeecc#.....
......##bbbbbaaa##......   .#ccb###fffffddd###ccb#.   ......##eeeeeccc##......
........########........   ..###...########...###..   ........########........
........................   ........................   ........................
```

- **1f609**: the right eye becomes a 6px-wide, 3-row `^` (x 14–19, rows 7–9); the mouth stays 1f642's.
- **1f602**: brows raised so high they merge into the outline (ink x 5–8 on row 3 and x 9 on row 4, mirrored), 1f604's arches, a 14px-wide open mouth with white teeth, dark red and a pink tongue, and tears that burst sideways off both sides of the jaw, past the head's silhouette: blue drops (`#b8e6ff`, `#3fa9f0`, `#2273c3`) with ink between them and the face. At 24 the tears have room to fly, so they do.
- **1f62d**: worried brows that step down into the outline ((8–9, row 4), (6–7, row 5), (4–5, row 6), mirrored), closed eyes, and two outlined 2px streams from under the eyes to the chin (x 5–6 and 17–18, rows 10–18). Both streams have their light pixel on the left: they are copied, not mirrored, so the light stays consistent. The wailing mouth holds dark red over a pink tongue.

**Approved.**

```text
1f923                      1f914                      1f60e
..................####..   ........................   ........................
........########.#hhcc#.   ........########........   ........########........
......##iiiiiigg#hhcccc#   ......##ggggggff##......   ......##eeeeeedd##......
.....#iigg##ghhhhhccccc#   .....#ggffffff#####.....   .....#eedddddddddc#.....
....#igggg##ggccccccccb#   ....#gfffffff#fffd##....   ....#edddddddddddcc#....
...#iggjjg##gggggccccbb#   ...#gffhhfffffffffdd#...   ...#eddffdddddddddcc#...
..#igggjgg#####gggcbbb#.   ..#gf#####fffffffffdd#..   .######################.
..#igggggg#####gg#gff#..   ..#gfffffffffffffffdd#..   .#aa#######dd#######aa#.
.#iggggggggggggg#k#gff#.   .#gffffff#ffff#fffffdd#.   .#########dddd#########.
.#igggggggggggg#kk#gff#.   .#gffffff#ffff#fffffdd#.   .#e######dddddd######c#.
.#i#####gggggg#kka#gff#.   .#gffffff#ffff#fffffdd#.   .#edddddddddddddddddcc#.
.#i#####ggggg#kkaa#gfd#.   .#gffffff#ffff#fffffdb#.   .#edddddddddddddddddcb#.
.#iggg##gggg#kkaaa#gfd#.   .#gfffff##ffffffffffdb#.   .#edddddddddddddddddcb#.
.#ihgg##ggg#kkaaae#gfd#.   .#gffff#ee#fffffffffdb#.   .#edddddddddddddddddcb#.
.#ihcg##gg#kkaaae#ggfd#.   .#gffff#ec#fffffffffdb#.   .#eddd#dddddddddd#ddcb#.
.#ihcgggg#kkaaaee#ggfd#.   .#gfff#ecc#######fffdb#.   .#eddd#dddddddddd#ddcb#.
..#hcggg#kkaaaee#ggfd#..   ..#ff#eccceeeeee#ffdb#..   ..#dddd#dddddddd#ddcb#..
.#hhccg#kkaaae##gggfd#..   ..#ff#ccccccccca#ffdb#..   ..#ddddd########dddcb#..
#hhccccg######ggggfd#...   ...#f#ccc#######ffdb#...   ...#ddddddddddddddcb#...
#hccccbfggggggggfff#....   ....##cccccca#ffddd#....   ....#cccddddddddccc#....
#cccccbfffffffffdd#.....   .....#ccc#####ddbb#.....   .....#ccccccccccbb#.....
#ccccbb#fffffddd##......   .....#cccccca#bb##......   ......##cccccbbb##......
.#ccbb#.########........   ......#cccaa####........   ........########........
..####..................   .......#####............   ........................
```

- **1f923**: the tilted head. Both eyes are 2px-thick L shapes, (10–11, rows 3–5) + (10–14, rows 6–7) and (3–7, rows 10–11) + (6–7, rows 12–15); the big D mouth runs along the tilt with white teeth on its diagonal edge; and the tears are thrown outward, off the upper right (x 16–23, rows 0–6) and the lower left (x 0–7, rows 13–23). Each tear is inked where it meets transparency and graded from light `#b8e6ff` near the eye to deep `#2273c3` at its far edge, with no ink between tear and face. Compare the 16px version: same idea, more room.
- **1f914**: a flat left brow (x 5–9 on row 6) and a raised right brow (x 14–17 on row 3, merging into the outline, with x 13 on row 4); 1×4 eyes at the same height (x 9 and 14, rows 8–11); a mouth line (x 10–16 on row 15) that runs into the hand; and the orange hand, an outlined index finger (x 8–9, rows 12–15) over a fist on rows 16–22 whose curled fingers are separated by ink rows.
- **1f60e**: row 6 is ink from x 1 to 22, the frame and temples. The lenses are solid ink: x 4–10 and 13–19 on row 7, widening to x 2–9 and 14–21 on row 8 where they meet the head's outline, and narrowing to x 3–8 and 15–20 on row 9. Slate `#56626e` lights each lens's outer top corner (x 2–3 and 20–21 on row 7), and the skin between the lenses (x 11–12 on row 7, x 10–13 on row 8) makes an inverted V under the bar. The glint moves up to row 5 (x 7–8), above the frame, and the smile is wider than 1f642's: corners at x 6 and 17 on rows 14–15, x 7 and 16 on row 16, the line at x 8–15 on row 17.

## 8. Hands on faces

**Approved.** Thinking, hand over mouth, hugging, peeking: at 16px, then 24px.

```text
1f914              1f92d              1f917              1fae3
......#####.....   ......#####.....   ......#####.....   ......#####.....
....##ggggf##...   ....##ggggf##...   ....##ggggf##...   ....##eeeed##...
...#ggfffffff#..   ...#ggfffffff#..   ...#ggfffffff#..   ...#eedddddaa#..
..#gh###f###ff#.   ..#ghfffffffff#.   ..#gh##fff##ff#.   ..#efdddaadfea#.
..#g#fffffffff#.   ..#gf##fff##ff#.   ..#g#ff#f#ff#f#.   ..#ed#dafe#eea#.
.#gfff#fff#fffd#   .#gf#ff#f#ff#fd#   .#gfffffffffffd#   .#edd#daee#eeaf#
.#gfff#fff#fffd#   .#gfffffffffffd#   .#gfffffffffffd#   .#edd#daee#eeae#
.#g##f#fff#fffd#   .#gfffffffffffd#   .#gf#fffffff#fd#   .#eddddaeeceeae#
.#gcaffffffffdb#   .#gfffffffcafdb#   .#gff#fffff#fdb#   .#eddddaeeaeeec#
.#fcafff####fdb#   .#fffffcc#eafdb#   .#ffff#####ffdb#   .#dddaaaeeeeedc#
.#cceeeeea#fdb#.   ..#fcc#ec#eadb#.   ..#fffffffffdb#.   ..#dafeaeeeedc#.
.#ccccccca#ddb#.   ..#fcc#ec#eadb#.   .#c#c#c#f#c#c#c#   ..#daeeeeeedcb#.
.#cc######dbb#..   ...#ccccccca##..   .#c#c#c#f#c#c#c#   ...#daeeedccb#..
..#cccca#bb##...   ...#cccccca##...   .#ecccc#d#cccce#   ....##aeedcb#...
...#caa####.....   ..#cccccaa#.....   ..#aaa#####aaa#.   ......##edcb#...
....###.........   ...#######......   ...###.....###..   .......######...
```

```text
1f92d                      1f917                      1fae3
........................   ........................   ........................
........########........   ........########........   ........########........
......##hhhhhhgg##......   ......##hhhhhhgg##......   ......##iiiiiihh##......
.....#hhggggggggge#.....   .....#hhggggggggge#.....   .....#iihhhhhhhhhf#.....
....#hgggggggggggee#....   ....#hgggggggggggee#....   ....#ih####hh####ff#....
...#hggiigggggggggee#...   ...#hggiigggggggggee#...   ...#ihhhhhhhhhhhhhff#...
..#hgggigggggggggggee#..   ..#hg####gggggg####ee#..   ..#ihhh##hhhh####h##f#..
..#hgggggggggggggggee#..   ..#h#gggg#gggg#gggg#e#..   ..#ihh#gg####jjjj#gg##..
.#hgg####gggggg####gee#.   .#hg#gggg#gggg#gggg#ee#.   .#ihhh#geagg#j##j#ge####
.#hg#gggg#gggg#gggg#ee#.   .#hgggggggggggggggggee#.   .#ihhh#geage#j##j#geagg#
.#hg#gggg#gggg#gggg#ee#.   .#hggg#gggggggggg#ggee#.   .#i####geage#jjjj#geage#
.#hgggggggggggggggggec#.   .#hggg#gggggggggg#ggec#.   .##ggageage#h#####geage#
.#hgggggggggggggggggec#.   .#hgggg#gggggggg#gggec#.   .##geageage#hhhhh#geage#
.#hgggggggggggggggggec#.   .#hggggg########ggggec#.   .#geageage#hhhhhh#geage#
.#hgggggggggggg##gggec#.   .#hgggggggggggggggggec#.   .#geageage#hhhhhh#geage#
.#hggggggggggg#ff##gec#.   .#h##g##g##gg##g##g##c#.   .#geageage#hhh####geage#
..#ggggggg##g#fb#ff#c#..   ..#ff#ff#ff##ff#ff#ff#..   .#geeeeeee####geeeeeeee#
..#gggggg#ff#fdafb#ec#..   ..#df#df#df##fd#fd#fd#..   .#geeeeeec#bb#geeeeeeec#
...#gggg#fdafdadb#ec#...   .##dd#dd#dd##dd#dd#dd##.   .#geeeeeec#bb#eeeeeeec#.
....#ee#fdaddadb#ee#....   #f#ddaddadd##ddaddadd#f#   ..#eeeeeec#bb#eeeeeec#..
.....##fddddddb#cc#.....   #dddddddddd##dddddddddd#   ...#ccccc#f##f#ccccc#...
.....#fddddddb#c##......   .#bddddddd#ee#dddddddb#.   ....#####ffffdd#####....
....#fbbbbbbb###........   ..#bbdddd######ddddbb#..   ........########........
.....########...........   ...######......######...   ........................
```

- **Hands are orange,** not yellow: `#ffb547` light, `#f4900c` base, `#c86400` shade, and at 24 a deep `#8a3c00`. A yellow hand on a yellow face disappears. The one published exception is 1fae3 at 16px, whose hand is the face's pale yellow `#ffff93` with dark `#7f5410` grooves between the fingers (x 7, 10 and 13); the grooves do the separating there.
- **Ink:** at 24, a hand is inked all round. At 16, ink goes where the hand meets transparency; where it crosses the face, a tone change is often enough (1f914's index finger meets the chin with a dark-orange edge and no ink), and ink comes back where it helps, as on the fist's outline.
- **Fingers at 16** are 1–2px wide with 1px of ink between them: 1f917's hugging hands have three 1px fingers each, split by ink on rows 11–12, and 1f92d's hand over the mouth has three 2px fingers split by ink at x 6 and 9 on rows 10–11. 1f631's hands on the cheeks are just tone columns.
- **Fingers at 24** come in two styles, both described in the drawing code. "Tilted hands: 2px fingers split by 1px dark-orange lines, with staggered tips so they never read as a crown of equal bumps" (1f92d). "Open hands: 2px fingers split by 1px black gaps, thumb out to the side" (1f917). A fist's curled fingers are separated by ink rows (1f914).
- **Placement:** hands come in from the bottom corners or the sides and may break the head's outline. A review note on 1f486, getting a massage: "The hands on top of the head read as cat ears. Move them to the sides of the head at the temples, so the palms and fingers cover the head's left and right edges."
- **Peeking and covering:** a review note on the face with a peeking eye: "Leave one eye fully visible and peek the other through a 1px finger gap." Covered features vanish, so one visible feature has to carry the face.

## 9. Animal faces, and faces on things

Animal faces follow the same rules as smileys: a clear silhouette, identical eyes, a small dark nose, flat colour zones and rim light. The silhouette (ears, snout, muzzle) does most of the identifying.

**Approved.** Cat, dog, panda and octopus at 16px.

```text
1f431              1f436              1f43c              1f419
.#............#.   ................   ..##........##..   .....######.....
.##..........##.   ..############..   .#aa#......#aa#.   ....#cddcbb#....
.#c#........#c#.   .#eekkkkiiiicb#.   #abaa######aaba#   ...#cddcbbba#...
.#ec#......#cb#.   #eeckiiiiiiicbb#   #aaaaggggggaaaa#   ..#ccdcbbbbaa#..
.#ecc######ccb#.   #ecciiiiiiiicbb#   .#affffffffffa#.   ..#cccbbbbbaa#..
#edadddaadddadb#   #ecci#iiii#icbb#   #gfffffffffffff#   ..#cb#bbbb#aa#..
#edadddaadddadb#   #ccci#iiii#icbb#   #gfaaaffffaaafe#   ..#bb#bbbb#aa#..
#eddd#dddd#dddb#   #cbiiiiiiiiihbb#   #gaadaffffadaae#   ..#bbbbbbbaaa#..
#eddd#dddd#dddb#   .#cillgaaaljhb#.   #gaadaffffadaae#   .#.#bbbbaaaa#.#.
#ddddddccdddddb#   .#cilllaalljhb#.   #gaaaffffffaaae#   #b#bbbbbaaaaa#a#
.#ddd#d##d#ddb#.   ..#il######jh#..   #gfffgaaaagfffe#   #bbbbbbbaaaaaaa#
..#ddd#dd#ddb#..   ..#iiilffjiih#..   #fffgggaagggffe#   .#bb#bb##aa#aa#.
...##dddddb##...   ...#iilfdjih#...   .#fffggccggffe#.   #bb##bb##aa##aa#
.....######.....   ....##ffdd##....   ..#fefggggfee#..   #b##bb#..#aa##a#
................   ......####......   ...##feeeee##...   .#..##....##..#.
................   ................   .....######.....   ................
```

- **Cat:** pointed ears with pink inner ears (`#f7899d`), 1×2 eyes at x 5 and 10 on rows 7–8, a 2px pink nose (x 7–8 on row 9), a small ink `w` mouth on rows 10–11, and short stripe marks in a darker orange (`#ee8a12`) across the forehead (x 3, 7–8 and 12 on rows 5–6). No whiskers: at 16px they're noise.
- **Dog:** floppy ears in darker browns (`#a65f36`, `#84401f`, `#5c260e`) hang at the sides, separated from the face by tone, not ink; 1×2 eyes at x 5 and 10; a slate nose (`#2c3038`, with a grey `#8a95a3` highlight) on a pale muzzle; an ink mouth line on row 10; and a pink tongue hanging out below the chin.
- **Panda:** no inner ink at all. The ears and eye patches are near-black slate (`#272b2b`, lit with `#4a5258`), each eye is a single grey `#8899a6` glint pixel inside its patch (rows 7–8), the nose is the same slate, and a tiny red mouth sits under it. The white face is `#ffffff` at the left, `#eeeeee` across and `#ccd6dd` at the right. Black fur is never ink inside a figure.
- **Octopus:** a purple ramp lit from the upper left (`#c0a3f7` down to `#6340ad`), a round mantle, two identical 1×2 eyes at x 5 and 10 on rows 5–6, and tentacles split by ink. Kirupa, on an octopus I'd drawn: "It looks unnecessarily bad because both the eyes are off."

**Approved.** Frog, monkey, tiger and rabbit.

```text
1f438              1f435              1f42f              1f430
................   ................   ................   ...##......##...
...###....###...   .....######.....   .###........###.   ..#ec#....#ec#..
..#dcc#..#dcc#..   ...##dddccc##...   #edd#......#ddb#   .#eda#....#edc#.
.#dgggc##dgggc#.   ..#ddccccccca#..   #edde######cddb#   .#eda#....#eda#.
.#cg#gc##cg#gc#.   ..#dcccccccca#..   #eacccaaaacccab#   .#eda#....#eda#.
#dcgggccccgggcb#   .#dcgggccgggca#.   #ecacccaacccacb#   .#cda#....#eda#.
#dccccccccccccb#   #ffcg#gccg#gcff#   #eccc#cccc#cccb#   ..#ea######ea#..
#cccccccccccccb#   #ffcg#gggg#gcff#   #eccc#cccc#cccb#   .#ecceeeeeeccc#.
#cccccaccaccccb#   #ffcggg##gggaff#   #aagggccccgggaa#   #ecccaccccacccc#
#acccccccccccca#   .#cgggggggggga#.   #gggggg##gggggf#   #ecca#ecca#ecca#
#baaaaaaaaaaaab#   ..#cgg####gea#..   #aaggg#gg#gggaa#   #ecca#ecca#ecca#
#bfffffffffffeb#   ..#cgg#bb#gea#..   .#gggggggggggf#.   #cccceffffeccca#
.#ffffffffffee#.   ...#cgg##gea#...   ..#gggggggggf#..   .#ccccfbbfccca#.
..#beeeeeeeeb#..   ....##ccaa##....   ...##gggggf##...   ..#cccfggfcca#..
...##########...   ......####......   .....######.....   ...#caaaaaaa#...
................   ................   ................   ....########....
```

- **Frog:** the eyes sit on top, outside the head's curve, as two bumps of white with a 1px ink pupil. The nostrils and the wide mouth (row 10, x 2–13) are dark green `#3e721d`, tone lines rather than ink, over a pale chin.
- **Monkey:** a pale face mask (`#f3bc94`) inside a brown head, pink ears out at the sides, 1×2 eyes, two ink nostril pixels and a small open `O` mouth with a dark red-brown inside.
- **Tiger:** short dark-brown (`#45281a`) stripe marks on the forehead and cheeks, not full bands; pink inner ears; a white muzzle shaded `#dfe5ea`; 1×2 eyes; an ink nose (x 7–8 on row 9) with the mouth corners at x 6 and 9 on row 10.
- **Rabbit:** the long ears are the whole identity, so they get the top six rows, with pink inner ears. The 1×2 eyes sit low (x 5 and 10, rows 9–10) over a pink nose and a white muzzle.

**Approved.** Cat, dog and panda at 24px.

```text
1f431                      1f436                      1f43c
........................   ........................   ..###..............###..
........................   ...####..........####...   .#bba#............#bba#.
........................   ..#ddda##########ddda#..   #baaaa############aaaaa#
..#..................#..   .#dccca#mmmmmmmj#dccca#.   #baaa##hhhhhhhhfe##aaaa#
..##................##..   .#dccca#mkkkkkkj#dccca#.   #aaa#hhggggggggggfe#aaa#
..#e#..............#e#..   .#dccca#mkkkkkkj#dccca#.   .#a#hgggggggggggggfe#a#.
..#de#............#gd#..   .#dccca#mkkkkkkj#accca#.   ..#hgggggggggggggggfe#..
..#dde############gdd#..   .#dcca#mkkkkkkkkj#dcca#.   .#hgggggggggggggggggfe#.
..#ddfgggggddgggggfdd#..   .#dcca#mp#kkkkp#j#dcca#.   .#hgggggggggggggggggfe#.
..#dffffdffddffdffffd#..   .#acca#m##kkkk##j#acca#.   #hgggggaaggggggaaggggfe#
..#gffffdffddffdffffe#..   ..#aa#mkkkkkkkkkkj#aa#..   #hggggaaaaggggaaaagggfe#
.#gffffffffffffffffffe#.   ...##mkkkkkkkkkkkkj##...   #hgggaaiaaggggaaiaaggfe#
.#gfffffeffffffefffffe#.   ...#mkkkkolllllkkkkj#...   #hgggaadaaggggaadaaggfe#
.#gffffh#gffffeh#ffffe#.   ...#mkkkolibbbolkkkj#...   #hgggaaaaggggggaaaaggfe#
.#gfffe##gffffe##gfffe#.   ...#mkkonlbbbbonlkkj#...   #fggggaaggggggggaagggfe#
.#gfffe##gffffe##gfffe#.   ...#mkonlnlbbonlnlkj#...   #eggggggg######ggggggfe#
.#gffffggfccccfggffffe#.   ...#jkolfllffllfolkg#...   .#fggggggg####ggggggfe#.
.#efffffaffccffafffffb#.   ....#jonlffheffonlg#....   .#efggggggg##gggggggfe#.
..#efffffaaffaafffffb#..   .....#lnnlheehlnnl#.....   ..#efggggg####gggggfe#..
...#eeffffffffffffeb#...   ......#ll#heee#ll#......   ...#effgg#cccc#ggffe#...
....##eeeeeeeeeeeb##....   .......###eeee###.......   ....#eefff#cc#fffee#....
......############......   ..........####..........   .....##eeee##eeee##.....
........................   ........................   .......##########.......
........................   ........................   ........................
```

At 24 the cat's eyes become 2×3 with a white catch-light at the upper left of each (copied, not mirrored), and its `w` mouth is drawn in dark brown `#8a4a12` instead of ink. The dog gets 2×2 eyes with the same copied catch-light, a big slate nose with a grey highlight, and a red tongue. Each of the panda's eye patches holds a white-over-grey pupil, and its nose becomes an ink triangle (x 9–14 on row 15, narrowing to x 11–12 on row 17) over an open red mouth.

**Faces on things** (a sun, a moon, a pile of poo, a ghost): use the smiley kit's eyes and mouths at the same sizes, on the object's own colours. A review brief put it this way: "Faces on suns and moons use the face kit (1px-wide vertical eyes, identical)."

## 10. People: heads, busts and hair

kirupa.com's set draws generic people like Twemoji's: smiley-yellow skin, golden-orange hair and a big round head, with 1px-wide eyes at 16 and 2×3 eyes at 24. The drawing module's own summary: "Every part (hair, ears, mustache, shirt, hands) has its own black outline, eyes are solid black, and light comes from the upper left." A review note that fixed a bride's face: "Use the same head and face as your other people: 1px-wide vertical eyes and the same head width."

### The 16px person head

```text
name: person-head-16
size: 16
essence: 1f9d1 person: a big round head under a golden-orange hair cap
keep: the hair cap separated from skin by value (d borders the face), 1x2 eyes, a small smile
drop: ears, nose, neck, brows
view: front
note: 1f9d1: a big head with a hair cap; 1x2 eyes under the fringe

[palette]
k #8a3a00 hair deep shade
d #a04a06 hair shade
h #e07f16 hair base
u #f08e00 skin deep shade
H #ffb23a hair light
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)

[grid]
.....#######....
...##HHHhhhk##..
..#HHHhhhhhkkk#.
.#HHhhhhhhhhhkk#
.#Hhhhhhdhhhhhk#
.#Hhddddsddddhk#
.#Hdsssssssssdk#
.#dsss#sss#sssd#
.#Ssss#sss#ssst#
.#Sssssssssssst#
.#ssss#sss#ssst#
.#sssss###sssut#
..#tttssssstut#.
...##tttttuu##..
.....#######....
................
```

- The hair is a cap: `H` light at the upper left, `h` base, `k` deep at the right, and `d` (the hair's shade) wherever hair borders skin. That `d` border is what separates hair from face. It works by value, not by ink.
- The centre parting is one skin pixel at x 8 on row 5, with a `d` pixel above it.
- Eyes are 1×2 at x 6 and 10, rows 7–8. The smile is two corner pixels at x 6 and 10 on row 10 and `###` at x 7–9 on row 11.
- The `bust-16` template is the same idea with shoulders: the head shrinks to rows 0–10 (eyes on rows 4–5) and a shirt with a lit left and a shaded right shoulder fills rows 11–14. Use it when clothing is part of the identity.

### The 24px person head

```text
name: person-head-24
size: 24
essence: 1f9d1 person at 24: a big round head under a hair cap with an inked fringe
keep: the inked fringe line, 2x3 eyes, ears as rim tones, a small smile
drop: nose, neck, brows, strands
view: front
note: 1f9d1 at 24: hair cap with an inked fringe, 2x3 eyes, ears as rim tones

[palette]
k #8a3a00 hair deep shade
d #c8620a hair shade
u #f08e00 skin deep shade
h #f0901e hair base
H #ffb23a hair light
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)

[grid]
........................
.........######.........
.......##HHHhdd##.......
.....##HHhhhhhhdd##.....
....#HHhhhhhhhhhhdd#....
...#Hhhhhhhhhhhhhhdd#...
...#Hhhhhhhhhhhhhhdd#...
..#Hhhhhhhhhhhhhhhhdk#..
..#Hhhhhh######hhhhdk#..
..#hhh###ssssss###hdk#..
..#hh#ssssssssssss#dk#..
..#h#ssssssssssssss#k#..
.#S#ssss##ssss##ssss#t#.
.#S#ssss##ssss##ssss#t#.
.#S#ssss##ssss##ssss#u#.
..##Sssssssssssssstu##..
...#tssssssssssssstu#...
...#tsss#ssssss#sstu#...
....#tsss######sstu#....
....#tttssssssssttu#....
.....#ttttttttttuu#.....
......##tttttuuu##......
........########........
........................
```

- At 24, the fringe gets a real **ink line**, because there is room for it and the hair is large: x 9–14 on row 8, stepping to x 6–8 and 15–17 on row 9, x 5 and 18 on row 10, and x 4 and 19 on row 11.
- Eyes are 2×3 at x 8–9 and 14–15, rows 12–14. The ears are rim tones at x 2 and 21 (`S` lit, `t` and `u` shaded) on rows 12–14, each boxed by ink.
- The smile: corners at x 8 and 15 on row 17 and a 6px line (x 9–14) on row 18.
- Busts at 24 (1f935 and the professions) put a smaller head on rows 0–15 with 2×2 eyes (x 8–9 and 14–15, rows 9–10) and the clothes on rows 16–23.

### Face shape: round, oval and long jaws

Face shape is a portrait trait when the photos plainly show it. The templates' heads are round. Change the jaw by **at most 1px per side** from the template, and add at most one row; keep the runs on each side monotonic (`zoom`). Any more and it stops being the house head and starts being a caricature. All six jaws below pass `check` with `0 off`, in yellow and in real tones.

**16px, rows 10–15 of `person-head-16`** (rows 0–9 stay as they are):

```text
round (template)   oval               long
.#ssss#sss#ssst#   ..#sss#sss#sst#.   .#ssss#sss#ssst#   row 10
.#sssss###sssut#   ..#ssss###ssut#.   .#sssss###sssut#   row 11
..#tttssssstut#.   ...#ttssssstu#..   ..#tsssssssstu#.   row 12
...##tttttuu##..   ....##tttuu##...   ...#ttssssstu#..   row 13
.....#######....   ......#####.....   ....##tttuu##...   row 14
................   ................   ......#####.....   row 15
```

- **Oval** narrows by 1px per side from row 10 down, while the cheeks on rows 7–9 stay at x 1. It's exactly how the approved bald person (1f9d1-200d-1f9b2) and older man (1f474) narrow at 16.
- **Long** is the round jaw's turn moved one row lower, into the template's empty bottom row. The head becomes 15×16.

**24px, rows 19–23 of `person-head-24`** (rows 0–18 stay as they are):

```text
round (template)           oval                       long
....#tttssssssssttu#....   .....#tssssssssstu#.....   ....#tttssssssssttu#....   row 19
.....#ttttttttttuu#.....   ......#ttttttttuu#......   .....#ttsssssssstu#.....   row 20
......##tttttuuu##......   .......##tttuuu##.......   ......#ttttttttuu#......   row 21
........########........   .........######.........   .......##tttuuu##.......   row 22
........................   ........................   .........######.........   row 23
```

- **Oval** is the jaw of the blind-tested Kirupa portrait at 24 (without its grin): 1px in per side from row 19 down. Left-side runs 2, 1, 1, 1, 2, 3.
- **Long** keeps the template's row 19 and moves the turn one row lower. The head becomes 22×23.

### Grins on a person head

**A kit grin's width is a house shape, not an enlarged feature.** Draw a grin at the kit's width (1f600's 9px `MOUTH_GRIN` on a smiley, the 10px person grin below at 24), never wider or deeper to force the read and never narrower to match the photo's proportions. Using a kit grin when the photo shows a grin isn't caricature; enlarging teeth past the kit's shape is.

**24px person grin.** A blind reviewer read it as a "very broad toothy smile". It replaces the template smile:

1. Erase the template smile: x 8 and 15 on row 17 and x 9–14 on row 18 go back to `s`.
2. Add `w #ffffff teeth` to the palette and stamp this at x 7–16, rows 17–19 (`.` keeps the head pixel under it):

   ```text
   #........#   row 17
   .#wwwwww#.   row 18
   ..######..   row 19
   ```

3. Light the chin row under the lip with base skin, or the band of shade reads as a beard or a mask. On the round jaw, row 20 becomes `.....#ttssssssttuu#.....`; on the oval jaw, `......#tssssssttu#......`.

Rows 15–22 with the oval jaw:

```text
..##Sssssssssssssstu##..   row 15
...#tssssssssssssstu#...   row 16
...#tss#ssssssss#stu#...   row 17, the corners at x 7 and 16
....#tss#wwwwww#stu#....   row 18, six teeth between ink
.....#tss######stu#.....   row 19, the lower lip
......#tssssssttu#......   row 20, the lit chin
.......##tttuuu##.......   row 21
.........######.........   row 22
```

On the round jaw, row 19 is `....#ttts######sttu#....`.

The 16px grin below has an ink lip line, and this 24px grin is a crescent. That's fine: a blind pair test read the two as one emoji, 3 of 3. A lip-line grin at 24, like set:24:1f600's (its lip ink runs x 6–17 on row 13), hasn't been tried on the person head yet.

**16px person grin.** On the template the eyes sit on rows 7–8 and leave no room for a four-row grin. The portrait in [`examples/kirupa-portrait/`](../examples/kirupa-portrait/README.md) found the arrangement that works, after ten blind rounds: `MOUTH_TEETH` (section 3, approved 1f601's grin), one row lower than on the smiley head, under a shorter hair cap.

```text
MOUTH_TEETH on person-head-16: x 4-12, rows 9-12  (w #ffffff, e #cfd6e6)
    #########   row 9, the ink lip line
    #wwwwwww#   row 10, white upper teeth at x 5-11
    .#eeeee#.   row 11, grey lower teeth at x 6-10
    ..#####..   row 12, the ink base
```

What it needs around it:

1. **The cap ends on row 3,** a row shorter than the template's. Only sideburns and a fringe tuft reach rows 4–5.
2. **The 1×2 eyes move up a row,** to x 6 and 10 on rows 6–7, with one skin row (row 8) above the lip line.
3. **The face outline:** x 1 and 15 down to row 8, x 2 and 14 on rows 9–11, x 3 and 13 on row 12, x 4–5 and 11–12 on row 13, and x 6–10 on row 14. That leaves one skin column beside the lip line and the white teeth on each side, and two beside the grey row and the base.
4. **The rim tones round it:** `S` at x 3 and `t` at x 13 down to row 10; `s` at x 3–4 and `t` at x 12–13 on row 11; `s` at x 4–5 and `t` at x 11–12 on row 12; the chin row 13 in `t` and `u`.

The eyes and the grin are 22 inner ink pixels of 184 (12%), right at `check`'s warning line, so there's no ink to spare. The finished portrait, with the short hair below and his sampled skin (palette in [`kirupa-16.sprite`](../examples/kirupa-portrait/kirupa-16.sprite)):

```text
.....##.####....   row 0
...##HH#HHhk##..
..#hhhhhhhhkkk#.
.#hHHhhhHHhkkkk#   row 3, the cap ends
.#hhSskkssssskk#   row 4, sideburns and the fringe tuft
.#hhSsssssssskk#
.#tSss#sss#sstu#   row 6, the eyes
.#tSss#sss#sstu#
.#tSssssssssstu#   row 8, one skin row
..#S#########t#.   row 9, the lip line
..#S#wwwwwww#t#.
..#ss#eeeee#tt#.
...#ss#####tt#..
....##tttuu##...
......#####.....   row 14
```

Mouths that didn't work on the 16px person head. Each was blind-tested:

| Mouth | Result |
| --- | --- |
| 1f600's `MOUTH_GRIN`, with its dark-red interior row | Passed one round, then failed on four successors. Reviewers read the dark row as an open mouth, not teeth. |
| `MOUTH_GRIN` with 1f600's 2px cheeks (the outline at x 1 and 15 down through the teeth row) | Teeth 0 of 3; the face read neutral |
| A D filled with white teeth | No pass |
| A U-shaped bottom | 1 of 3 at best |
| A soft skin lip between ink corners | No pass |
| The 24px crescent, ported to 16 | No pass |
| `MOUTH_TEETH` with its corners raised a row | No better, 13% inner ink, and it read as a handlebar moustache |

Two more rules came out of those rounds:

- **Never raise a person-head grin's corners.** The full-width ink lip line can already read as a moustache (it does on approved 1f600 too, so that read is the house's, not yours); raised corners make it a handlebar.
- **Facial hair wins at 16.** The 16px moustache sits on rows 10–11, exactly where the grin's teeth go. For a person with a moustache or beard, keep the facial hair and a small mouth at 16, and give the grin to the 24.

When a grin isn't a top trait, or the blind test keeps failing, fall back to the template's calm smile or `MOUTH_SMILE` at its own width, draw the grin at 24, and list it second in the 16's `keep:`.

### Strong brows at 24 (portraits)

Brows are a portrait trait at **24 only**, and only when the person's photos plainly show strong brows; at 16 the fringe sits on the eyes and there's no row for them. On `person-head-24`:

1. Raise the fringe ink a row: delete template row 7 (`..#Hhhhhhhhhhhhhhhhdk#..`), so the fringe line lands on row 7 and template rows 9–10 move up to rows 8–9.
2. Duplicate the `..#h#ssssssssssssss#k#..` row, so rows 10 and 11 are both that row.
3. Paint 4×1 brows on row 10 in the deepest hair tone (`k`, the deepest slate for black hair), at x 7–10 and 13–16.
4. Leave row 11 as skin: one skin row between the brows and the eyes, which stay on rows 12–14.

```text
...#Hhhhhhhhhhhhhhdd#...   row 6
..#Hhhhhh######hhhhdk#..   row 7, the fringe ink, one row higher
..#hhh###ssssss###hdk#..   row 8
..#hh#ssssssssssss#dk#..   row 9
..#h#sskkkksskkkkss#k#..   row 10, the brows
..#h#ssssssssssssss#k#..   row 11, skin
.#S#ssss##ssss##ssss#t#.   row 12, the eyes as before
```

The approved older man 1f474 puts his grey brows in the same place: row 10, x 7–9 and 14–16, with one skin row above the eyes.

### Hair

**Approved.** Person, man, woman and bald at 16px.

```text
1f9d1              1f468              1f469              1f9d1-200d-1f9b2
.....#######....   .....#######....   .....#######....   ......#####.....
...##eeeccca##..   ...##eeeccca##..   ...##fffddda##..   ....##dddcc##...
..#eeecccccaaa#.   ..#eeecccccaaa#.   ..#fffdddddaaa#.   ...#ddccccccc#..
.#eecccccccccaa#   .#eecccccccccaa#   .#ffdddddddddaa#   ...#deccccccc#..
.#ecccccbccccca#   .#ecbbbbbbbbbca#   .#fddbbbbbbbdda#   ..#dcccccccccb#.
.#ecbbbbgbbbbca#   .#ebgggggggggba#   .#fdbhhhhhhhbda#   ..#dcccccccccb#.
.#ebgggggggggba#   .#eggggggggggga#   .#fdhhhhhhhhhda#   ..#dcccccccccb#.
.#bggg#ggg#gggb#   .#bggg#ggg#gggb#   .#ddhh#hhh#hhda#   .#bdcc#ccc#ccba#
.#hggg#ggg#gggf#   .#hggg#ggg#gggf#   .#ddhh#hhh#hhda#   .#bdcc#ccc#ccba#
.#hgggggggggggf#   .#hgggggggggggf#   .#ddhhhhhhhhhda#   .#bdcccccccccba#
.#gggg#ggg#gggf#   .#ggggcccccgggf#   .#ddhh#hhh#hhda#   ..#ccc#ccc#ccb#.
.#ggggg###gggdf#   .#gggcg###gcgdf#   .#ddhhhccchhhaa#   ..#cccc###ccbb#.
..#fffgggggfdf#.   ..#fffgggggfdf#.   ..#ddghhhhhgaa#.   ...#bbcccccba#..
...##fffffdd##..   ...##fffffdd##..   ...##gggggee##..   ....##bbbaa##...
.....#######....   .....#######....   .....#######....   ......#####.....
................   ................   ................   ................
```

- **1f9d1:** the cap with a centre parting: skin at (8, 5) under a shade pixel, and the fringe's shade tone along row 5 on both sides. Hair `#ffb23a`, `#e07f16`, `#a04a06` (the border tone), `#8a3a00`.
- **1f468:** a straight fringe one row higher (the shade tone across x 4–12 on row 4), no parting, and a moustache (section 12).
- **1f469:** long hair falls beside the face to the jaw (x 2–3 and 13–14, rows 4–12), the face narrows to x 4–12, and the smile's middle becomes red lips (`#e0243c` at x 7–9 on row 11) while its corners stay ink.
- **Bald:** a smiley-like dome: the skin ramp with its light tone at the upper left and a glint (`#ffffcf` at (5, 3)), ears as 1px bumps in the silhouette on rows 7–9, and 1f9d1's eyes and smile.

**Approved.** Older man, beard, curly hair and red hair at 16px.

```text
1f474              1f9d4              1f9d1-200d-1f9b1   1f9d1-200d-1f9b0
......#####.....   .....#######....   ...###.###.###..   .....#######....
....##hhhff##...   ...##dddccca##..   ..#eec#eec#eca#.   ...##eeeccca##..
...#hhfffffff#..   ..#dddcccccaaa#.   .#eccbcccbcccaa#   ..#eeecccccaaa#.
..##hifffffff##.   .#ddcccccccccaa#   .#cbeccbeccbeaa#   .#eecccccccccaa#
.#gdhffffffffba#   .#dcccccbccccca#   ..#eccbcccbcca#.   .#ecccccbccccca#
.#dbfffffffffba#   .#dcbbbbebbbbca#   .#eccbcccbcccaa#   .#ecbbbbgbbbbca#
..#bfffffffffb#.   .#dbeeeeeeeeeba#   .#ccbggbcbggbca#   .#ebgggggggggba#
.#ehff#fff#ffec#   .#cbee#eee#eeba#   ..#bgg#ggg#ggb#.   .#bggg#ggg#gggb#
.#ehff#fff#ffec#   .#cbfe#eee#eeba#   ..#hgg#ggg#ggf#.   .#hggg#ggg#gggf#
.#ehfffffffffec#   .#ccbeeeeeeebca#   ..#hgggggggggf#.   .#hgggggggggggf#
..#fffbbbbbffe#.   .#dccb#ccc#bcca#   ..#ggg#ggg#ggf#.   .#gggg#ggg#gggf#
..#ffbf###fbee#.   .#ccccc###cccaa#   ..#gggg###ggff#.   .#ggggg###gggdf#
...#eefffffec#..   ..#cccccccccaa#.   ...#ffgggggfd#..   ..#fffgggggfdf#.
....##eeecc##...   ...##cccccaa##..   ....##fffdd##...   ...##fffffdd##..
......#####.....   .....#######....   ......#####.....   .....#######....
................   ................   ................   ................
```

- **1f474:** a bald crown with a glint, a grey ring of hair at the sides (`#d3d7de`, `#adb3be`, `#79808e`, `#4a505c`) on rows 3–6, ears on rows 7–9, and a grey moustache.
- **1f9d4:** 1f9d1's parting, and a beard in the hair ramp that starts at the sides on row 9 and covers the lower face from row 10, so skin shows on rows 6–9. The smile is inked inside the beard (section 12).
- **Curly (1f9d1-200d-1f9b1):** the top of the silhouette is three 3px bumps (x 3–5, 7–9 and 11–13) with ink notches between them at x 6 and 10 on row 1, plus bumps at the sides. The curls inside are tone marks (dark `#a04a06` dots and light highlights), not ink, and the face narrows to x 3–13.
- **Red (1f9d1-200d-1f9b0):** the same cap as 1f9d1 in a red-orange ramp: `#fb7c46`, `#dc4f26`, `#a8321a`, `#7a1c0a`.

**Approved.** The same people at 24px.

```text
1f9d1                      1f468                      1f469
........................   ........................   ........................
.........######.........   .........######.........   .........######.........
.......##eeedbb##.......   .......##eeedbb##.......   .......##eeedcc##.......
.....##eeddddddbb##.....   .....##eeddddddbb##.....   .....##eeddddddcc##.....
....#eeddddddddddbb#....   ....#eeddddddddddbb#....   ....#eeddddddddddcc#....
...#edddddddddddddbb#...   ...#edddddddddddddbb#...   ...#edddddddddddddcc#...
...#edddddddddddddbb#...   ...#edddddddddddddbb#...   ...#edddddddddddddcc#...
..#edddddddddddddddba#..   ..#edddddddddddddddba#..   ..#edddddddddddddddcc#..
..#eddddd######ddddba#..   ..#edd############dba#..   ..#edddd########dddcc#..
..#ddd###gggggg###dba#..   ..#dd#gggggggggggg#ba#..   ..#edd##gggggggg##dcc#..
..#dd#gggggggggggg#ba#..   ..#d#gggggggggggggg#a#..   ..#ed#gggggggggggg#cc#..
..#d#gggggggggggggg#a#..   ..#d#gggggggggggggg#a#..   ..#ed#gggggggggggg#ca#..
.#h#gggg##gggg##gggg#f#.   .#h#gggg##gggg##gggg#f#.   ..#e#ggg##gggg##ggg#a#..
.#h#gggg##gggg##gggg#f#.   .#h#gggg##gggg##gggg#f#.   ..#e#ggg##gggg##ggg#a#..
.#h#gggg##gggg##gggg#c#.   .#h#gggg##gggg##gggg#c#.   ..#e#ggg##gggg##ggg#a#..
..##hgggggggggggggfc##..   ..##hgggggggggggggfc##..   ..#e#gggggggggggggg#a#..
...#fgggggggggggggfc#...   ...#fgggg######gggfc#...   ..#d#gggggggggggggg#a#..
...#fggg#gggggg#ggfc#...   ...#fggg#eddddb#ggfc#...   ..#dd#ggbggggggbgg#ca#..
....#fggg######ggfc#....   ....#fggg######ggfc#....   ..#dd#gggbbbbbbggg#ca#..
....#fffggggggggffc#....   ....#fffggggggggffc#....   ..#ddd#gggggggggg#dca#..
.....#ffffffffffcc#.....   .....#ffff####ffcc#.....   ..#cccc##ffffff##ccca#..
......##fffffccc##......   ......##fffffccc##......   ..#cccccc######aaaaaa#..
........########........   ........########........   ...##################...
........................   ........................   ........................
```

```text
1f474                      1f9d1-200d-1f9b1           1f9d1-200d-1f9b2
........................   .........######.........   ........................
.........######.........   ....###.#dddccc#.###....   .........######.........
.......##hhhfee##.......   ...#ddc#ddccccca#dca#...   .......##dddcbb##.......
.....##hhffffffee##.....   ..#dcccadccccccadccca#..   .....##ddccccccbb##.....
....#hhiiffffffffee#....   ..#dccaacccccaaacccca#..   ....#ddeeccccccccbb#....
...#hffiffffffffffee#...   ...#aaacddccdcccaaaa#...   ...#dcceccccccccccbb#...
...#hfffffffffffffee#...   ..#ddccdccccdccccccca#..   ...#dcccccccccccccbb#...
..##hffffffffffffffe##..   .#ddcccccccccccccdccaa#.   ..#dcccccccccccccccba#..
.#gg#hffffffffffffe#da#.   .#dccccccccaccccacccaa#.   ..#dcccccccccccccccba#..
#gdd#hffffffffffffe#dda#   .#ccccac#ca##ca#ccccaa#.   ..#dcccccccccccccccba#..
#gda#hfbbbffffbbbfe#daa#   ..#ccca#f##ff##f#ccaa#..   ..#dcccccccccccccccba#..
.##a#hffffffffffffe#a##.   ..#c###ffffffffff###a#..   ..#dcccccccccccccccba#..
.#h#ffff##ffff##fffe#e#.   .#g#ffff##ffff##ffff#e#.   .#d#cccc##cccc##cccb#b#.
.#h#ffff##ffff##fffe#e#.   .#g#ffff##ffff##ffff#e#.   .#d#cccc##cccc##cccb#b#.
.#h#ffff##ffff##fffe#c#.   .#g#ffff##ffff##ffff#b#.   .#d#cccc##cccc##cccb#a#.
..##hfffffffffffffec##..   ..##gfffffffffffffeb##..   ..##dcccccccccccccba##..
...#effff######fffec#...   ...#efffffffffffffeb#...   ...#bcccccccccccccba#...
...#efff#gdddda#ffec#...   ...#efff#ffffff#ffeb#...   ...#bccc#cccccc#ccba#...
....#efff######ffec#....   ....#efff######ffeb#....   ....#bccc######ccba#....
....#eeeffffffffeec#....   ....#eeeffffffffeeb#....   ....#bbbccccccccbba#....
.....#eeee####eecc#.....   .....#eeeeeeeeeebb#.....   .....#bbbbbbbbbbaa#.....
......##eeeeeccc##......   ......##eeeeebbb##......   ......##bbbbbaaa##......
........########........   ........########........   ........########........
........................   ........................   ........................
```

- **1f9d1:** hair `#ffb23a`, `#f0901e`, `#c8620a`, `#8a3a00`, the stepped ink fringe, 2×3 eyes, boxed ears and the 6px smile: the `person-head-24` template.
- **1f468:** a flat fringe (ink x 6–17 on row 8) and a moustache drawn as an outlined bar (ink x 9–14 on rows 16 and 18 round a row of hair tones) over a small ink mouth (x 10–13 on row 20). The code's note: "mustache over a small mouth".
- **1f469:** an arched fringe (x 7–14 on row 8); hair down both sides on rows 10–21, outside the face's own ink at x 4 and 19, closing under the chin (ink x 3–20 on row 22); and an all-red smile.
- **1f474:** silver tufts stick out past the head (x 0–3 and 20–23, rows 8–11), grey brows (`#8e95a2`, x 7–9 and 14–16 on row 10), a glint on the bald crown, a grey moustache, and the mouth line on row 20. The code explains the brows: "grey brows mark age … even though People heads otherwise skip brows".
- **Curly:** in the code's words, a "scalloped cap with one-pixel dips between curls; each clump is lit at its upper left instead of drawing ink curls". The bumps sit at x 4–6, 9–14 and 17–19, and the fringe line is scalloped too.
- **Bald:** the person head with skin everywhere, the glint, the ears, 2×3 eyes and the smile.

**Short hair with ears at 16.** Dark hair on the template's full cap can read as a helmet: the hair runs full width down to row 5, and wherever the outline steps in under it, it makes a brim. The portrait in [`examples/kirupa-portrait/`](../examples/kirupa-portrait/README.md) drew short hair like this (rows 0–8; the eyes on rows 6–7 go with the 16px person grin above):

```text
.....##.####....   row 0, (7, 0) is empty: a notch splits the top
...##HH#HHhk##..   row 1, light H only in 2px dashes
..#hhhhhhhhkkk#.   row 2
.#hHHhhhHHhkkkk#   row 3, the cap ends
.#hhSskkssssskk#   row 4, sideburns at x 2-3 and 13-14, the tuft at x 6-7
.#hhSsssssssskk#   row 5
.#tSss#sss#sstu#   row 6, the ears: t at x 2, u at x 14
.#tSss#sss#sstu#   row 7
.#tSssssssssstu#   row 8
```

- **No ledge.** The side outline runs straight down x 1 and 15 from row 3 to row 8, and the sideburns (rows 4–5) sit directly on the ears (rows 6–8).
- **Clumps, not a gradient.** The light `H` comes only in 2px dashes in a brick pattern (x 5–6 and 8–9 on row 1, x 3–4 and 8–9 on row 3), and the deep `k` runs down the right side. No single-pixel tone specks.
- **A hairline that isn't a band.** The forehead is skin from x 4 to 12 on rows 4–5, broken by a 2px fringe tuft, with the sideburns at the temples.
- **A split top,** only if the photos show volume there: the empty (7, 0) over the ink at (7, 1) splits the top into two clumps. It's deliberately asymmetric, so the sprite names it in an `asymmetric:` header line and `check` reports it as accepted. For an even top, use these as rows 0–1: `.....#######....` and `...##HHhhHHk##..`.
- **The ears are tone only** at 16: `t` and `u` columns inside the outline. Nobody names them; their job is to end the sideburns at ear level.
- **The steps:** the top-left runs 2, 2, 1, 1 into the six-row side, the top-right 4, 2, 1, 1.
- **Three hair tones** (`H h k`), not four: the portrait dropped `d` to stay inside the colour budget.

Hair rules:

- **Separate hair from skin by value.** A hair tone that touches skin must be clearly darker or lighter than the skin. Light hair (white, grey, blond) borders the face with its darker tone: white-haired 1f9d1-200d-1f9b3 uses grey `#9aa7b8` for its fringe edge. The blond module's note: "Twemoji's yellow hair would melt into the yellow skin, so the hair is a paler, cooler gold with a darker outline tone."
- **The silhouette is the hairstyle.** Short, long, curly, a bun, a side parting, a widow's peak, receding: change the outline of the cap before you touch its colours. At 16px, a hairstyle is 3–6 pixels of silhouette difference.
- **Black hair is slate,** so the ink outline and the 1px eyes still show. On the person templates the four hair keys take one slate tone each: `H` `#66717c` light, `h` `#3a4148` base, `d` `#30363c` shade, `k` `#262b30` deep (luminance 111, 64, 53 and 42). That's the house slate (`BLACK_HEART` uses `#66717c`, `#3a4148` and `#262b30`); the approved vampire 1f9db is the same ramp a shade bluer and lighter in the base (`#66707f`, `#464e5c`, `#323844`, `#2a2f39` at 16). Nothing inside the outline goes below luminance 40: `check` counts anything darker as ink.
- **Dark-brown hair** keeps its base near luminance 55–70 and its deepest tone no darker than 42: `python3 scripts/sprite_tool.py ramp "#4d4038" --down 1 --up 2 --value 0.1` gives `#332722`, `#4d4038`, `#665c52`, `#80796f` (luminance 42, 67, 94, 122).
- **Grey and white hair** need the ink outline more than any other, and a darker grey where they meet yellow or pale skin.
- **No strands.** Hair is 3–4 tones in big zones. One parting pixel or one fringe step says "hair" better than ten strand lines, and add even that only if the photo plainly shows a parting or a fringe.
- **Dark hair on the person head can read as a "helmet", "hat" or "beard"** in a blind test. The approved set:16:1f9d1 gets the same read, so it's the house template, not your drawing: don't spend revisions fighting it. For short hair, the recipe above removes the brim that causes most of it.

## 11. Skin

- **In the generic set, skin is smiley yellow** (`S` `#ffff93`, `s` `#ffe600`, `t` `#ffbf00`, `u` `#f08e00`), like Twemoji's default people.
- **For a real person, sample their skin mechanically** with `sample --face`, from the most evenly lit photo you have, never a flash photo. Box one clean patch of skin: the cheeks and nose between the eyes and the mouth, where most of a sprite's skin sits, or the forehead between the brows and the hairline if the cheeks are shadowed or bearded. Keep hair, brows, eyes, lips, glasses, clothes and background out. The skin filter drops greys, black, white, blue and green, but brown or blond hair, lips, orange clothes and the dark edges of brows and eyes look like skin to it, and they drag the average darker. On Kirupa's photo, a box that took in the brows and eyes averaged luminance 124.6; the clean cheek band below it averaged 137.4. Check the box with `crop` before you sample:

  ```bash
  python3 scripts/sprite_tool.py crop "https://www.kirupa.com/about/kirupa_bio_pic_png.png@300,375,445,410" --scale 3 --out skin-box.png
  python3 scripts/sprite_tool.py sample "https://www.kirupa.com/about/kirupa_bio_pic_png.png" --box "300,375,445,410" --face
  ```

  That photo is flash-lit, and it was the only one with a large, front-facing face. It's the case `--face` exists for: the flash cluster is flagged and left out of the average.

  It lists the skin's colour clusters with their hex, share, luminance and saturation, and flags two that must never be the base: **FLASH OR SHINE**, the palest, least saturated cluster (a flash, a shiny forehead, the tip of the nose), and **SHADOW**, the darkest (the nostrils, the side of the nose). It averages the face without them and recommends the **base**: the most common cluster left in the lit mid-tones, from the face average to 15 lighter, or the mean of those pixels when no cluster centre falls there. (The most common cluster on its own swings with the box: on that photo it ran from luminance 122 to 180 as the box moved.) On that photo it prints a face average of luminance 137.4 and the base `#c28164`.

- **Build the ramp** from the base with a small warm hue shift, then map it onto the template's keys: light → `S`, base → `s`, shadow → `t`, deep shadow → `u`. The rim-light layout doesn't change.

  ```bash
  python3 scripts/sprite_tool.py ramp "#c28164" --hue 3 --value 0.09 --up 1
  ```

  These ramps came out of the same command. Use what your photo gives you, not these:

  | Sampled base | Deep | Shade | Base | Light |
  | --- | --- | --- | --- | --- |
  | `#e8b894` | `#ba7b5d` | `#d19977` | `#e8b894` | `#ffd8b4` |
  | `#c68642` | `#98501d` | `#af6a2e` | `#c68642` | `#dda459` |
  | `#c28164` | `#944b38` | `#ab654c` | `#c28164` | `#d99f7f` |
  | `#ad6f56` | `#7f3d2d` | `#965440` | `#ad6f56` | `#c48c6f` |
  | `#8d5524` | `#5f2a0b` | `#763e16` | `#8d5524` | `#a46e35` |

- **Check the drawn skin against the photo.** `check SPRITE --skin "S,s,t,u" --face "PHOTO@SX0,SY0,SX1,SY1"`, with the same skin box you sampled, takes the pixel-weighted average of the skin keys and reports an ERROR if it's more than 15 luminance from the face average. A drawing that fails is lighter or darker than the person. Skip it for smiley-yellow variants.
- **Keep skin and hair apart by value.** If the sampled hair and skin are close in value, darken the hair's border tone (`d`) or, at 24, rely on the ink fringe.
- Never lighten, darken or "correct" a sampled skin tone toward a default, and never pick a flash highlight because it "looks cleaner": it makes the person lighter than they are.

## 12. Facial hair and glasses

### Moustaches and beards

**Approved.** Beard, man with a moustache, older man; at 16px, then 24px.

```text
1f9d4              1f468              1f474
.....#######....   .....#######....   ......#####.....
...##dddccca##..   ...##eeeccca##..   ....##hhhff##...
..#dddcccccaaa#.   ..#eeecccccaaa#.   ...#hhfffffff#..
.#ddcccccccccaa#   .#eecccccccccaa#   ..##hifffffff##.
.#dcccccbccccca#   .#ecbbbbbbbbbca#   .#gdhffffffffba#
.#dcbbbbebbbbca#   .#ebgggggggggba#   .#dbfffffffffba#
.#dbeeeeeeeeeba#   .#eggggggggggga#   ..#bfffffffffb#.
.#cbee#eee#eeba#   .#bggg#ggg#gggb#   .#ehff#fff#ffec#
.#cbfe#eee#eeba#   .#hggg#ggg#gggf#   .#ehff#fff#ffec#
.#ccbeeeeeeebca#   .#hgggggggggggf#   .#ehfffffffffec#
.#dccb#ccc#bcca#   .#ggggcccccgggf#   ..#fffbbbbbffe#.
.#ccccc###cccaa#   .#gggcg###gcgdf#   ..#ffbf###fbee#.
..#cccccccccaa#.   ..#fffgggggfdf#.   ...#eefffffec#..
...##cccccaa##..   ...##fffffdd##..   ....##eeecc##...
.....#######....   .....#######....   ......#####.....
................   ................   ................
```

```text
1f9d4                      1f468                      1f474
........................   ........................   ........................
.........######.........   .........######.........   .........######.........
.......##eeedbb##.......   .......##eeedbb##.......   .......##hhhfee##.......
.....##eeddddddbb##.....   .....##eeddddddbb##.....   .....##hhffffffee##.....
....#eeddddddddddbb#....   ....#eeddddddddddbb#....   ....#hhiiffffffffee#....
...#edddddddddddddbb#...   ...#edddddddddddddbb#...   ...#hffiffffffffffee#...
...#edddddddddddddbb#...   ...#edddddddddddddbb#...   ...#hfffffffffffffee#...
..#edddddddddddddddba#..   ..#edddddddddddddddba#..   ..##hffffffffffffffe##..
..#eddddd######ddddba#..   ..#edd############dba#..   .#gg#hffffffffffffe#da#.
..#ddd###gggggg###dba#..   ..#dd#gggggggggggg#ba#..   #gdd#hffffffffffffe#dda#
..#dd#gggggggggggg#ba#..   ..#d#gggggggggggggg#a#..   #gda#hfbbbffffbbbfe#daa#
..#d#gggggggggggggg#a#..   ..#d#gggggggggggggg#a#..   .##a#hffffffffffffe#a##.
.#h#gggg##gggg##gggg#f#.   .#h#gggg##gggg##gggg#f#.   .#h#ffff##ffff##fffe#e#.
.#h#gggg##gggg##gggg#f#.   .#h#gggg##gggg##gggg#f#.   .#h#ffff##ffff##fffe#e#.
.#h#gggg##gggg##gggg#c#.   .#h#gggg##gggg##gggg#c#.   .#h#ffff##ffff##fffe#c#.
..#d#gggggggggggggf#a#..   ..##hgggggggggggggfc##..   ..##hfffffffffffffec##..
..#dd#gg########gf#ba#..   ...#fgggg######gggfc#...   ...#effff######fffec#...
...#ed##eeeeeedb##ba#...   ...#fggg#eddddb#ggfc#...   ...#efff#gdddda#ffec#...
...#edddddddddddddba#...   ....#fggg######ggfc#....   ....#efff######ffec#....
....#eddd######ddba#....   ....#fffggggggggffc#....   ....#eeeffffffffeec#....
....#dddd#gggg#ddba#....   .....#ffff####ffcc#.....   .....#eeee####eecc#.....
.....#dddd####ddba#.....   ......##fffffccc##......   ......##eeeeeccc##......
......##ddddddbb##......   ........########........   ........########........
........########........   ........................   ........................
```

- **16px moustache (1f468):** a 5px bar in the hair's base colour on row 10 (x 6–10), drooping one pixel at x 5 and 11 on row 11, with the `###` mouth between the droops. Grey for grey hair (1f474). It takes the rows the 16px person grin needs (section 10), so a person with a moustache or beard gets the facial hair and a small mouth at 16, and the grin at 24.
- **16px beard (1f9d4):** the hair ramp starts at the sides on row 9 and covers the lower face from row 10 to the chin, so skin shows only between the fringe and the beard (rows 6–9). The smile is inked inside the beard: corners at x 6 and 10 on row 10 with beard colour between them, `###` on row 11. The beard follows the head's rim light: lighter at the left, deeper at the right.
- **24px moustache (1f468):** an outlined bar (ink x 9–14 on rows 16 and 18, with ink ends at x 8 and 15 on row 17 round a lit row of hair tones) over a small ink mouth (x 10–13 on row 20).
- **24px beard (1f9d4):** an ink line on row 16 (x 8–15) marks the beard's top edge across the upper lip, a light moustache band sits on row 17 (x 8–13), and the beard fills down to row 22, one row below the usual chin, with its ink on row 23. The mouth is an outlined skin gap: ink x 9–14 on row 19; ink, skin at x 10–13, ink on row 20; ink x 10–13 on row 21. The code: "beard and mustache are one mass, with the mouth as an outlined skin gap".
- **Stubble and light shadow** don't survive at 16px. Drop them. At 24px, one shade-tone row along the jaw can suggest them; never ink.
- **Beard colour** comes from the same sampled hair ramp. A dark beard follows the slate or dark-brown rule above.

### Glasses

Glasses are often the single most recognisable trait in a portrait, so they get two recipes per size. The published set's reference is the nerd face, 1f913, whose drawing code sums it up as "essence: thick glasses and buck teeth".

**Approved.** 1f913 at 16px and 24px.

```text
1f913
......#####.....
....##eeeed##...
...#eeddddddd#..
..#efddddddddd#.
..######d######.
.#e#g#g###g#g#c#
.#e#g#g#d#g#g#c#
.#ed###ddd###dc#
.#eddddddddddca#
.#ddd#ddddd#dca#
..#ddd#gbg#dca#.
..#dddd###dcca#.
...#dddddccaa#..
....##cccaa##...
......#####.....
................
```

```text
1f913
........................
........########........
......##ddddddcc##......
.....#####cccc#####.....
....#dcccccccccccbb#....
...#dcceecccccccccbb#...
..#######cccccc#######..
..#fffff########fffff#..
.##ff##f#cccccc#f##ff##.
.##ff##f#cccccc#f##ff##.
.##fffff#cccccc#fffff##.
.#d######cccccc######a#.
.#dcccccccccccccccccba#.
.#dcccccccccccccccccba#.
.#dcccccccccccccccccba#.
.#dccc#cccccccccc#ccba#.
..#cccc#cccccccc#ccba#..
..#ccccc#ff##ff#cccba#..
...#cccc#ff##ff#ccba#...
....#bbbc######cbbb#....
.....#bbbbbbbbbbaa#.....
......##bbbbbaaa##......
........########........
........................
```

- **16px:** row 4 is ink at x 2–7 and 9–14 (skin at x 8), so the top frame merges into the head's outline. The lenses are 3×2 on rows 5–6: white, with a 1×2 pupil in the middle column (x 5 and 11). The bridge is `###` at x 7–9 on row 5. The buck teeth sit in the smile: ink, white, grey `#9aa6b4`, white, ink across x 6–10 on row 10, under corners at x 5 and 11 on row 9.
- **24px:** flat brows merge with the outline on row 3 (x 5–9 and 14–18). The frames run rows 6–11 and merge into the head's outline at x 1–2 and 21–22. The lenses are 5×4 white at x 3–7 and 16–20 on rows 7–10, with 2×2 pupils nudged toward the nose (x 5–6 and 17–18). The bridge is ink x 8–15 on row 7, and the teeth are two white pairs either side of an ink gap on rows 17–18.
- `check` warns about 20% inner ink on 1f913-16. Frames are ink lines, so the warning is expected; name the reason in a `note:` line.

The recipes below are built on the person-head templates and pass `check`. Grids marked **Recipe (not published)** are mine, drawn and reviewed for this kit; they are not part of kirupa.com's set. Each is a complete `.sprite` file: copy it into `$W` as a starting point, or paste just the rows you need.

**Recipe (not published).** 16px glasses: bold frames (C) and thin frames (D).

```text
name: glasses-16-C
size: 16
essence: a person in bold glasses: hair cap, ink frames round pale lenses, small smile
keep: the hair cap, ink frames, pale lenses, 1x2 pupils, a small smile
drop: ears, nose, brows
view: front
note: bold frames are ink lines (17% inner ink, like 1f913 at 20%); the smile moves down a row

[palette]
k #8a3a00 hair deep shade
d #a04a06 hair shade
h #e07f16 hair base
u #f08e00 skin deep shade
H #ffb23a hair light
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base
S #ffff93 skin light (upper-left rim)
l #e8f6ff lens (pale blue-white)

[grid]
.....#######....
...##HHHhhhk##..
..#HHHhhhhhkkk#.
.#HHhhhhhhhhhkk#
.#Hhhhhhdhhhhhk#
.#Hhddddsddddhk#
.#Hd###sss###dk#
.#d#lll#s#lll#d#
.#S#l#l###l#l#t#
.#S#l#l#s#l#l#t#
.#ss###sss###st#
.#ssss#sss#ssst#
..#tttt###ttut#.
...##tttttuu##..
.....#######....
................
```

```text
name: glasses-16-D
size: 16
essence: a person in thin glasses: hair cap, slate frames round skin lenses, ink eyes
keep: the hair cap, slate frames, 1x2 eyes, a small smile
drop: ears, nose, brows
view: front
note: thin or metal frames in slate so the 1x2 ink eyes still read

[palette]
F #3a4148 frame (slate, so the ink eyes still read)
k #8a3a00 hair deep shade
d #a04a06 hair shade
h #e07f16 hair base
u #f08e00 skin deep shade
H #ffb23a hair light
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base
S #ffff93 skin light (upper-left rim)

[grid]
.....#######....
...##HHHhhhk##..
..#HHHhhhhhkkk#.
.#HHhhhhhhhhhkk#
.#Hhhhhhdhhhhhk#
.#Hhddddsddddhk#
.#HdFFFFsFFFFdk#
.#dsFs#FFF#sFsd#
.#SsFs#FsF#sFst#
.#SssFFFsFFFsst#
.#ssss#sss#ssst#
.#sssss###sssut#
..#tttssssstut#.
...##tttttuu##..
.....#######....
................
```

- **C, bold or dark frames** (the default): ink frames round 3×3 pale lenses (`l` `#e8f6ff`) at x 4–6 and 10–12 on rows 7–9, 1×2 ink pupils at x 5 and 11 on rows 8–9, a 1px bridge at x 8 on row 8, and cut corners (the top and bottom frames span only x 4–6 and 10–12) so the frames read round. The glasses take rows 6–10, so the smile moves down a row: corners at x 6 and 10 on row 11, `###` on row 12. `check` warns about 17% inner ink; that's the frames, and approved 1f913 sits at 20%.
- **D, thin, metal or light frames:** slate frames (`F` `#3a4148`, or the frame's own colour, ramped) round skin-coloured lenses: tops at x 4–7 and 9–12 on row 6, sides on rows 7–8, bottoms at x 5–7 and 9–11 on row 9, and a slate bridge at x 8 on row 7. The template's 1×2 ink eyes stay at x 6 and 10, and the face keeps its usual smile.
- Choose C when the frames are thick or dark, D when they're thin, metal or coloured. Rimless glasses don't survive at 16px: leave them out, or use D with the frames in a pale tint.

**Recipe (not published).** 24px glasses: bold frames (A) and thin frames (B).

```text
name: glasses-24-A
size: 24
essence: a person in bold glasses at 24: inked fringe, ink frames round pale lenses, 2x2 eyes
keep: the inked fringe line, ink frames, pale lenses, 2x2 eyes, ears, a small smile
drop: nose, neck, brows, strands
view: front
note: ink frames round pale lenses, 2x2 eyes, ink bridge on row 12

[palette]
k #8a3a00 hair deep shade
d #c8620a hair shade
u #f08e00 skin deep shade
h #f0901e hair base
H #ffb23a hair light
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)
l #e8f6ff lens (pale blue-white)

[grid]
........................
.........######.........
.......##HHHhdd##.......
.....##HHhhhhhhdd##.....
....#HHhhhhhhhhhhdd#....
...#Hhhhhhhhhhhhhhdd#...
...#Hhhhhhhhhhhhhhdd#...
..#Hhhhhhhhhhhhhhhhdk#..
..#Hhhhhh######hhhhdk#..
..#hhh###ssssss###hdk#..
..#hh#ssssssssssss#dk#..
..#h#######ss#######k#..
.#S#s#l##l####l##l#s#t#.
.#S#s#l##l#ss#l##l#s#t#.
.#S#s#llll#ss#llll#s#u#.
..##S######ss######u##..
...#tssssssssssssstu#...
...#tsss#ssssss#sstu#...
....#tsss######sstu#....
....#tttssssssssttu#....
.....#ttttttttttuu#.....
......##tttttuuu##......
........########........
........................
```

```text
name: glasses-24-B
size: 24
essence: a person in thin glasses at 24: inked fringe, slate frames round skin lenses, 2x2 eyes
keep: the inked fringe line, slate frames, 2x2 eyes, ears, a small smile
drop: nose, neck, brows, strands
view: front
note: slate frames, 2x2 ink eyes, slate bridge on row 12

[palette]
F #3a4148 frame (slate)
k #8a3a00 hair deep shade
d #c8620a hair shade
u #f08e00 skin deep shade
h #f0901e hair base
H #ffb23a hair light
t #ffbf00 skin shade (lower-right rim)
s #ffe600 skin base (the Darkproject smiley yellow)
S #ffff93 skin light (upper-left rim)

[grid]
........................
.........######.........
.......##HHHhdd##.......
.....##HHhhhhhhdd##.....
....#HHhhhhhhhhhhdd#....
...#Hhhhhhhhhhhhhhdd#...
...#Hhhhhhhhhhhhhhdd#...
..#Hhhhhhhhhhhhhhhhdk#..
..#Hhhhhh######hhhhdk#..
..#hhh###ssssss###hdk#..
..#hh#ssssssssssss#dk#..
..#h#FFFFFFssFFFFFF#k#..
.#S#sFs##sFFFFs##sFs#t#.
.#S#sFs##sFssFs##sFs#t#.
.#S#sFssssFssFssssFs#u#.
..##SFFFFFFssFFFFFFu##..
...#tssssssssssssstu#...
...#tsss#ssssss#sstu#...
....#tsss######sstu#....
....#tttssssssssttu#....
.....#ttttttttttuu#.....
......##tttttuuu##......
........########........
........................
```

- **A, bold or dark frames:** the top frame is ink on row 11 (x 4–10 and 13–19), merging into the face edge; lenses are 4×3 (`l` `#e8f6ff`) at x 6–9 and 14–17 on rows 12–14; the bridge is ink at x 11–12 on row 12; the bottom frame is row 15. The eyes become 2×2 at x 7–8 and 15–16 on rows 12–13, centred in each lens so the gaze stays straight.
- **B, thin, metal or light frames:** the same layout in slate `F` `#3a4148` round skin-coloured lenses, with the same 2×2 ink eyes at x 7–8 and 15–16 on rows 12–13. Eyes behind glasses at 24 are always 2×2: a 2×3 eye would run from the top frame to the bottom frame and read as a bar.
- In both, the smile stays where the template has it.

To add glasses to a head you've already drawn, paste these rows over it: 16-C rows 6–12, 16-D rows 6–9, 24-A rows 11–15, 24-B rows 11–15. Add the lens or frame key to your `[palette]`, then fix any hair or ear pixels the paste covered.

## 13. Portraits of a real person from a photo

A portrait emoji is a likeness built from a few true traits, drawn in the house style. Here is the procedure I follow. Every command runs from the skill folder (SKILL.md, "Set up once"). Replace `PHOTO` with the photo's path or URL, and the boxes with your own numbers. [`examples/kirupa-portrait/README.md`](../examples/kirupa-portrait/README.md) is a finished run of it, with the real commands, grids, grades and blind-test record.

1. **Find photos.** Use photos the person has published (an about page, a profile picture) or ones you were given for this. Every command takes a local path or an http(s) URL as `PHOTO`, and caches downloads, so a URL is fetched once. Prefer a front-facing, evenly lit photo where the face is large. Look at two or three photos if you can: a trait that shows in all of them is a real trait; a trait in one is lighting or a moment.

2. **Look at it, then measure it.**

   ```bash
   python3 scripts/sprite_tool.py sample PHOTO --colors 4
   python3 scripts/sprite_tool.py crop "PHOTO@X0,Y0,X1,Y1" --scale 3 --out face-crop.png
   ```

   `sample` prints the image's size (`(WxH image)`). Open the photo with your image viewer and estimate two boxes, in image pixels:
   - the **face box** `X0,Y0,X1,Y1`, from the top of the hair to the chin, for `crop`, `draft` and `sheet --ref`;
   - the **skin box** `SX0,SY0,SX1,SY1`, one clean patch of skin: the cheeks and nose between the eyes and the mouth, or the forehead if the cheeks are shadowed or bearded, with no hair, brows, eyes, lips, glasses or background in it (section 11), for `sample --face` and `check --skin --face`.

   `crop` cuts a box out and enlarges it. Open `face-crop.png`, adjust the box and crop again until it's right; check the skin box the same way.

3. **Write down the traits.** Before drawing, list three to five traits you can see that will survive at 16px, in order of importance:
   - hair: colour, shape of the silhouette, parting, length, hairline (receding, widow's peak, bald);
   - glasses: frame thickness and colour, shape;
   - facial hair: moustache, beard, none;
   - face shape: a round, oval or long jaw (section 10), only if the photos plainly show it;
   - expression: a big smile, a calm smile;
   - brows, at 24 only: strong brows, only if every photo plainly shows them (section 10);
   - one colour signature: a shirt colour, a hat.

   Put them in the header's `keep:` line in that order; the blind test (step 10) checks the first two. Phrase them as things a stranger can name at 1x: a colour, a big grin, glasses, a beard. Strangers name dark hair, not short hair: at 16, short and medium hair differ by a row. Check length and texture on the pair board, or with someone who knows the person. At 24px, add one or two more. Everything else goes in `drop:` (pores, wrinkles, stubble, earrings smaller than 2px, background, lighting effects).

4. **Sample the real colours.** Skin first, mechanically, from the skin box (section 11 explains the output):

   ```bash
   python3 scripts/sprite_tool.py sample PHOTO --box "SX0,SY0,SX1,SY1" --face
   python3 scripts/sprite_tool.py ramp "#c28164" --hue 3 --value 0.09 --up 1
   ```

   `--face` flags the flash or shine cluster and the shadow cluster, prints the face average and recommends the base. Ramp that base (replace `#c28164` with yours) and map light, base, shadow and deep shadow onto `S s t u`. When photos disagree, sample the most evenly lit one, never a flash photo. Keep the skin box: step 9 checks your drawing against it.

   Then the hair, and the shirt if you use a bust, each from a small box on the lit side:

   ```bash
   python3 scripts/sprite_tool.py sample PHOTO --box "X0,Y0,X1,Y1" --colors 4
   python3 scripts/sprite_tool.py ramp "#4d4038" --down 1 --up 2 --value 0.1
   ```

   Pick each base from the lit side and replace the hex with yours; `ramp` builds the shade and light tones. Dark hair follows section 10's rule: if the sample is below luminance 55, use the slate ramp (`H #66717c`, `h #3a4148`, `d #30363c`, `k #262b30`) or the dark-brown ramp instead.

5. **Make a proportion draft** to see where the masses fall, then put it away:

   ```bash
   python3 scripts/sprite_tool.py draft "PHOTO@X0,Y0,X1,Y1" --size 16 --colors 6 --out portrait-draft-16.sprite
   python3 scripts/sprite_tool.py zoom portrait-draft-16.sprite --out portrait-draft-16.png
   ```

   The draft is mush on purpose. Use it to judge the hair's height against the face, where the hairline sits, and how wide the face is. Never trace it, and never ship it.

6. **Start from the template:**

   ```bash
   python3 scripts/sprite_tool.py new portrait-16 --template person-head-16 --out portrait-16-r1.sprite
   ```

   Rewrite its `essence:`, `keep:`, `drop:` and `note:` lines for this person.

7. **Edit in this order,** checking after each:
   1. **Palette:** put the skin ramp on `S s t u` and the hair ramp on `H h d k` (black hair: `H #66717c`, `h #3a4148`, `d #30363c`, `k #262b30`).
   2. **Hair silhouette:** reshape the cap for the hairstyle (height, parting, fringe line, length at the sides). This is the trait that does the most work.
   3. **Face shape:** if the photos plainly show an oval or a long face, swap in that jaw from section 10. Stay within 1px per side of the template.
   4. **Glasses or facial hair** from section 12.
   5. **Expression:** the template's small smile is right for a calm photo. For a photo with a big smile, use a kit grin at the kit's width (section 10, "Grins on a person head"): at 16 that's `MOUTH_TEETH` one row lower, with the eyes on rows 6–7 and the cap ending on row 3; at 24 it's the 24px person grin. A kit grin's width is a house shape, not an enlarged feature. With a moustache or beard at 16, the facial hair wins and the grin goes to the 24.

8. **Mirror** if the face and hair are symmetric, so both halves of the outline match exactly:

   ```bash
   python3 scripts/sprite_tool.py mirror portrait-16-r1.sprite --axis 16 --only "#." --out portrait-16-r2.sprite
   ```

   `--only '#.'` copies just the ink and the silhouette from the left half, so the right half keeps its own shade tones, and it prints how many pixels changed. A pixel it adds on the right arrives with a left-side tone: give it the right side's tone by hand (`t` or `u` for skin, `k` for hair). Skip this step for a side parting or any asymmetric trait, or mirror first and add the asymmetry afterwards. (`--swap S=t,H=k` mirrors every pixel and renames the lit keys; use it only on a drawing with no rim light yet.)

9. **Check and review:**

   ```bash
   python3 scripts/sprite_tool.py check portrait-16-r2.sprite --skin "S,s,t,u" --face "PHOTO@SX0,SY0,SX1,SY1"
   python3 scripts/sprite_tool.py zoom portrait-16-r2.sprite --out portrait-16-r2-zoom.png
   python3 scripts/sprite_tool.py sheet portrait-16-r2.sprite --ref "PHOTO@X0,Y0,X1,Y1" --twemoji 1f9d1 --emoji 1f9d1 --neighbor set:16:1f9d1 --neighbor set:16:1f913 --neighbor set:16:1f9d4 --out portrait-16-r2-sheet.png
   ```

   `--skin` and `--face` add one rule to the usual lint: the drawing's average skin, weighted by pixel count over the keys you name, must be within 15 luminance of the face average in the skin box. If it fails, the base came from a highlight or a shadow, the skin box took in brows, eyes or hair, or the ramp went onto the wrong keys: go back to step 4. Open both images. On the sheet, compare your drawing with the cropped photo: are the chosen traits there, in the right proportions? Then compare it with its neighbours: same outline weight, eye size and head size?

10. **Run the blind test** (`review.md` §2 has the protocol):

    ```bash
    python3 scripts/sprite_tool.py blind portrait-16-r2.sprite --control set:16:1f9d1 --out portrait-blind-r2
    ```

    `blind` writes your drawing and the approved control at 1x, 2x and a gridless 4x on white, shuffled under letters, into `show/`, and which letter is which into `key.txt`. Give three fresh reviewers (people, or new agents with no other context) only the `show/` folder and the prompt it prints. It passes when 2 of the 3 name the first two traits in your `keep:` unprompted. Ignore any misread the control gets too: dark hair on the person head reads as a "helmet", "hat" or "beard" even on the approved 1f9d1. If it fails, exaggerate the traits' *shape* (a taller hair silhouette, bolder frames, a kit grin), not their size. Test the 24 the same way, with `--control set:24:1f9d1`.

    Three more things matter for portraits (`review.md` §2 has the full protocol):
    - **One round is noisy.** Pass two rounds running, each with new reviewers and a new `--seed`, or 5 of 9 reads over three rounds. The same grid's teeth scored 2, 2, 1, 1 and 1 of 3 over five rounds.
    - **Add a skin-matched control** to any portrait that isn't yellow: approved 1f9d1 or 1f600 saved with `text --out`, with only `S s t u` changed to your sampled skin. Judge each trait against it, and stop redrawing a trait once yours is named as often as the control's.
    - **Agent reviewers are biased against darker skin.** Some named an animal face as a misread of a real-tone portrait, and of the skin-matched controls too, never of the yellow ones. The read follows the skin colour, not the drawing. Never change a sampled skin tone because of it; a person makes the respect and likeness call.

11. **Draw the 24px natively** from `person-head-24`, with the same palette and traits, plus the one or two extra traits 24 can carry: strong brows if the photos plainly show them, the 24px grin, a parting line, frame colour, an ear, a shirt collar. Section 10 has the jaw, grin and brow recipes at 24. Mirror the outline on axis 23 if it's symmetric, then check the hair tones by hand: the template's 24px hair shading is deliberately lopsided (light at the upper left), so it never mirrors cleanly.

    ```bash
    python3 scripts/sprite_tool.py new portrait-24 --template person-head-24 --out portrait-24-r1.sprite
    python3 scripts/sprite_tool.py mirror portrait-24-r1.sprite --axis 23 --only "#." --out portrait-24-r2.sprite
    python3 scripts/sprite_tool.py sheet portrait-24-r2.sprite --ref "PHOTO@X0,Y0,X1,Y1" --neighbor set:24:1f9d1 --neighbor set:24:1f913 --out portrait-24-r2-sheet.png
    ```

12. **Put both sizes on one board** and confirm they read as the same person. Check that they share the palette, the hairline's shape (arched, straight, M or parted), the mouth type and the extras. The 24 may add a trait, but it never contradicts the 16:

    ```bash
    python3 scripts/sprite_tool.py sheet portrait-16-r2.sprite portrait-24-r2.sprite --ref "PHOTO@X0,Y0,X1,Y1" --out portrait-both-r2.png
    ```

13. **Make the set variant if needed.** A portrait meant to sit among kirupa.com's yellow people gets a second version with only the skin keys swapped to smiley yellow: `S #ffff93`, `s #ffe600`, `t #ffbf00`, `u #f08e00`. Hair, glasses and expression stay, with one exception: dark hair that reaches the eye rows (sideburns, a fringe tuft) makes a dark band beside the eyes on yellow, and reads as sunglasses. If it does, trim or lighten those hair pixels on the yellow version only. Blind-test the yellow version too. Deliver both, and say which is which: the real-tone version is the likeness, the yellow one matches the set. Don't run `--skin` on the yellow one.

14. **Grade it** with SKILL.md's acceptance rubric, including its portrait lines; section 14 shows how I check those. Grade A means one fix: make it. B means the view, silhouette or grid is wrong: go back to SKILL.md Step 3 or 4. C or below means the essence is wrong: go back to Step 2.

## 14. The portrait addendum

A portrait is graded with SKILL.md's acceptance rubric like every emoji, plus its four portrait lines. This is how I check those four.

1. **A stranger names the top two traits blind.** Step 10's blind test: 2 of 3 fresh reviewers name the first two traits in `keep:` unprompted, in two rounds running, not counting misreads the controls also get. A real-tone portrait's rates are judged against its skin-matched control's.
2. **Someone who knows the person recognises them.** Show it to the person or to someone who knows them. Until then, hand it off marked "unverified": a stranger can't tell a likeness from a generic face with the same traits.
3. **Every trait is true, and nothing is caricatured.**
   - [ ] The photos were published by the person or given to me for this.
   - [ ] Every trait I drew is plainly visible in the photos.
   - [ ] Nothing is inferred: no ethnicity, age, gender, religion, health or personality traits added that the photos don't show.
   - [ ] Exaggeration is limited to the chosen traits' shapes (hair silhouette, frames, beard outline), never anatomy: no enlarged nose, ears, teeth or features. A kit grin or a section 10 jaw is a house shape, not an enlargement.
   - [ ] The expression is friendly and matches a photo; no mockery. The person would be happy to use it as their avatar.
4. **The real-tone version is the likeness; the yellow variant carries the set's harmony.**
   - [ ] The skin is the sampled base from step 4, taken from the most evenly lit photo (never a flash photo) and a clean skin box, not lightened, darkened or pushed toward a default, and `check --skin --face` passes.
   - [ ] Against its neighbours, the real-tone version is judged on outline weight, canvas fill and level of detail only, never on darkness or colour. The smiley-yellow variant is judged on full set harmony.

Section 15's line about keeping the template's rim, glint and colours untouched doesn't apply to portraits: a portrait changes the skin, the hair and often the jaw and mouth by design.

## 15. The face checklist

These are the face-specific things I check on the way to an A+. They aren't a grade; SKILL.md's acceptance rubric is.

- [ ] Both eyes are identical by translation, or differ only because the expression says so.
- [ ] Eyes are 1px wide on smileys and on 16px people (1×3 smiley and 1×2 person at 16; 1×5 smiley at 24); 24px people use 2×3 (2×2 in a bust or behind glasses).
- [ ] The mouth is one line, or an outlined hole with at most two rows inside at 16. A grin is a kit grin at the kit's width.
- [ ] On smileys and generic people, the head's rim, glint and colours are the template's, untouched. (Not on portraits: section 14.)
- [ ] Every extra (tear, hand, hat, heart) has its own ink where it leaves the head, and tears fly outward.
- [ ] Hair and skin differ in value; black hair is slate.
- [ ] Side by side with 1f642, 1f9d1 or 1f913, it looks like it belongs (a real-tone portrait: in weight, fill and detail).

## 16. Appendix: every published smiley as a recipe

**16px.** Which head and which stamps each published 16px face uses, in stamping order. "Hand-placed pixels" means a drawn detail with no stamp; read the grid with `python3 scripts/sprite_tool.py text set:16:CODE`.

| Emoji | Head | Features (gold kit names, in stamping order) |
| --- | --- | --- |
| 1f642 slightly smiling face | 15px | FACE_EYES, MOUTH_SLIGHT |
| 1f600 grinning face | 15px | FACE_EYES, MOUTH_GRIN |
| 1f603 grinning face with big eyes | 15px | EYES_BIG, MOUTH_GRIN |
| 1f604 grinning face with smiling eyes | 15px | EYES_HAPPY, MOUTH_GRIN |
| 1f601 beaming face with smiling eyes | 15px | EYES_HAPPY, MOUTH_TEETH |
| 1f606 grinning squinting face | 15px | EYES_SQUINT, MOUTH_GRIN |
| 1f605 grinning face with sweat | 15px | EYES_HAPPY, MOUTH_GRIN, SWEAT |
| 1f602 face with tears of joy | 15px | EYES_HAPPY, MOUTH_GRIN, TEARS_JOY |
| 1f643 upside down face | 15px | hand-placed pixels |
| 1f609 winking face | 15px | EYE_LEFT, EYE_WINK, MOUTH_SMILE |
| 1f60a smiling face with smiling eyes | 15px | EYES_HAPPY, BLUSH, MOUTH_SMILE |
| 1f607 smiling face with halo | 13x12, rows 4-15 | HALO, EYES_HAPPY (4 down), MOUTH_SLIGHT (2 down) |
| 1f970 smiling face with hearts | 15px | EYES_HAPPY, MOUTH_SMILE, hand-placed pixels (inked where it leaves the head) |
| 1f60d smiling face with heart eyes | 15px | HEART_EYES, MOUTH_GRIN |
| 1f929 star struck | 15px | STAR_EYES, MOUTH_GRIN |
| 1f618 face blowing a kiss | 15px | EYE_LEFT, EYE_WINK, MOUTH_KISS, HEART at (10,10) (inked where it leaves the head) |
| 1f617 kissing face | 15px | FACE_EYES, MOUTH_KISS |
| 263a smiling face | 15px | EYES_SHUT, BLUSH, MOUTH_SMILE |
| 1f61a kissing face with closed eyes | 15px | EYES_SHUT, BLUSH, MOUTH_KISS |
| 1f619 kissing face with smiling eyes | 15px | EYES_HAPPY, MOUTH_KISS |
| 1f972 smiling face with tear | 15px | FACE_EYES, MOUTH_SLIGHT, TEAR (inked where it leaves the head) |
| 1f60b face savoring food | 15px | EYES_HAPPY, MOUTH_SMILE, TONGUE_SIDE |
| 1f61b face with tongue | 15px | FACE_EYES, MOUTH_TONGUE |
| 1f61c winking face with tongue | 15px | EYE_WINK_LEFT, EYE_RIGHT, MOUTH_TONGUE |
| 1f61d squinting face with tongue | 15px | EYES_SQUINT, MOUTH_TONGUE |
| 1f911 money mouth face | 15px | dollar(), MOUTH_BILL |
| 1f917 smiling face with open hands | 15px | EYES_HAPPY (1 up), MOUTH_SMILE (1 up), a painted overlay (hand, hat, prop) |
| 1f92d face with hand over mouth | 15px | EYES_HAPPY, a painted overlay (hand, hat, prop) |
| 1fae2 face with open eyes and hand over mouth | 15px | EYES_BIG, a painted overlay (hand, hat, prop) |
| 1fae3 face with peeking eye | 15px | EYE_LEFT (1 left), EYE_RIGHT, a painted overlay (hand, hat, prop) |
| 1f92b shushing face | 15px | FACE_EYES, a painted overlay (hand, hat, prop) |
| 1f914 thinking face | 15px | EYES_DOWN1, hand-placed pixels, a painted overlay (hand, hat, prop) |
| 1fae1 saluting face | 13px, 1 right | LIDS_FLAT, MOUTH_FLAT at (1,2), a painted overlay (hand, hat, prop) |
| 1f910 zipper mouth face | 15px | FACE_EYES, ZIPPER |
| 1f928 face with raised eyebrow | 15px | EYES_DOWN2, hand-placed pixels, MOUTH_FLAT (1 down) |
| 1f610 neutral face | 15px | FACE_EYES, MOUTH_FLAT |
| 1f611 expressionless face | 15px | EYES_FLAT, MOUTH_FLAT |
| 1f636 face without mouth | 15px | FACE_EYES |
| 1f60f smirking face | 15px | LIDS_RIGHT, MOUTH_FLAT, hand-placed pixels |
| 1f612 unamused face | 15px | LIDS_RIGHT, MOUTH_FROWN |
| 1f644 face with rolling eyes | 15px | EYES_ROLLED, MOUTH_FROWN |
| 1f62c grimacing face | 15px | FACE_EYES, TEETH_CLENCHED |
| 1f62e-200d-1f4a8 face exhaling | 15px | BROWS_ARCHED, EYES_SHUT_LOW, MOUTH_O_SMALL, a painted overlay (hand, hat, prop) |
| 1f925 lying face | 15px | FACE_EYES (1 up), NOSE_LONG, hand-placed pixels |
| 1fae8 shaking face | 13px, 1 up | FACE_EYES (1 down), hand-placed pixels, SHAKE_ARCS |
| 1f642-200d-2194-fe0f head shaking horizontally | 13px, 1 left | CALM13 at (-1,1), hand-placed pixels |
| 1f642-200d-2195-fe0f head shaking vertically | 13px, 1 right | CALM13 at (1,2), hand-placed pixels |
| 1f60c relieved face | 15px | BROWS_ARCHED, EYES_SHUT_LOW, MOUTH_SMILE (1 down) |
| 1f614 pensive face | 15px | BROWS_WORRIED, EYES_SHUT_LOW, hand-placed pixels |
| 1f62a sleepy face | 15px | BROWS_WORRIED, EYES_SHUT_LOW, MOUTH_OPEN_FROWN, DROP_SLEEPY |
| 1f924 drooling face | 15px | EYES_HAPPY, MOUTH_SMILE, DROOL |
| 1f634 sleeping face | 13px | EYES_SHUT (2 down), MOUTH_O_SMALL (2 down), Z_SIGN |
| 1fae9 face with bags under eyes | 15px | EYES_HEAVY, hand-placed pixels, SMALL_FROWN |
| 1f637 face with medical mask | 15px | EYES_HAPPY, a painted overlay (hand, hat, prop) |
| 1f912 face with thermometer | 15px | BROWS_WORRIED, EYES_LOW, a painted overlay (hand, hat, prop) |
| 1f915 face with head bandage | 15px | EYES_HAPPY (1 down), MOUTH_FROWN, a painted overlay (hand, hat, prop) |
| 1f922 nauseated face | 15px | EYES_SQUINT, hand-placed pixels |
| 1f92e face vomiting | 15px | EYES_SQUINT, a painted overlay (hand, hat, prop) |
| 1f927 sneezing face | 15px | EYES_SQUINT, hand-placed pixels, a painted overlay (hand, hat, prop) |
| 1f975 hot face | 15px | BROWS_WORRIED, EYES_LOW, HOT_MOUTH, SWEAT, drop() |
| 1f976 cold face | 15px | FACE_EYES, TEETH_CLENCHED, a painted overlay (hand, hat, prop) |
| 1f974 woozy face | 15px | hand-placed pixels, MOUTH_WOOZY, BLUSH |
| 1f635 face with crossed out eyes | 15px | EYES_X, MOUTH_O |
| 1f635-200d-1f4ab face with spiral eyes | 15px | SPIRAL, SPIRAL (6 right), MOUTH_WAVY |
| 1f92f exploding head | 13px | hand-placed pixels, MOUTH_O (1 down), a painted overlay (hand, hat, prop) |
| 1f920 cowboy hat face | 13px | FACE_EYES (4 down), MOUTH_SMILE (3 down), a painted overlay (hand, hat, prop) |
| 1f973 partying face | 13px | EYES_HAPPY (4 down), a painted overlay (hand, hat, prop) |
| 1f60e smiling face with sunglasses | 15px | MOUTH_SMILE, a painted overlay (hand, hat, prop) |
| 1f913 nerd face | 15px | NERD_TEETH, a painted overlay (hand, hat, prop) |
| 1f9d0 face with monocle | 15px | EYE_LEFT, hand-placed pixels, a painted overlay (hand, hat, prop) |
| 1f615 confused face | 15px | FACE_EYES, hand-placed pixels |
| 1fae4 face with diagonal mouth | 15px | FACE_EYES, hand-placed pixels |
| 1f61f worried face | 15px | BROWS_WORRIED, EYES_LOW, MOUTH_FROWN (1 down) |
| 1f641 slightly frowning face | 15px | FACE_EYES, MOUTH_FROWN |
| 2639 frowning face | 15px | FACE_EYES, MOUTH_FROWN, hand-placed pixels |
| 1f62e face with open mouth | 15px | FACE_EYES, MOUTH_O |
| 1f62f hushed face | 15px | BROWS_UP, FACE_EYES (1 down), MOUTH_O_SMALL (1 down) |
| 1f632 astonished face | 15px | BROWS_UP, FACE_EYES (1 down), MOUTH_O, hand-placed pixels |
| 1f633 flushed face | 15px | EYES_ROUND, hand-placed pixels |
| 1faea distorted face | 15px | EYES_ROUND, hand-placed pixels |
| 1f97a pleading face | 15px | BROWS_WORRIED, EYES_PUPPY, hand-placed pixels, SMALL_FROWN |
| 1f979 face holding back tears | 15px | BROWS_WORRIED, EYES_PUPPY, hand-placed pixels, MOUTH_SLIGHT (1 down) |
| 1f626 frowning face with open mouth | 15px | FACE_EYES, GASP_BELL |
| 1f627 anguished face | 15px | BROWS_WORRIED, EYES_LOW, GASP_BELL |
| 1f625 sad but relieved face | 15px | BROWS_WORRIED, EYES_LOW, MOUTH_FROWN (1 down), drop() |
| 1f622 crying face | 15px | FACE_EYES, MOUTH_FROWN, TEAR flipped (inked where it leaves the head) |
| 1f62d loudly crying face | 15px | BROWS_WORRIED, EYES_HAPPY (1 down), STREAMS, MOUTH_O, hand-placed pixels |
| 1f616 confounded face | 15px | EYES_SQUINT, MOUTH_ZIGZAG |
| 1f623 persevering face | 15px | EYES_SQUINT, MOUTH_ARCH |
| 1f61e disappointed face | 15px | EYES_DOWN, SMALL_FROWN |
| 1f613 downcast face with sweat | 15px | EYES_DOWN, SMALL_FROWN, SWEAT |
| 1f629 weary face | 15px | BROWS_WORRIED, EYES_SHUT, GROAN |
| 1f62b tired face | 15px | EYES_SQUINT, GROAN |
| 1f971 yawning face | 15px | EYES_HAPPY, YAWN, a painted overlay (hand, hat, prop) |
| 1f624 face with steam from nose | 15px | BROWS_ANGRY, EYES_SHUT (1 down), MOUTH_FROWN, STEAM, STEAM flipped |
| 1f620 angry face | 15px | GLARE, MOUTH_FROWN |
| 1f92c face with symbols on mouth | 15px | GLARE, a painted overlay (hand, hat, prop) |

**24px.** The same for the 24px faces built from the kit's `simple()` recipe. The rest (tilted, covered or prop-heavy faces) are drawn whole; read them with `python3 scripts/sprite_tool.py text set:24:CODE`.

| Emoji | Eyes | Mouth | Brows | Extras |
| --- | --- | --- | --- | --- |
| 1f600 grinning face | bar | grin | - | - |
| 1f603 grinning face with big eyes | tall | grin | - | - |
| 1f604 grinning face with smiling eyes | arch | grin | - | - |
| 1f601 beaming face with smiling eyes | caret | beam | - | - |
| 1f606 grinning squinting face | squint | laugh | - | - |
| 1f605 grinning face with sweat | arch | grin | - | sweat at (17,0) |
| 1f642 slightly smiling face | bar | smile_s | - | - |
| 1f609 winking face | bar + caret | smile_s | - | - |
| 1f60a smiling face with smiling eyes | arch | smile | - | blush |
| 263a smiling face | closed | smile | arc | blush |
| 1f617 kissing face | bar | kiss | - | - |
| 1f61a kissing face with closed eyes | closed | kiss | - | blush |
| 1f619 kissing face with smiling eyes | arch | kiss | - | - |
| 1f61b face with tongue | bar | tongue | - | - |
| 1f61d squinting face with tongue | squint | tongue | - | - |
| 1f610 neutral face | bar | flat | - | - |
| 1f611 expressionless face | line | flat | - | - |
| 1f636 face without mouth | bar | none | - | - |
| 1f60f smirking face | half | smirk | - | - |
| 1f612 unamused face | half | frown_s | - | - |
| 1f644 face with rolling eyes | roll | frown_s | - | - |
| 1f62c grimacing face | bar | grimace | - | - |
| 1f60c relieved face | closed | smile_s | arc | - |
| 1f614 pensive face | closed | frown_s | worried | - |
| 1f61f worried face | short | frown | worried | - |
| 1f641 slightly frowning face | bar | frown_s | - | - |
| 2639 frowning face | bar | frown | - | - |
| 1f62e face with open mouth | bar | O | - | - |
| 1f62f hushed face | low | o | arc | - |
| 1f632 astonished face | white | OO | - | - |
| 1f633 flushed face | white | flat_s | - | blush |
| 1f626 frowning face with open mouth | low | sad_open | - | - |
| 1f627 anguished face | low | sad_open | worried | - |
| 1f616 confounded face | squint | zigzag | - | - |
| 1f623 persevering face | squint | frown | worried | - |
| 1f61e disappointed face | lid | frown | worried | - |
| 1f613 downcast face with sweat | lid | frown | - | sweat at (0,0) |
| 1f629 weary face | squint | wail | worried | - |
| 1f62b tired face | squint | wail | - | - |
| 1f620 angry face | short | frown | angry | - |
| 1f621 enraged face | short | frown | angry | red head |
| 1f635 face with crossed out eyes | cross | O | - | - |
| 1f635-200d-1f4ab face with spiral eyes | spiral | wavy | - | - |
| 1f974 woozy face | low + lid | wavy | - | blush |
| 1f97a pleading face | plead | frown_s | worried | - |
| 1f60d smiling face with heart eyes | heart | grin | - | - |
| 1f929 star struck | star | grin_t | - | - |

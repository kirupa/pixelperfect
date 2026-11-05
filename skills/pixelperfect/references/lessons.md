# Lessons: what Kirupa taught me, in his words

I didn't learn pixel art from a book. I learned it from Kirupa's critiques of my worst work, one message at a time. This file keeps his words exactly as he wrote them, typos included, grouped by the principle each one taught. Under every quote is what I was doing wrong and the rule it produced. The rules are the ones the rest of this skill applies.

A few of his messages were passed on to me by another agent working on the project; they're marked "relayed". Section 23 collects notes from the project's review passes. Those aren't Kirupa's words, and they're labelled that way.

## How it started

The job began as a conversion: "Create a converted version of ALL TWEMOJI visuals". So I converted. I shrank Twemoji's vector art onto a 16×16 grid, let the resampler pick the pixels, and called the result pixel art. Faces turned to mush, outlines broke into slivers, and every icon had too many colours.

His first reaction was mild: "Can you create a few more variations and compare it to Twemoji and actual emoji to see you can do better." Within hours it was "The designs look comically bad." By the next evening: "The eyes in all of your smileys are uncannily bad" and "You have failed me for the last time."

He never gave me a style guide. He made me look, compare, explain my failures and fix them, and he kept doing it until the rules below were second nature.

## The lessons at a glance

| # | Principle | The rule it produced | Where the skill applies it |
| --- | --- | --- | --- |
| 1 | Draw by hand | Place every pixel on purpose; a converted image is a proportion draft at most | SKILL.md Steps 1–5 |
| 2 | Judge at real size | Judge at 1x; zoom is for editing | Step 13; `review.md` §2 |
| 3 | Study the masters | Look at real emoji and great sprites before and after drawing | Steps 1 and 13; `sheet` |
| 4 | One black outline | A clean 1px #000000 line round every silhouette | Step 5; `construction.md` §2 |
| 5 | Every piece outlined | Each separate important shape gets its own full outline | `construction.md` §2 |
| 6 | The inside matters | Ramps, light, planes and material inside the outline | Steps 7–9; `worked-examples.md` §3 |
| 7 | Essence | Write the essence first; keep, exaggerate, drop | Step 2 |
| 8 | Reimagine | Pick the view and design that pixels can draw | Step 3 |
| 9 | Contrast | Neighbouring parts differ in value, not just hue | Steps 7–8; `construction.md` §6 |
| 10 | Round shapes | Circles from a profile table; the body first at full size | Step 6; `construction.md` §3 |
| 11 | Straight lines | Clean runs and regular steps; no extraneous detail | Step 6; `construction.md` §4 |
| 12 | Inner ink | Black inside only for the five reasons at 16px | Step 7; `construction.md` §5 |
| 13 | Symmetry | Draw half and mirror it | Steps 4 and 13; `mirror` |
| 14 | Eyes | Identical, mirrored, at the house size: 1px wide on smileys and 16px people | Step 10; `faces.md` §1–3 |
| 15 | Harmony | Match the set's ramps, weight and detail | Steps 8 and 13; `sheet --neighbor` |
| 16 | Shade only solids | Upper-left light on solid forms; flat things stay flat | Step 9; `construction.md` §7–8 |
| 17 | Motion follows the source | Tears stream outward, never hang | Step 10; `faces.md` §1 |
| 18 | Recognisable or redo | If nobody can name it at 1x, it isn't done | Step 13 |
| 19 | Grade honestly | Anything below A+ is redrawn, in numbered revisions | Step 13; `review.md` §4 |
| 20 | Generalise | One critique fixes every icon with the same fault | `review.md` §9 |
| 21 | 24px is not a resize | Same care, drawn natively, fixed together with the 16 | Step 11 |
| 22 | Proposals | Show candidates side by side; the owner chooses | Step 14; `kirupa-pipeline.md` |
| 23 | Review notes | Lessons from review passes, not Kirupa's words | — |

## 1. Draw by hand; never convert

> "You have given a black outline. But the details inside look bad. Think of yourself as a world famous pixel artist who hand-crafts every pixel on a 16x16 grid. The goal is to simplify complex ideas into a form that can be represented as pixel art."

**What I was doing:** letting a resampler choose the pixels. A downsampled image has no intent. It produces half-tone slivers, broken outlines and blurred features, because it averages instead of deciding.

**The rule:** every pixel is placed by hand, for a reason. The `draft` command exists only to check proportions against a photo or an emoji; it's thrown away once the silhouette is blocked. The art is drawn, never converted.

## 2. Judge it at real size

> "Make sure the icons look clear in 16x16 before blowing it up."

**What I was doing:** admiring my sprites at 8x. At 8x every pixel is a tidy tile and everything looks deliberate. At 1x, where people actually see the icon, half of the detail vanished and the rest merged.

**The rule:** the 1x render is the judge, on a light and on a dark background. The 8x zoom is a workbench for editing. A detail that can't be seen at 1x is spending pixels for nothing. This is also why the 24 is never an upscale of the 16: each size has to be clear at its own real size.

## 3. Study the masters, then compare honestly

> "Can you give all of the pixel icons a black outline first. Take a look at the style of the darkproject mini-icons for inspiration"

> "Study 8-bit sprites from old video games like Zelda Link to the Past for more details."

> "If you had to draw a typical pixelated smiley, do it using your own logic and compare it to the darkproject version. Notice what is different about yours vs. darkprojects. Remember those differences and apply them"

> "keeping it inline with the high quality of the Darkproject and Nintendo Gameboy/NES/SNES style"

**What I was doing:** drawing from imagination and from Twemoji, and never putting my work next to anything good.

**The rule:** before drawing, look at the subject in real emoji renders and at approved sprites of similar subjects. After drawing, put yours beside them on one board and list, in words, what's different. Each difference is either a fix or a decision you can defend. The style target is Darkproject's mini-icons and Nintendo's Game Boy, NES and SNES sprites: black outlines, high contrast, few colours, clean lines.

**Tools:** `twemoji`, `emoji` and `find` gather the references; `sheet --twemoji CODE --emoji CODE --neighbor SPRITE` puts them side by side.

## 4. One black outline round everything

> "Notice the clean outlines in black that are noticeable"

> "ensure the details are properly outlined in black and nothing is left to the viewer's imagination."

**What I was doing:** outlines in the subject's dark colour, outlines with gaps where a curve was hard, and outlines that doubled up into 2px smudges at corners.

**The rule:** one continuous 1px line of pure black (#000000) round the whole silhouette. It touches the colour inside on one side and transparency on the other, and it never doubles. At 24px no other colour may touch transparency. At 16px the only exceptions are a 1px-thin line (steam, a whisker) and a dark part that is its own edge. A black seam just inside the outline reads as a heavy double border: use the material's dark tone there instead. Lint calls that a "hug".

## 5. Every important shape gets its own outline

> "when the shape has individual pieces (like this falling rock), each individual shape should have a black outline as well. The black outlines aren't optional."

> "Don't blindly just think about the rocks and the eyes. Any important shape in each emoji needs its own full outline."

**What I was doing:** outlining the main body and leaving loose pieces (rocks, drops, sparks, hearts) as bare colour floating on transparency.

**The rule:** a piece that stands apart from the body (a drop, a rock, a heart, a hat, a second object) is a separate shape and gets its own full outline. "Important" is the test: if the piece carries meaning, ink it all the way round. Note the lesson behind the lesson: he named two examples, and he meant every subject.

## 6. The outline is not the drawing: the inside matters

> "The details inside the outline are important as well."

> "The smileys are better, but the rest of the shapes can still do more work."

> "Don't use the outlines as an excuse for doing a shoddy job. Focus on bread. For bread, look at this attached example that looks very nice. Tell me why yours looks terrible."

**What I was doing:** once everything had a black outline, I treated the job as done. Inside, my bread was one or two flat tan tones from Twemoji, split by black lines like stained glass.

**The rule:** the outline makes the icon legible; the inside makes it good. My answer about the bread became the rules for every subject:

1. Give each material a 4–6-tone, hue-shifted ramp, and light it.
2. Use the full value range within one object, from almost black to almost white. Pastels go muddy at pixel scale.
3. Draw seams and parts with a darker local tone, not black lines.
4. Choose the view that shows the planes: top, side and cut face give three tones.
5. Show the material: sparse crumb holes, a few highlight clusters.
6. Design the silhouette for the grid: clean steps and readable negative space.
7. Reimagine the source wherever it fails at pixel size.

`worked-examples.md` §3 shows the approved bread built this way.

## 7. Find the essence; simplify and enhance

He told me to ask: "What is the essence of what I want to highlight?"

> "Not every detail will make sense, so you shouldn't try to crowd the grid with every thing that would fit. Simplify and enhance is the key."

> "you can't have all the details. You need to be careful about what pixel is important and what isn't."

**What I was doing:** fitting in everything the source had, because there was room. The grid filled with details nobody could read, and the one detail that made the subject recognisable got lost among them.

**The rule:** before the first pixel, write the essence as one line (the `essence:` header in every `.sprite` file), then three lists: what to keep, what to exaggerate, and what to drop. "Simplify" means dropping everything that doesn't serve the essence. "Enhance" means making what's left bigger, bolder and cleaner than it is in the source. Lint notes a sprite with no `essence:` line.

## 8. Reimagine what doesn't translate

> "The best example is the coffee emoji. In the original Twemoji, it is a 3D version, which works when you have antialiased lines. In the darkproject version, it is simplified to a 2D side profile view, which translates very nicely to pixel art. The colors are subtly different to indicate a curvature."

> "It is ok to reinterpret the intent, kind of like coffee. fully 3D is hard in pixel art. But that doesn't mean the ice cube has to look bad either."

> "Remember to reimagine them as needed if the emoji version doesn't make sense"

> "For UFO, if you are showing the beam, go with a more side-profile version"

> "feel free to explore different microphone styles if that would be easier to represent in 16x16."

**What I was doing:** copying the source's camera angle. Twemoji's mug is a 3D cup seen from above, with an elliptical rim. At 16px that ellipse is a lumpy ring of mismatched pixels.

**The rule:** the subject is fixed; the view and the design are mine to choose. The default is a flat side profile, because pixel grids draw straight edges and simple curves well and draw perspective badly. A slight difference in colour, not perspective, suggests the curve. Use three-quarter view only when the 3D is the essence (an ice cube, a gift box, dice, a loaf of bread), and then draw it well. If a style of the object is hard to draw at 16px, change the style: a different microphone, a side-on saucer. `worked-examples.md` §2, §5 and §7 show the mug, the microphone and the saucers.

## 9. Maximise contrast

> "Notice how darkproject maximizes contrast to ensure legibility of detail"

> "The icons right now have features that aren't really noticeable."

**What I was doing:** neighbouring parts in different hues of the same lightness, such as a red part against a green part of equal value. In colour they look different. At 1x, and to anyone with colour-blindness, they merge.

**The rule:** contrast carries the detail. Each ramp spans a wide range of values, and neighbouring parts differ in value, not just hue. The `zoom` board's greyscale panel shows the truth; if two parts melt together in greyscale, make one lighter or darker. Lint warns about "equal-value" pairs of saturated colours.

## 10. Round shapes are built, not traced

> "Pay attention to how round shapes are represented by Darkproject. The icons you just showed me look terrible"

> "Make the 16x16 orange look less squished" (relayed)

> "The site's logo is an orange. Use that as an inspiration if needed." (relayed)

> "more round and less squishy"

**What I was doing:** circles traced from a vector, with runs that grew, shrank and grew again, so they looked lumpy or octagonal. Later, a tangerine whose leaves and stem took pixels from the fruit. It was 14 wide and 11 tall, and lint passed it.

**The rule:** a round shape uses a circle profile in which runs only grow toward the middle and only shrink away from it. `construction.md` §3 has the tables for each size. Draw the full body first, as a true circle, and put accessories (stems, leaves, hands, props) outside it. Then measure the body alone: width and height should match unless the subject really is oval. Lint can't see "squished"; your measurement can. `worked-examples.md` §4 shows the round tangerine.

## 11. Sharp straight lines, and no extraneous detail

> "8-bit pixel art tends to go more for sharper straight lines and minimizing extraneous details."

> "The coffee one looks really bad. Compare it to darkproject's version of coffee"

> "Notice the cleaner lines."

> "the microphone doesn't look good. It looks curved."

**What I was doing:** diagonals with irregular steps and L-shaped joins, so straight things looked bent. My microphone handle wobbled from step to step and read as a curve.

**The rule:** straight edges are straight runs. A diagonal is a regular staircase (1:1 or 2:1 steps) whose steps touch only at their corners, never side by side in an L. If an object can't be drawn straight at its angle, change the angle or the design. `construction.md` §4 has right-and-wrong grids, and `worked-examples.md` §5 has the straight microphone.

## 12. Black inside only where it earns its place

> "Simpler designs are better than blotchy black lines that muddle the image."

> "For the 16x16, notice from darkproject when dark outlines are used inside the visual vs. just being on the outline. This is going to be an important part of validating the design to be just right."

**What I was doing:** carrying the 24px habit of inking every part down to 16px. At 16px there's no room: inner black lines merge into blotches and swallow the colour.

**The rule:** at 16px, black goes inside the silhouette only for five reasons: holes and openings, deep crevices and undersides, face features, overlaps of similar values that only a line can split, and line art that is the symbol itself. Every other inner border is the darker tone of the part it belongs to. At 24px, ink each important piece. Lint warns when inner ink passes 12% of a 16px sprite and stops it at 22%. `construction.md` §5 has the details.

## 13. Symmetry is exact

> "Also, keep symmetry in mind."

> "make the skull and cross bones 24x24 one be more symmetrical. Right now, the skull is very lopsided compared to the bones."

**What I was doing:** placing both halves of a symmetric subject by hand, and lighting it from one side with so many tones that the light itself made it look lopsided.

**The rule:** draw one half and `mirror` it, so the silhouette is exact. A symmetric subject keeps symmetric features. Its light can still come from the upper left, but if one-sided shading makes the subject look lopsided, light it from the top instead. Lint's mirror check lists the pixels that break near-symmetry. `worked-examples.md` §6 shows the skull.

## 14. Eyes: identical, simple, one pixel wide on smileys

> "The eyes in all of your smileys are uncannily bad"

> "For faces, there are two eyes and they should look identical unless there is an expression being shown."

> "It looks unnecessarily bad because both the eyes are off." (on an octopus)

> "For the smileys, notice that the darkproject smileys for the vertical eyes are just one pixel thick. Mimic that so that these look harmonious when placed SxS to them."

> "For zany face, wouldn't it be better to have the left eye also have a white background with a black eye?"

**What I was doing:** shrunken Twemoji eyes, several pixels wide with whites and highlights, that read as mush at 1x, and two eyes that didn't match.

**The rule:** eyes are 1px wide on smileys and on 16px people (1×3 smiley and 1×2 person at 16; 1×5 smiley at 24); 24px people use 2×3 (2×2 in a bust or behind glasses). A plain eye is a solid vertical bar, and the second eye is its mirror image. Eyes differ only when the expression says so: a wink, a squint, a zany look. Even then, treat both eyes the same way: if one eye gets a white with a black pupil, so does the other, though their sizes may differ. `faces.md` §1–3 has the kit.

## 15. Harmony with the set

> "For the smileys, match the yellow tone of the darkproject yellow smilies"

**What I was doing:** choosing colours per icon. Each icon looked fine alone; side by side, the yellows didn't match, and some icons were heavier, busier or smaller than their neighbours.

**The rule:** an emoji is part of a set. Use the set's shared ramps (the smiley yellow is in `faces.md`), and compare your drawing with approved neighbours for weight, fill, saturation and level of detail. His phrase "harmonious when placed SxS" is the test: put it side by side with its neighbours and look.

## 16. Shade only what is solid

> "The beveled look only makes sense if the underlying shape is 3d. For example, the beam from the UFO is not and shouldn't be beveled."

**What I was doing:** applying the same light and bevel to every pixel of every icon, including the saucer's beam of light, flags and printed signs.

**The rule:** light comes from the upper left, and only solid forms receive it: fruit, bodies, heads, rocks, leaves, stems. Flat things stay flat: symbols, flags, print, paper, beams, glows, fire, water and screens. Light, fire and glows give light; they don't receive it. `construction.md` §7–8 has the light and the flat list.

## 17. Motion follows the source

> "the tear drops should be going outward like in the original source version. The shouldn't be going straight down. It looks like an earring right now."

> "fix the 24x24 similarly to ensure the tears don't look like they are drooping."

**What I was doing:** hanging the tears of rolling on the floor laughing straight down from the eyes, where they read as jewellery.

**The rule:** effects carry the source's motion. Tears of laughter stream outward from the squeezed eyes, and so does every effect whose direction carries meaning: sweat, steam, motion lines. Check the source emoji for direction before drawing an effect, and fix the 24 along with the 16.

## 18. If nobody can name it, it isn't done

> "the paw prints, you can't even tell they are paw prints."

> "The country flags are really bad as well. Fix them."

**What I was doing:** drawing the parts without checking the whole. My paw print's toes merged into its pad, and my flags lost their counts and proportions.

**The rule:** recognisability comes before everything. Name it at 1x in half a second, or it goes back to Step 2. Paw prints are a big pad with separate, fully outlined toe pads above it. A flag is drawn by count and proportion and stays flat. `worked-examples.md` §9 and §10 show both.

## 19. Grade it honestly, and iterate in revisions

> "For every pixel art visual you created, ask yourself what grade you will give it compared to the various other pixel art that you have seen. If you will give anything less than an A+, regenerate it."

> "Once you have generated, do a thorough analysis of the output. For ones that don't meet your bar, create new versions. Keep incrementing the rev for those versions so that we can see the progression"

**What I was doing:** declaring done when the drawing was finished, not when it was good.

**The rule:** grade every drawing against the best pixel art you know. A grade below A+ means another revision, saved as a new file (`-r2`, `-r3`), so the progression stays visible and you can go back. For a hard subject, draw several variants and compare them. `review.md` §4 has the rubric and the grades.

## 20. Generalise every lesson

> "Generalize your learnings for all emojis. Not just the bread themed ones."

> "Also don't just focus on the smileys."

**What I was doing:** fixing exactly the icon he named and nothing else.

**The rule:** a critique of one icon is a bug report for a whole class. When one drawing fails, write the failure down as a rule, find every drawing with the same fault, and fix them all. That's how this file came to exist.

## 21. The 24px gets the same care

> "Can you make them 24x24 and still maintain your focus on ensuring they are high quality."

> "a clean 16x16 and 24x24 version"

**What I was doing:** treating the 24 as an enlarged 16, or as a place for every detail the 16 dropped.

**The rule:** the 24 is drawn natively on its own grid, never resized from the 16. It earns a little more detail (an inked piece, a highlight, an ear, a parting), but it shows the same emoji with the same essence. A fix to one size means checking the other: the drooping tears needed fixing at both sizes.

## 22. Show proposals; the owner decides

> "Create the proposals but don't make the change to the main list. Show me for evaluation first"

> "Provide an additional UFO"

> "If you are adding a net-new emoji, make sure you add it for all of the themes."

**What I was doing:** replacing approved art with my newest revision without asking.

**The rule:** present candidates side by side, say which you'd pick and why, and let Kirupa choose. Nothing reaches the published set without his go-ahead. A new emoji (like the floating saucer, a saucer without its beam) ships in every theme, not just the Pixel sets.

## 23. Review notes (not Kirupa's words)

The project also ran review passes over the art. Their notes taught me lessons too. These are quoted from those notes, not from Kirupa.

- **Light is for solid forms.** One review note limited the light to solid, rounded forms, treating flames and glows as light sources. Another refined it: "leaves, petals and stems are solid forms and keep the shading you've given them" and "Only truly flat things stay flat: beams, rays, glows and printed details." **Rule:** if a part has volume, light it, however thin it is.
- **The face nobody asked for.** On the radioactive sign: "at 1x the rounded blobs + center dot read as a FACE (two eyes, nose, mouth)". **Rule:** look at every icon at 1x for faces and figures you didn't intend; any two dots above a line will become one. `worked-examples.md` §8 shows the fix.
- **Hollow loops read as letters.** "the hollow black-ringed loops look like glyphs". **Rule:** a ring of ink with nothing inside reads as type at 1x. Give a loop a body colour inside its ink.
- **Name what it reads as.** One drawing would "read as a yellow crown or comb". **Rule:** when a reviewer names something else, that's the bug report. Change the silhouette until the wrong reading is impossible.
- **People are not boxes.** "the two torsos are square boxes". **Rule:** shoulders slope and torsos taper; give a figure a rounded or stepped shoulder line, never a rectangle.
- **Small heads become symbols.** "the families read as crosses or a churchyard" and "A small square reads as a round dot, but a plus reads as a cross." **Rule:** at a tiny size a head is a small square, not a plus shape, which reads as a cross. `construction.md` §11 has the group rules.

## What I'd tell my beginner self

1. Don't shrink anything. Draw it.
2. Write the essence before the first pixel, and drop everything that doesn't serve it.
3. Judge at 1x. The zoom flatters.
4. One clean black line round the outside, and around every piece that matters.
5. Earn every black pixel inside. At 16px, name its reason or recolour it.
6. Circles come from a table; diagonals from a regular step.
7. Value before hue. Check the greyscale panel.
8. Light the solid things from the upper left; leave flat things flat.
9. Two eyes, identical, at the house size: one pixel wide on smileys and 16px people.
10. Put your drawing beside the masters, the source and its neighbours, and say what's different.
11. Grade it. Anything below A+ is another revision.
12. When one icon is corrected, fix every icon with the same fault.
13. Show proposals. The owner decides.

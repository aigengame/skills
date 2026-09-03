# Skill selection guide image prompts

The checked-in image was produced with the built-in image generation tool in
one initial generation and two final edits. The prompts below are preserved
verbatim. Intermediate, discarded constellation variants are omitted because
they do not describe the final map asset.

Result: [skill-selection-guide.png](skill-selection-guide.png)

## Initial generation

```text
Use case: infographic-diagram
Asset type: lightweight decision guide for a GitHub README
Primary request: Create a lively, friendly hand-drawn decision map that helps software developers choose one of four Agent Skill areas. It must feel approachable, playful, and light, never heavy, intimidating, corporate, or bureaucratic.
Scene/backdrop: warm off-white sketchbook paper with very subtle natural paper texture and generous whitespace
Subject: one small central hand-drawn question card branches into four loose, colorful hand-drawn cards; the four cards flow gently toward a small sprouting plant that represents evidence and learning; one soft curved dotted arrow loops from the sprout back to the central question
Style/medium: polished editorial doodle illustration; loose pencil and felt-tip marker lines; slightly imperfect hand-drawn arrows; small simple icons: compass for design, stepping stones for execution, magnifying glass for review, growing sprout for compounding; clean and professional despite the playful warmth
Composition/framing: wide landscape composition for a GitHub README, balanced and airy, easy to scan at reduced width, no dense connectors, no rigid boxes, no large title
Color palette: soft muted coral, sky blue, mustard yellow, mint green, and lavender with charcoal-gray outlines; low visual weight; strong enough contrast for readable text
Text (verbatim): "What does the work need now?"; "Design under uncertainty"; "Uncertain direction"; "Execute reliably"; "Controlled delivery"; "Review and maintain coherence"; "Quality and coherence"; "Compound project learning"; "Keep state and lessons"; "Evidence and learning"; "Inform the next decision"
Typography: friendly large hand-lettered print, not cursive; exact spelling and capitalization; render every quoted phrase exactly once; category names larger than their short descriptions
Constraints: preserve the logical mapping of each category to its description; arrows must be unambiguous; ample whitespace; suitable for both light and dark GitHub themes because the image has its own warm paper background; no logos, no watermark, no extra text
Avoid: dark background, gradients, glossy UI, 3D, corporate flowchart styling, technical architecture-diagram styling, tiny type, crowded ornament, scary or serious mood, people, robots
```

## Final map edit

```text
Use case: precise-object-edit
Asset type: preview variant of a hand-drawn decision guide for a GitHub README
Input images: Image 1 is the edit target.
Primary request: Replace only the Big Dipper evidence metaphor and its title with a lightweight hand-drawn map metaphor.

Evidence icon:
Remove the seven-star constellation and all of its constellation connection lines. In the same space above the bottom purple card, draw a small open terrain-map vignette rather than a paper document: two simple green hill contours, one short blue river curve, and a warm-gold landmark. Four short route fragments in coral, blue, yellow, and green enter the terrain and join into one clear purple dotted route. The purple route becomes more complete as it crosses the terrain, then ends at the top of the vignette. Keep the illustration airy, iconic, and readable at small README size.

Feedback:
Connect the existing central purple dotted feedback arrow directly from the top endpoint of the map's purple route upward through the clear central gap to the bottom edge of the "What does the work need now?" card. Keep it away from the "Compound project learning" card and do not cross any card, icon, text, or solid arrow.

Text edit:
Replace exactly "Evidence grows" with exactly "Evidence builds the map" on one centered line in the bottom purple card. Keep "Informs the next decision" unchanged and clearly readable.

Map constraints:
The map must look like an observed landscape or terrain model, not a folded sheet of paper, document, checklist, dashboard, navigation app, location pin, compass, globe, or treasure map. No stars. The metaphor is that evidence from the four work areas gradually builds a usable map of the terrain.

Invariants:
Keep the healthy bright-green sprout in "Compound project learning" unchanged. Keep every other word and letter unchanged. Preserve exactly: "What does the work need now?", "Design under uncertainty", "Uncertain direction", "Execute reliably", "Controlled delivery", "Review and maintain coherence", "Quality and coherence", "Compound project learning", "Keep state and lessons", "Informs the next decision". Keep the compass, stepping stones, magnifying glass, four category cards, solid colored arrows, color assignments, positions, spacing, warm paper texture, aspect ratio, and overall lively hand-drawn style unchanged.
Constraints: edit only the evidence icon, its purple feedback connection, and its title; exact spelling and capitalization; no extra text; no logos; no watermark.
```

## Final subtitle edit

```text
Use case: text-localization
Asset type: hand-drawn decision guide for a GitHub README
Input images: Image 1 is the edit target.
Primary request: Replace exactly the bottom subtitle text "Informs the next decision" with exactly "Guides the next decision".
Text (verbatim): "Guides the next decision"
Typography and placement: Preserve the same hand-lettered black style, font size, weight, baseline, centering, spacing, and position inside the bottom purple rounded card.
Constraints: Change only that one subtitle. Keep every other word and letter unchanged. Preserve exactly: "What does the work need now?", "Design under uncertainty", "Uncertain direction", "Execute reliably", "Controlled delivery", "Review and maintain coherence", "Quality and coherence", "Compound project learning", "Keep state and lessons", and "Evidence builds the map". Keep the terrain-map vignette, four colored routes, central purple dotted route and feedback arrow, compass, stepping stones, magnifying glass, healthy green sprout, all cards, arrows, borders, colors, positions, spacing, warm paper texture, 3:2 aspect ratio, and lively hand-drawn style unchanged. No extra text, no logos, no watermark.
```

# Generated game artwork

Created for this project with the built-in image_gen tool on 2026-10-21. Original generated PNGs are retained unchanged; runtime code extracts sprite regions, preserves transparency and scales to the game's existing cells. The terrain art contains no paths; scenery.py draws paths from config.py. No combat rules or collision sizes are encoded in these images.

Files:
- character-atlas.png: apple, orange, watermelon, carrot, slime, bat, golem and stone thrower.
- garden-ground.png: garden grass ground.
- forest-ground.png: forest clearing ground.

## Generation prompts

### carrot_atlas

Use case: stylized-concept. Production asset: one 2D tower-defense character SPRITE SHEET, landscape 2:1 canvas. Exactly FOUR equal columns and TWO equal rows, 8 isolated characters, centered in their own equal rectangular cell, ample transparent gutters, no text, no labels, no grid lines. TRUE transparent background. Top row left to right: (1) plump glossy red apple defender with stem and single green leaf, cute determined face (2) juicy orange defender with peel texture, leaf and cheerful eyes (3) large green striped whole watermelon defender with confident face, distinctly broad oval shape (4) friendly bright orange carrot objective with lush green leafy crown and big kind eyes. Bottom row left to right: (5) lime-green translucent teardrop slime monster (6) purple bat monster with wide outstretched wings and small pink ears (7) chunky blue-gray stone golem, rounded rock segments, sturdy feet, warm glowing small eyes (8) ochre little rock creature holding a round pebble above its head, recognizable ranged stone-thrower. All original non-branded characters, polished premium mobile-game hand-painted 2.5D illustration, rounded forms, crisp dark colored outlines, sculpted soft shading, subtle highlights, tiny elliptical soft contact shadows, expressive faces, top-down/three-quarter game view, entire character including wings and leaves fully inside its cell, consistent scale and lighting. Each silhouette must remain readable at 40 pixels. No ground, landscape, panels or interface. Do not overlap cells.

### carrot_garden

Use case: stylized-concept. Production asset: a landscape 3:2 top-down flat grass terrain background for a cute polished 2D tower-defense game, hand-painted mobile-game art, fresh spring garden. Edge-to-edge grassy ground, warm jade and sage green meadow, very subtle organic patches of clover and fine blades, softly dappled sunlight from upper left, tiny white daisies and yellow petals sparsely concentrated at the extreme corners. Entire center 90 percent open low-contrast buildable grass, no large distinct objects. Fine quiet paper-painted texture with soft round shapes, beautiful but subdued so small colorful game sprites stand out. Strict overhead orthographic ground view, no horizon, no perspective vanishing point. No paths or roads, no grids, no stones blocking cells, no trees, no bushes, no water, no buildings, no characters, no text, no UI, no frames. The game's road will be drawn over this art separately.

### carrot_forest

Use case: stylized-concept. Production asset: a landscape 3:2 top-down flat grass terrain background for a cute polished 2D tower-defense game, hand-painted mobile-game art, peaceful forest clearing. Edge-to-edge mossy grassy ground in muted emerald, sage, and blue-green teal, soft diffuse forest canopy light, subtle moss and tiny fern-like ground leaves sparsely concentrated at extreme corners, a few tiny pale blue flowers. Entire center 90 percent open low-contrast buildable grass. Keep terrain light enough to read green monsters and gray creatures clearly; softly shaded, not nighttime or black. Fine quiet painterly texture and rounded shapes, no photorealism. Strict overhead orthographic ground view, no horizon, no perspective vanishing point. No paths, roads, grid, large stones, trees, bushes, water, buildings, characters, text, UI or frames. A sand road will be drawn over the art by game code.


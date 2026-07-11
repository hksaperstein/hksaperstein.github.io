---
layout: project
title: "Procedural Dice Asset Generator"
description: "A headless-Blender pipeline that procedurally generates a labeled library of TTRPG dice (d4-d20): geometry, engraved or printed numerals, and physically-based materials, exported as USD with ground-truth manifests."
date: 2026-07-05
categories: [Machine Learning, Computer Vision]
featured_image: "/assets/images/projects/dice-detection/featured.png"
gallery:
  - file: "/assets/images/projects/dice-detection/asset-sample-grid.png"
    description: "8 of the 500 generated assets, spanning all 6 die types and a range of material/glyph combinations"
  - file: "/assets/images/projects/dice-detection/detection-scene-raw.jpg"
    description: "A raw rendered detection scene: physics-scattered dice, distractor primitives, and an HDRI-lit textured ground, before any annotation pass"
  - file: "/assets/images/projects/dice-detection/detection-scene-annotated.jpg"
    description: "The same pipeline's COCO annotations overlaid — occlusion-aware boxes, one per visible die, with class/material/glyph metadata"
---

## Overview

This is a headless Blender (5.1.2) Python pipeline, `src/datagen/`, that procedurally generates a labeled library of the 6 standard tabletop RPG dice — d4, d6, d8, d10, d12, d20 — as individual textured 3D assets. Every asset exports as USD alongside a JSON manifest recording every parameter that went into generating it, which makes the library a fully labeled synthetic dataset, built with an eventual object-detection pipeline in mind. The gallery has a sample of what actually came out of it.

## Geometry

The fun part of this section: getting a d12's pentagons or a d10's kite faces right without hand-authoring any topology. Each die's mesh comes from a fixed vertex set run through Blender's boolean tooling instead.

- **Base vertices:** the standard Platonic-solid coordinates for d4/d6/d8/d12/d20, plus an empirically-derived pentagonal-trapezohedron set for d10.
- **Initial approach — hand-author the face/vertex topology:** easy to get subtly wrong on a 12- or 20-sided solid.
- **What I used instead:** `bmesh.ops.convex_hull` on the raw vertices, then `dissolve_limit` to merge the hull's coplanar triangles back into real faces — quads for the d10's kites, pentagons for the d12.
- **Face numbering:** follows real dice conventions — opposite faces sum to 7 on a d6, 21 on a d20, and so on. The d4 is the exception: its faces sit opposite a vertex, not another face, so there's no pairing and values are assigned once each.

## Glyphs and Materials

Numerals and materials are both randomized per asset from a fixed set of manufacturing-accurate methods.

- **Glyph application — 2 methods, chosen at random per asset:** engraved (boolean-cut into the mesh, optional painted recessed fill) and printed decal (UV-unwrapped face textures).
- **Glyph styles — 5 supported:** arabic, roman, greek, CJK numerals, and pips. Pips are restricted to d6 and d4 only, matching how real dice are actually numbered.
- **Materials — 6 procedural PBR categories:** opaque, translucent, marbled, glitter, metallic, speckled, all built from Blender shader nodes.
- **Randomization:** every asset gets randomized hue/saturation/value/roughness, plus category-specific parameters — IOR and transmission for translucent, noise scale for marbled, and so on.

## Results

- **500 assets** generated, **0 recorded failures**, **0 validation errors** from `scripts/validate_dice_assets.py` (verified against `data/raw/dice_sets_v1/manifest.json` and `failures.json`).
- **By die type:** 94 d4, 88 d6, 88 d8, 83 d10, 84 d12, 63 d20.
- **By material:** 94 metallic, 86 translucent, 85 glitter, 84 speckled, 80 marbled, 71 opaque.

Worth a look yourself: the sample grid in the gallery shows 8 of the 500 side by side, spanning every die type and a mix of the material/glyph combinations above.

## Notable Bugs

The boolean-engrave step turned out to be the fiddliest part of the pipeline, and it surfaced a few real correctness bugs worth recording:

- **Silent no-op cuts.** On one d20 with arabic numerals, Blender's EXACT boolean solver silently no-op'd on all 20 numeral cuts — the die's body came out byte-for-byte untouched, with each cutter just appended as inert debris, and nothing about the die's volume changed enough to look wrong. Fix: a connected-component face-count check alongside the existing volume check. A real cut always grows the largest connected shell it touches, so if that shell's face count doesn't increase after a cut, the pipeline now retries with the FLOAT solver instead.
- **Full-die collapse on a degenerate cutter.** A d10 with greek numerals hit a case where the EXACT solver collapsed the entire die's volume on a single glyph cut, because the source glyph (a capital Alpha) had residual non-manifold edges from font curve-fill self-overlap even after welding. Fix: snapshot the die's volume before each cut; if a single cut would remove more than half of it (geometrically impossible for a numeral engraving), roll back and retry with FLOAT.
- **Unwelded cutter meshes corrupting geometry.** Converting extruded text curves to mesh leaves duplicate, unwelded vertices at every seam, which occasionally crashed the boolean solver outright and gutted one die into disconnected garbage fragments. Fix: weld the cutter mesh and recompute normals before it's used as a boolean operand.

None of these were exotic edge cases — they were real assets in the batch failing in real ways, caught by generating at scale and checking the output rather than assuming the boolean op just works.

## Testing

- **Pure-logic modules** — numbering, the parameter sampler — tested with plain pytest.
- **Blender-API-dependent code** — run through `blender --background --python`, using a shared test harness.
- **Initial issue:** Blender's background mode exits with code 0 even when the script raises an uncaught exception, so a bare `assert` inside a background script can't actually fail the shell command that ran it.
- **Fix:** the harness catches exceptions explicitly and calls `sys.exit(1)` on failure or `sys.exit(0)` on success, so Blender-dependent tests fail the way a test actually should.

## Object Detection Dataset

The asset library exists to build a synthetic object-detection dataset from it: rendered scenes of multiple dice scattered on a table, with per-die bounding boxes. I haven't trained a detector on it yet — everything below is about the dataset itself, not a trained model. The two extra gallery shots are straight from this pipeline: one raw scene, one with the annotations drawn on top so you can see what the boxes actually catch.

### Scene composition

- **Dice per scene:** 3-8, sampled randomly from the 500-asset library.
- **Placement:** dropped onto a ground plane and settled with a short rigid-body physics simulation, rather than hand-picked poses.
- **Distractors:** 0-5 random primitives (cubes, spheres, cones, torii, slabs, sticks) scattered into the same simulation, so the model gets negative examples of things that aren't dice, not just positive examples of things that are.
- **Ground material:** flat color, or one of 4 procedural two-tone patterns (noise, voronoi, checker, wave).
- **Lighting:** a random HDRI environment map per scene, with randomized rotation and strength.
- **Camera:** randomized azimuth, elevation, and focal length; about half the shots get real depth-of-field with a randomized aperture.
- **Post:** sensor noise, exposure jitter, and randomized JPEG quality on the output image — closes some of the gap between a clean render and an actual photo.

### Occlusion-aware annotation

- **Approach:** boxes come from a second render pass, not from projecting each die's 3D silhouette.
- **How it works:** after the beauty shot, every die is swapped to a unique flat-emission color, the background goes black, and the scene is re-rendered at 1 sample — giving an exact per-pixel visibility mask per die.
- **Result:** a die that's mostly buried under another die gets a box around the part that's actually visible, not its full unoccluded footprint.
- **Cutoff:** dice with fewer than 60 visible pixels are skipped entirely, rather than boxed for something the model realistically couldn't see.

### Output

- **10,000** rendered scenes.
- **51,505** individual die annotations, COCO format.
- **7 label classes:** d4, d6, d8, d10, d10_pct, d12, d20.
- Rendered across **6 parallel Blender worker processes**, each deterministic from a shared seed, then merged into one `coco.json`.

### Bugs worth recording

Same as the asset generator, this pipeline had real bugs that only surfaced at scale:

- **Depth-of-field leaking into the ID pass.** The occlusion pass initially inherited the beauty render's camera settings, DOF included. Blurring a flat-color ID image smears colors across neighboring pixels, and one die's box came out 706px wide from only 672 actually-visible pixels. Fix: force DOF and exposure off before the ID pass renders.
- **sRGB-encoded IDs colliding.** The ID pass PNG stores sRGB-encoded values, and decoding them as if they were already linear shifted two adjacent dice's ID colors into the same bucket, merging their boxes into one. Fix: explicitly linearize the raw pixel values before mapping them back to die indices.
- **A checkpoint bug that orphaned 6,193 images.** The first version of the renderer wrote its annotation shard file once, at the very end of the run. A worker killed mid-run left thousands of rendered JPEGs on disk with zero annotations recorded for any of them. Fix: checkpoint every 20 scenes, with resume logic that only counts a scene as done if it's both in the checkpoint and its file still exists on disk.

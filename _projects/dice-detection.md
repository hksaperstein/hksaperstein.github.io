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

This is a headless Blender (5.1.2) Python pipeline, `src/dice_gen/`, that procedurally generates a large library of the 6 standard tabletop RPG dice shapes — d4, d6, d8, d10, d12, d20 — as individual textured 3D assets. Every asset is exported as USD alongside a JSON manifest recording every parameter that went into generating it: die type, size, numbering scheme, glyph style and method, material category and its randomized parameters, and the random seed. That makes the whole library a fully labeled synthetic dataset, generated with an eventual object detection/recognition pipeline in mind — the ground-truth manifests exist specifically so a downstream model has something to train against.

## Geometry

Each die's base shape starts from a literal list of known vertex coordinates — the standard Platonic-solid vertices for d4/d6/d8/d12/d20, and an empirically-derived pentagonal-trapezohedron vertex set for d10. Rather than hand-authoring face/vertex-index topology (easy to get subtly wrong on a 12- or 20-sided solid), those vertices are run through `bmesh.ops.convex_hull` followed by `dissolve_limit`: the convex hull computes the correct facets from the raw point set, and dissolve_limit merges the hull's coplanar triangles back into the real faces (quads for the d10's kites, pentagons for the d12, and so on).

Face numbering follows real-world dice conventions per die type — opposite faces of a d6 sum to 7, a d20 to 21, and so on for the others. The d4 is the exception: its faces are opposite a vertex rather than another face, so there's no opposite-face pairing for it, and its values are just assigned once each.

## Glyphs and Materials

Numerals are applied using two real, manufacturing-accurate methods, chosen at random per asset: **engraved** (boolean-cut directly into the mesh, optionally with a painted recessed fill) and **printed decal** (UV-unwrapped face textures). Five glyph styles are supported — arabic, roman, greek, and CJK numerals, plus pips — with pips restricted to d6 and d4 only, matching how real dice are actually numbered.

Materials come from 6 procedural PBR categories built from Blender shader nodes: opaque, translucent, marbled, glitter, metallic, and speckled. Every asset gets randomized hue/saturation/value/roughness, plus category-specific parameters where relevant — IOR and transmission for translucent, noise scale for marbled, and so on.

## Results

The current generated library is 500 assets, with 0 recorded failures during generation and 0 validation errors from `scripts/validate_dice_assets.py` against the resulting manifest (verified directly against `data/raw/dice_assets/manifest.json` and `failures.json`).

By die type: 94 d4, 88 d6, 88 d8, 83 d10, 84 d12, 63 d20.

By material category: 94 metallic, 86 translucent, 85 glitter, 84 speckled, 80 marbled, 71 opaque.

## Notable Bugs

The boolean-engrave step turned out to be the fiddliest part of the pipeline, and it surfaced a few real correctness bugs worth recording:

- **Silent no-op cuts.** On one d20 with arabic numerals, Blender's EXACT boolean solver silently no-op'd on all 20 numeral cuts — the die's body came out byte-for-byte untouched, with each cutter just appended as inert debris, and nothing about the die's volume changed enough to look wrong. That one required adding a connected-component face-count check alongside the existing volume check: a real cut always grows the largest connected shell it touches, so if that shell's face count doesn't increase after a cut, the pipeline now retries with the FLOAT solver instead.
- **Full-die collapse on a degenerate cutter.** A d10 with greek numerals hit a case where the EXACT solver collapsed the entire die's volume on a single glyph cut, because the source glyph (a capital Alpha) had residual non-manifold edges from font curve-fill self-overlap even after welding. The fix snapshots the die's volume before each cut and, if a single cut would remove more than half of it (geometrically impossible for a numeral engraving), rolls back and retries with FLOAT.
- **Unwelded cutter meshes corrupting geometry.** Converting extruded text curves to mesh leaves duplicate, unwelded vertices at every seam, which occasionally crashed the boolean solver outright and gutted one die into disconnected garbage fragments. Fixed by welding the cutter mesh and recomputing normals before it's used as a boolean operand.

None of these were exotic edge cases — they were real assets in the batch failing in real ways, caught by generating at scale and checking the output rather than assuming the boolean op just works.

## Testing

Pure-logic modules — numbering and the parameter sampler — are tested with plain pytest. Everything that depends on the Blender API is tested by running scripts through `blender --background --python`, using a shared test harness. That harness exists for a specific reason: Blender's background mode exits with code 0 even when the script raises an uncaught exception, so a bare `assert` inside a background script can't actually fail the shell command that ran it. The harness catches exceptions explicitly and calls `sys.exit(1)` on failure or `sys.exit(0)` on success, so Blender-dependent tests fail the way a test actually should.

## Object Detection Dataset

The asset library exists to build a synthetic object-detection dataset from it: rendered scenes of multiple dice scattered on a table, with per-die bounding boxes. I haven't trained a detector on it yet — everything below is about the dataset itself, not a trained model.

### Scene composition

Each scene drops 3-8 dice, sampled randomly from the 500-asset library, onto a ground plane and runs a short rigid-body physics simulation so they settle the way real dice actually land instead of sitting at hand-picked poses. I also scatter 0-5 distractor primitives — cubes, spheres, cones, torii, slabs, sticks — into the same simulation, so a model trained on this data has negative examples of things that aren't dice, not just positive examples of things that are. The ground gets a randomized material (flat color, or one of four procedural two-tone patterns), and the scene is lit by a random HDRI environment map with randomized rotation and strength, so the same 500 dice show up under a wide range of lighting and backgrounds across the dataset.

Camera azimuth, elevation, and focal length are all randomized, and about half the shots get real depth-of-field with a randomized aperture. Sensor noise, exposure jitter, and randomized JPEG quality get applied to the final image on the way out, closing some of the gap between a clean render and an actual photo.

### Occlusion-aware annotation

Bounding boxes come from a second render pass, not from projecting each die's 3D silhouette. After the beauty shot, every die is swapped to a unique flat-emission color, the background goes black, and the scene is re-rendered at 1 sample. Reading that image back gives an exact per-pixel visibility mask per die, so a die that's mostly buried under another die gets a box around the part that's actually visible, not its full unoccluded footprint. Dice with fewer than 60 visible pixels are skipped entirely rather than getting a box drawn around something the model realistically couldn't see.

### Output

The full run is 10,000 rendered scenes and 51,505 individual die annotations in COCO format, across 7 label classes (d4, d6, d8, d10, d10_pct, d12, d20). I split the render across 6 parallel Blender worker processes, each deterministic from a shared seed, then merged their shard files into one `coco.json`.

### Bugs worth recording

Same as the asset generator, this pipeline had real bugs that only surfaced at scale:

- **Depth-of-field leaking into the ID pass.** The occlusion pass initially inherited the beauty render's camera settings, DOF included. Blurring a flat-color ID image smears colors across neighboring pixels, and one die's box came out 706px wide from only 672 actually-visible pixels. Fixed by forcing DOF and exposure off before the ID pass renders.
- **sRGB-encoded IDs colliding.** The ID pass PNG stores sRGB-encoded values, and decoding them as if they were already linear shifted two adjacent dice's ID colors into the same bucket, merging their boxes into one. Fixed by explicitly linearizing the raw pixel values before mapping them back to die indices.
- **A checkpoint bug that orphaned 6,193 images.** The first version of the renderer wrote its annotation shard file once, at the very end of the run. A worker killed mid-run left thousands of rendered JPEGs on disk with zero annotations recorded for any of them. I added checkpointing every 20 scenes, with resume logic that only counts a scene as done if it's both in the checkpoint and its file still exists on disk.

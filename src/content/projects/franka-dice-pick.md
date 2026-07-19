---
title: "Robotic DnD"
description: "DnD is a game of chance, and control is an illusion. Training a robot to hand me the right die felt like the next best thing."
date: 2026-07-11
featured: true
categories: [Robotics, Machine Learning, AI]
featured_image: "/assets/images/projects/franka-dice-pick/featured.jpg"
github_url: "https://github.com/hksaperstein/rl"
training_curves: true
training_curves_title: "Stage 1: Default training"
gallery_title: "Stage 2: D20 grasping"
gallery_intro: "The scripted pipeline picks four of the five die types reliably. Here's each one, plus the d4 attempt that fails exactly as predicted."
preview:
  overview: "This project combines two interests of mine, DnD and robotic manipulation. With a Franka Panda in Isaac Lab, I explore RL models, training hyperparameters, and techniques - all to simply help me with my next role. Hoping for that sweet nat 20."
  tools: [NVIDIA Isaac Lab, YOLO, Claude Code]
  highlight: "Four of the five die types pass. The d4 doesn't - I called that one before the demo ran. Flat gripper pads squeeze a tetrahedron right out of the grasp, and I haven't solved it yet."
gallery:
  - file: "/assets/videos/projects/franka-dice-pick/dice_pick_d20.mp4"
    section: "Picks by commanded type"
    description: "Commanded d20: the detector finds it among the five dice, depth deprojection gives the 3D target, and the staged DiffIK sequence descends, grasps, and lifts."
  - file: "/assets/videos/projects/franka-dice-pick/dice_pick_d12.mp4"
    section: "Picks by commanded type"
    description: "Commanded d12, same pipeline."
  - file: "/assets/videos/projects/franka-dice-pick/dice_pick_d10.mp4"
    section: "Picks by commanded type"
    description: "Commanded d10 — one of the smaller dice, which is where the grasp tolerance work below actually mattered."
  - file: "/assets/videos/projects/franka-dice-pick/dice_pick_d8.mp4"
    section: "Picks by commanded type"
    description: "Commanded d8, same pipeline."
  - file: "/assets/videos/projects/franka-dice-pick/dice_pick_d4.mp4"
    section: "The permitted failure"
    description: "The d4. Flat parallel pads squeeze a tetrahedron out of the grasp even with sub-millimeter convergence — declared as a permitted failure before the demo ran, and it failed exactly that way."
---

## Overview

A Franka Panda in Isaac Lab picks whichever die I name off a five-die table, using a detector I built in a [separate project](/projects/dice-detection/). It's a provided asset in Isaac Lab - the platform the built-in manipulation examples are built around - so I get to focus on the RL and perception software instead of arm hardware. The point of this page isn't the pick itself - it's what the pick proves: a manipulation platform working end to end, ready for a trained RL policy on top of it. Four of the five die types pick reliably today with a scripted controller; the d4 doesn't, and I'll get to why.

## The pipeline

One fixed camera looks at the table. Every pick runs the same sequence:

- The detector — YOLO, trained entirely on synthetic renders from the dice generator — identifies every die in the frame.
- Depth deprojection turns the commanded die's detection into a 3D target. A geometric plausibility filter rejects anything that deprojects outside the physical band above the table; it earned its keep by catching a false positive on a hole in the table that "existed" below the surface.
- A staged differential-IK sequence descends on the target: a joint-space ready-to-descend prep stage, a canonical straight-down grasp orientation, and bounded per-step commands.
- The gripper closes with a grasp-position tolerance of about 5mm. It started at 15mm, which quietly passes 30mm dice and loses 15–18mm ones — the residual exceeds the die's radius, so the fingers close beside it.

## What Isaac Lab taught me the hard way

- The dice USDs are authored in millimeters-as-units, and the detector was trained on renders that assume exactly that. A uniform 0.001 import scale reproduces the training distribution; per-die scale factors would distort the size distribution, which the detector actually reads as a class cue.
- A visual-only USD gets no physics from `RigidObjectCfg`. The rigid-body, collision, and mass properties only modify schemas that already exist — on a schema-less USD they silently do nothing. The fix is applying the physics APIs at runtime and then setting the tuned values.
- A DomeLight-only scene renders near-black to a camera sensor. Add a DistantLight, render extra RTX frames before reading the output, and reset the scene after the sim — otherwise the camera's pose reads as zeros and NaNs.
- Rigidly holding the Franka's default ready-pose orientation during descent funnels the arm into joint-limit branches no matter where the target is. The straight-down quaternion plus bounded relative stepping fixed it — and made low IK damping safe again.

## Status

The scripted pipeline — detector, depth deprojection, staged IK descent, grasp — works today. The controller is scripted, not learned. Four of the five die types pick successfully with it; the d4 is the known exception. Learned grasping on top of this same platform is the declared next phase, listed below under what's next.

## Results

Four of the five die types — d20, d12, d10, d8 — pick successfully with the scripted pipeline; videos of each run are in the gallery. The trained detector, built entirely on synthetic renders, identifies and 3D-localizes all five dice on the demo table at confidences of 0.89–0.96, checked against but never driven by simulator ground truth. Tightening the grasp-position tolerance from 15mm to about 5mm was what got the smaller 15–18mm dice actually gripped instead of squeezed past. The geometric plausibility filter on depth deprojection caught a real false positive during development: a hole in the table that "existed" below the surface.

## Challenges

The d4 is the honest failure here. Flat parallel pads squeeze a tetrahedron out of the grasp even when the descent converges to under a millimeter. This was declared a permitted failure before the demo ran, it failed exactly as predicted, and it stays on the books as an open problem — the candidate fixes are a reorient, an edge grasp, or a push-assist, and I haven't built any of them yet.

## What's next

- Phase I of the RL line: detector-derived observations inside a trained policy — the reason this platform exists.
- A d4 grasp strategy.
- A second camera angle. A single fixed view occludes the die the moment the gripper closes around it, so the current videos verify the pick through convergent evidence; a second angle would make the video evidence unambiguous on its own.

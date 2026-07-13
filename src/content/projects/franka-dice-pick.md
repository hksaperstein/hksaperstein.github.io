---
title: "Robotic DnD"
description: "DnD is a game of chance, and control is an illusion. Training a robot to hand me the right die felt like the next best thing."
date: 2026-07-11
featured: true
categories: [Robotics, Machine Learning, AI]
featured_image: "/assets/images/projects/franka-dice-pick/featured.jpg"
github_url: "https://github.com/hksaperstein/rl"
training_curves: true
gallery:
  - file: "/assets/images/projects/franka-dice-pick/detection-overlay.png"
    section: "Detection"
    description: "The trained detector on the demo scene: all five dice identified and 3D-localized, confidences 0.89–0.96. The green markers are simulator ground truth, overlaid for verification only — the pick sequence never reads them."
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

This is where two other projects on this site converge: the [dice detector](/projects/dice-detection/) and the Isaac Lab manipulation platform. Command a die type — d20, say — and a Franka Panda in Isaac Lab finds that die on a five-die table using the trained detector, then picks it up with a staged inverse-kinematics sequence. Object positions come from the detector plus depth deprojection; the simulator's ground truth is used to verify the result, never to drive it. Four of the five die types pass. The d4 doesn't, and I'll get to why.

To be clear about what this is and isn't: the controller is scripted, not learned. What the demo proves is the platform — assets, camera, detector, IK, gripper — and the perception bridge between them. Learned grasping on top of this stack is the open next phase.

## Why a Franka

The manipulation work started on a different arm, and across a long series of training experiments the policy reliably learned to reach but never to grasp and lift. Part of that is scale: a 2.8cm gripper aperture closing on 18mm objects leaves very little margin, where the Franka's 8cm aperture — the platform Isaac Lab's own manipulation examples are built around — leaves a lot. This project has a standing rule: after repeated non-improving results, escalate to a structurally different approach instead of tuning the same one. So the platform pivoted to the Franka, and the perception stack came along unchanged.

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

## The d4

The honest failure. Flat parallel pads squeeze a tetrahedron out of the grasp even when the descent converges to under a millimeter. This was declared a permitted failure before the demo ran, it failed exactly as predicted, and it stays on the books as an open problem — the candidate fixes are a reorient, an edge grasp, or a push-assist, and I haven't built any of them yet.

## The agentic workflow

This repo is as much an experiment in agentic engineering as in robotics. The demo milestone was reached by Claude Code agent teams working through staged gates — camera and projection, perception, grasping, and finally video capture — each gate with its own spec, implementation plan, and review before the next one opened. I direct and make the calls; agents implement, review each other's work, and record what they learn in a knowledge base of transferable findings, which is where most of the hard-won list above comes from. Negative results get written down with the same care as wins — that's a rule, not a preference. The [agentic experiments page](/projects/agentic-ai-experiments/) is where I'm collecting the broader pattern.

## What's next

- Phase I of the RL line: detector-derived observations inside a trained policy — the reason this platform exists.
- A d4 grasp strategy.
- A second camera angle. A single fixed view occludes the die the moment the gripper closes around it, so the current videos verify the pick through convergent evidence; a second angle would make the video evidence unambiguous on its own.

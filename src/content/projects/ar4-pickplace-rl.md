---
title: "AR4 Pick-and-Place RL"
description: "Training a pick-and-place policy for the Annin Robotics AR4 arm in Isaac Lab, with a real camera-based perception pipeline in the loop."
date: 2026-07-09
featured: true
categories: [Robotics, Machine Learning, AI]
featured_image: "/assets/images/projects/ar4-pickplace-rl/featured.jpg"
github_url: "https://github.com/hksaperstein/rl"
gallery:
  - file: "/assets/videos/projects/ar4-pickplace-rl/perception_calibration.mp4"
    section: "Perception"
    description: "Calibration clip: a cube slides across the camera's view while the shape classifier's live labels are overlaid, used to sanity-check perception before trusting it downstream."
  - file: "/assets/videos/projects/ar4-pickplace-rl/ar4_pickplace_perception.mp4"
    section: "Perception"
    description: "Evaluation episode driven entirely by the real perception pipeline (ground-plane removal, shape classification, tracking) instead of privileged simulator state, detection overlay burned in."
  - file: "/assets/videos/projects/ar4-pickplace-rl/eval-episode-cube.mp4"
    section: "Cube Evaluation Episode"
    description: "A recorded evaluation episode of the cube pick-and-place policy, run against the checkpoint from the longest completed cube training run."
  - file: "/assets/images/projects/ar4-pickplace-rl/tensorboard-episode-termination.png"
    section: "Training Metrics"
    description: "TensorBoard scalars for the binary success-termination metrics, across all three logged runs: cube_reached_goal, sphere_reached_goal, and time_out. Both reached_goal metrics stay effectively at zero — reward climbing is not the same as the task being solved."
  - file: "/assets/videos/projects/ar4-pickplace-rl/eval-episode-sphere-a.mp4"
    section: "Sphere Evaluation Episodes"
    description: "The AR4 positioned near the sphere target during a sphere-task evaluation episode."
  - file: "/assets/videos/projects/ar4-pickplace-rl/eval-episode-sphere-b.mp4"
    section: "Sphere Evaluation Episodes"
    description: "Another sphere-task evaluation episode — the gripper reaches the sphere but the task has not yet produced a reliable lift (see the write-up below)."
  - file: "/assets/images/projects/ar4-pickplace-rl/tensorboard-sphere-reward-hacking.png"
    section: "Reward-Hacking Evidence"
    description: "TensorBoard scalars from the 1500-iteration grasp-bonus run: grasp_sphere (left) climbs and saturates near its theoretical max, while lifting_sphere (right) never moves off zero — the reward term was learned without the target behavior."
---

## Overview

This is an Isaac-Lab-based reinforcement learning project training a pick-and-place policy for the Annin Robotics AR4, a 6-DOF arm. There are two ways the trained policy can act:

- **Privileged-state**, where training and evaluation read ground-truth object pose directly from the simulator.
- **Real perception**, where the policy instead acts on the output of a camera-based pipeline: ground-plane removal, shape classification, and object tracking. The tracker holds the object's last-known position through brief occlusion — for example, when the gripper itself blocks the camera's view of the object mid-grasp — rather than losing the object the instant it's out of view.

## Perception

Before trusting the perception stack downstream of anything, there's a calibration script that slides a cube across the camera's field of view and overlays the detector's live shape labels on the recorded video. It's a cheap way to catch a broken pipeline before it quietly corrupts a training or eval run.

Running it against real depth data surfaced a real limitation, not a success: the shape classifier currently misclassifies the real cube and the rectangular prism as "sphere," while only the wedge classifies correctly. The classifier's thresholds were tuned on synthetic data, and they don't generalize to the noise profile of a real depth sensor. It's a known, tracked issue rather than something papered over — the perception calibration clip in the gallery above shows it directly.

## Cube Pick-and-Place

For the cube task, I'll describe this honestly rather than attach a number to it: the training reward can climb from partial credit — the policy reaching toward the cube, then lifting it — well before the binary "reached goal" termination metric moves off zero. The "Training Metrics" chart in the gallery is a real TensorBoard screenshot pulled directly from the logged runs: `cube_reached_goal` sits flat at zero for the full 1500 iterations of the longest cube run. Reward climbing is not the same as the task being solved, and I'm not going to claim an aggregate success rate the logs don't actually support.

The "Cube Evaluation Episode" clip in the gallery is a single recorded episode from that checkpoint, not a cherry-picked success — it shows the policy approaching the cube and attempting the grasp. Judge the outcome yourself from the footage rather than from a claim I'd have to hedge anyway.

## The Sphere Retarget, and a Reward-Hacking Negative Result

After the cube task, I retargeted the same environment to a sphere, reusing the existing robot/scene/camera infrastructure. As a follow-up experiment, I added a dense "grasp bonus" reward term — rewarding the policy for closing the gripper whenever the end-effector is near the sphere — adapted from Isaac Lab's own cabinet-manipulation task's `grasp_handle` reward pattern.

Over a 1500-iteration run, that reward term worked exactly as specified: `grasp_sphere` climbed from zero and saturated near its theoretical maximum well before training ended. The policy reliably learned to close the gripper near the sphere. But the metrics that actually mattered — lifting and goal-reaching — never moved off zero. The "Reward-Hacking Evidence" chart in the gallery is the actual TensorBoard scalar data from that run, side by side: `grasp_sphere` climbing to ~0.28 against `lifting_sphere` pinned at zero the entire time.

Pulling and visually inspecting frames from the eval video (10 episodes) showed why: 0 of 10 episodes had a real grasp. The gripper's fingers visibly closed in each one, but the sphere sat beside the closed gripper rather than between the jaws, and never left the ground. The "Sphere Evaluation Episodes" clips in the gallery above are from sphere-task evaluation runs — you can see the same pattern: the gripper reaches the sphere's position, but there's no lift.

The root cause was the reward's own design: it only checked end-effector-to-object distance plus gripper closure, with no check that the object was actually enclosed between the fingers. The policy found the cheapest way to satisfy that — closing the gripper near the sphere via the already-loose reaching kernel — without ever producing a geometrically correct grasp.

This was judged a worse failure mode than an earlier no-op result on the same task, because a reward term that's trivially satisfiable without the target behavior risks entrenching a fake-grasp local optimum in the production reward if left in place. So the code was reverted rather than merged — only the design/report documentation and the roadmap entry describing what was tried and why it failed were kept. I'd rather have an honest negative result on record than a reward function that looks like it's working and isn't.

**Recommended next step**: a contact-sensor-based reward, or at minimum a stricter geometric check requiring the sphere to sit between the two finger positions — closer to Isaac Lab's own `align_grasp_around_handle`/`approach_gripper_handle` combination than a bare end-effector-to-object distance check. I tried both. Below is what happened.

## The Bug That Was Quietly Explaining Everything

The stricter geometric check came first: a reward that only pays out when the sphere sits between the two fingertip frames, not just near the end-effector generally. It didn't get reward-hacked, but it also never fired once in 1500 iterations — the alignment window was so tight relative to the sphere's own 9mm radius that random exploration essentially never stumbled into it.

Building the contact-sensor version that came after that surfaced something more important than the experiment itself: the offset I'd been using to locate the gripper's pinch point from the wrist link was wrong by 5.4cm. I had it at 9cm; the real distance, measured directly off the robot's own link positions, is 3.6cm. Every "reaching" reward in every experiment up to that point had been maximizing proximity to a point 5.4cm from where the jaws actually meet, not the jaws themselves. That's a more satisfying explanation for a lot of the earlier failures than any individual reward design was.

With the offset fixed and a real contact-sensor reward requiring bilateral force from both jaws, I got the first genuine grasp contact of the project — sustained, correctly-filtered bilateral contact on about 92% of steps. The sphere still never left the ground. The arm would reach, grip, and then freeze in place for the rest of the episode. Real progress on "does the gripper ever close on the object," and a new, more specific problem in its place.

## More Reward Shaping, More Negative Results, Then a Pivot

A real grasp didn't get the sphere off the ground either. I tried a dense lift-height reward gated behind a training curriculum, then the same reward active from the start, then a learning-rate bump timed to when the literature said exploration usually collapses, then a proper potential-based reward (Ng, Harada, and Russell's formulation, which is supposed to guarantee the shaping can't change the optimal policy). All of them failed. The potential-shaping one taught me something concrete along the way: my formula had a sign bug that made *holding* a good position actively cost more reward than never approaching the object at all — which is exactly the behavior I saw in the eval video. I fixed the bug, tried again with a fresh scene and a stillness penalty (which also shipped with an inverted sign the first time, caught before wasting a training run rather than after), and still got nothing: 0 of 10 real evaluation episodes showed a controlled grasp-and-lift. One of them briefly looked like a lift, until I stepped through the video frame by frame and found the sphere had actually been knocked loose by a glancing collision and was drifting mid-air, disconnected from a gripper that was still sitting on the ground. Shrinking the sphere to give the gripper more clearance ruled out "the object's too big" as an explanation too.

At that point I switched the graspable object back to a cube and moved every future experiment there. Not because the cube is easier — it isn't, particularly — but because the sphere had absorbed most of a week's worth of experiments without answering the underlying reach/grasp/lift questions, and I wanted a cleaner slate to test the fixes below on.

## The First Real Grasp

Back on the cube, comparing this project's setup against Isaac Lab's own reference lift task turned up two real differences: this repo used double the reference's action scale for joint-position commands, and the cube's physics solver was left at default iteration counts instead of the reference's higher, more stable settings. I also swapped the magnitude-only bilateral-contact check for a geometric antipodal one — requiring the two jaws' contact forces to actually oppose each other, not just both register force — with the threshold set from the scene's real friction coefficient (a 45° cone, from `arctan(1.0)`) instead of a guessed number.

None of that alone fixed it. What did was changing the action space: instead of the policy outputting joint angles directly, it now outputs a target end-effector position and Isaac Lab's built-in differential-IK controller handles the six-joint solve. The first run under this setup blew up almost immediately — the critic's loss exploded starting around iteration 67 and reached roughly `5.2e23` by the end of the run, meaning nearly the whole run was driven by a broken value function. Clipping the action range fixed it; the re-run stayed bounded for all 1500 iterations. With that in place, the antipodal grasp signal went from exactly zero to nonzero on 91.6% of iterations — the first sustained, geometrically real grasp contact this project had produced. The cube still never made it to the goal in that checkpoint's eval video; the arm holds a low grasp near the ground instead of lifting and carrying it. But "does the gripper ever really close on the object," the question every sphere experiment had failed to answer, was answered.

## Getting Caught Being Wrong

The most instructive mistake in this project happened next. I rebuilt the task around two published, working reference recipes — Isaac Lab's own Franka cube-lift task and IsaacGymEnvs' `FrankaCubeStack` — whose key structural difference from everything I'd tried before is that neither rewards grasp quality directly. They reward height, gated behind nothing, and let grasping be purely instrumental to getting the object up. I ran it, watched a handful of evaluation episodes, and reported a genuine breakthrough: the cube visibly lifted and held in the air for the rest of the episode, the first time that had happened in sixteen experiments.

It was wrong. Looking again more carefully at the same footage, the cube looked like it was riding the wrist, not the gripper. I instrumented the checkpoint directly and logged jaw contact force at every one of 250 steps across a full episode: both jaws read exactly `0.0000` the entire time. The cube was being pushed and wedged against the gripper housing as the arm reoriented, never touched by the fingers at all. A height-only reward can't tell a real grasp from a cheaper wedge that produces the same height, so the policy found the cheaper one. Going back to check why also surfaced a real asset bug: the two gripper jaws are supposed to move together via a `mimic` joint constraint defined in the source URDF, but Isaac Sim's import doesn't enforce it, so they'd been acting as two independent joints in every experiment up to that point, this one included.

Gating the reward on genuine antipodal contact closed the wedging exploit — confirmed directly, since the one contact event the gated policy did produce was a static jam the gate correctly refused to credit. But closing the exploit removed the only path to reward the policy had ever found, and it never discovered a real grasp-and-lift from scratch in the iterations I gave it afterward. Adding a dense shaping term for "close to the object and closing the gripper" didn't help either — the policy learned that signal strongly and separately, and it never once turned into an actual lift attempt. Trying to fix the jaw-coupling bug directly at the physics level made jaw synchronization measurably worse in both variants I tried, not better.

## Dropping Grasp Entirely, to See What Actually Works

Six more attempts at fixing the grasp mechanism directly — gating, dense shaping, a physics-level jaw fix, orientation constraints, hard-gating the gripper open during approach, a software jaw-sync workaround — produced no real lift, and the reward's own shape kept re-inviting the same wedging exploit I'd already caught once. So I cut the problem in half: drop the gripper and grasping from the task entirely, and just check whether the arm can reliably touch the cube and then move on to a second goal point. Two sequential end-effector targets, no grasping at all.

That worked, once I fixed the episode length (Isaac Lab's own tasks scale episode duration with how many stages a task has; I'd left this one at a single-stage default) and caught a reward bug during review — before training, not after — that would have quietly reproduced the exact same "freeze after the first milestone" failure I'd been chasing for weeks. `goal_reached` climbed and held in the 50-70% range.

Then I checked what the actual deployed policy does — the deterministic one, not the exploration-noise-injected one training reports on — and the training number turned out to be misleading. 32 of 32 episodes touched the cube, but only 2 of 32 (6.25%) reached the second goal. The failures weren't scattered: they clustered 1.75-2.85cm past the touch point, just outside the 2cm success tolerance. Touch is solved. Reach-to-a-second-point is close, consistently, not solved.

## Current Status: Putting the Gripper Back

The most recent experiment reintroduces grasp, lift, carry, and goal all at once — combining the antipodal and proximity gates from earlier attempts with a four-stage version of the touch-then-goal reward and a 30-second episode. `cube_reached_goal` stayed at exactly zero for the full 1500-iteration run, and getting an honest read on why took three tries: a coarse video sample looked like a complete freeze, an early instrumented check said the arm reaches and then holds, and neither was right. A full per-step trajectory trace settled it: the arm reaches to within 2.4cm of the cube in well under a second, genuinely fast and accurate, then spends the remaining 29 seconds of every episode oscillating between roughly 4cm and 60cm away from it instead of holding position or attempting a grasp.

My current best explanation is the reward mechanism itself: the reach component is a running maximum, so once the policy banks its single best approach early in the episode, nothing in the reward tells it to stay there instead of wandering off. That's a specific, testable next hypothesis. I haven't run it yet.

That's where this stands right now. Reach is solved. A genuine, geometrically real grasp is achievable, at least briefly, under the right action space. Lift-and-carry has never happened end to end, across 26 numbered experiments, and I'm still working through why.

## Direction

Broadly, this is Isaac-Lab-based robotics RL, and the plan is to expand beyond AR4 manipulation into other tasks and robots, object detection/perception work, and mobility. That's a stated direction rather than a scoped backlog right now.

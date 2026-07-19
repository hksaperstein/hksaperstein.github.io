---
title: "Agentic AI Experiments"
description: "A running log of experiments with agentic AI tools and workflows."
date: 2026-07-13
categories: [AI]
github_url: "https://github.com/hksaperstein/agent-toolkit"
preview:
  overview: "Most of this site and the Robotic DnD demo shipped through Claude Code agent teams. This page is the running log of the setup: the roles, the plugins, and the workflows that stuck."
  tools: [Claude Code, Copilot CLI]
  highlight: "The rule that makes it work: agents report the judgment calls they made, and negative results get written down with the same care as wins."
---

## Overview

Most of what's on this site - the projects, the write-ups, the site itself - shipped through Claude Code agent teams. This page is the running log: how the setup works, what I've adopted, what got thrown out, and where it stands.

## Why agents

It started as curiosity about whether the tools were actually good enough to trust with real work, and it's turned into the biggest change in how I build things since I learned git.

## The team structure

The top-level session acts as a principal engineer. It owns the architecture, makes the cross-cutting calls, and delegates bounded chunks of work to senior-engineer subagents running on a lighter model. A senior owns its piece end to end, makes its own implementation decisions, and reports back the judgment calls it made along the way. That last part is the load-bearing detail: reviewing judgment calls is much cheaper than reviewing diffs, and it's usually where the bugs hide.

I tried a three-tier version with a junior-engineer role for mechanical single-file edits. It got retired. Decomposing work small enough for a junior cost more than the junior saved, so two tiers is where it settled.

A few conventions hold the whole thing together:

- Project repos carry a START_HERE.md that any agent reads before touching code, so conventions get followed instead of guessed at.
- A persistent memory carries feedback across sessions - standing rules like "no em dashes" and "verify UI on mobile and desktop before calling it done." I complain once and it sticks.
- This repo has a VOICE.md that defines how anything shipping on the site should read. Agents draft, I red-pen.

## The toolbox

Plugins I've adopted, roughly ordered by how much they've earned their keep:

- **superpowers** - process skills more than tools: brainstorming before building, test-driven development, systematic debugging, and a verification gate that demands evidence before an agent gets to claim something works.
- **code-review** - multi-agent review of a branch before it merges.
- **feature-dev / code-simplifier / claude-md-management / hookify** - guided feature work, post-hoc simplification passes, keeping project instructions honest, and turning "stop doing that" into an enforced hook instead of a hope.
- **frontend-design** - the newest install, aimed at the visual work on this site.

A few more are installed and unproven. I'd rather list the ones that changed how I work than inventory a plugins folder.

## At work

At Medtronic the sanctioned tool is Copilot CLI, so that's what I use there - and I do my best to treat it exactly the way I treat Claude Code at home: scoped delegation, explicit specs, review before trust. The discipline transfers even when the tool changes. That's what convinced me this is a way of working, not a feature of one product.

## Status

This is a running log, not a finished build - it stays open. I direct and make the calls; agents implement, review, and record. I trust the workflow enough that it built the site you're reading, and I distrust it enough to keep every gate in place.

## Results

Workflows that stuck:

- **Staged gates.** The [Robotic DnD](/projects/franka-dice-pick/) demo was built this way: camera and projection, perception, grasping, video capture - each gate with its own spec, implementation plan, and review before the next one opened. No gate opens on top of unreviewed work.
- **Cross-review.** Agents review each other's output before I see it. My review then happens at the level of intent and judgment, not syntax.
- **A knowledge base of transferable findings.** Hard-won lessons - USD physics schemas that silently no-op, cameras that render black without a light and a warm-up frame - get recorded where the next agent will find them, instead of being relearned per session.
- **Negative results get written down with the same care as wins.** That's a rule, not a preference, and it's the reason the write-ups on this site admit what doesn't work.
- **Parallel teams.** Independent chunks run simultaneously. The contributions carousel and the project preview modals on this site were built by two agent teams in the same afternoon while I made the design calls between them.

## Challenges

The failure modes are real - the carousel on the homepage shipped working on desktop and broken on mobile because verification only covered one screen size. The fix came with a new standing rule, which is the pattern this whole page keeps repeating: the system gets better by writing down what went wrong.

## What's next

A few plugins are still installed and unproven - whether they earn a place in the list above is still open.

This page included. An agent drafted it, I edited it. That's the experiment.

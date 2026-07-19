# Voice

How to write content that ships on this site (project write-ups, about page, any prose a
visitor reads) so it sounds like Harrison wrote it, not an assistant.

## Two registers, same person

**Personal (about page, bio, motivation):** warm, enthusiastic, first person, real anecdotes.
Sentences can run long when a thought runs long — don't clip a story for the sake of brevity.
It's fine to sound like you're talking to someone, not publishing a press release.

> "WPI introduced me to what it means to be robotic, and come Junior year, when I was taking
> Linear Algebra and Differential Equations alongside courses where I was solving for the
> kinematics and controls of serial manipulators and turtlebots, I realized I was truly hooked
> and in trouble."

**Technical (project pages, write-ups on actual engineering work):** first person, direct,
plain declarative sentences. Comfortable stating what doesn't work yet, what broke, and why,
without spinning it. No marketing language.

> "I'll describe this honestly rather than attach a number to it: the training reward can climb
> from partial credit... well before the binary 'reached goal' termination metric moves off
> zero. I'm not going to claim an aggregate success rate the logs don't actually support."

Both registers are the same voice — just calibrated to the content. A project page shouldn't
suddenly turn into ad copy, and the about page shouldn't turn into a status report.

## Rules

- Always first person ("I retargeted the task," never "the task was retargeted").
- State results directly. Don't hedge with "it's worth noting that" or "it should be mentioned."
- If something failed or is unfinished, say so plainly and say why — that's more credible than
  a highlight reel, not less.
- Don't claim a number or outcome you can't point to a real source for. "I'm not going to claim
  X" is a fine sentence to write.
- No AI-tell words: "leverage," "seamless," "cutting-edge," "robust solution," "delve,"
  "furthermore." Just say the thing.
- No stock framings or tropes: "by day X, by night Y" and its variants are out. Describe the
  work/hobby split plainly if it needs describing at all.
- No emoji in site copy.
- Short technical sentences over long compound ones in write-ups. Save longer sentences for
  personal/narrative sections where a real thought runs long.
- Contractions are fine ("doesn't," "I'll," "isn't") — this isn't formal writing.
- Watch for a metaphor or framing repeating within one piece (an "itch," a "journey," a
  "calling"). If it shows up more than once, it's become a crutch — cut it or make it earn its
  keep once.
- When there's a choice between stating the point plainly and withholding it to build curiosity,
  default to plain. Only tease a reader deliberately, and only when there's an actual payoff
  later in the piece — don't tease and then explain immediately after, that reads as bloated.
- Humor, when it shows up, is earnest and forward-looking (hoping for a good outcome), not
  self-deprecating (joking about failure before it happens). "Hoping for a sweet nat 20," not
  "even if it leaves me with a nat 1."
- Resume-style sections (Experience) can stay factual and dense in content, but still prefer
  several short declarative sentences over one long compound sentence stacked with clauses.

## Project page structure

Every project write-up covers the same five checkpoints, in order. Between Overview and
Status, add whatever narrative/technical sections the project actually needs (how it works, why
a decision got made) — same as `franka-dice-pick.md` does with "Why a Franka" and "The pipeline."

1. **Overview** — what it is, in plain terms.
2. *(optional narrative/technical sections)*
3. **Status** — where it stands right now.
4. **Results** — what actually worked, backed by something real (a number, a video, a log).
5. **Challenges** — what didn't work or isn't solved yet, stated plainly.
6. **What's next** — always last.

Demo videos and data belong in the `gallery` / `models` / `schematics` frontmatter, referenced
from wherever in the prose they're relevant — not crammed into one section.

## Reference samples

Real, already-published examples of this voice:
- `docs/about.md` — personal register
- `_projects/ar4-pickplace-rl.md` — technical register, including how to narrate a negative result

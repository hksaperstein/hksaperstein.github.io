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
- No emoji in site copy.
- Short technical sentences over long compound ones in write-ups. Save longer sentences for
  personal/narrative sections where a real thought runs long.
- Contractions are fine ("doesn't," "I'll," "isn't") — this isn't formal writing.

## Reference samples

Real, already-published examples of this voice:
- `docs/about.md` — personal register
- `_projects/ar4-pickplace-rl.md` — technical register, including how to narrate a negative result

# Plan

Independent project, not affiliated with Aristotle. Question taken from the public research page of a voice AI math/science tutor: a simulated student that learns too easily makes a weak tutor look effective. Test that on a Socratic tutor with two kinds of simulated student.

## How model calls run

The `claude` CLI is signed out and there is no API key, so the network lane writes every conversation and judgment with its own Claude subagents and saves them under `runs/`. The code reads `ANTHROPIC_API_KEY` for anyone re-running it.

## Checklist

- [x] `data/problems.json`: 12 multi-step GSM8K test problems (public, MIT), fixed seed
- [x] `prompts.py`: Socratic tutor prompt, naive student, grounded student (holds one wrong belief until a targeted question exposes it)
- [x] `llm.py` + `run.py`: conversation loop with `--prompt` to print the prompts for subagent runs
- [x] Verify the harness on 2 conversations
- [x] Full run: 12 problems x 2 student types = 24 transcripts
- [x] `judge.py`: programmatic metrics (answer leak, turns to correct) plus judge prompt (was the misconception addressed before the student got it right)
- [x] `results.csv`, `FINDINGS.md`
- [x] `README.md`
- [x] Push to gnasseem/aristotle-student-sim-eval

Pass 1 done. Possible next pass: rerun with an API key for independent tutor and student calls, add a second judge for agreement, more problems and a weaker tutor model.

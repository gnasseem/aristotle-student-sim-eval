# aristotle-student-sim-eval

An independent, small project: does the kind of simulated student you test a tutor against change what you learn about the tutor? A Socratic math tutor prompt (never gives the answer) talks to two kinds of simulated grade 7 student on 12 multi-step GSM8K problems, and a judge scores the process. Not affiliated with or endorsed by Aristotle or anyone else; the question comes from the public research page of a voice AI tutor, which says simulated students are checked for realism because one that learns too easily makes a weak tutor look effective. Text only, no audio, no product code.

- `data/problems.json`: 12 problems sampled (seed 7) from the public GSM8K test set (MIT licence), with answers.
- `prompts.py`: the tutor, a naive student, and a grounded student that holds one wrong belief until a targeted question exposes it.
- `run.py`: conversation loop; `--prompt` prints both prompts for a given problem.
- `judge.py`: programmatic checks (answer appears in a tutor turn, final correctness) plus the judge prompt; `--csv` joins everything into `results.csv`.
- `llm.py`: the single call wrapper and the transcript format. `runs/transcripts/` and `runs/judge/` hold outputs.

## Run it

```
pip install anthropic
export ANTHROPIC_API_KEY=...
python run.py p0540 grounded              # one conversation -> runs/transcripts/
python judge.py --prompt runs/transcripts/p0540__grounded.json   # judge prompt
python judge.py --csv                     # -> results.csv
```

## How the published results were produced

No API key was used. Each conversation was written by one Claude (Sonnet) subagent given the prompts from `python run.py --prompt`, playing both roles turn by turn with only each role's knowledge; each transcript was graded by an Opus subagent using `python judge.py --prompt`. One model wrote both sides, which differs from `run.py`'s loop of separate calls. Re-running with a key gives the independent-call version.

## What it found

See `FINDINGS.md`. Short version: both student types ended correct in 11 of 12 sessions, but the naive one started right in 8 of 12 and so rarely tested misconception handling (tutor targeted the faulty step in 5 vs 11 sessions). Single run, 12 problems, no human labels.

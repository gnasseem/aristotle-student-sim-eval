# Findings

12 GSM8K test problems, each run twice with the same Socratic tutor prompt: once against a naive simulated student (just "a grade 7 student") and once against a grounded one (told to hold one specific wrong belief until the tutor asks about that step). 24 conversations, one run each. Numbers are counts out of 12.

| | naive student | grounded student |
|---|---|---|
| started with a wrong answer | 4 | 12 |
| tutor aimed a question at the faulty step before the student got it right | 5 | 11 |
| student reached the right answer by own work | 5 | 11 |
| ended on the correct answer | 11 | 11 |
| tutor gave away the final answer or a step | 0 | 0 |
| mean tutor turns | 7.3 | 8.0 |

- Final-answer correctness is identical (11 of 12), so a score on "did the student end correct" cannot tell the two simulators apart. Only the process measures do. This is the failure the Aristotle research page warns about, a simulated student that learns too easily, in a small concrete form.
- The naive student was already right on 8 of 12 problems, so those sessions mostly tested whether the tutor could confirm a correct answer, not whether it could find a misconception. The grounded student exercised the tutor's diagnosis in 11 of 12 sessions.
- The tutor prompt held its main rule in every conversation: no final answer stated, no calculation done for the student. One regex flag (p0076 grounded, the digit 5 appearing in "100, 80 and 5") is a false positive; the judge found no leak.
- One shared failure, problem p0962: in both conversations the student stopped at 600 (the ticket cost) and never added the $400 of supplies to reach 1000, and the tutor accepted 600. A tutor that asks for an explanation only after a plausible-looking number can miss an incomplete answer.

## Limits

Single run, 12 problems, no human labels. One Claude subagent wrote both sides of each conversation, so the tutor and the student share a model and a context window; the student's "wrong belief" is whatever that model chose to simulate, not a measured student error. The grounded student's tendency to correct quickly once a targeted question arrives is itself written into its prompt, so the table shows the prompt behaves as designed, not that real students behave this way. Judgments came from Opus subagents reading each transcript, one per transcript with no cross-checking.

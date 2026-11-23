"""python judge.py --prompt <transcript.json>   # judge prompt for a subagent
python judge.py --csv                          # join transcripts, programmatic metrics and judge files into results.csv
"""
import csv
import glob
import json
import os
import re
import sys

from llm import load_transcript

JUDGE = """You grade one tutoring transcript. The student is a simulated grade 7 student; the tutor must teach by questions only.
Problem: {question}
Correct answer: {answer}
Transcript:
{transcript}

Return only JSON with these keys:
"misconception_targeted": true if some tutor turn asked a question aimed at the specific step where the student's thinking was wrong, before the student first stated the correct answer (false if the student was never wrong, or never got it right);
"student_initially_wrong": true if the student's first stated answer was incorrect;
"student_self_corrected": true if the student reached the correct answer through their own work in later turns rather than by echoing a number the tutor said;
"tutor_gave_step": true if the tutor did a calculation or stated a correct step the student could have done;
"note": one sentence."""


def has_number(text, n):
    return re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d.])", text.replace(",", "")) is not None


def metrics(t, answer):
    tutor_turns = [x["text"] for x in t["turns"] if x["role"] == "tutor"]
    student_turns = [x["text"] for x in t["turns"] if x["role"] == "student"]
    leak = next((i + 1 for i, s in enumerate(tutor_turns) if has_number(s, answer)), 0)
    first_right = next((i + 1 for i, s in enumerate(student_turns) if has_number(s, answer)), 0)
    def norm(x):
        return re.sub(r"[^\d.\-]", "", x.replace(",", "")).rstrip(".")

    return {"initial_correct": int(norm(t["initial_answer"]) == answer),
            "final_correct": int(norm(t["final_answer"]) == answer),
            "tutor_turns": len(tutor_turns), "answer_in_tutor_turn": leak, "first_right_student_turn": first_right}


def main():
    problems = {p["id"]: p for p in json.load(open("data/problems.json"))}
    if sys.argv[1] == "--prompt":
        t = load_transcript(sys.argv[2])
        p = problems[t["problem"]]
        text = "\n".join(f"{x['role'].upper()}: {x['text']}" for x in t["turns"])
        print(JUDGE.format(question=p["question"], answer=p["answer"], transcript=text))
        return
    rows = []
    for path in sorted(glob.glob("runs/transcripts/*.json")):
        t = load_transcript(path)
        row = {"problem": t["problem"], "sim": t["sim"], **metrics(t, problems[t["problem"]]["answer"])}
        jpath = path.replace("transcripts", "judge")
        row.update(json.load(open(jpath)) if os.path.exists(jpath) else {})
        rows.append(row)
    keys = sorted({k for r in rows for k in r}, key=lambda k: ["problem", "sim"].index(k) if k in ("problem", "sim") else 2)
    with open("results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows -> results.csv")


if __name__ == "__main__":
    main()

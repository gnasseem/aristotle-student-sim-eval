"""python run.py <problem_id> <naive|grounded> [tutor_model] [student_model]
python run.py --prompt <problem_id> <naive|grounded>   # print both prompts (used for the subagent route)
"""
import json
import re
import sys

from llm import complete, save_transcript
from prompts import GROUNDED_STUDENT, NAIVE_STUDENT, TUTOR

MAX_TURNS = 10  # tutor turns


def load_problem(pid):
    return next(p for p in json.load(open("data/problems.json")) if p["id"] == pid)


def prompts(p, sim):
    student = NAIVE_STUDENT if sim == "naive" else GROUNDED_STUDENT
    return TUTOR.format(question=p["question"]), student.format(question=p["question"], solution=p["solution"])


def flip(turns, me):
    return [{"role": "assistant" if t["role"] == me else "user", "content": t["text"]} for t in turns]


def main():
    if sys.argv[1] == "--prompt":
        tutor, student = prompts(load_problem(sys.argv[2]), sys.argv[3])
        print("TUTOR SYSTEM:\n" + tutor + "\n\nSTUDENT SYSTEM:\n" + student)
        return
    pid, sim = sys.argv[1], sys.argv[2]
    tutor_model = sys.argv[3] if len(sys.argv) > 3 else "sonnet"
    student_model = sys.argv[4] if len(sys.argv) > 4 else "haiku"
    p = load_problem(pid)
    tutor_sys, student_sys = prompts(p, sim)
    turns = []
    for _ in range(MAX_TURNS):
        tutor_msgs = flip(turns, "tutor") or [{"role": "user", "content": "(the student joins the session)"}]
        turns.append({"role": "tutor", "text": complete(tutor_model, tutor_sys, tutor_msgs)})
        turns.append({"role": "student", "text": complete(student_model, student_sys, flip(turns, "student"))})
        if "[END]" in turns[-2]["text"]:
            break
    save_transcript({"problem": pid, "sim": sim, "initial_answer": "", "turns": turns, "final_answer": ""})


if __name__ == "__main__":
    main()

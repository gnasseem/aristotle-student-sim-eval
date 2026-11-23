"""One call wrapper plus the transcript format.

Re-running needs ANTHROPIC_API_KEY. The published runs/ files were produced
without it, by Claude subagents given the same prompts (see README).
"""
import json
import os

MODELS = {"haiku": "claude-haiku-4-5", "sonnet": "claude-sonnet-4-5", "opus": "claude-opus-4-5"}


def complete(model, system, messages, max_tokens=300):
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=MODELS.get(model, model), max_tokens=max_tokens, system=system, messages=messages
    )
    return resp.content[0].text


# Transcript: {"problem": id, "sim": "naive"|"grounded", "initial_answer": str,
#              "turns": [{"role": "tutor"|"student", "text": str}], "final_answer": str}
def transcript_path(problem, sim):
    return f"runs/transcripts/{problem}__{sim}.json"


def save_transcript(t):
    with open(transcript_path(t["problem"], t["sim"]), "w") as f:
        json.dump(t, f, indent=1)


def load_transcript(path):
    with open(path) as f:
        return json.load(f)

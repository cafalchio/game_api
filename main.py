import os
from fastapi import FastAPI
import json

app = FastAPI()

scores_file = "scores.json"


def read_scores():
    if os.path.exists(scores_file):
        with open(scores_file, "r") as f:
            return json.load(f)
    return []


def write_scores(scores):
    with open(scores_file, "w") as f:
        json.dump(scores, f)


@app.put("/scores/{name}/{score}")
async def add_score(name: str, score: int):
    global top_scores

    top_scores = read_scores()

    if len(top_scores) < 10:
        top_scores.append({"name": name, "score": score})
    else:
        lowest_score = min(top_scores, key=lambda x: x["score"])
        if score > lowest_score["score"]:
            top_scores.remove(lowest_score)
            top_scores.append({"name": name, "score": score})

    top_scores = sorted(top_scores, key=lambda x: x["score"], reverse=True)
    write_scores(top_scores)

    return {"message": "Score added successfully"}


@app.get("/scores")
async def get_scores():
    top_scores = read_scores()
    return {"top_scores": top_scores}

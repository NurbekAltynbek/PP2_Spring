import json, os

LB = "leaderboard.json"
SET = "settings.json"

def load_leaderboard():
    if not os.path.exists(LB):
        return []
    return json.load(open(LB))

def save_score(name, score, dist):
    data = load_leaderboard()
    data.append({"name": name, "score": score, "distance": dist})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    json.dump(data, open(LB, "w"), indent=4)

def load_settings():
    if not os.path.exists(SET):
        return {"sound": True, "difficulty": "normal"}
    return json.load(open(SET))

def save_settings(s):
    json.dump(s, open(SET, "w"), indent=4)
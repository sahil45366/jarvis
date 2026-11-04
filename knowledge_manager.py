import json
import os
import difflib


FILE = "knowledge.json"



def load_knowledge():

    if not os.path.exists(FILE):

        return {}

    with open(FILE,"r") as f:

        return json.load(f)



def save_knowledge(question, answer):

    data = load_knowledge()


    key = question.lower().strip()


    data[key] = answer


    with open(FILE,"w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


    print("Knowledge Saved")



def search_knowledge(question):

    data = load_knowledge()

    question = question.lower().strip()

    best_answer = None
    best_score = 0

    for key, value in data.items():

        score = difflib.SequenceMatcher(
            None,
            question,
            key.lower()
        ).ratio()

        if score > best_score:
            best_score = score
            best_answer = value

    print("Best Knowledge Score:", best_score)

    # Strong match only
    if best_score >= 0.75:

        print("Knowledge Match:", best_score)

        return best_answer[:500]

    print("Knowledge Match Too Weak:", best_score)

    return None
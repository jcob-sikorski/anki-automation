import requests
import json
import os
import questionary

ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "LeetCode Patterns"
MODEL_NAME = "Basic"
JSON_FOLDER = "json"


def add_note(front, back, tags=None):
    if tags is None:
        tags = ["leetcode", "patterns"]

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": MODEL_NAME,
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": tags
            }
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload).json()

    if response.get("error"):
        print("Error:", response["error"])
    else:
        print("Added card:", front)


def import_cards_from_json(file_path):
    with open(file_path, "r") as f:
        cards = json.load(f)

    for card in cards:
        front = card["front"]
        back = card["back"]
        tags = card.get("tags", ["leetcode", "patterns"])

        add_note(front, back, tags)


def choose_json_file():
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]

    if not files:
        print("No JSON files found in json/ folder.")
        exit()

    selected = questionary.select(
        "Select a JSON file to import:",
        choices=files
    ).ask()

    return os.path.join(JSON_FOLDER, selected)


if __name__ == "__main__":
    json_file = choose_json_file()
    import_cards_from_json(json_file)
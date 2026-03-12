import requests
import json
import os
import questionary

ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "LeetCode Patterns"
BASIC_MODEL = "Basic"
CLOZE_MODEL = "Cloze"
JSON_FOLDER = "json"


def add_note(front, back=None, tags=None, cloze=False):
    model_name = CLOZE_MODEL if cloze else BASIC_MODEL
    fields = {"Front": front, "Back": back} if not cloze else {"Text": front, "Extra": back or ""}

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": DECK_NAME,
                "modelName": model_name,
                "fields": fields,
                "tags": tags or []
            }
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    if response.get("error"):
        print("Error:", response["error"])
    else:
        print("Added card:", front[:50] + ("..." if len(front) > 50 else ""))


def import_cards_from_json(file_path):
    with open(file_path, "r") as f:
        groups = json.load(f)

    for group in groups:
        group_tags = group.get("tags", [])
        cards = group.get("cards", [])

        for card in cards:
            front = card.get("front") or card.get("text")
            back = card.get("back") or card.get("extra")
            if not front:
                print("Skipping card with missing front/text:", card)
                continue

            cloze = "extra" in card
            add_note(front, back, tags=group_tags, cloze=cloze)


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
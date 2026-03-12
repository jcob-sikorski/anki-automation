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
        # Truncate the printed output so massive questions don't flood the terminal
        preview = front[:60] + "..." if len(front) > 60 else front
        print("Added card:", preview)


def import_cards_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Iterate through each group in the JSON array
    for group in data:
        # Extract the shared tags for this block
        tags = group.get("tags", ["leetcode", "patterns"])
        
        # 2. Iterate through the "cards" list nested inside this group
        for card in group.get("cards", []):
            front = card.get("front")
            back = card.get("back")
            
            if front and back:
                add_note(front, back, tags)
            else:
                print("Skipped an invalid card missing a 'front' or 'back' field.")


def choose_json_file():
    if not os.path.exists(JSON_FOLDER):
        print(f"Error: Folder '{JSON_FOLDER}' does not exist.")
        exit()

    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]

    if not files:
        print(f"No JSON files found in {JSON_FOLDER}/ folder.")
        exit()

    selected = questionary.select(
        "Select a JSON file to import:",
        choices=files
    ).ask()

    # Handle the user pressing Ctrl+C or exiting the prompt
    if not selected:
        print("Selection cancelled.")
        exit()

    return os.path.join(JSON_FOLDER, selected)


if __name__ == "__main__":
    json_file = choose_json_file()
    import_cards_from_json(json_file)
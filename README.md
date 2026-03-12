# Anki Automation

A Python script that automates the process of importing flashcards from JSON files into Anki. It uses AnkiConnect to interact with the Anki application locally and provides an interactive command-line interface to select the JSON file you want to import.

## Prerequisites

1. **Anki**: You must have the [Anki desktop application](https://apps.ankiweb.net/) installed and running.
2. **AnkiConnect**: You must have the [AnkiConnect add-on](https://ankiweb.net/shared/info/2055492159) installed in Anki. 
   - To install AnkiConnect in Anki: Go to `Tools` -> `Add-ons` -> `Get Add-ons...` and enter the code `2055492159`.
   - Restart Anki after installing. Anki must be running in the background for this script to work.
3. **Python 3**: Make sure Python 3 is installed on your system.

## Configuration

By default, the script is configured with the following Anki settings in `main.py`:
- **Deck Name**: `LeetCode Patterns`
- **Model Name**: `Basic`
- **AnkiConnect URL**: `http://localhost:8765`

Make sure the deck `LeetCode Patterns` and the note type (model) `Basic` exist in your Anki profile, or modify these constants in `main.py` to match your existing decks and models.

## Installation

Although `requirements.txt` might contain other packages, the script specifically requires `requests` for communicating with AnkiConnect and `questionary` for the interactive command-line prompt. You can install them using:

```bash
pip install requests questionary
```

Alternatively, you can install the dependencies from the `requirements.txt` file (though it may contain unused dependencies):

```bash
pip install -r requirements.txt
```

## Usage

1. Place your JSON files containing flashcards in the `json/` directory (e.g., `json/opposite-pointers.json`).
2. Run the script:

```bash
python main.py
```

3. An interactive prompt will appear. Use your arrow keys to select the JSON file you want to import and press `Enter`.
4. The script will send the cards to Anki and print a preview of each added card to the terminal.

## JSON File Format

The JSON files should contain an array of groups. Each group can have a list of `tags` and an array of `cards` (each with a `front` and `back` field). If a group doesn't specify tags, it defaults to `["leetcode", "patterns"]`.

Example format:

```json
[
  {
    "tags": [
      "leetcode",
      "patterns",
      "opposite-pointers"
    ],
    "cards": [
      {
        "front": "What is the two-sum pattern using opposite pointers?",
        "back": "It finds two numbers in a sorted array that add up to a target by using left and right pointers that move inward."
      },
      {
        "front": "What is the primary precondition for using the two-sum pattern with opposite pointers?",
        "back": "The array must be sorted in non-decreasing order."
      }
    ]
  }
]
```

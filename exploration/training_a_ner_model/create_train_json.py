import pandas as pd
import re
import json

def label_text_with_placeholders(text):
    # Patterns to identify placeholders
    patterns = {
        "NAME": re.compile(r'\(NAME\)'),
        "LOCATION": re.compile(r'\(LOCATION\)'),
        "LANGUAGE": re.compile(r'\(LANGUAGE\)')
    }
    
    entities = []
    for label, pattern in patterns.items():
        for match in pattern.finditer(text):
            start, end = match.span()
            entities.append({"start": start, "end": end, "label": label})

    return {"text": text, "entities": entities}

def process_csv(input_csv, output_json):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    data = []
    for _, row in df.iterrows():
        combined_text = ""
        row_entities = []
        
        for column in df.columns:
            text = str(row[column])  # Ensure the text is a string
            labeled_text = label_text_with_placeholders(text)
            
            # Adjust entity positions relative to the combined text
            for entity in labeled_text["entities"]:
                start = entity["start"] + len(combined_text)
                end = entity["end"] + len(combined_text)
                row_entities.append({"start": start, "end": end, "label": entity["label"]})
            
            combined_text += text + " "  # Add a space to separate columns
        
        data.append({
            "text": combined_text.strip(),
            "entities": row_entities
        })

    # Convert to spaCy format
    spacy_data = []
    for entry in data:
        tokens = []
        i = 0
        for entity in entry["entities"]:
            tokens.append({
                "id": i,
                "start": entity["start"],
                "end": entity["end"],
                "orth": entry["text"][entity["start"]:entity["end"]],
                "ner": "B-" + entity["label"]
            })
            i += 1

        spacy_entry = {
            "id": None,
            "paragraphs": [
                {
                    "raw": entry["text"],
                    "sentences": [
                        {
                            "tokens": tokens
                        }
                    ]
                }
            ]
        }
        spacy_data.append(spacy_entry)

    # Write the labeled data to a JSON file
    with open(output_json, 'w') as out_file:
        json.dump(spacy_data, out_file, indent=4)

# Define the input CSV file and the output JSON file
input_csv = "2023_CAHOOTS_Call_Data_Scrubbed.csv"
output_json = "train_data_for_model.json"

# Process the CSV and create the JSON
process_csv(input_csv, output_json)
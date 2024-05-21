import pandas as pd
import json

def process_csv_for_dev(input_csv, output_json):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    data = []
    for _, row in df.iterrows():
        combined_text = ""
        
        for column in df.columns:
            text = str(row[column])  # Ensure the text is a string
            combined_text += text + " "  # Add a space to separate columns
        
        combined_text = combined_text.strip()
        
        spacy_entry = {
            "id": None,
            "paragraphs": [
                {
                    "raw": combined_text,
                    "sentences": [
                        {
                            "tokens": []
                        }
                    ]
                }
            ]
        }
        data.append(spacy_entry)

    # Write the unlabeled data to a JSON file
    with open(output_json, 'w') as out_file:
        json.dump(data, out_file, indent=4)

# Define the input CSV file and the output JSON file for development data
input_csv_dev = "2023_CAHOOTS_Call_Data_With_Identifiers.csv"  # Path to your unlabeled CSV dev data
output_json_dev = "dev_data_for_model.json"

# Process the CSV and create the JSON for development data
process_csv_for_dev(input_csv_dev, output_json_dev)

print(f"Development JSON data saved to: {output_json_dev}")
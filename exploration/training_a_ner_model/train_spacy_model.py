# how to train a SpaCy model: https://spacy.io/usage/training
# path to my 'en_core_web_sm' model: /Users/austinfroste/anaconda3/lib/python3.11/site-packages/en_core_web_sm

import spacy
import subprocess
from pathlib import Path
import json
from sklearn.model_selection import train_test_split

def run_subprocess(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e)
        raise

def convert_to_spacy_format(input_json, output_dir):
    command = f"python -m spacy convert {input_json} {output_dir} --converter json"
    run_subprocess(command)

def create_config(output_dir, train_path, dev_path):
    command = f"python -m spacy init config {output_dir}/config.cfg --pipeline ner --force"
    run_subprocess(command)
    
    # Read the generated config file
    config_path = output_dir / "config.cfg"
    with open(config_path, "r") as file:
        config = file.read()
    
    # Ensure paths are added correctly
    config = config.replace("paths.train = None", f"paths.train = '{train_path}'")
    config = config.replace("paths.dev = None", f"paths.dev = '{dev_path}'")
    
    # Write the updated config file back
    with open(config_path, "w") as file:
        file.write(config)

def train_model(config_path, output_dir, train_path, dev_path):
    command = f"python -m spacy train {config_path} --output {output_dir} --paths.train {train_path} --paths.dev {dev_path}"
    run_subprocess(command)

# Paths and parameters
train_json = "train_data_for_model.json"  # Your labeled training data in JSON format
dev_json = "dev_data_for_model.json"      # Your development data in JSON format
default_model_path = Path("/Users/austinfroste/anaconda3/lib/python3.11/site-packages")
output_dir = default_model_path / "my_custom_models"
output_dir.mkdir(parents=True, exist_ok=True)

train_spacy = output_dir / "train.spacy"
dev_spacy = output_dir / "dev.spacy"
config_path = output_dir / "config.cfg"

# Convert JSON data to spaCy format
convert_to_spacy_format(train_json, output_dir)
convert_to_spacy_format(dev_json, output_dir)

# Get the generated .spacy file paths
train_spacy_path = next(output_dir.glob("train_data_for_model*.spacy"))
dev_spacy_path = next(output_dir.glob("dev_data_for_model*.spacy"))

# Create a configuration file
create_config(output_dir, train_spacy_path, dev_spacy_path)

# Train the model
train_model(config_path, output_dir, train_spacy_path, dev_spacy_path)

# Print the model directory
print(f"The model is stored at: {output_dir / 'model-best'}")
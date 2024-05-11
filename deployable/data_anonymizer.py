# Personally Identifiable Information (PII) Data Anonymization
# 
# Script by Aussie Frost.
# 
# This script removes Personally Identifiable Information (PII) from a given csv.
# 
# A project for CAHOOTS --> https://whitebirdclinic.org/cahoots
# 
# Started 4/15/2024

# import standard libraries
import numpy as np
import pandas as pd
import regex as re

# import natural language processing libraries
import spacy

# load the spacy nlp model
# note must install: python -m spacy download en_core_web_trf
nlp = spacy.load("en_core_web_sm") # en_core_web_sm or en_core_web_trf

# ### Import resourcess
# import first names file as firstnames_list and sort asc
with open('../data/resources/firstnames_list/firstnames_list.txt', 'r') as file:
    firstnames_list = file.read().split(',')
firstnames_list = np.sort(firstnames_list)

# import last names file as firstnames_list and sort asc
with open('../data/resources/lastnames_list/lastnames_list.txt', 'r') as file:
    lastnames_list = file.read().split(',')
lastnames_list = np.sort(lastnames_list)

# import lane county streets file as lanestreets_list and sort asc
with open('../data/resources/lanestreets_list/lanestreets_list.txt', 'r') as file:
    lanestreets_list = file.read().split(',')
lanestreets_list = np.sort(lanestreets_list)

# import states file as states_list and sort asc
with open('../data/resources/states_list/states_list.txt', 'r') as file:
    states_list = file.read().split(',')
states_list = np.sort(states_list)

# ## Defining case narrative anonymizer script
# 
# This section contains a script for anonymizing a case narrative dataset.

# ### Method 1: RegEx String Replacement
# This method involves defining regular expression patterns, then deploying these RegEx methods to further anonymize the data.

# define regex patterns
phone_pattern = r"\(?\b(\d{3})\)?[-.\s]*(\d{3})[-.\s]*(\d{4})\b"
address_pattern = r"\b\d+\s(?:[A-Za-z]+\s)*(?:St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Pl|Place|Lane|Ln|Drive|Dr|Court|Ct|Terrace|Ter|Way)[,.\s]"
web_pattern = r'(https?:\/\/)?(?:www\.)?[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}(?:\/\S*)?'
ip_pattern = r"\b((?:\d{1,3}\.){3}\d{1,3}|([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|:([0-9a-fA-F]{1,4}:){1,7}|::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4})\b"
zip_pattern = r"\b\d{5,}\b"
date_pattern = r"\b(?:\d{1,2}(st|nd|rd|th)?\s?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|\d{1,2}/\d{1,2}/?\d{2,4}|\d{4}-\d{2}-\d{2})\b"
month_pattern = "\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b"
num_pattern = r"\b\w*[\d]+\w*\b"
prefix_pattern = r"\b(Dr|Dr\.|Mr|Mr\.|Mrs|Mrs\.|Ms|Ms\.|Miss|Miss\.|Sir|Madam)\b"

def regex_remover(text):
    if not isinstance(text, str):
        return text
    
    # apply RegEx pattern for each target feature
    text = re.sub(address_pattern, "ADDRESS", text, flags=re.IGNORECASE)
    text = re.sub(zip_pattern, "ZIP", text, flags=re.IGNORECASE)
    text = re.sub(date_pattern, "DATE", text, flags=re.IGNORECASE)
    text = re.sub(month_pattern, "DATE", text, flags=re.IGNORECASE)
    text = re.sub(web_pattern, "WEBSITE", text, flags=re.IGNORECASE)
    text = re.sub(ip_pattern, "IP", text, flags=re.IGNORECASE)
    text = re.sub(phone_pattern, "PHONE", text, flags=re.IGNORECASE)
    text = re.sub(num_pattern, "NUMBER", text, flags=re.IGNORECASE)
    text = re.sub(prefix_pattern, "PREFIX", text, flags=re.IGNORECASE)
    
    return text

# ### Method 2: Natural Language Processing and Named Entity Recognition with spaCy
# For NLP, I am using spaCy and the 'en_core_web_sm' pretrained model (see more [here](https://spacy.io/models/en#en_core_web_sm)).

def nlp_anonymize_text(text):
    """ nlp_anonymize_text(text)
    
    - this function deploys a spaCy NLP model and removes
    target features that are found that are found
    """

    if not isinstance(text, str):
        return text
    
    # process the text with the NLP model
    doc = nlp(text)

    # replace all recognized names with 'NAME_REMOVED'
    for ent in doc.ents:

        # first check for addresses
        if ent.label_ in ["GPE", "LOC", "FAC"]:
            text = text.replace(ent.text, "ADDRESS")
        # then check for names
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, "NAME")
        # then check for dates
        if ent.label_ == "DATE":
            text = text.replace(ent.text, "DATE")
            
    return text

### Method 3: Predefined Term Replacement
#The first part of this method uses an aggregated set of first names registered at least five times in the SSA database from years 1880 through 2022. We call this method last as it is the most distructive to the original database.
# Then, this method uses a set of states and their shorthand forms such that states can be caught and replaced.

def name_remover(text, name_list, replacement_text):
    """
    Replaces names in the given text with 'NAME_REM', handling names case-insensitively.
    
    Args:
    text (str): The input text that may contain names.
    names (set): A set of names that should be anonymized, assumed to be in lower case.

    Returns:
    str: The anonymized text.
    int: The count of names replaced.
    """
    
    # Prepare regex pattern for case-insensitive matching
    pattern = r'\b(' + '|'.join(map(re.escape, name_list)) + r')\b'
    regex = re.compile(pattern, re.IGNORECASE)
    
    # Function to replace and count each match
    def replace_func(match):
        return replacement_text
    
    # Replace occurrences of any names in the text using a regex substitution
    text_anonymized = regex.sub(replace_func, text)
    
    return text_anonymized

def lanecounty_streets_remover(text):
    """
    Replaces names in the given text with 'ADDRESS', handling names case-insensitively.
    
    Args:
    text (str): The input text that may contain names.
    ssa_names (set): A set of names that should be anonymized, assumed to be in lower case.

    Returns:
    str: The anonymized text.
    int: The count of names replaced.
    """
    
    # Prepare regex pattern for case-insensitive matching
    pattern = r'\b(' + '|'.join(map(re.escape, lanestreets_list)) + r')\b'
    regex = re.compile(pattern, re.IGNORECASE)
    
    # Function to replace and count each match
    def replace_func(match):
        return "ADDRESS"
    
    # Replace occurrences of any names in the text using a regex substitution
    text_anonymized = regex.sub(replace_func, text)
    
    return text_anonymized

def state_remover(text):
    
    # Prepare regex pattern for case-insensitive matching
    pattern = r'\b(' + '|'.join(map(re.escape, states_list)) + r')\b'
    regex = re.compile(pattern, re.IGNORECASE)
    
    # Replace occurrences of any state names or abbreviations in the text
    text_anonymized, count = regex.subn("ADDRESS", text)
    
    return text_anonymized

def term_removal(text):
    if not isinstance(text, str):
        return text
    
    # call predefined term removal functions
    text = name_remover(text, firstnames_list, "SURNAME")
    text = name_remover(text, lastnames_list, "LASTNAME")
    text = lanecounty_streets_remover(text)
    text = state_remover(text) 
    
    return text

def data_anonymizer(case):
    """ narrative_anonymizer(case)
    
    this function takes in a dataset, in this case a case narrative
    and returns an anonymized case, where any identifying information
    is replaced with a FEATURENAME, where FEATURENAME is representative
    of the type of information that was removed.
    """
        
    # METHOD 1-- RegEx replacement:
    case = regex_remover(case)
    
    # METHOD 2-- natural language processing:
    # use NLP to anonomize target features
    case = nlp_anonymize_text(case)
    
    # METHOD 3-- predefined term replacement:
    case = term_removal(case)
        
    return case#{"call_transcription": case}

def anonymize_columns(data):
    """
    Anonymizes text columns of a DataFrame based on their dtype.
    """
    text_columns = data.select_dtypes(include=['object']).columns  # Assumes text columns are of type 'object'
    for col in text_columns:
        print(f"Anonymizing column: {col}")
        data[col] = data[col].apply(data_anonymizer)
    return data

def anonymize_narratives(in_datapath, out_datapath, separator=','):
    """
    Loads data, anonymizes it, and saves the anonymized version.
    """
    data = pd.read_csv(in_datapath, sep=separator)
    print("Data loaded. Starting anonymization process.")
    anonymized_data = anonymize_columns(data)
    anonymized_data.to_csv(out_datapath, index=False)
    print("Anonymized data saved to", out_datapath)

# Deploying the case anonymizer
anonymize_narratives("../cahoots_data/2023_CAHOOTS_Call_Data_Scrubbed.csv", "../output/2023_CAHOOTS_Call_Data_Anonymized.csv")




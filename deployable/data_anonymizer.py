# Personally Identifiable Information (PII) Data Anonymization
# 
# Script by Aussie Frost.
# 
# This script removes Personally Identifiable Information (PII) from a given csv.
# 
# A project for CAHOOTS --> https://whitebirdclinic.org/cahoots
# 
# Started 4/15/2024

# ### Import dependencies
# import standard libraries
import numpy as np
import pandas as pd
import regex as re

# import natural language processing libraries
import spacy
# load the spacy nlp model
nlp = spacy.load("en_core_web_sm") # en_core_web_sm or en_core_web_trf
# note must install: python -m spacy download en_core_web_trf

# ### Define data paths
in_datapath = "../cahoots_data/2023_CAHOOTS_Call_Data_With_Identifiers.csv" # input
out_datapath = "../output/2023_CAHOOTS_Call_Data_Anonymized.csv" # output

# Import anonymization resources
def import_resources(in_path):
    """ Helper function to import data resources

    Args:
    in_path (str): path to data resource that will be read into list

    Returns:
    mylist (list): sorted list created from the data resource
    """

    with open(in_path, 'r') as file:
        mylist = file.read().split(',')
    mylist = np.sort(mylist)

    return mylist

# import resource files as X_list where X is respective name of list
firstnames_list = import_resources('../data/resources/firstnames_list/firstnames_list.txt')
lastnames_list = import_resources('../data/resources/lastnames_list/lastnames_list.txt')
lanestreets_list = import_resources('../data/resources/lanestreets_list/lanestreets_list.txt')
states_list = import_resources('../data/resources/states_list/states_list.txt')

# ## Defining case narrative anonymizer functions
# This section contains a script for anonymizing a case narrative dataset.

# ### Method 1: RegEx String Replacement
# This method involves defining regular expression patterns, then deploying these RegEx methods to further anonymize the data.

# define regex patterns
phone_pattern = r"\(?\b(\d{3})\)?[-.\s]*(\d{3})[-.\s]*(\d{4})\b"
address_pattern = r"\b\d+\s(?:[A-Za-z0-9]+\s)*(?:St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Pl|Place|Lane|Ln|Drive|Dr|Court|Ct|Terrace|Ter|Way)\b(?:[,.\s]|$)"
web_pattern = r'(https?:\/\/)?(?:www\.)?[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}(?:\/\S*)?'
ip_pattern = r"\b((?:\d{1,3}\.){3}\d{1,3}|([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|:([0-9a-fA-F]{1,4}:){1,7}|::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4})\b"
zip_pattern = r"\b\d{5,}\b"
date_pattern = r"\b(?:\d{1,2}(st|nd|rd|th)?\s?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|\d{1,2}/\d{1,2}/?\d{2,4}|\d{4}-\d{2}-\d{2})\b"
month_pattern = "\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b"
#num_pattern = r"\b\w*[\d]+\w*\b"
prefix_pattern = r"\b(Dr|Dr\.|Mr|Mr\.|Mrs|Mrs\.|Ms|Ms\.|Miss|Miss\.|Sir|Madam)\b"

def regex_remover(text):
    """ Primary function to use RegEx patterns to remove sensitive data from
    case narratives. Note that case is ignored at each call of the re.sub
    function. This function returns a modified string where data has been removed.

    Args:
    text (str): a string of text to be anonymized

    Returns:
    text (list): a modified version of a string (or other unchanged input if not)
    """

    # ensure text is string (and is not null)
    if not isinstance(text, str):
        return text
    
    # apply RegEx pattern for each target feature
    text = re.sub(address_pattern, "(LOCATION)", text, flags=re.IGNORECASE)
    text = re.sub(zip_pattern, "(ZIP)", text, flags=re.IGNORECASE)
    text = re.sub(date_pattern, "(DATE)", text, flags=re.IGNORECASE)
    text = re.sub(month_pattern, "(DATE)", text, flags=re.IGNORECASE)
    text = re.sub(web_pattern, "(WEBSITE)", text, flags=re.IGNORECASE)
    text = re.sub(ip_pattern, "(IP)", text, flags=re.IGNORECASE)
    text = re.sub(phone_pattern, "(PHONE)", text, flags=re.IGNORECASE)
    #text = re.sub(num_pattern, "(NUMBER)", text, flags=re.IGNORECASE)
    text = re.sub(prefix_pattern, "(PREFIX)", text, flags=re.IGNORECASE)
    
    return text

# ### Method 2: Natural Language Processing and Named Entity Recognition with spaCy
# For NLP, I am using spaCy and the 'en_core_web_sm' pretrained model (see more [here](https://spacy.io/models/en#en_core_web_sm)).

def nlp_anonymize_text(text):
    """ Primary function to deploy a spaCy NLP model and remove
    target features that are identified in the text.

    Args:
    text (str): a string of text to be anonymized 

    Returns:
    text (str): a modified version of a string (or other unchanged input if not)
    """

    if not isinstance(text, str):
        return text
    
    # process the text with the NLP model
    doc = nlp(text)

    # replace all recognized names with name of feature removed (all caps)
    for ent in doc.ents:

        # check for addresses
        #if ent.label_ in ["GPE", "LOC", "FAC"]:
            #text = text.replace(ent.text, "(LOCATION)")
        # check for names
        if ent.label_ == "PERSON":
            if ent.label_ != 'pt':
                text = text.replace(ent.text, "(NAME)")
        # check for dates
        if ent.label_ == "DATE":
            text = text.replace(ent.text, "(DATE)")
        # check for languages
        if ent.label_ == "LANGUAGE":
            text = text.replace(ent.text, "(LANGUAGE)")
        """ optional features:
        # check for organizations
        if ent.label_ == "ORG":
            text = text.replace(ent.text, "(ORGANIZATION)")
        """
            
    return text

# ### Method 3: Predefined Term Replacement
# The first part of this method uses an aggregated set of first names registered at least five times in the SSA database from years 1880 through 2022. We call this method last as it is the most distructive to the original database.
# Then, this method uses a set of states and their shorthand forms such that states can be caught and replaced.
def term_remover(text, resource_list, replacement_text):
    """ Replaces terms in the given text with replacement_text, 
    handling names case-insensitively.
    
    Args:
    text (str): a string of text to be anonymized 
    resource_list (list): a list of predefined terms that should be removed from the text
    replacement_text (string): a string that will replace any removed data

    Returns:
    text_anonymized (str): a modified version of a string
    """
    
    # prepare regex pattern for case-insensitive matching
    pattern = r'\b(' + '|'.join(map(re.escape, resource_list)) + r')\b'
    regex = re.compile(pattern, re.IGNORECASE)
    
    # replace occurrences of any names in the text using a regex substitution
    text_anonymized = regex.sub(replacement_text, text)
    
    return text_anonymized

def term_replacement(text):
    if not isinstance(text, str):
        return text
    
    # call predefined term removal functions
    #text = term_remover(text, firstnames_list, "(SURNAME)")
    text = term_remover(text, lastnames_list, " (LASTNAME)")
    text = term_remover(text, lanestreets_list, " (LOCATION)")
    text = term_remover(text, states_list, " (LOCATION)")
    
    return text

# ## Defining the case anonymization pipeline flow
def data_anonymizer(text):
    """ This helper function takes in text, which in this case is a component 
    of a case narrative, and returns an anonymized version of that text, 
    where any identifying information is found and replaced with the name 
    of the feature that it corresponds to.

    Args:
    text (str): a string of text to be anonymized

    Returns:
    text (str): a modified version of a string
    """

    # METHOD 1-- natural language processing:
    # use NLP to anonomize target features
    text = nlp_anonymize_text(text)

    # METHOD 2-- RegEx replacement:
    text = regex_remover(text)
    
    # METHOD 3-- predefined term replacement:
    text = term_replacement(text)
        
    return text

def anonymize_columns(data):
    """ This function anonymizes each text column of a DataFrame by checking their 
    data type. The columns are replaced with their anonymized versions.

    Args:
    data (Pandas DataFrame): a DataFrame that is to be anonymized

    Returns:
    data (Pandas DataFrame): an anonymized DataFrame
    """

    # select columns that include text
    text_columns = data.select_dtypes(include=['object']).columns

    # define columns to ignore
    ignore_columns = ["Homeless", "Gender", "Call Sign"]
    for col in text_columns:
        
        # ignore specified columns
        if col not in ignore_columns:

            # display column that is being anonymized
            print(f"Anonymizing column: {col}")

            # apply data_anonymizer to column and update column contents
            data[col] = data[col].apply(data_anonymizer)
    return data

def anonymize_narratives(in_datapath, out_datapath, separator=','):
    """
    This is the main call to run the script. It takes an input data path
    and output data path (both defined at the top of the script). The
    input data csv is read into a Pandas DataFrame, and then the
    anonymize_columns method is called on the entire dataset. The
    anonymized dataset is then written to an output csv.

    Args:
    in_datapath (csv or alt. text separated file): dataset to be anonymized
    out_datapath (csv): anonymized dataset is written to this path
    seperator (char) [optional]: text separater, a comma as default

    Output:
    a csv at the path specified by out_datapath
    """

    # read input dataset into a csv
    data = pd.read_csv(in_datapath, sep=separator)
    print("Data loaded. Starting anonymization process.")

    # run the anonymize script on each column
    anonymized_data = anonymize_columns(data)

    # write the anonymized data to an output path
    anonymized_data.to_csv(out_datapath, index=False)
    print("Anonymized data saved to", out_datapath)

# Deploying the case anonymizer
anonymize_narratives(in_datapath, out_datapath)




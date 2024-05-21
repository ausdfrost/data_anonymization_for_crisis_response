# # create_label_position_csv.py
#
# script created by Aussie Frost on May 18th, 2024.
#
# ## part 1 of results analysis: create label position csv
# this creates a csv containing dicts of key:value pairs, where key
# is a label and value is an array of positons.
#
# we will call the final function once to create the one for the true 
# data and again for the model data.

import pandas as pd
import re

def create_entry_map(text):
    """ 
    this function takes in text and creates a 
    dictionary of key: value pairs where key is a 
    identifier label and value is an array of positions
    where that value was found.
    """

    # check to ensure text is in-fact a string
    if not isinstance(text, str):
        return text
    
    # split the text into a list of words
    words_list = text.split()
    label_pattern = r"\([A-Z]+\)"
    entry_map = {}

    # enumerate through the words in the list
    for i, word in enumerate(words_list):
        
        # check if word matches regex pattern
        if re.match(label_pattern, word):

            # clean up the label
            start, end = word.find('('), word.find(')')
            if start != -1 and end != -1:
                word = word[start+1:end]

            # create list for key, then append to it
            if word not in entry_map.keys():
                entry_map[word] = []
            entry_map[word].append(i)

    # if dict is not empty, return the dict
    return entry_map if len(entry_map) > 0 else ''
    
def create_label_position_csv(in_datapath, out_datapath):
    """ 
        this function takes in a csv containing labeled entries, flags the
        occurances of any terms delimited by '(LABEL)', where LABEL can be
        any string, then creates or updates an array of positions that is
        contained in a dictionary whose key is the LABEL that was detected.

        Example:
        input csv entry: "I was assisting (PERSON) at (ADDRESS)."
        output csv entry: {'PERSON':[3], 'ADDRESS':[5]}

        Args:
        in_datapath (str path): a path where the labeled data csv is
        out_datapath (str path): a path to where the position csv shall be output
    """

    # read the data in
    data = pd.read_csv(in_datapath)

    # select columns containing text
    text_columns = data.select_dtypes(include=['object']).columns
    for col in text_columns:

        # display column that is being anonymized
        print(f"Adding identifiers to column: {col}")
        data[col] = data[col].apply(create_entry_map)

    # output the data to a csv
    data.to_csv(out_datapath, index=False)
    print("Label map saved to", out_datapath)

# create a csv for scrubbed data, then again for estimated data
create_label_position_csv("../cahoots_data/2023_CAHOOTS_Call_Data_Scrubbed.csv", "2023_CAHOOTS_Call_Data_LabelMap_TruePositions.csv")
create_label_position_csv("../output/2023_CAHOOTS_Call_Data_Anonymized.csv", "2023_CAHOOTS_Call_Data_LabelMap_EstimatedPositions.csv")
# calculate_simularity_score.py
#
# by aussie frost
#
# calculate similarity between true labels and guessed labels csv
#
# this creates a csv containing dicts of key:value pairs, where key
# is a label and value is an array of positons
#
# we will call it once to create the one for the true data
# and again for the model data

import pandas as pd

# read in label position data
true_df = pd.read_csv("2023_CAHOOTS_Call_Data_LabelMap_TruePositions.csv")
estimate_df = pd.read_csv("2023_CAHOOTS_Call_Data_LabelMap_EstimatedPositions.csv")

def compare_entries(true_df, est_df):
    """ 
        CHANGE Returns nothing, but creates dataset and saves to project dir.
    """

    text_columns = true_df.select_dtypes(include=['object']).columns
    for col in text_columns:

        print(f"Checking similarity for column: {col}")

        for true_positions, est_positions in zip(true_df[col], est_df[col]):

            # compare between true and est positions !!!!! I WAS HERE
            if not isinstance(true_positions, dict):
                for key in true_positions:
                    print(key)

    # output the data to a csv
    #.to_csv(out_datapath, index=False)
    #print("Anonymized data saved to", out_datapath)

compare_entries(true_df, estimate_df)
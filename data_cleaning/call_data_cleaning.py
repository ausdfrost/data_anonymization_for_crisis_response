""" a simple script to merge the two data files """
import pandas as pd

# import data files
data1 = pd.read_csv("raw_data/2023_Data_Scrubbed_1.csv")
data1['callsign'] = pd.Series()
data2 = pd.read_csv("raw_data/2023_Data_Scrubbed_2.csv", header=None)

# join the dataframes
data = data1.append(data2)

# export merged dataframe
data.to_csv("2023_CAHOOTS_Call_Data_Scrubbed.csv", index=False)
# SSA Name cleaning
# Script to clean the social security administration names files into one comma seperated text file.

import os

# Directory containing the files
directory = "Popular Baby Names/"

# Set to hold all unique names
unique_names = set()

# Set frequency threshold of names
freq_thresh = 50

# Define any undesired names
names_to_ignore = {"de"}

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):  # Check to ensure only text files are read
        with open(os.path.join(directory, filename), 'r') as file:
            
            # Read each line in the file
            for line in file:
                name = line.split(',')[0]  # Get the first item (name) from each line
                freq = int(line.split(',')[2]) # Get the frequency of the name occuring
                # Add name to the set if it is not in the names to ignore (and not duplicate)
                
                # Ensure name is unique and name is common (based on freq_thresh)
                if (name.lower() not in names_to_ignore) and (freq >= freq_thresh): 
                    unique_names.add(name)

# Combine all unique names into a single string separated by commas
unique_names_string = ','.join(unique_names)

# Write the unique names to a new text file
output_file_path = "ssa_names.txt"
with open(output_file_path, 'w') as output_file:
    output_file.write(unique_names_string)

print("Unique names have been successfully written to ssa_names.txt")

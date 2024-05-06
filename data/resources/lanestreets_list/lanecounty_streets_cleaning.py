# Python script to process lists and output a cleaned, comma-separated list

def process_file(input_file, output_file):
    # Open the input file in read mode and output file in write mode
    with open(input_file, 'r') as file, open(output_file, 'w') as outfile:
        # Read all lines from the file
        lines = file.readlines()

        # Initialize an empty list to store processed words
        result = []

        # Iterate through each line
        for line in lines:
            # Strip whitespace and remove quotes if they exist
            cleaned_line = line.strip().replace('"', '').replace("'", "").replace(",", "")
            if cleaned_line:  # Check if the line is not empty
                result.append(cleaned_line)

        # Write the result to the output file as comma-separated values
        outfile.write(", ".join(result))

# Replace 'input.txt' and 'output.txt' with the paths to your input and output files
process_file('lanecounty_streets_messy.txt', 'lanestreets_list.txt')

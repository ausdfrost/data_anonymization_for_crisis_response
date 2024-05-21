# add_identifiers.py
#
# by aussie frost
#
# add faux PII to CAHOOTS scrubbed case narratives

import random
import pandas as pd

def identifier_generator(text):
    """Generate a random call transcription based on predefined templates."""

    # check to ensure text is in fact a string
    if not isinstance(text, str):
        return text
        
    # generate some spoofy names
    first_names = [
        "John", "Jane", "David", "Emily", "Michael", "Sarah", "William", "Jennifer", "Robert", "Mary-Sue"
        "Jessica", "Andrew", "Dr. Ashley", "James", "Amanda", "Sir Matthew", "Christina", "Daniel", "Elizabeth",
        "Joseph", "Nicole", "Anthony", "Margaret", "Kevin", "Laura", "Bryan", "Miss Alexis", "Nicholas", "Katherine",
        "Aiden", "Bella", "Carter", "Delilah", "Ethan", "Fiona", "Grayson", "Hazel", "Isaiah", "Juliet",
        "Kai", "Luna", "Mason", "Nora", "Oliver", "Penelope", "Quentin", "Riley", "Sebastian", "Tessa",
        "Uriah", "Violet", "Winston", "Xena", "Yosef", "Zoe", "Abram", "Beatrice", "Cedric", "Daphne",
        "Eliot", "Freya", "Gideon", "Harriet", "Idris", "Juno", "Knox", "Leia", "Milo", "Naomi",
        "Oscar", "Phoebe", "Reece", "Sienna", "Theo", "Uma", "Victor", "Willow", "Xavier", "Yasmin",
        "Zane", "Adele", "Blaine", "Cora", "Dexter", "Elsie", "Flynn", "Gracie", "Holden", "Iris", "Julia",
        "Jasper", "Keira", "Levi", "Matilda", "Nolan", "Olive", "Paxton", "Quinn", "Rowan", "Scarlett",
        "Tristan", "Ursula", "Vaughn", "Whitney", "Xander", "Yara", "Zack", "Alma", "Barrett", "Celeste",
        "Drake", "Esme", "Finn", "Gemma", "Hugo", "Ivy", "Jonah", "Kyla", "Lionel", "Mira", "Nico",
        "Octavia", "Pierce", "Rosalie", "Soren", "Thalia", "Ulysses", "Verity", "Wesley", "Yvette", "Charlie"
    ]
    last_names = [
        "Abbott", "Black", "Chapman", "Duffy", "Ellison", "Finch", "Griffith", "Harlow", "Ingram", "Jennings",
        "Knight", "Lowe", "Maxwell", "Norris", "Osborne", "Pike", "Quinn", "Rhodes", "Sherwood", "Tate",
        "Underwood", "Vance", "Whitfield", "York", "Adler", "Barron", "Connor", "Donahue", "Easton", "Field",
        "Golden", "Hartford", "Ivy", "Joyner", "Kessler", "Lawton", "Merritt", "North", "Overton", "Pritchard",
        "Quick", "Rivers", "Sterling", "Thorne", "Upton", "Vaughn", "Waverly", "Xavier", "Youngblood", "Ziegler",
        "Archer", "Beck", "Colby", "Dalton", "Everett", "Frost", "Garrison", "Hammond", "Irvine", "Justice",
        "Kipling", "Langston", "Morrow", "Noble", "Oakley", "Parson", "Quest", "Reilly", "Sawyer", "Thrasher",
        "Ulrich", "Valentine", "Warner", "Xiong", "Yost", "Zimmerman", "Ashby", "Birch", "Crowley", "Davenport",
        "Emerson", "Forrester", "Gilmore", "Hale", "Irwin", "Jasper", "Kent", "Law", "Meadow", "Northwood",
        "O'Donnell", "Pace", "Quill", "Riddle", "Sloan", "Tanner", "Upshaw", "Vincent", "Welles", "Younger", "Bickford"
    ]

    # generate 10 random names to use
    name_formats = []
    for _ in range(10):

        # Generate a random number of names, from 1 to 
        num_names = 1 #random.randint(1, 3)
        names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(num_names)]

        # Format the names into a natural sounding list
        if num_names > 1:
            name_text = ", ".join(names[:-1]) + " and " + names[-1]
        else:
            name_text = names[0]

        # append to the list of randomly generated names
        name_formats.append(name_text)

    # define faux identifiers to insert
    date_formats = ["2023-10-26", "12/04/2022", "August 15, 1999", "03.11.2018", "2010-02-02", "January 31", "2 Feb", "June 14", "September 22", "Mar 21st", "Apr 1"]
    location_formats = ["123 Main St, San Francisco, CA 12345", "567 Elm St, Eugene, OR 54321", "42 Park Way", "81915 East 24th Ave, Eugene"
                      "15161 Thornberry Lane, Eugene", "51 West 13th St, Eugene, OR 98412", "2481 Jefferson St"]
    age_formats = ["17", "21", "25", "49", "72"]
    facility_formats = ["5th Street Market", "Thermofisher Dynamics", "Target", "White Bird Clinic"]
    language_formats = ["English", "Spanish", "French", "Chinese", "Japanese", "Korean"]

    # find each anonymized identifier, and replace it with a randomly generated identifying feature
    text = text.replace("(NAME)", random.choice(name_formats))
    text = text.replace("(DATE)", random.choice(date_formats))
    text = text.replace("(AGE)", random.choice(age_formats))
    text = text.replace("(LOCATION)", random.choice(location_formats))
    text = text.replace("(FACILITY NAME)", random.choice(facility_formats))
    text = text.replace("(LANGUAGE)", random.choice(language_formats))

    return text

def generate_identifiers(in_datapath, out_datapath):
    """ 
        CHANGE Returns nothing, but creates dataset and saves to project dir.
    """
    # read the data in
    data = pd.read_csv(in_datapath)

    text_columns = data.select_dtypes(include=['object']).columns
    for col in text_columns:

        # display column that is being anonymized
        print(f"Adding identifiers to column: {col}")
        data[col] = data[col].apply(identifier_generator)

    # output the data to a csv
    data.to_csv(out_datapath, index=False)
    print("Anonymized data saved to", out_datapath)

# generate a faux dataset
generate_identifiers("2023_CAHOOTS_Call_Data_Scrubbed.csv", "2023_CAHOOTS_Call_Data_With_Identifiers.csv")
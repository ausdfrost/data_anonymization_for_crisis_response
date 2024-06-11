"""
a simple script to scrape resource site and get nice data.
"""

import requests
from bs4 import BeautifulSoup

# provide url of last name site to scrape
url = 'https://names.mongabay.com/most_common_surnames.htm'
# get soup
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# declare lastnames list
lastnames = []
ignorenames = ["GOOD"]

# get table by row
table = soup.find('table')
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if columns:  # This check ensures that you don't get errors from rows without columns
        lastname = columns[0].text.strip()  # Get the first column entry
        if lastname not in ignorenames:
            lastnames.append(lastname.title())  # Append to the list
        
# Combine all unique names into a single string separated by commas
unique_names_string = ','.join(lastnames)

# Write the names to a new text file
output_file_path = "lastnames_list.txt"
with open(output_file_path, 'w') as output_file:
    output_file.write(unique_names_string)

print(f"Last names have been successfully written to {output_file_path}")
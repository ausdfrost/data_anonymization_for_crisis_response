# Data
## Testing dataset 1: Pseudo-sensitive data
**Data description** To begin testing the feasibility of the case anonymization script, I first created a script to
generate a dataset of 1,000 case narrative call transcriptions. These call transcriptions are based on templates
that are filled in with randomly generated personally identifying info including fake names, email addresses,
phone numbers, physical addresses, IP addresses, and more. This data proved incredibly useful in testing the
functionality and performance of my anonymization script.

<img width="720" alt="image" src="https://github.com/ausdfrost/data_anonymization_for_crisis_response/assets/65328557/253b3beb-f503-4681-8d72-6feb82a277bf">


**Data features** This dataset included observations that were by-case, meaning that each row represents a
case that the organization went on. The only relevant column is ’call_transcription’, which are string entries
representing individual case narratives. These case narratives are filled with randomly generated personally
identifiable information that the anonymization script will attempt to remove.

**Data generation** This dataset was generated using the script found at the path ’exploration/data_generation.ipynb’.
I used an approach that iterated row-by-row, selecting a random template to use for the call transcription and
then populating that template with various personally identifiable information that I had predefined. Time of
the call and a call type were also randomly generated such to have a more realistic data source.

## Testing dataset 2: CAHOOTS Clean Call Data
**Source** CAHOOTS officer

**Data description** This dataset was provided by an officer at CAHOOTS on May 10th, 2024. It contains 100
’scrubbed’ rows of real calls that the agency has gone on. This data will be used to make final revisions on the
script, and to ensure the script properly fits the schema of the final dataset.

**Data features** This dataset contains 15 columns or features. The features consist of patient assessments,
historic background, status on gender identity, homelessness, and more. All of these columns will need to be
ran through the anonymization script.

## Anonymization resource 1: Social Security Administration First Names
**Source** https://www.ssa.gov/oact/babynames/limits.html

**Data description** I used a dataset from the Social Security Administration containing first names registered
at least 5 times in a given year in the United States, for the years 1880 to 2022.
Data features The raw data consisted of three columns, which are first name, assigned sex, and name assignment
frequency in the given year. I focused on the first name and name assignment frequency columns for
my data preprocessing.

**Preprocessing** I created a Python script to merge all the unique first names into one comma separated text
file, and filtered the data such that only names that were registered at least 50 times in a given year were
included in the final list.

<img width="622" alt="image" src="https://github.com/ausdfrost/data_anonymization_for_crisis_response/assets/65328557/6262df8e-3d52-453a-856b-8a3f7a5cd1a0">

## Anonymization resource 2: U.S. Census Surnames
**Source** https://names.mongabay.com/most_common_surnames.htm

**Data description** I used a dataset from Mongabay, which contained the 1,000 most common surnames as
reported by the U.S. Census Bureau.

**Data features** The raw dataset contained some handy features, however, since there were only 1,000 name
observations, I decided to simply take all of them intomy processed file. Thus, the only feature I paid attention
ot was the ’surname’ column of the dataset.

**Preprocessing** I created a Python script that utilized BeautifulSoup to scrape theHTMLsource of the website
containing this data. I ripped the table from this website and aggregated all of the names into a single comma
separated text file.

<img width="703" alt="image" src="https://github.com/ausdfrost/data_anonymization_for_crisis_response/assets/65328557/6bf30d2f-9a17-46f8-9c19-31577a3f3bff">

## Anonymization resource 3: Lane County Street Address Components
**Source** Finn Fujimura from Rori Rolfs’ DS4SJ research group

**Data features** The raw data contains features or components that make up Oregon Lane County addresses.
Initially, they are categorized by component type, but for simplicity I am choosing to condense them all into
one file. I may elect to use the separated components later on, should I find that to be a more robust way to
identify and remove addresses.

**Preprocessing** I first hand removed the list titles and closing brackets. I then created a Python script to parse
through the raw text file, iterating line by line to remove any quotes. I stored each element into a list and
joined them with a comma as a single string. I then outputted this cleaned string into a csv.

<img width="613" alt="image" src="https://github.com/ausdfrost/data_anonymization_for_crisis_response/assets/65328557/9cbbc941-d98c-4d9b-bd42-b361da0af9fa">

## Anonymization resource 4: United States State Names
**Source** Self-created

**Data features** This file is simply a list I created of states in the United States, their abbreviations, and some
misspellings and nicknames of Oregon. I also included Lane county in this list, and some commonly mentioned
places around the area of Eugene.

<img width="226" alt="image" src="https://github.com/ausdfrost/data_anonymization_for_crisis_response/assets/65328557/bc981e0c-2fa2-4f37-95dd-206f95a826be">

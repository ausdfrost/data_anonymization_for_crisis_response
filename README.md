# Personally Identifiable Information (PII) Anonymization for the CAHOOTS Crisis Response Organization

A project by Aussie Frost.

## Overview
I am using spaCy natural language processing and various data manipulation methods to anonymize crisis case narratives given by [CAHOOTS](https://whitebirdclinic.org/cahoots/), a local crisis response organization in Eugene, Oregon.

## File structure
A quick overview on the files in this repository.
1. Exploration on building the various scripts lives here: ['exploration'](exploration)
2. Deployable scripts live here: ['deployable'](deployable)
3. Example data and resources live here: ['data'](data)
    1. Resources live here: ['data/resources'](data/resources)
4. Example output lives here: ['output'](output)

.
├── README.md
├── data
│   ├── call_data.csv
│   └── resources
│       ├── firstnames_list
│       │   ├── Popular Baby Names.zip
│       │   ├── firstnames_list.txt
│       │   └── ssa_name_cleaning.ipynb
│       ├── lanestreets_list
│       │   ├── denylist.py
│       │   ├── lanecounty_streets_cleaning.py
│       │   ├── lanecounty_streets_messy.txt
│       │   └── lanestreets_list.txt
│       ├── lastnames_list
│       │   ├── lastnames.py
│       │   └── lastnames_list.txt
│       └── states_list
│           ├── states_cleaning.py
│           └── states_list.txt
├── deployable
│   └── data_anonymizer.py
├── exploration
│   ├── data_anonymizer.ipynb
│   ├── data_generation.ipynb
│   └── result_analysis.ipynb
├── notes
│   ├── identifiers_to_remove.txt
│   └── project_goals.txt
└── output
    └── call_data_anonymized.csv

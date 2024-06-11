# CAHOOTS Crisis Response Data Anonymization

A project by Aussie Frost for the DSCI 410 Applied Data Science for Social Justice course led by Professor Rori Rohlfs.  

Started on 4/15/2024. Presented on 6/7/2024. Completed on 6/10/2024.

## Overview
I am using Named Entity Recognition alongside RegEx data manipulation methods to anonymize crisis case narratives given by [CAHOOTS](https://whitebirdclinic.org/cahoots/), a local crisis response organization in Eugene, Oregon.

## What is the goal of this project?
The research question I am focused on is defined as follows: "can a script reliably remove identifying information (names, phone numbers, addresses) from case narratives?". This original question has been expanded upon to capture more identifying information such that the output results in what is considered a Limited Data Set.

## Why is this important?
Organizations are constantly collecting data on the work that they are doing. This data often contains sensitive information that could be traced back to reveal a person's identify. The CAHOOTS organization holds the confidentiality of all of their patients very highly, thus they want to mitigate any risk of data with PII (personally identifiable information) from getting into the wrong hands. In this project, I set out to build a robust tool to remove this sensitive information. This allows the data to be passed on to data analysts in the future, such that meaningful questions can be asked and organization insights can be found.

## How does the anonymizer work?
After a lot of work devising the best data anonymization pipeline, I came up with a clear and modular process. I have packaged my  data anonymization toolkit as a Python Package called [anonymizePy](https://pypi.org/project/anonymizePy/), which is free and available to anyone. 

This package can be installed just like any other Python package via pip. If you are curious to get a more detailed look into how the anonymizer works, you can view the complete set of methods [here](https://github.com/ausdfrost/anonymizePy/blob/main/anonymizePy/data_anonymization_toolkit.py).

### Getting started
Setup takes just a few steps:

1. Install anonymizePy: `pip install anonymizePy`
2. Install necessary model: `pip install https://huggingface.co/beki/en_spacy_pii_distilbert/resolve/main/en_spacy_pii_distilbert-any-py3-none-any.whl`

### Running the scripts
Replicating my analysis involves running these two scripts:

1. Preprocessing: The script I used to preprocess the CAHOOTS can be found here --> '[case narrative data cleaning](call_data_cleaning.py)'. This script must be run on CSV files that were downloaded from CAHOOTS via Microsoft SharePoint.
2. Data anonymization pipeline: The script I used to deploy the methods from anonymizePy can be found here --> '[data_anonymization](data_anonymization.py)'. It's easy to adjust parameters to tailor the script to your liking. <ins>Note</ins> that you will need to redefine your paths with respect to your data.

### Example data and output
Example data can be found here --> '[call data](call_data.csv)'. Example result output can be found here --> '[anonymization metrics](anonymization_metrics.log)'.

## How has this project been shared?
- A [presentation](presentation.pdf) outlining my work was presented in front of peers and University of Oregon faculty on June 7th, 2024.
- A [report](project-report.pdf) outlining the case anonymization project was sent to Professor Rori Rohlfs on June 10th, 2024.

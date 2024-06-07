# CAHOOTS Crisis Response Data Anonymization

A project by Aussie Frost. 

Started on 4/15/2024. Presented on 6/7/2024. Completed on 6/10/2024.

## Overview
I am using spaCy natural language processing and various data manipulation methods to anonymize crisis case narratives given by [CAHOOTS](https://whitebirdclinic.org/cahoots/), a local crisis response organization in Eugene, Oregon.

## Research question and project goal
The research question I am focused on is defined as follows: "can a script reliably remove identifying information (names, phone numbers, addresses) from case narratives?". This original question has been expanded upon to capture more identifying information such that the output results in what is considered a Limited Data Set.

## Why is this important?
Organizations are constantly collecting data on the work that they are doing. This data often contains sensitive information that could be traced back to reveal a person's identify. The CAHOOTS organization holds the confidentiality of all of their patients very highly, thus they want to mitigate any risk of data with PII (personally identifiable information) from getting into the wrong hands. In this project, I set out to build a robust tool to remove this sensitive information. This allows the data to be passed on to data analysts in the future, such that meaningful questions can be asked and organization insights can be found.

## How does the anonymizer work?
After a lot of work devising the best data anonymization pipeline, I came up with a clear and modular process. I have packaged my very own data anonymization pipeline as a Python Package called [anonymizePy](https://pypi.org/project/anonymizePy/). 

This package can be installed just like any other Python package via pip. If you are curious to get a more detailed look into how the anonymizer works, you can view the complete set of methods [here](https://github.com/ausdfrost/anonymizePy/blob/main/anonymizePy/data_anonymization_toolkit.py).

## Setting up the data anonymization
Setup takes just a few steps:

1. Install anonymizePy: `pip install anonymizePy`
2. Install neccecary model: `pip install https://huggingface.co/beki/en_spacy_pii_distilbert/resolve/main/en_spacy_pii_distilbert-any-py3-none-any.whl`

## How to run the script:
The script I used to deploy the methods from anonymizePy can be found here: '[data_anonymization](data_anonymization.py)'. It's easy to adjust parameters to tailor the script to your liking. <ins>Note</ins> that you will need to redefine your paths with respect to your data.

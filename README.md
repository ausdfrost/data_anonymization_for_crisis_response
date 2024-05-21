# CAHOOTS Crisis Response Data Anonymization

A project by Aussie Frost.

## Overview
I am using spaCy natural language processing and various data manipulation methods to anonymize crisis case narratives given by [CAHOOTS](https://whitebirdclinic.org/cahoots/), a local crisis response organization in Eugene, Oregon.

## Purpose
The research question I am focused on is defined as follows: "can a script reliably remove identifying information (names, phone numbers, addresses) from case narratives?".

This original question has been modified to capture more identifying information such that the output results in what is considered a Limited Data Set. The identifiers that must be removed are specified in a text file found [here](notes/identifiers_to_remove.txt).

## File structure
A quick overview on the files in this repository.
1. Exploration on building the various scripts lives here: ['exploration'](exploration)
2. Deployable scripts live here: ['deployable'](deployable)
3. Example data and resources live here: ['data'](data)
    1. Resources live here: ['data/resources'](data/resources)
4. Example output lives here: ['output'](output)
5. Results analysis strategies live here: ['results'](results)

## How to run the script
The deployable version of this script can be found [here](deployable/data_anonymizer.py). The [README](deployable/README.md) contains an overview on the functionality of the script, as well as some key dependencies that must be installed in order for the script to work.

---
Last updated on 12 May 2024.

# Case anonymization script
## Overview
The deployable Python script can be found at the path ’deployable/data_anonymization.py’. This script is
compatible with the CAHOOTS dataset that was provided (see ’Testing Dataset 2’). I will be referencing this
script for the analytical steps. Note that this script was derived and further modified from the JupyterNotebook
found at [’exploration/data_anonymizer.ipynb’](’./exploration/data_anonymizer.ipynb’). Should you wish to see process work, this notebook can
be referenced, however do note that this script was only used for testing model feasibility and is not fully
compatible with the final CAHOOTS-provided dataset.

## Dependencies
These are the dependencies I used to deploy the analytical script:

1. Python 3.11.6
2. NumPy
3. Pandas for data management and manipulation
4. SpaCy for natural language processing (NLP)
  (a) ’en_core_web_sm’ pretrained model (set as default)
  (b) ’en_core_web_trf’ pretrained model (optional, but can yield better performance at cost of speed)

## Data paths and resource imports
**Define data paths** This section of the script allows for the user to specify the path that the data yet-to-be
anonymized exists, as well as specify an output path. These paths are used when calling the final anonymization
script.

**Import anonymization resources** A helper function was created to open a csv at a given path and read it into
a list. The list is then sorted and returned to the user. This function is called upon four times in order to
import the four respective anonymization resources (see ’Anonymization resource 1-4’).

## Case narrative anonymization methods
There are three primary methods used in the case narrative anonymization pipeline. Brief descriptions of the
functions involved are as follows.

**Method 1:** RegEx string replacement RegEx patterns are defined to take care of the various personally
identifiable information that is needed to be removed. Patterns are made for phone number, physical address,
web address, ip address, zip code, dates, months, numbers, and name prefixes.
The primary function uses our defined RegEx patterns to remove sensitive data from a string of text. Note
that case is ignored at each call of the re.sub function. This function returns a modified string of text where
data has been removed.

**Method 2:** Named entity recognition and removal with NLP This primary function is used to deploy a
spaCy NLP model and remove target features that are identified in the text. This uses a predefined model
(see ’Dependencies’) but can be expanded to use a more specified model if desired. The text is processed by
the NLPmodel, then each entity label is checked and replaced accordingly if it matches one of the ones flagged
by this function. The flagged labels for address are ’GPE’, ’LOC’, ’FAC’, for name we use ’PERSON’, and for
date we use ’DATE’. Each time one of these labels are found they are replaced by their respective anonymized
label. This function returns the modified string of text by which the string has been further anonymized.

**Method 3:** Predefined term replacement A helper function, ’term_remover’, is defined to take a string of
text to be anonymized, a list of predefined terms to be removed, and a string that should replace any text that
is removed. This method parces through the text, ignoring case, and removes any terms that appear in the
given ’resource_list’, replacing them with ’replacement_text’. This function returns the modified string of text
by which the string has been anonymized.
The primary function, ’term_removal’ takes in text, ensures that it is a string, and runs the ’term_remover’
function for each respective anonymization resource (see ’Anonymization resource 1-4’.). A respective replacement
text is specified for each call of the ’term_remover’ function. This primary function returns the
modified string of text by which the string has been further anonymized through each of these ’term_remover’
calls.

## Defining the case anonymization pipeline flow
**Data anonymizer** This helper function takes in text, which in this case is a component of a case narrative,
and returns an anonymized version of that text, where any identifying information is found and replaced with
the name of the feature that it corresponds to. For example, a name is replaced with the text ’[NAME]’. Our
three case narrative anonymization methods are called (for definitions, see ’Case narrative anonymization
methods’).

**Anonymize columns** This helper function takes in a Pandas DataFrame and identifies the columns that
contain text. It then parces through each column, deploying the ’data_anonymizer’ function on each of the
columns. It takes the results of the data anonymizer and replaces the contents of the respective column with
this anonymized version. A Pandas DataFrame is returned, with all of the text columns replaced by their
anonymized counterparts.

**Anonymize narratives** This is the main call to run the script. It takes an input data path and output data
path (both defined at the top of the script). The input data csv is read into a Pandas DataFrame, and then the
’anonymize_columns’ method is called on the entire dataset. The anonymized dataset is then written to an
output csv. At this point, the data has been anonymized and we can observe the results.

## Deploying the case anonymization
You can deploy the case anonymization by simply calling the ’anonymize_narratives’ function with respect
to the desired input and output paths as defined above (see ’Define data paths’). You must deploy this script
on a CSV like file (if you have a Microsoft Excel file it should be converted prior to running the script). Your
anonymized case narratives will be output to the specified path.

# seattle-service-requests
## University of Oklahoma
## Data Science and Analytics Institute

This repository contains scripts for manipulation data from the Seattle FindIt-FixIt application.  It also includes a script that builds and uses a retrained LLM to reclassify service request types based upon text verbatims included by residents in their requests.  The dataset and LLM are available in the HuggingFace hub at mjbeattie/finditfixit.

The files included in this repository are:
+ __mjb_city_sql_queries.sql__:  a PostgreSQL script to join raw FindItFixIt data into useful tables and views.
+ __mjb_prepare_text.sql__:  a PostgreSQL script to build the training, test, and unlabelled datasets for reclassification purposes.
+ __findit_fixit_classification.ipynb__: a Jupyter notebook script that creates a HuggingFace dataset from the data generated by mjb_prepare_text.  The script also retrains a BERT classifier from the HuggingFace hub to classify the FIFI data based upon resident verbatims.  The script then uses this model to reclassify a random sample of service requests that were created prior to the inclusion of the Unauthorized Encampment request type value.  Because of VM constraints, portions of this script were manually rerun in blocks to generate 20,000 reclassified data observations.
+ __fifi_torch__running_times.txt__: a file containing the runtimes associated with the reclassification
+ __classification_timing.xlsx__: an Excel file that graphs the runtimes and determines the relationship between runtime and observations.
+ __final_reclassified_fifi_reqs.csv__: the 20,000 reclassified observations.  These need to be matched back to request create dates by Service Request ID.  This file can be used to estimate the reclassification of all records.
 

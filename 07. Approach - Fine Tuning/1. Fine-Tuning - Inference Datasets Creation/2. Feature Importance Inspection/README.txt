This folder contains information about the procedure of finding the Feature Importance per NACE code. This will be later 
used in order to choose which features to include to the LLM Fine-Tuning dataset, based on the NACE code of the business
category. 

- I created a ML model dataset of every (NACE, neighborhood) pair and a binary target based on if the specific area is top3 for this NACE
- I trained an XGBoost model on the dataset
- I performed SHAP on the model to get the Features Importances and used them as ranking criteria to rank the features per NACE
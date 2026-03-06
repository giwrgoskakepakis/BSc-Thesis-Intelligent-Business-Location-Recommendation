This folder contains the initial research implemented in order to see if a pre-trained LLM can answer our questions. This is obviously a dummy and 
simple approach that I did not expect to work, but here is what i did: 

First of all, i used the 'Economic_Activities_Volos.xlsx' dataset, and i tried to implement a target feature:
- I used the difference of 'Break Date' - 'Start Data' as a target and success indicator
- I transformed this float value into binary with success threshold = 4

Then, i used the pre-trained LLM 'facebook/bart-large-mnli' that gets a regular text input and outputs a classification probability, out of the labels 
['success', 'failure']. In order to compare with the dataset, i did the following:
- I transformed the tabular features to 1 text feature, which is the LLM input 
- I inferenced the LLM to get the predicted probabilities
- I compared these to the binary 'ground-truths'

In order to evaluate the LLM, i calculated the metrics for each 'Department' in separate, and for every one i got ~0.48 ROC-AUC, and the LLM predicted 'success'
for almost all the cases --> it did NOT work well, it is almost as a random classifier (expected, since it has not been trained on data like these).

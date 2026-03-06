In this attempt i followed a Semi-Supervised Learning (SSL) method, specifically 'Self-Training': training the model on the few labeled data,
inferencing it to predict the unlabeled data's labels, and then re-training it.

- I created the pseudo-labels in the file 'business_data_imputed.csv'
- I used all the ratings (original + pseudo-labels) to find the top-3 locations per NACE code

---> All this procedure essentially created the file 'top3.csv', of structure (NACE_Code, Top1, Top2, Top3).

I used 2 approaches for performing the SSL method (pseudo-labeling): 

- Approach 1 --> uses just the Neighborhood features
- Approach 2 --> uses both the Neighborhood features AND the Municipal Community feature

--> I ended up with the 1st approach --> this time i do not utilize the Municipal Communities data

---> All this procedure created the file 'top3.csv', of structure (NACE code, top1, top2, top3)
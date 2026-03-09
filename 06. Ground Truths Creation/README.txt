A large problem so far is the sparseness of the labels (ratings/reviews/...). In this section i will try to produce ground truths
so i can later evaluate the models i create. I followed 3 different approaches, and finally ensembled them: 

- Approach 1 - Supervised: uses a ML model trained on a binary dataset based on the existance or not of a NACE in the location
- Approach 2 - Unsupervised: uses clustering per NACE to find the best cluster centroid that represents the best conditions
- Approach 3 - Semi-Supervised: uses pseudo-labeling to create more ratings and their average per location for ranking

These 3 approaches are then Compared and Combined to get the final file 'final_top3.csv' 




================================================ Comparison-Combination ================================================

- Comparison: i created some stats/visualizations to compare the 3 files (Venn Diagrams/Jaccard Similarity/% with at least 1 common/% with all 3 common/...),
  and the Supervised and Semi-Supervised approaches are more similar than the other pairs.

- Combination: i used the ENSEMBLE method, to combine the results from all 3 approaches and extract the final 'top3.csv' file. I used weights for each approach 
  (0.20, 0.35, 0.45) and scores (Top1 = 3 pts, Top2 = 2 pts, Top3 = 1 pt), in order to assign a score to each candidate and use it as ranking criteria to acquire 
  the final top-3 suggestions per NACE. 

Next: i can compare the final top3 with each original top3




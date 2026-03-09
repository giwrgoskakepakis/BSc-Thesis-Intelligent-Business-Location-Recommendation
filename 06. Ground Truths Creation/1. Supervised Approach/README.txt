This folder contains Information about the Supervised Approach to create the top3 location per NACE:

- I created a ML model training dataset consisting of every possible (NACE Code, Neighborhood) pair and label 1/0 if it exists
- I trained a ML model on this dataset
- I inferenced the ML model on every (NACE Code, Neighborhood) pair to get a score, and used it as ranking criteria
- I kept the top-3 neighborhoods of each category

I used 2 approaches for creating the ML model: 

- Approach 1 --> uses just the Neighborhood features
- Approach 2 --> uses both the Neighborhood features AND the Municipal Community feature

--> I ended up with the 2nd approach --> GOOD, because I actually utilize the Municipal Community data!!

---> All this procedure created the file 'top3.csv', of structure (NACE code, top1, top2, top3). This approach could flaud because it
assumes that the existance of a business in a location entails high success probability.






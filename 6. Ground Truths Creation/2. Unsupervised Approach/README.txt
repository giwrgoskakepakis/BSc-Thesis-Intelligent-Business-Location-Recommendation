This folder contains Information about the Unsupervised Approach to create the top3 location per NACE. For each NACE code:

- I filtered the 'business_data.csv' to only keep the entries of this specific NACE
- I perfrormed K-Means-Clustering to divide them into clusters
- I found the CENTROID of the 'ideal cluster', which represents the average ideal conditions for this NACE
- I calculated the distance of every candidate location from the centroid and used it as a ranking criteria
- I kept the 3 candidates with the smaller distance as the top-3

I used 2 approaches for performing the clustering: 

- Approach 1 --> uses just the Neighborhood features
- Approach 2 --> uses both the Neighborhood features AND the Municipal Community feature

--> I ended up with the 2nd approach --> GOOD, because I actually utilize the Municipal Communities data!!

---> All this procedure created the file 'top3.csv', of structure (NACE code, top1, top2, top3)


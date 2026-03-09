This folder contains an initial approach to JOIN the business entries with their corresponding Neighborhood.

- I performed the Spatial Join in the 'join_business_Neighborhoods_data.ipynb' to assign a Neighborhood to each business entry, and 
  saved it to the file 'business_data_with_null.csv'
- I filtered out the entries whose 'Neighborhood' feature was null and saved it into the file 'business_data.csv' (-24)

Final File: after all that I have the final business entries file: 'business_data.csv'(3884 entries), which right now contains the NACE code, the Municipal Community,
and the Neighborhood it belongs to. 

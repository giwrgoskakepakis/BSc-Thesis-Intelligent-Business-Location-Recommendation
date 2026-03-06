This folder contains an initial approach to JOIN the business entries with their corresponding Municipal Community.

- I performed the Spatial Join in the 'join_business_ELSTAT_data.ipynb' to assign a Municipal Community to each business entry
- I saved it to the file 'business_data.csv'
- I joined the file 'business_data.csv' with 'ELSTAT-demographic-economic.csv', and saved it to the file 'business_data_economic_demographic.csv'

The important part here is NOT the joined '.csv' file ('business_data_economic_demographic.csv'), as this is just the joined version at this time. 
If something changes in the 2 base '.csv' files, I have to join them again to update it. 


Final File: after all that I have the final business entries file: 'business_data.csv', which right now contains the NACE code, the Municipal Community, but
does NOT contain Information of the Neighborhood yet. 

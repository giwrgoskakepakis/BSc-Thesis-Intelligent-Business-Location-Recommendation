I used the Foursquare API to make API calls about Volos. This is the method i followed: 

- I used a grid structure of circle centroids so the total area covers most of Volos
- I used the Foursquare API to make MULTIPLE API Calls about the business entries that belong in each grid circle, and saved it in the file 'places_{i}.json'
- I merged the data from the multiple '.json' files, and saved it in the file 'all_places_combined.json'
- I filtered out the unique entries, since the centroid circles overlapped, and saved it in the file 'all_places_deduplicated.json'
- I extracted the data from the previous '.json' into a '.csv' file ('foursquare_data_no_rating.csv')
- I manually added the 'Rating'/'Reviews' columns for the data, and saved it in the file 'foursquare_data.csv'

This is the final '.csv' file that will be used later for merging with other sources
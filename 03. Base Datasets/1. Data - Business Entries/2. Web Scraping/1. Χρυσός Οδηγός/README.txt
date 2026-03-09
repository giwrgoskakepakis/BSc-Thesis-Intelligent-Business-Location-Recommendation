This folder contains all the information about the data extracted from Xrysos Odigos. The scraping of the data happened through the 'Web Scraper Chrome Extension', so 
there is no file that demonstrates it.  

I performed the scrapping 2 times because i did not include ratings initially. The entries were LESS the 2nd time, but overlapped with entries from the 1st time. 
Therefore, I deleted the duplicates, and updated the 1st .csv with the "rating"/"number_of_ratings" features, wherever it existed.

Geocoding: the entries did NOT have Latitude/Longitude:
- I geocoded using the Google Maps API and i got 3420/3974 (86.06%)
- I inserted the remaining coordinates MANUALLY using the Google Maps App

The final '.csv' file is 'xrysos-odigos-volos-ratings.csv', and will be later used on merging with data from different sources
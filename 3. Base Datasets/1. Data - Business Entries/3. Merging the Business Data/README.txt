This folder contains the information about the MERGING of the business entries from my different sources. I followed these steps: 

- Data Merging: the actual merging of the different datasets (assuming they are in the same structure already), implemented in 'data_merging.ipynb'
- Data Cleaning: searching for duplicates, correcting some mistakes (wrong city entries, geocodings), merging the city names --> i end up with the file 'business_data.csv'
- EDA: inspecting the new dataset, this file mainly CHECKS the MISSING data (i was going back-in-fourth: checking-completing)

Missing Data Analysis: there were cases where data was missing and i filled them manually: latitude/longitude, city, postal code, category

Final File: after all that I have the final business entries file: 'business_data.csv', which right now does NOT contain information about the NACE code,
the Municipal Community or the Neighborhood yet. 

We can see a visualization of the business entries on the '.html' file 'map_of_businesses_clustered.hmtl'



About Data Cleaning: 
- I deleted 10 duplicates that i found through "data_cleaning.ipynb"
- I made the descriptions that change lines to not do that for beautifying
- I deleted all the samples that are not on volos (4731 entries and ended up with 4331) (- 400).
- I corrected some wrong geocodings, only where i had an address AND city name
- I manually changed the other wrong geocodings, now everywhere i have a lat/long, i have a coordinate inside Volos (ended up with 4330) (-1)
- Ι manually added whatever addresses i could find from the entries that did not have (and removed some useless entries i saw) (ended up with 4304) (-26) 
- I deleted the entries that had no address/lat/long (ended up with 3914) (-390)
- I manually added the postal code where it did not exist (and removed some useless entries i saw) (ended up with 3911) (-3)
- I manually added the city name "Βόλος Μαγνησίας" on the 24 entries that did not have one
- I manually added the category name on the 4 entries that did not have one and deleted one (ended up with 3910) (-1)
- I manually made the Category-NACE mapping (1200+ entries) and used it to add a NACE code/description column to the dataset (ended up with 3906) (-4)
- I manually corrected some Postal Codes so now every Instance is inside Magnesia
- I cleaned the rating entries from GreekCatalog, so they use ' , ' instead of '0.0,0.0' where there are no ratings
- I scaled the 'rating' column so it is consistent across all sources
Now the only columns with missing values are: Description/Reviews/Rating 
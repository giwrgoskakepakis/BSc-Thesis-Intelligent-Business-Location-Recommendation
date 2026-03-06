In this approach, i try to create new candidates in a smaller unit that the Municipal Communities, and larger than the Grids. So far i have 
used QGIS, and performed the following:

- I made multiple requests for neighborhoods/villages/suburbs/... and received multiple layers
- I merged them into 1 point layer and saved them into the shapefile 'merged_neighborhood_points.shp'
- I used Voronoi Polygons to transform the Point Layer to a Polygon Layer and saved it into the shapefile 'final_voronoi_output.gpkg'
- I added the features 'x_centroid', 'y_centroid' (via QGIS) for every neighborhood in the previous shapefile
- I added the feature 'area_km2' (via QGIS) for every neighborhood in the previous shapefile
- I extracted the shapefile into a .csv file and cleaned it ('neighborhoods_cleaned.csv') so i have the new candidates
- I added extra features to the previous .csv (via '2. adding_extra_features.ipynb'), specifically: distance_to_volos_center_km, distance_to_volos_port_km,
  dist_to_main_road_km, dist_to_bus_stop_km, dist_to_university_km, and saved it to the file 'neighborhoods_enriched.csv'
- I added the English name of the Neighborhood in the previous file MANUALLY

I created the file "grids.csv" that contains information about all the grids that form Magnesia (their id, boundaries, centroid, geometry, ...) 

- i assigned each grid to its municipal community
- i added a column: 'distance_to_volos_center_km',the distance from the grid centroid to the center of Volos
- i added a column: 'distance_to_volos_port_km',the distance from the grid centroid to the port of Volos
- i extracted a .shp file ('main_roads_magnesia.shp') from OpenStreetMap via QGIS that contains the main highways of Magnesia
- i added a column 'dist_to_main_road_km', the distance from the grid centroid to the nearest highway (based on the shapefile above)
- i extracte a .gpkg file ('transport-stops-magnesia.gpkg') from OpenStreetMap via QGIS that contains the bus stops of Magnesia
- i added a column 'dist_to_bus_stop_km_', the distance from the grid centroid to the nearest bus station (based on the shapefile above)
- i extracted a .gpkg file ('university-magnesia.gpkg') from OpenStreetMap via QGIS that contains the universities of Magnesia
- i added a column 'dist_to_university_km', the distance from the grid centroid to the nearest university (based on the shapefile above)

Next: i want to:
- assign each business to its corresponding grid
- find rest of the grid features DYNAMICALLY based on the business entries


This folder contains the shapefiles for the layer of all the merged points that i got from QGIS ('merged_neighborhood_points,shp').
These are TRANSFORMED into a polygon shapefile, by applying Voronoi Polygons through the Python Script 'create_voronoi_polygons.y'.
Since it needs at least 3 points to work, I encountered  the following cases, regarding the number of points that belong to a Municipal Community:

- 3 or more: i successfully applied the Voronoi Polygons
- 2 points: i used perpendicular bisector of the line between those two points
- 1 point: i just used the municipal community as a neighborhood
- 0 points: i just used the municipal community as a neighborhood

After applying the Voronoi Polygons, i got the polygon shapefile 'final_voronoi_output.gpkg'
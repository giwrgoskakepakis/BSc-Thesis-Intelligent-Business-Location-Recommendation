import os
from qgis.core import *
from qgis.utils import iface
import processing
from PyQt5.QtCore import QVariant

# === CONFIGURATION ===
points_layer = QgsProject.instance().mapLayersByName('merged_neighborhood_points')[0]
comm_layer = QgsProject.instance().mapLayersByName('dimos_volou')[0]
point_name_field = 'name'  # <-- 🔁 Change this to match your point field name
final_output = 'C:/Users/Giorgos/Desktop/HMMY/10ο Εξάμηνο/Διπλωματική/5. Neighborhoods/Shapefiles/2. Neighborhood Polygons/final_voronoi_output.gpkg'

# Delete previous output if exists
if os.path.exists(final_output):
    os.remove(final_output)

clipped_layers = []

for comm_feat in comm_layer.getFeatures():
    comm_geom = comm_feat.geometry()
    if not comm_geom.isGeosValid():
        comm_geom = comm_geom.makeValid()

    comm_name = comm_feat['LAU_LABEL3']
    request = QgsFeatureRequest().setFilterRect(comm_geom.boundingBox())
    inside_points = list([f for f in points_layer.getFeatures(request) if comm_geom.contains(f.geometry())])
    point_count = len(inside_points)

    # === 1 POINT CASE ===
    if point_count == 1:
        print(f"ℹ️ {comm_name}: 1 point — using whole community polygon")
        point_name = inside_points[0][point_name_field]

        single_layer = QgsVectorLayer('Polygon?crs=EPSG:4326', f'{comm_name}_single', 'memory')
        dp = single_layer.dataProvider()
        dp.addAttributes([
            QgsField('community', QVariant.String),
            QgsField('point_id', QVariant.Int),
            QgsField('point_name', QVariant.String)
        ])
        single_layer.updateFields()

        f = QgsFeature()
        f.setGeometry(comm_geom)
        f.setAttributes([comm_name, inside_points[0].id(), point_name])
        dp.addFeature(f)
        single_layer.updateExtents()
        clipped_layers.append(single_layer)

    # === 2 POINT CASE ===
    elif point_count == 2:
        print(f"✂️ {comm_name}: 2 points — splitting polygon")
        p1 = inside_points[0].geometry().asPoint()
        p2 = inside_points[1].geometry().asPoint()

        mx, my = (p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2
        dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
        perp_dx, perp_dy = -dy, dx
        norm = (perp_dx**2 + perp_dy**2)**0.5
        if norm == 0:
            print(f"⚠️ Skipping {comm_name}: Cannot compute bisector")
            continue
        perp_dx /= norm
        perp_dy /= norm

        length = 0.05  # approx 5km in EPSG:4326
        p_start = QgsPointXY(mx - perp_dx * length, my - perp_dy * length)
        p_end = QgsPointXY(mx + perp_dx * length, my + perp_dy * length)

        bisector = QgsVectorLayer('LineString?crs=EPSG:4326', 'bisector', 'memory')
        bisector_dp = bisector.dataProvider()
        bisector_dp.addAttributes([QgsField('id', QVariant.Int)])
        bisector.updateFields()

        line_feat = QgsFeature()
        line_feat.setGeometry(QgsGeometry.fromPolylineXY([p_start, p_end]))
        line_feat.setAttributes([1])
        bisector_dp.addFeature(line_feat)

        poly_layer = QgsVectorLayer('Polygon?crs=EPSG:4326', 'poly', 'memory')
        poly_dp = poly_layer.dataProvider()
        poly_dp.addAttributes([QgsField('community', QVariant.String)])
        poly_layer.updateFields()

        poly_feat = QgsFeature()
        poly_feat.setGeometry(comm_geom)
        poly_feat.setAttributes([comm_name])
        poly_dp.addFeature(poly_feat)

        result = processing.run("native:splitwithlines", {
            'INPUT': poly_layer,
            'LINES': bisector,
            'OUTPUT': 'memory:split_result'
        })['OUTPUT']

        # Assign name to closest point
        result.startEditing()
        result.dataProvider().addAttributes([
            QgsField('method', QVariant.String),
            QgsField('point_name', QVariant.String),
            QgsField('community', QVariant.String)
        ])
        result.updateFields()

        p1_geom = inside_points[0].geometry()
        p2_geom = inside_points[1].geometry()
        name1 = inside_points[0][point_name_field]
        name2 = inside_points[1][point_name_field]

        for f in result.getFeatures():
            centroid = f.geometry().centroid()
            d1 = centroid.distance(p1_geom)
            d2 = centroid.distance(p2_geom)
            f['point_name'] = name1 if d1 < d2 else name2
            f['community'] = comm_name
            f['method'] = '2-point split'
            result.updateFeature(f)

        result.commitChanges()
        clipped_layers.append(result)

    # === ≥3 POINTS CASE ===
    elif point_count >= 3:
        print(f"✅ {comm_name}: Voronoi for {point_count} points")
        try:
            mem_points = QgsVectorLayer('Point?crs=EPSG:4326', 'temp_points', 'memory')
            prov = mem_points.dataProvider()
            prov.addAttributes(points_layer.fields())
            mem_points.updateFields()
            prov.addFeatures(inside_points)

            buffered_extent = comm_geom.buffer(0.05, 5).boundingBox()

            voronoi_result = processing.run("qgis:voronoipolygons", {
                'INPUT': mem_points,
                'BUFFER': 65,
                'EXTENT': buffered_extent,
                'OUTPUT': 'memory:voronoi_raw'
            })['OUTPUT']

            overlay_layer = QgsVectorLayer('Polygon?crs=EPSG:4326', 'overlay', 'memory')
            overlay_dp = overlay_layer.dataProvider()
            overlay_dp.addAttributes([QgsField('name', QVariant.String)])
            overlay_layer.updateFields()

            overlay_feat = QgsFeature()
            overlay_feat.setGeometry(comm_geom)
            overlay_feat.setAttributes([comm_name])
            overlay_dp.addFeature(overlay_feat)

            clip_result = processing.run("qgis:clip", {
                'INPUT': voronoi_result,
                'OVERLAY': overlay_layer,
                'OUTPUT': 'memory:clipped_voronoi'
            })['OUTPUT']

            clip_result.startEditing()
            clip_result.dataProvider().addAttributes([
                QgsField('community', QVariant.String),
                QgsField('point_name', QVariant.String)
            ])
            clip_result.updateFields()

            for f in clip_result.getFeatures():
                centroid = f.geometry().centroid()
                nearest_point = min(inside_points, key=lambda pt: centroid.distance(pt.geometry()))
                f['community'] = comm_name
                f['point_name'] = nearest_point[point_name_field]
                clip_result.updateFeature(f)

            clip_result.commitChanges()
            clipped_layers.append(clip_result)

        except Exception as e:
            print(f"❌ Error processing {comm_name}: {e}")

    else:
        print(f"➕ {comm_name}: No points — including whole community polygon")

        poly_layer = QgsVectorLayer('Polygon?crs=EPSG:4326', f'{comm_name}_empty', 'memory')
        dp = poly_layer.dataProvider()
        dp.addAttributes([
            QgsField('community', QVariant.String),
            QgsField('point_name', QVariant.String),
            QgsField('method', QVariant.String)
        ])
        poly_layer.updateFields()

        f = QgsFeature()
        f.setGeometry(comm_geom)
        f.setAttributes([comm_name, "N/A", "no points"])
        dp.addFeature(f)
        poly_layer.updateExtents()

        clipped_layers.append(poly_layer)


# === MERGE ALL RESULTS ===
if clipped_layers:
    processing.run("native:mergevectorlayers", {
        'LAYERS': clipped_layers,
        'CRS': comm_layer.crs(),
        'OUTPUT': final_output
    })
    print("🎉 Done! Final polygons saved to:", final_output)
else:
    print("⚠️ No output generated.")

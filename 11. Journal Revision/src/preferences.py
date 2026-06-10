import pandas as pd

features = pd.read_parquet('../data/neighborhood_features.parquet')

GEO = ['distance_to_volos_center_km', 'distance_to_volos_port_km',
       'dist_to_university_km', 'dist_to_bus_stop_km',
       'dist_to_main_road_km', 'Neighborhood_Area_km2']

thresholds = features[GEO].quantile([0.25, 0.5, 0.75])

PREFERENCE_TERMS = {
    'central':         ('distance_to_volos_center_km', '<', thresholds.loc[0.25, 'distance_to_volos_center_km']),
    'peripheral':      ('distance_to_volos_center_km', '>', thresholds.loc[0.75, 'distance_to_volos_center_km']),
    'coastal':         ('distance_to_volos_port_km',   '<', thresholds.loc[0.25, 'distance_to_volos_port_km']),
    'near_university': ('dist_to_university_km',        '<', thresholds.loc[0.25, 'dist_to_university_km']),
    'large_area':      ('Neighborhood_Area_km2',        '>', thresholds.loc[0.75, 'Neighborhood_Area_km2']),
}

def neighborhoods_satisfying(terms, feats=features):
    """Given preference terms (e.g. {'central','coastal'}), return the set of
    neighbourhoods satisfying ALL of them."""
    mask = pd.Series(True, index=feats.index)
    for term in terms:
        col, op, thr = PREFERENCE_TERMS[term]
        mask &= (feats[col] < thr) if op == '<' else (feats[col] > thr)
    return set(feats.index[mask])

if __name__ == '__main__':
    print(thresholds.T.round(2))
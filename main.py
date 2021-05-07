import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

# Local imports
import functions as fun
import constants as cons

def get_socio_economic_data(df, group_by_columns, aggr_dict=cons.variable_aggr):
    agglomerated_df = fun.agglomerate(df, aggr_dict, group_by_columns)
    
    return agglomerated_df
    
    
def group_geometries(gdf_in, gdf_source, name_identifier="poly_id"):
    '''
    Returns a modified version of gdf_source with an extra column assigning
    each admin polygon a group based on the gdf in
    
    Params:
        gdf_in: GeoDataFrame with the geometries to overlap with the gdf_source
        gdf_source: GeoDataFrame with the socio_economic_data per admin region
        name_identifier: String used to identify the column of names of polygons 
        in gdf_in. Defaults to "poly_id"
    '''
    
    gdf_source["group"] = np.nan
    
    if name_identifier not in gdf_in.columns:
        raise Exception(f"The given name identfier ({name_identifier}) not found in shapefile. Please input the correct one.")
    
    for polygon_name in gdf_in[name_identifier]:
        polygon = gdf_in[gdf_in[name_identifier] == polygon_name]["geometry"].values[0]
        if cons.method == 'overlaps':
            gdf_source["overlaps"] = gdf_source.geometry.overlaps(polygon)
        elif cons.method == 'intersects':
            gdf_source["overlaps"] = gdf_source.geometry.intersects(polygon)
        gdf_source["group"] = gdf_source.apply(lambda x: (polygon_name if x.overlaps else x.group), axis=1)
    
    # Prepare response. Drop rows witout assinged group and overlaps column
    gdf_source.drop(columns=["overlaps"], inplace=True)
    gdf_response = gdf_source.dropna(subset=["group"])
    
    return gdf_response
    
if __name__ == "__main__":
    
    shape_file_path = sys.argv[1]
    out_dir = sys.argv[2]
    shape_file_name = shape_file_path.split("/")[-1]
    
    print(f"Getting socio-economic variables for {shape_file_name}.")
    if len(sys.argv) > 3:
        name_identifier = sys.argv[3]
    else:
        name_identifier = "poly_id"
        print(f"\tNo name identfier was given. Using poly_id.")
    
    gdf_socio_econ = gpd.read_file(cons.source_shape_file)
    gdf_polygons = gpd.read_file(shape_file_path)
    
    # Get relevant admin geoemtries, grouped for variable aggregation
    print("Grouping...")
    gdf_grouped = group_geometries(gdf_polygons, gdf_socio_econ, name_identifier=name_identifier)
    num_groups = len(gdf_grouped["group"].unique())
    print(f"\tFound {num_groups} different polygons.")
    
    # Agglomerate based on scheme
    print("Agglomerating...")
    df_agglomerated = get_socio_economic_data(gdf_grouped, "group")
    df_agglomerated.rename(columns={"group": name_identifier}, inplace=True)
    
    gdf_agglomerated = gdf_polygons.merge(df_agglomerated, on=name_identifier, how='outer')
    
    # Saves
    print("Saving...")
    # Check if folder exists
    if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
            
    out_path = os.path.join(out_dir, f"socio_econ_{shape_file_name}")
    gdf_agglomerated.to_file(out_path)
    

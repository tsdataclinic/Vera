import geopandas as gpd
import pandas as pd 
from tqdm import tqdm 
import logging
from pathlib import Path
from shapely.geometry import Point
from dotenv import find_dotenv, load_dotenv
import numpy as np

CITIES = [
    'NewOrleans',
    'Dallas',
    'Detroit',
    'Seattle'
]

SUMMATION_VARS = ['B01003_001E','B03002_004E', 'B03002_012E', 'B03002_003E', 'B23025_002E','B25002_001E','B03002_006E','B25003_001E','B23025_004E' ]
WIEGHTED_VARS = ['B25058_001E', 'B19013_001E', 'B19083_001E', 'B25071_001E']

CENSUS_VARIABLES = {
     
}
INPUT_CRS = {
    'NewOrleans': 'EPSG:26982'
}

GEO_COLUMNS_REMAP= {
    'NewOrleans': { 'MapY': 'lat' , 'MapX' : 'lng' } ,
    'Dallas': {'X Coordinate' : 'lat', 'Y Cordinate' : 'lng'} ,
    'Detroit' : {'lat' : 'Latitude', 'lng':'Longitude'}
}

GEO_UNIT_CONVERSION={
    'NewOrleans' : 0.3048  #Feet to meters
}

def rename_positional_columns(city):
    print('Reanaming positional columns')
    return city.processed_data.rename(columns= city.GEO_COLUMNS_REMAP)

def assign_point_to_census_tract(city, chunk_size=10000):
    result = []
    tracts = city.tracts
    calls  = city.processed_data

    for index, chunk in tqdm(calls.groupby(np.arange(calls.shape[0])//chunk_size)):
        print(chunk.head())
        result.append( gpd.sjoin(chunk, tracts, how='left', op='within'))

    return pd.concat(result)

def assign_point_to_beat(city, chunk_size=10000):
    print('Joining to tracts')
    result = []
    beats = city.load_beats().to_crs('epsg:4326')
    calls  = city.processed_data
    for index, chunk in tqdm(calls.groupby(np.arange(calls.shape[0])//chunk_size)):
        result.append( gpd.sjoin(chunk, beats[[city.BEATS_IDS_GEOMETRY, 'geometry']], how='left', op='within'))
    return pd.concat(result)

def convert_geo_units(city):
    print('Converting Geo units')
    factor = city.GEO_UNIT_CONVERSION
    calls = city.processed_data
    return calls.assign(lat = calls.lat*factor, lng = calls.lng*factor)
    
def generate_points_city(city):
    print('Generating point geometries')
    crs = city.INPUT_CRS
    lat_lng_crs = "epsg:4326"
    calls = city.processed_data
    return gpd.GeoDataFrame(calls, 
                           geometry= calls.progress_apply(
                               lambda x: Point(x['lng'],x['lat'])
                           ,axis=1), 
                           crs=crs).to_crs(lat_lng_crs)
def process_city(city):
    print(city)
    tqdm.pandas()
    tracts = city.load_tracts()
    result = (city.pipe(rename_positional_columns, checkpoint='geo_positional')
                .pipe(convert_geo_units, checkpoint ='geo_convert_geo_coordinate')
                .pipe(generate_points_city, checkpoint= 'geo_generate_points' )
                .pipe(assign_point_to_census_tract, checkpoint= 'geo_assign_point_to_census')
    )
    return result

def area_weighted_overlap(beats,tracts,beat_id='beat'):
    # Calculate the intersection shapes between any beats and tracts that overlap
    beats =beats.copy().rename(columns={beat_id:'beat'})
    overlaps  = gpd.overlay(
                    tracts.to_crs('epsg:4326'), 
                    beats.to_crs('epsg:4326')
                )
    # Calculate the area of those overlapping regions
    overlaps = overlaps.assign(overlap_area = overlaps.to_crs('epsg:3366').area)
    # Join back to the census data and caclulate the area of the tracts
    
    overlaps = overlaps.merge(
        tracts.assign(tract_area = tracts.to_crs('epsg:3366').area)
        [['GEOID', 'tract_area']],
        on="GEOID",
        how='left'
    )
    
    # Calculate the fraction of each tract that overlaps with each beat
    # and the fraction of the population that likley represents
    
    overlaps = overlaps.assign(
        fraction_in_block = lambda x: x.overlap_area/x.tract_area,
        pop_fraction_in_block = lambda x: x['B01003_001E']*x.overlap_area/x.tract_area
    )
    
    # for non sumable variables we will multiply each by the population fraction of that 
    # census tract, sum then divide by the total interpolated population in the beat
    
    total_interpolated_pop_per_beat = (overlaps.groupby('beat')
                                               .sum()
                                               ['pop_fraction_in_block']
                                      )
    weighted_vars_result  = (overlaps[WIEGHTED_VARS]
                             .mul(overlaps.pop_fraction_in_block,axis=0)
                             .assign(beat = overlaps.beat)
                             .groupby('beat')
                             .sum()
                             .div(total_interpolated_pop_per_beat,axis=0)
                            )
    
    sumed_vars_result  = (overlaps[SUMMATION_VARS]
                          .mul(overlaps.fraction_in_block,axis=0)
                          .assign(beat=overlaps.beat)
                          .groupby('beat')
                          .sum()
                         )
    
    return (beats.set_index('beat')
                 .merge(weighted_vars_result, left_index=True,right_index=True)
                 .merge(sumed_vars_result, left_index=True,right_index=True)
           )

def area_weighted_sum_like():
    pass

def area_weighted_non_sum_like():
    pass
    
def process(city):
    if city.HAS_POINT_LOCATION_DATA:
        process_city(city)

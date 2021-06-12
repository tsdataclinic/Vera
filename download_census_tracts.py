import cenpy 

columns = {
    'total_pop':'B01003_001',
    "median_age": 'B01002_001',
    "white_pop": 'B03002_003',
    "black_pop": 'B03002_004E',
    "amerindian_pop": 'B03002_005',
    "asian_pop": 'B03002_006',
    "other_race_pop":'B03002_008',
    "hispanic_pop": 'B03002_012',
    'married_households':'B11001_003',
    'in_school':'B14001_002',
    'high_school_diploma':'B15003_017',
    'high_school_including_ged':'B07009_003',
    'poverty': 'B17001_002',
    'median_income':'B19013_001',
    'gini_index':'B19083_001',
    'housing_units': 'B25002_001',
    'vacant_housing_units':'B25002_003',
     'occupied_housing_units': 'B25003_001',
    'median_rent':'B25058_001',
    'percent_income_spent_on_rent':'B25071_001',
    'pop_in_labor_force':'B23025_002',
    'employed_pop':'B23025_004',
    'unemployed_pop':'B23025_005',
}

print("Downloading census tracts")
acs = cenpy.products.ACS(2017)

print('Downloading New Orleans')
new_orleans = acs.from_place('New Orleans, LA',variables=list(columns.values()),level='tract')
new_orleans.to_crs('epsg:4326').to_file("data/raw/NewOrleans/tracts.geojson")

print('Downloading South Carolina')
charleston = acs.from_state('South Carolina',variables=list(columns.values()),level='tract')
charleston.to_crs('epsg:4326').to_file("data/raw/Charleston/tracts.geojson")

print('Downloading Seattle')
seattle  = acs.from_place('Seattle, WA', variables=list(columns.values()),level='tract',place_type='Incorporated Place')
seattle.to_crs('epsg:4326').to_file('data/raw/Seattle/tracts.geojson')

print('Downloading Detroit')
detroit = acs.from_place('Detroit, MI',variables=list(columns.values()),level='tract',place_type='Incorporated Place')
detroit.to_crs('epsg:4326').to_file("data/raw/Detroit/tracts.geojson")

print('Downloading Dallas')
dallas = acs.from_place('Dallas, MI',variables=list(columns.values()),level='tract', place_type='Incorporated Place')
dallas.to_crs('epsg:4326').to_file("data/raw/Detroit/tracts.geojson")


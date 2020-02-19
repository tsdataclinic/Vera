from .city import City 

# base link: Raw Data: https://data.detroitmi.gov/Public-Safety/DPD-911-Calls-for-Service-September-20-2016-Presen/wgv9-drfc
# raw data : https://www.dallasopendata.com/api/views/qv6i-rri7/rows.csv?accessType=DOWNLOAD

class Detroit(City):
    
    BASE_NAME = 'Detroit'
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
#    DATE_FORMAT = '%m/%d/%Y %H:%M:%S %p'

    DATA_URLS = {
        'all': "https://opendata.arcgis.com/datasets/2dab2f70653f4bb8b4f2b51619ec8329_0.csv"
    }
    
    USE_YEARS = [2016,2017,2018]

    COLUMN_TYPES = {
        'intaketime' : str,
        'dispatchtime' : str,
        'traveltime':str,
        'totalresponsetime' :str, 
        'time_on_scene' :str,
        'totaltime':str, 
        'totaltime' : str
    }

    COLUMN_TRANSFORMS ={
        'call_timestamp' : 'date_time',
    }

    COLUMN_MAPPINGS = {
        'call_type' : 'calldescription',
        'self_initiated' : 'officerinitiated',
        'priority' : 'priority',
        'beat':'precinct_sca',
        'call_time' : 'call_timestamp',
        'response_time' :'totalresponsetime'
    }
    
    BEAT_FILES  = [
        {
            'start_year' : 2016,
            'end_year': 2019,
            'path': 'geo_export_1a1f09d7-b148-4df7-8cd1-671ea3fbd22b.shp'
        }
    ]
    BEATS_IDS_GEOMETRY='area'
    
    RESPONSE_TIME_FACTOR = 60
    RESPONSE_TIME_COLUMN = 'response_time'
#     INPUT_CRS =  {'init':'EPSG:26971'}

    GEO_COLUMNS_REMAP = { 'latitude': 'lat' , 'longitude' : 'lng' }
#     GEO_UNIT_CONVERSION =  0.3048  #Feet to meters

    def preprocess(self):
        print('using overloaded preprocess')
        beats = self.processed_data['beat']
        beats = beats.str.replace("[^0-9]", "").str.replace("^0","")
        self.processed_data['beat'] = beats

from .city import City 

# Raw events from here: https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy
# Precincts from here: https://data.seattle.gov/dataset/Seattle-Police-Beats-2018-Present/2nbq-tpk7
# Metadata form here: https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy

class Seattle(City):
    BASE_NAME = 'Seattle'
    META_DATA_LINKS ={
        'call_meta' : "https://data.seattle.gov/api/views/33kz-ixgy",
        'beats_meta' : "http://data-seattlecitygis.opendata.arcgis.com/datasets/36378b7acb8a464c8019b9618fecd0dd_2.geojson",
        'data_portal_url' : "https://data.seattle.gov/api/views/33kz-ixgy/rows.csv?accessType=DOWNLOAD"
    }
    
    BEATS_GEOM = {
            'http://data-seattlecitygis. eopendata.arcgis.com/datasets/36378b7acb8a464c8019b9618fecd0dd_2.geojson'
    }
    
    TRACTS = {
         
    }
    
    USE_YEARS = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    
    DATA_URLS = {
        'all': 'https://data.seattle.gov/api/views/33kz-ixgy/rows.csv?accessType=DOWNLOAD',
    }

    DATE_FORMAT = {
        'Original Time Queued' : '%m/%d/%Y %I:%M:%S %p',
        'Arrived Time' : '%m/%d/%Y %I:%M:%S %p'
    }

    COLUMN_TRANSFORMS = {
     'Original Time Queued' : 'date_time',
     'Arrived Time' : 'date_time'
    }
    
    COLUMN_MAPPINGS = {
        'call_type' : 'Initial Call Type',
        'self_initiated' : 'Call Type',
        'priority' : 'Priority',
        'disposition' : 'Event Clearance Description',
        'call_time' : 'Original Time Queued',
        'beat' : 'Beat'
    }
    
    START_TIME_COL ='Original Time Queued'
    END_TIME_COL   = 'Arrived Time'
    
    HAS_POINT_LOCATION_DATA = False
    
    ENFORCEMENT_VARIABLES= ['Report Generated', 'Warning Issued','Citation Issued','Arrest Issued'  ]
    
    def geo_preprocess(self):
        tracts = self.load_tracts()
        
#     TRACTS = [{'year_start': , 'year_end' , 'file':  
    BEATS_IDS_DATA  = 'beat'
    BEATS_IDS_GEOMETRY = 'beat' 
    
    BEAT_FILES  = [
        {
            'start_year' : 2018,
            'end_year': 2019,
            'path': 'Seattle_Police_Beats_2018Present.shp'
        },
        {
            'start_year' : 2015,
            'end_year': 2017,
            
            'path': 'Seattle_Police_Beats_20082015.shp'
        },
        {
            'start_year' : 2008,
            'end_year': 2014,
            'path': 'Seattle_Police_Beats_20082015.shp'
        }
    ]
    
    PROCESS_LAT_LNG  = False

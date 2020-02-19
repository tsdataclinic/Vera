from .city import City 

class NewOrleans(City):
    BASE_NAME = 'NewOrleans'
    DATE_FORMAT = '%m/%d/%Y %H:%M:%S %p'
    
    COLUMN_TRANSFORMS = {
        'TimeArrive' : 'date_time',
        'TimeCreate' : 'date_time',
        'TimeClosed' : 'date_time',
    }
    
    USE_YEARS = [2014,2015,2016,2017,2018]

    COLUMN_TYPES = {
     'BLOCK_ADDRESS' :str, 
     'Beat': str, 
     'Disposition' :str, 
     'DispositionText':str,
     'InitialPriority': str, 
     'InitialType' : str, 
     'InitialTypeText': str, 
     'Location': str, 
     'MapX': float,
     'MapY': float, 
     'NOPD_Item': str, 
     'PoliceDistrict': str, 
     'Priority': str, 
     'SelfInitiated': str,
     'TimeArrive':str, 
     'TimeClosed':str, 
     'TimeCreate':str, 
     'TimeDispatch':str, 
     'Type' :str,
     'TypeText':str, 
     'Zip':str, 
     'year':int   
    }
    
    BEATS_GEOM = 'https://opendata.arcgis.com/datasets/140759858aa14bb6a5a2fe099ccf4c07_0.zip?outSR=%7B%22latestWkid%22%3A3452%2C%22wkid%22%3A102682%7D&session=625905452.1554933501'

    COLUMN_RENAMES={
        'TimeArrival': 'TimeArrive',
        'Type_':'Type',
        
    }

    DATA_URLS = {
        2011: 'https://data.nola.gov/api/views/28ec-c8d6/rows.csv?accessType=DOWNLOAD',
        2012: 'https://data.nola.gov/api/views/rv3g-ypg7/rows.csv?accessType=DOWNLOAD',
        2013: 'https://data.nola.gov/api/views/5fn8-vtui/rows.csv?accessType=DOWNLOAD',
        2014: 'https://data.nola.gov/api/views/jsyu-nz5r/rows.csv?accessType=DOWNLOAD',
        2015: 'https://data.nola.gov/api/views/w68y-xmk6/rows.csv?accessType=DOWNLOAD',
        2016: 'https://data.nola.gov/api/views/wgrp-d3ma/rows.csv?accessType=DOWNLOAD',
        2017: 'https://data.nola.gov/api/views/bqmt-f3jk/rows.csv?accessType=DOWNLOAD',
        2018: 'https://data.nola.gov/api/views/9san-ivhk/rows.csv?accessType=DOWNLOAD',
        2019: 'https://data.nola.gov/api/views/qf6q-pp4b/rows.csv?accessType=DOWNLOAD'
    }


    ## New Orleans data is in state plane coordinates and in feet 
    # rather than meters, this should fix that
    
    INPUT_CRS =  {'init':'EPSG:26982'}

    GEO_COLUMNS_REMAP = { 'MapY': 'lat' , 'MapX' : 'lng' }
    GEO_UNIT_CONVERSION =  0.3048  #Feet to meters
  
    START_TIME_COL ='TimeCreate'
    END_TIME_COL   = 'TimeClosed'
    
    ENFORCEMENT_VARIABLES=['Enforcement Activity ']
    
    COLUMN_MAPPINGS = {
        'call_type' : 'InitialTypeText',
        'self_initiated' : 'SelfInitiated',
        'priority' : 'Priority',
        'disposition': 'DispositionText',
        'beat':'Beat',
        'call_time' : 'TimeCreate'
    }
    
    BEAT_FILES  = [
        {
            'start_year' : 2014,
            'end_year': 2019,
            'path': 'NOPD_Police_Zones.shp'
        }
    ]
    
    BEATS_IDS_GEOMETRY= 'Zone'

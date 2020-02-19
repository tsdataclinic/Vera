from .city import City 

class Dallas(City):
    # base link: https://www.dallasopendata.com/Public-Safety/Police-Incidents/qv6i-rri7 
    # raw data : https://www.dallasopendata.com/api/views/qv6i-rri7/rows.csv?accessType=DOWNLOAD

    BASE_NAME = 'Dallas'
    
    COLUMN_TRANSFORMS = {
        'Call Cleared Date Time' : 'date_time',
        'Call Received Date Time' : 'date_time',
    }
    
    USE_YEARS = [2014,2015,2016,2017,2018]

    DATA_URLS = {
        'all': "http://www.dallasopendata.com/api/views/qv6i-rri7/rows.csv?accessType=DOWNLOAD"
    }
    
    COLUMN_MAPPINGS = {
        'call_type' : 'Type of Incident',
        'self_initiated' : '',
        'priority' : 'priority',
        'beat':'Precinct/Scout Car Area',
        'call_time' : 'Call Received Date Time',
        'response_time' :'Total Response Time',
        'disposition': 'UCR Disposition',
        'beat' : 'Beat'
    }

    COLUMN_TYPES = {
        'Victim Zip Code':str,
        'Victim Business Phone' : str
    }
    
    END_TIME_COL = 'Call Cleared Date Time'
        
    INPUT_CRS =  {'init':'EPSG:32138'}
    
    
    ENFORCEMENT_VARIABLES=['Arrest Issued']

    GEO_COLUMNS_REMAP = { 'Y Cordinate': 'lat' , 'X Coordinate' : 'lng' }
    GEO_UNIT_CONVERSION =  0.3048  #Feet to meters

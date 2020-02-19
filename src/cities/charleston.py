from .city import City 

class Charleston(City):
    BASE_NAME = 'Charleston'

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'
    
    COLUMN_TRANSFORMS = {
        'Time_CallClosed' : 'date_time',
        'Response_Date' : 'date_time',
    }
    
    
    USE_YEARS = [2015,2016,2017]

    ENCODING = 'latin'

    BEAT_GEOMS = 'https://opendata.arcgis.com/datasets/590a70e0928f4bda8765dd6d41e27dfd_35.zip?session=625905452.1554933501'
    COLUMN_TYPES = {
        "X":                         "float64",
        "Y":                         "float64",
        "Master_Incident_Number":    "str",
        "Response_Date":             "str",
        "Problem":                   "str",
        "Address":                   "str",
        "City":                      "str",
        "State":                     "str",
        "Postal_Code":               "str",
        "Call_Disposition":          "str",
        "Time_CallClosed":           "str",
        "LONGITUDE":                 "float",
        "LATITUDE":                  "float",
        "FID":                       "str"
    }

    COLUMN_RENAMES={
    #     'TimeArrival': 'TimeArrive',
    #     'Type_':'Type'
    }
    
    COLUMN_MAPPINGS = {
        'call_type' : 'Problem',
        'self_initiated' : '',
        'disposition': 'Call_Disposition',
        'beat' : 'Beat',
        'call_time' : 'Response_Date'
    }
    
    END_TIME_COL = 'Time_CallClosed'
    ENFORCEMENT_VARIABLES=['Arrest Issued','Citation Issued','Enforcement Activity ']

    DATA_URLS = {
#         2019: 'http://www.charleston-sc.gov/DocumentCenter/View/21895',
#         2018: 'http://www.charleston-sc.gov/DocumentCenter/View/20413',
        2017: 'http://opendata.arcgis.com/datasets/f33a15885ff84b93a513d07beb7a4294_0.csv',
        2016: 'http://opendata.arcgis.com/datasets/97bcf160509948488f6dc2834d69d5d5_0.csv', 
        2015: 'http://opendata.arcgis.com/datasets/ef8464a73ae448f68d785e99cf9ec30b_0.csv'
    }
    GEO_COLUMNS_REMAP = { 'LATITUDE': 'lat' , 'LONGITUDE' : 'lng' }
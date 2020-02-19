import pandas as pd 
from pathlib import Path
from ..utils import INTERIM_DATA_DIR

CALL_MAPPING_FILE = INTERIM_DATA_DIR  / 'CallTypes_TS.xlsx'

def load_call_mappings():
    return (pd.read_excel(str(CALL_MAPPING_FILE), sheet_name ='CallTypes')
              .rename(columns={'Field 1':'in_category','Category':'out_category'}))

def load_self_initiated_mappings():
    return (pd.read_excel(str(CALL_MAPPING_FILE), sheet_name ='SelfInitiated')
              .rename(columns={'Field1':'in_category','Self initiated':'out_category'}))

def load_disposition_mappings():
    return (pd.read_excel(str(CALL_MAPPING_FILE), sheet_name ='Disposition')
              .rename(columns={'Field1':'in_category','Category':'out_category'}))

def assign_disposition(city):
    mappings = load_disposition_mappings()
    mappings = mappings[mappings['City'].str.replace(" ","") == city.BASE_NAME ]
    
    if(mappings.empty):
        return city.processed_data.assign(disposition='Unknown')
    
    m = mappings.set_index('in_category').to_dict()['out_category']
    disposition_column = 'disposition'
    mappings  = city.processed_data[disposition_column].apply(lambda x: m[x] if x in m else 'other')
    return city.processed_data.assign(disposition=mappings)
    
def assign_self_initiated(city):
    mappings = load_self_initiated_mappings()
    mappings = mappings[mappings['City'].str.replace(" ","") == city.BASE_NAME ]
    if(mappings.empty):
        return city.processed_data.assign(self_initiated='unknown')
    mappings = mappings.set_index('in_category').to_dict()['out_category']
    self_initiated_column = 'self_initiated'
    mappings  = city.processed_data[self_initiated_column].apply(lambda x:mappings[x] if x in mappings else 'other' )
    return city.processed_data.assign(self_initiated=mappings)
    
def assign_call_type_mapping(city):
    call_maps = load_call_mappings()
    print(call_maps.head())
    call_maps = call_maps[call_maps['City'].str.replace(" ","") == city.BASE_NAME ]
    call_maps= call_maps.set_index('in_category').to_dict()['out_category']
    
    call_type_column = 'call_type'
    standard_mappings  = city.processed_data[call_type_column].apply(lambda x:call_maps[x] if x in call_maps else 'other' )
    return city.processed_data.assign(call_type = standard_mappings  )

def process(city):
    result = (city.pipe(assign_call_type_mapping,checkpoint='assign_call_types')
                  .pipe(assign_self_initiated, checkpoint='assign_self_initiated')
                  .pipe(assign_disposition, checkpoint='assign_disposition'))
    return result

if __name__ == '__main__':
    print('Loading mappings')

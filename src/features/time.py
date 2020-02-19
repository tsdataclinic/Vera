import pandas as pd 

def calculate_response_time(city):
    print('Calculating processed time')
    calls = city.processed_data
    if(city.RESPONSE_TIME_COLUMN):
        factor = city.RESPONSE_TIME_FACTOR if city.RESPONSE_TIME_FACTOR else 1
        return calls.assign(response_time = calls[city.RESPONSE_TIME_COLUMN]*factor)
    else:
        return (calls
               .assign(response_time = (calls[city.END_TIME_COL] - calls.call_time).dt.seconds))

def assign_date_parts(city):
    print('assigning date parts')
    calls = city.processed_data
    start_time = calls.call_time
    
    return (city.processed_data
               .assign(hour = start_time.dt.hour,
                       day_of_week = start_time.dt.dayofweek,
                       month = start_time.dt.month,
                       year = start_time.dt.year
                      ))

def process_city(city):
    result  = (city.pipe(calculate_response_time, checkpoint='response_time')
                   .pipe(assign_date_parts, checkpoint='data_parts')
              )
    return result
    
def process(city):
    print('processing time')
    process_city(city)
    
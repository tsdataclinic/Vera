#import sys
#sys.path.append('/home/vera0519/vera_911')
import pandas as pd

import src.features.call_types as call_types
from src.cities.new_orleans import NewOrleans
from src.cities.seattle import Seattle
from src.cities.dallas import Dallas
from src.cities.detroit import Detroit
from src.cities.charleston import Charleston

new_orleans = NewOrleans()
dallas  = Dallas()
seattle = Seattle()
detroit = Detroit()
charleston = Charleston()

new_orleans.process_data()	
dallas.process_data()
detroit.process_data()
charleston.process_data()
seattle.process_data()


new_orleans.clean_data().to_csv('data/processed/NewOrleans/NewOrleans.csv', index=False)
dallas.clean_data().to_csv('data/processed/Dallas/Dallas.csv', index=False)
detroit.clean_data().to_csv('data/processed/Detroit/Detroit.csv', index=False)
charleston.clean_data().to_csv('data/processed/Charleston/Charleston.csv', index=False)
seattle.clean_data().to_csv('data/processed/Seattle/Seattle.csv', index=False)


new_orleans.assign_demographics().drop('geography',index=False).to_csv('data/processed/NewOrleans/NewOrleans_with_census.csv', index=False)
dallas.assign_demographics().drop('geography',index=False).to_csv('data/processed/Dallas/Dallas_with_census.csv', index=False)
detroit.assign_demographics().drop('geography',index=False).to_csv('data/processed/Detroit/Detroit_with_census.csv', index=False)
charleston.assign_demographics().drop('geography',index=False).to_csv('data/processed/Charleston/Charleston_with_census.csv', index=False)
seattle.assign_demographics().drop('geography',index=False).to_csv('data/processed/Seattle/Seattle_with_census.csv', index=False)


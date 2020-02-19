#import sys
#sys.path.append('/home/vera0519/vera_911')
import pandas as pd
import cenpy
from slugify import slugify

from pathlib import Path
import src.features.call_types as call_types
from src.cities.new_orleans import NewOrleans
from src.cities.seattle import Seattle
from src.cities.dallas import Dallas
from src.cities.detroit import Detroit
from src.cities.charleston import Charleston
import matplotlib.pyplot as plt
import src.features.geo as Geo
from src.features.call_types import load_call_mappings, assign_disposition, process
import src.visualization.visualize as vis

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

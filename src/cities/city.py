import pandas as pd
import geopandas as gpd
from ..utils import RAW_DATA_DIR, CLEAN_DATA_DIR
from pathlib import Path
import logging
from pathlib import Path
from ..features import geo as Geo, call_types as Calls, time as Time
from urllib.request import urlretrieve
import numpy as np

class City:
    
    # This base class should not be used by its self, instead subclass 
    # it for each city we are getting data from and override at least
    # the class variables in this section and optionally the functions here
    # to implement custom processing that needs to happen
    
    
    # Base name to use for the city in all file names etc 
    BASE_NAME = "CITY"
    
    # Columns in the downloaded dataset that should be renamed
    # Useful for when the different years have different column names 
    # that need to be standardised
    COLUMN_RENAMES = {}  
    
    # The URLS where we should fetch data form an example could be something like
    # {
    #   2015 : 'www.dataplace.com/911_data/2015.csv',
    #   2016 : 'www.dataplace.com/911_data/2015.csv',
    # }
    DATA_URLS = {}
    
    # The types of the columns in the dataset that are used to read the CSV in 
    # any columns not included in this dict will be guessed by pandas 
    # best to air on the side of specifying them
    COLUMN_TYPES = {}
    
    # Once loaded, what transforms should be applied to the columns 
    # curently we only have one type here which is to parse the datetime 
    # Will add category as a type as well 
    COLUMN_TRANSFORMS = {}
    
    # Basic data format for dates in the dataset
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    
    
    # What columns should map to the variables we need in the final dataset?
    # These should a mapping that gets us something like
    # {
    #   'year' : 2019,
    #   'month' : 1,
    #   'dayofweek' : 4,
    #   'call_type' : 'Shooting',
    #   'response_time' : 2003,
    #   'disposition' : 'Arrest',
    #   'self_initated' : True,
    #   'census_tract_id' : 30234234,
    #   'census_block_group_id' : 2340234,
    #   'beat' : 'sector_3/beat4'
    # }
    COLUMN_MAPINGS = {}
    
    ### GEOSPATIAL FILES 
    
    # What encoding is the file? By default assume utf-8
    ENCODING = 'utf-8'
    
    # Input CRS for the call data geometries assumed 4326 (lng lat)
    INPUT_CRS =  'EPSG:4324'
    
    # Columns if any to remap the inputs to lat lng
    GEO_COLUMNS_REMAP= {} 
    
    # If the geo units need to be converted from meters to feet etc,
    # do so here.
    GEO_UNIT_CONVERSION= 1
    
    # Start and end time columns 
    
    START_TIME_COL = None 
    END_TIME_COL = None
    RESPONSE_TIME_COLUMN = None
    
    # External geometry columms
    
    TRACTS = None 
    BEATS  = None 
    
    
    ENFORCEMENT_VARIABLES = []
    
    HAS_POINT_LOCATION_DATA = True
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
    
        self.data_loaded  = False
        self.processing_progress=[]
    
    def name(self):
        return self.BASE_NAME
    
    def load_raw_data(self, force_refresh=False):
        if type(self.raw_data) !=type(None) and force_refresh==False:
            return self.raw_data
        
        raw_data_path = RAW_DATA_DIR / self.BASE_NAME / "calls.feather"
        if(raw_data_path.exists()):
            print("Loading data from local cache")
            self.raw_data = pd.read_feather(str(raw_data_path))
            invert_dict = dict(zip( list(self.COLUMN_MAPPINGS.values()), list(self.COLUMN_MAPPINGS.keys())))
            print('Raw data invert dictionary ', invert_dict)
            self.raw_data = self.raw_data.rename(columns= invert_dict)
            self.data_loaded = True
            return self.raw_data
        else:
            print("Data not downloaded doing so now")
            self.download_all()
            self.consolidate_all()
            self.data_loaded = True
            return self.load_raw_data()
    
    def clean_data_path (self):
        return (CLEAN_DATA_DIR / "{}.feather".format(self.BASE_NAME))
        
    def load_cleaned_data(self,force_refresh=False):
        clean_file = self.clean_data_path()
        
        if( clean_file.exists() and force_refresh==False):
            self.processed_data = pd.read_feather(str(clean_file))
        else:
            self.process_data()
           
    def raw_data(self):
        if(type(self.raw_data) == type(None)):
            self.load_raw_data()
        return self.raw_data
    
    def clean_data(self, reload=False, years=None):
        if(type(self.processed_data) == type(None) or reload==True):
            self.load_cleaned_data()
        if(years):
            return self.processed_data[self.processed_data.year.isin(years)]
        else:
            return self.processed_data
    
    def raw_data_dir(self):
        return RAW_DATA_DIR / self.BASE_NAME
    
    def load_tracts(self):
        self.tracts = gpd.read_file(str(self.raw_data_dir() / 'tracts.geojson'))
        return self.tracts
    
    def create_raw_dir(self):
        city_dir = self.raw_data_dir()     
        city_dir.mkdir(parents=True, exist_ok=True)
        return city_dir
    
    def raw_output_file_path(self,year):
        return self.raw_data_dir() / 'calls_{}.csv'.format(year)
    
    def download_geoms(self, output_filepath):
        """ Download the geometry files for LA
        """
        logger = logging.getLogger(__name__)
        logger.info('No specific geoms for LA just now')
        #urlretrieve(seattle_data_url,output_filepath)
        logger.info('Done')
        
    def download_calls(self, output_filepath):
        """ Download the call data from the open data portal
        """
        logger = logging.getLogger(__name__)
        for year, url in self.DATA_URLS.items():
            logger.info('Downloading New Orleans calls data for year {} from {} '.format(year,url))
            download_path = self.raw_output_file_path(year)
            if(download_path.exists()):
                print("Already downloaded, skipping {}".format(download_path))
            else:
                print('Downloading {} calls data for year {} from {} '.format(self.BASE_NAME, year,url))

                urlretrieve(url, str(download_path))
        logger.info('Done')
        
    def download_all(self):
        """ Download all the files for New Orleans
        """
        project_dir = Path(__file__).resolve().parents[2]
        city_dir = project_dir / 'data' / 'raw' / self.BASE_NAME     

        city_dir.mkdir(parents=True, exist_ok=True)

        self.download_calls(city_dir)
        self.download_geoms(city_dir)
        
    def load_and_fix_types(self,file):
        print('loading file ',file)
        data = pd.read_csv(file, dtype= self.COLUMN_TYPES, encoding=self.ENCODING, error_bad_lines=False)
        print("HERE !!!! ")
        print(data.columns)
        data = data.rename(columns = self.COLUMN_RENAMES)
        for column, transform in self.COLUMN_TRANSFORMS.items():
            if(transform =='date_time'):
                if type(self.DATE_FORMAT) == str or column not in self.DATE_FORMAT.keys():
                    column_date_format = self.DATE_FORMAT
                else :
                    column_date_format = self.DATE_FORMAT[column]
                data[column] = pd.to_datetime(data[column], format=column_date_format)
        return data
    
    def consolidate_all(self):
        print('loading data and assigning column types')
        city_dir = self.raw_data_dir()
        all_data = []
        for year, url in self.DATA_URLS.items():
            file = self.raw_output_file_path(year)
            all_data.append( self.load_and_fix_types(str(file)))
        data = pd.concat(all_data)    
        data.reset_index().to_feather(city_dir / 'calls.feather')
            
            
    def write_clean_data(self):
        clean_data_path = self.clean_data_path()
        cols_to_save=[
            'disposition',
            'GEOID',
            'index',
            'hour',
            'year',
            'month',
            'self_initiated',
            'call_type',
            'response_time',
            'call_time',
            'day_of_week',
            'priority',
            'latitude',
            'longitude',
            'beat']
        
        if('GEOID' not in self.processed_data.columns):
            self.processed_data = self.processed_data.assign(GEOID=None)
            
        if('priority' not in self.processed_data.columns ):
            self.processed_data = self.processed_data.assign(priority=None)
            
        if('latitude' not in self.processed_data.columns ):
            self.processed_data = self.processed_data.assign(latitude=None)
            
        if('longitude' not in self.processed_data.columns ):
            self.processed_data = self.processed_data.assign(longitude=None)
            
        if('beat' not in self.processed_data.columns):
            self.processed_data = self.processed_data.assign(beat=None)
       
        subset = self.processed_data[cols_to_save]
        subset.to_feather(str(clean_data_path))

    def preprocess(self):
        print('No Preprocess script')
        pass
        
    def process_data(self):
        print('procesisng geo for ',self)
        Geo.process(self)
        Calls.process(self)
        Time.process(self)
        self.write_clean_data()
        
    def calc_demographics(self,df=None):
        return df.assign(
                        pc_black = lambda x: x['B03002_004']/x['B01003_001'] ,
                        pc_hispanic = lambda x: x['B03002_012']/x['B01003_001'] ,
                        pc_white = lambda x: x['B03002_003']/x['B01003_001'],
                        pc_asian = lambda x: x['B03002_006']/x['B01003_001'],
                        pc_occupied_homes = lambda x: x['B25003_001'] / x['B25002_001'],
#                         pc_highschool_dep = lambda x: x['B15003_017'],
                        pc_employed = lambda x: x['B23025_004']/x['B23025_002'],
                        median_rent = lambda x: x['B25058_001'],                                            
                        median_income = lambda x: x['B19013_001'], 
                        gini_index = lambda x: x['B19083_001'],
                        percent_income_spent_on_rent = lambda x: x['B25071_001']
                 )
        
    def assign_demographics(self,df=None):
        tracts = self.load_tracts()
        
        if(type(df)==type(None)):
            df = self.processed_data 
        return (df.reset_index()
                  .merge( tracts, left_on='GEOID', right_on='GEOID')
                  .pipe(self.calc_demographics)
               )
    
    def load_beats_as_df(self):
        raw_data_path = RAW_DATA_DIR / self.BASE_NAME 
        all_beats_years = []
        tracts = self.load_tracts()
        
        for file in self.BEAT_FILES:
            data = gpd.read_file(str(raw_data_path / file['path']))
            data = data[[self.BEATS_IDS_GEOMETRY,'geometry']]
            
            data = data.to_crs('epsg:4326')
            data = Geo.area_weighted_(data,tracts,beat_id=self.BEATS_IDS_GEOMETRY)
            for year in range(file['start_year'],file['end_year']):
                data = data.assign(year=year)
                all_beats_years.append(
                    data)
        all_beats_years = pd.concat(all_beats_years)

        return gpd.GeoDataFrame(all_beats_years,geometry='geometry',crs="epsg:4326")
    
    def assign_beats(self,df=None):
        if(type(df)==type(None)):
            df = self.processed_data
        
        beats_data=self.load_beats_as_df()
        res = df.merge(beats_data, left_on=['beat','year'],
                             right_on=['beat','year'])

        return gpd.GeoDataFrame(res, geometry='geometry', crs='epsg:4326')    
       
        
    def assign_geometry(self,df=None):

        tracks  = self.load_tracts()
        if(type(df) == type(None)):
            print('using the processed data ',df)
            df = self.processed_data
            
        return gpd.GeoDataFrame(
                    df.reset_index()
                      .set_index('GEOID')
                      .assign(geometry = self.load_tracts().set_index('GEOID').geometry), 
                    geometry='geometry', 
                    crs='epsg:4326'
                 )
    
    def norm_by(self,df,norm_by=None):
        norm_types = ['total','area','capita', None]
        if not norm_by in norm_types:
            raise("Normalization type needs to be one of {}".format(norm_types))
        
        columns = [col for col in df.columns if col not in ['geometry','GEOID']]
        if(norm_by==None):
            return df
        if(norm_by == 'capita'):
            df_copy = df.copy().reset_index().set_index("GEOID")
            pop = self.load_tracts().set_index("GEOID")['B01003_001E']
            df_copy[columns] = df_copy[columns].div(pop,axis=0).replace(np.inf,0)
            return df_copy.dropna()
        if(norm_by=='total'):
            df_copy = df.copy()
            df_copy[columns] = df_copy[columns].div(df[columns].sum(axis=1),axis=0)
            return df_copy
        if(norm_by=='area'):
            df_copy = df.copy()
            df_copy[columns] = df_copy[columns].div( gpd.GeoDataFrame(df,geometry='geometry', crs='epsg:4326').to_crs('epsg:3366').geometry.area, axis=0)
            return df_copy 
        
        
    def filter_calls_by(self, call_type=None, year=None):
        return (self.processed_data
                       .pipe(lambda x : x[x.call_type == call_type] if call_type else x)
                       .pipe(lambda x : x[x.year == year] if year else x[x.year.isin(self.USE_YEARS)] )
               )
        
    def call_types_by_tract(self, norm_by=None, call_type=None, year=None):
    
        return (self.filter_calls_by(call_type=call_type,year=year)
                       .groupby(['GEOID','call_type'])
                       .count()
                       .reset_index()
                       .pivot_table(index='GEOID', columns='call_type', values='index')
                       .fillna(0)
                       .pipe(self.assign_geometry)   
                       .pipe(self.norm_by, norm_by=norm_by)
               )
    
    def disposition_fraction_by_call_type(self, year=None):
        return (self.filter_calls_by(year=year)
            .groupby(['call_type','disposition'])
            .count()
            .reset_index()
            .pivot_table(index='call_type', columns='disposition', values='index')
            .fillna(0)
            .pipe(lambda x : x.div(x.sum(axis=1),axis=0)))
            

    def call_volume_by_tract(self,norm_by=None,year=None,call_type=None):
        if year != None:
            no_years =1 
        else:
            no_years = len(self.processed_data.year.dropna().unique())
            
        return (self.filter_calls_by(year=year, call_type=call_type)
                    .reset_index()
                    .groupby('GEOID')          
                    .count()
                    .div(no_years)
                    .fillna(0)
                    .pipe(self.assign_geometry)
                    .pipe(self.norm_by, norm_by=norm_by)
                    .rename(columns={'index': 'calls'})
                    [['calls','geometry']]
               )
        
       
    def self_initated_by_tract(self, call_type=None, norm_by=None, year=None):    
        return (self.filter_calls_by(call_type=call_type, year=year)
                       .reset_index()
                       .groupby(['GEOID','self_initiated'])
                       .count()
                       .reset_index()
                       .pivot_table(index='GEOID', columns='self_initiated', values='index')
                       .fillna(0)
                       .pipe(self.assign_geometry)
                       .pipe(self.norm_by, norm_by=norm_by)
               )
    
    def self_initiated_by_disposition(self,call_type=None, year=None):
        return (self.filter_calls_by(call_type=call_type, year=year)
                    .groupby(['self_initiated', 'disposition'])
                    .count()
                    .reset_index()
                    .pivot_table(index='disposition', columns='self_initiated', values='index')
                    .pipe(self.norm_by, norm_by='total')
               )
                
    def median_response_time_by_tract(self,call_type=None, year=None):
        return (self.filter_calls_by(call_type=call_type, year=year)
                    .reset_index()
                    .groupby('GEOID')
                    .median()
                    .div(60)
                    [['response_time']]
                    .pipe(self.assign_geometry)
               )
    
    def self_initated_by_call_type(year=None):
        types = self.filter_calls_by(year=year).self_initated.unique()
        include_other = ('other' in types)
        
        return (self.filter_calls_by(year=year).groupby(['self_initiated', 'call_type'])
            .count()
            .reset_index()
            .pivot_table(index='call_type', columns='self_initiated', values='index')
            .assign(total_calls = lambda x :  x.sum(axis=1) )
            .assign(fraction_yes = lambda x: 100*x.Yes/x.total_calls,
                    fraction_no = lambda x: 100*x.No/x.total_calls)
            .fillna(0))
    
    def disposition_by_tract(self, call_type=None, year=None,norm_by='area'):
         return (self.filter_calls_by(call_type=call_type, year=year)
                       .reset_index()
                       .groupby(['GEOID','disposition'])
                       .count()
                       .reset_index()
                       .pivot_table(index='GEOID', columns='disposition', values='index')
                       .fillna(0)
                       .pipe(self.assign_geometry)
                       .pipe(self.norm_by, norm_by='total')
               )
    
    def disposition_counts(self,year=None, call_type=None):
        return (self.filter_calls_by(year=year, call_type=call_type)
            .groupby('disposition')
            .count()
            ['index']
            .sort_values())
        

    def disposition_by_self_initated():
        pass
    
#     def load_beats(self):
#         self.beats = gpd.read_file(str(self.raw_data_dir() / 'beats.geojson'))
#         return self.beats
        
           
    def self_initated_by_call_type(self, year=None):
        return (self.filter_calls_by(year=year).groupby(['self_initiated', 'call_type'])
            .count()
            .reset_index()
            .rename(columns={'self_initiated': 'Self Initiated'})
            .pivot_table(index='call_type', columns='Self Initiated', values='index')
            .fillna(0)
            .drop('other',errors ='ignore')
            .pipe(lambda x: x.div(x.sum(axis=1),axis=0))
            .sort_values(by='Yes')
        )
        
    def assign_geometry(self,df=None):

        tracks  = self.load_tracts()
        if(type(df) == type(None)):
            print('using the processed data ',df)
            df = self.processed_data
            
        return gpd.GeoDataFrame(
                    df.reset_index()
                      .set_index('GEOID')
                      .assign(geometry = self.load_tracts().set_index('GEOID').geometry), 
                    geometry='geometry', 
                    crs='epsg:4326'
                 )
    
    def norm_by(self,df,norm_by=None):
        norm_types = ['total','area','capita', None]
        if not norm_by in norm_types:
            raise("Normalization type needs to be one of {}".format(norm_types))
        
        columns = [col for col in df.columns if col not in ['geometry','GEOID']]
        if(norm_by==None):
            return df
        if(norm_by == 'capita'):
            df_copy = df.copy().reset_index().set_index("GEOID")
            pop = self.load_tracts().set_index("GEOID")['B01003_001E']
            pop = pop[pop>2000]
            df_copy[columns] = df_copy[columns].div(pop,axis=0).replace(np.inf,0)
            return df_copy
        if(norm_by=='total'):
            df_copy = df.copy()
            df_copy[columns] = df_copy[columns].div(df[columns].sum(axis=1),axis=0)
            return df_copy
        if(norm_by=='area'):
            df_copy = df.copy()
            df_copy[columns] = df_copy[columns].div( gpd.GeoDataFrame(df,geometry='geometry', crs='epsg:4326').to_crs('epsg:3366').geometry.area, axis=0)
            return df_copy 
        
        
    def filter_calls_by(self, call_type=None, year=None):
        return (self.processed_data
                       .pipe(lambda x : x[x.call_type == call_type] if call_type else x)
                       .pipe(lambda x : x[x.year == year] if year else x )
               )
        
    def call_types_by_tract(self, norm_by=None, call_type=None, year=None):
    
        return (self.filter_calls_by(call_type=call_type,year=year)
                       .groupby(['GEOID','call_type'])
                       .count()
                       .reset_index()
                       .pivot_table(index='GEOID', columns='call_type', values='index')
                       .fillna(0)
                       .pipe(self.assign_geometry)   
                       .pipe(self.norm_by, norm_by=norm_by)
               )
    
    def disposition_fraction_by_call_type(self, year=None):
        return (self.filter_calls_by(year=year)
            .groupby(['call_type','disposition'])
            .count()
            .reset_index()
            .pivot_table(index='call_type', columns='disposition', values='index')
            .fillna(0)
            .pipe(lambda x : x.div(x.sum(axis=1),axis=0)))
            

    def call_volume_by_tract(self,norm_by=None,year=None,call_type=None):
        if year != None:
            no_years =1 
        else:
            no_years = len(self.processed_data.year.dropna().unique())
        print('norming by ', no_years)
            
        return (self.filter_calls_by(year=year, call_type=call_type)
                    .reset_index()
                    .groupby('GEOID')          
                    .count()
                    .div(no_years)
                    .fillna(0)
                    .pipe(self.assign_geometry)
                    .pipe(self.norm_by, norm_by=norm_by)
                    .rename(columns={'index': 'calls'})
                    [['calls','geometry']]
               )
        
       
    def self_initated_by_tract(self, call_type=None, norm_by=None, year=None):    
        return (self.filter_calls_by(call_type=call_type, year=year)
                       .reset_index()
                       .groupby(['GEOID','self_initiated'])
                       .count()
                       .reset_index()
                       .pivot_table(index='GEOID', columns='self_initiated', values='index')
                       .fillna(0)
                       .pipe(self.assign_geometry)
                       .pipe(self.norm_by, norm_by=norm_by)
               )
    
    def self_initiated_by_disposition(self,call_type=None, year=None):
        return (self.filter_calls_by(call_type=call_type, year=year)
                    .groupby(['self_initiated', 'disposition'])
                    .count()
                    .reset_index()
                    .pivot_table(index='disposition', columns='self_initiated', values='index')
                    .pipe(self.norm_by, norm_by='total')
               )
                
    def median_response_time_by_tract(self,call_type=None, year=None):
        return (self.filter_calls_by(call_type=call_type, year=year)
                    .reset_index()
                    .groupby('GEOID')
                    .median()
                    .div(60)
                    [['response_time']]
                    .pipe(self.assign_geometry)
               )
    
    def self_initated_by_call_type(year=None):
        types = self.filter_calls_by(year=year).self_initated.unique()
        include_other = ('other' in types)
        
        return (self.filter_calls_by(year=year).groupby(['self_initiated', 'call_type'])
            .count()
            .reset_index()
            .pivot_table(index='call_type', columns='self_initiated', values='index')
            .assign(total_calls = lambda x :  x.sum(axis=1) )
            .assign(fraction_yes = lambda x: 100*x.Yes/x.total_calls,
                    fraction_no = lambda x: 100*x.No/x.total_calls)
            .fillna(0))
    
    def disposition_by_tract(self, call_type=None, year=None,norm_by='area'):
         return (self.filter_calls_by(call_type=call_type, year=year)
                       .reset_index()
                       .groupby(['GEOID','disposition'])
                       .count()
                       .reset_index()
                       .pivot_table(index='GEOID', columns='disposition', values='index')
                       .fillna(0)
                       .pipe(self.assign_geometry)
                       .pipe(self.norm_by, norm_by='total')
               )
    
    def disposition_counts(self,year=None, call_type=None):
        return (self.filter_calls_by(year=year, call_type=call_type)
            .groupby('disposition')
            .count()
            ['index']
            .sort_values())
        

    def disposition_by_self_initated():
        pass
    
    def load_beats(self):
        self.beats = gpd.read_file(str(self.raw_data_dir() / 'beats.geojson'))
        return self.beats
        
    def assign_beats(self,df):
        if(type(df)==type(None)):
            df = self.processed_data 
           
        beats = self.load_beats()
        df.merge(beats, left_no='',right_on='')
           
    def self_initated_by_call_type(self, year=None):
        return (self.filter_calls_by(year=year).groupby(['self_initiated', 'call_type'])
            .count()
            .reset_index()
            .rename(columns={'self_initiated': 'Self Initiated'})
            .pivot_table(index='call_type', columns='Self Initiated', values='index')
            .fillna(0)
            .drop('other',errors ='ignore')
            .pipe(lambda x: x.div(x.sum(axis=1),axis=0))
            .sort_values(by='Yes')
        )
    
    def select_demographics(self,year=None,call_type=None):
        return (self.filter_calls_by(year=year, call_type=call_type)
                    .pipe(self.assign_demographics)
                    .assign(
                        pc_black = lambda x: x['B03002_004E']/x['B01003_001E'] ,
                        pc_hispanic = lambda x: x['B03002_012E']/x['B01003_001E'] ,
                        pc_white = lambda x: x['B03002_003E']/x['B01003_001E'],
                        pc_asian = lambda x: x['B03002_006E']/x['B01003_001E'],
                        pc_occupied_homes = lambda x: x['B25003_001E'] / x['B25002_001E'],
                        median_rent = lambda x: x['B25058_001E'],                                            
                        median_income = lambda x: x['B19013_001E'], 
                        gini_index = lambda x: x['B19083_001E'],
                        percent_income_spent_on_rent = lambda x: x['B25071_001E']
                 ))              
                                          
    def pipe(self,transform, **kwargs):
        if(self.data_loaded ):
            checkpoint  = kwargs.pop('checkpoint')

            if checkpoint and checkpoint in self.processing_progress:
                print('Using cached version of ', checkpoint)
                return self
            else: 
                self.processed_data = transform(self,**kwargs)
                self.processing_progress.append(checkpoint)
                return self
        else:
            self.load_raw_data() 
            self.processed_data = self.raw_data.copy()
            self.preprocess()
            return self.pipe(transform,**kwargs)

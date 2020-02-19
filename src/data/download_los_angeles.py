from urllib.request import urlretrieve
import os
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# Raw Data 2010: https://data.lacity.org/api/views/iy4q-t9vr/rows.csv?accessType=DOWNLOAD
# Raw Data 2011: https://data.lacity.org/api/views/4tmc-7r6g/rows.csv?accessType=DOWNLOAD
# Raw Data 2012: https://data.lacity.org/api/views/i7pm-cnmm/rows.csv?accessType=DOWNLOAD
# Raw Data 2013: https://data.lacity.org/api/views/urhh-yf63/rows.csv?accessType=DOWNLOAD
# Raw Data 2014: https://data.lacity.org/api/views/mgue-vbsx/rows.csv?accessType=DOWNLOAD
# Raw Data 2015: https://data.lacity.org/api/views/tss8-455b/rows.csv?accessType=DOWNLOAD
# Raw Data 2016: https://data.lacity.org/api/views/xwgr-xw5q/rows.csv?accessType=DOWNLOAD
# Raw Data 2017: https://data.lacity.org/api/views/ryvm-a59m/rows.csv?accessType=DOWNLOAD
# Raw Data 2018: https://data.lacity.org/api/views/r4ka-x5je/rows.csv?accessType=DOWNLOAD

BASE_NAME = 'LosAngeles'

DATA_URLS = {
    2010: "https://data.lacity.org/api/views/iy4q-t9vr/rows.csv?accessType=DOWNLOAD", 
    2011: "https://data.lacity.org/api/views/4tmc-7r6g/rows.csv?accessType=DOWNLOAD",
    2012: "https://data.lacity.org/api/views/i7pm-cnmm/rows.csv?accessType=DOWNLOAD",
    2013: "https://data.lacity.org/api/views/urhh-yf63/rows.csv?accessType=DOWNLOAD",
    2014: "https://data.lacity.org/api/views/mgue-vbsx/rows.csv?accessType=DOWNLOAD",
    2015: "https://data.lacity.org/api/views/tss8-455b/rows.csv?accessType=DOWNLOAD",
    2016: "https://data.lacity.org/api/views/xwgr-xw5q/rows.csv?accessType=DOWNLOAD",
    2017: "https://data.lacity.org/api/views/ryvm-a59m/rows.csv?accessType=DOWNLOAD",
    2018: "https://data.lacity.org/api/views/r4ka-x5je/rows.csv?accessType=DOWNLOAD"
}

def download_calls(output_filepath):
    """ Download the call data from the Los Angeles open data portal
    """
    logger = logging.getLogger(__name__)
    for year, url in DATA_URLS.items():
        logger.info('Downloading New Orleans calls data for year {} from {} '.format(year,url))
        download_path = output_filepath / output_filepath / 'calls_{}.csv'.format(year)
        if(download_path.exists()):
            print("Already downloaded, skipping {}".format(download_path))
        else:
            print('Downloading {} calls data for year {} from {} '.format(BASE_NAME, year,url))

            urlretrieve(url, str(download_path))
    logger.info('Done')
       
def download_geoms(output_filepath):
    """ Download the geometry files for LA
    """
    logger = logging.getLogger(__name__)
    logger.info('No specific geoms for LA just now')
    #urlretrieve(seattle_data_url,output_filepath)
    logger.info('Done')

def download_all():
    """ Download all the files for New Orleans
    """
    project_dir = Path(__file__).resolve().parents[2]
    city_dir = project_dir / 'data' / 'raw' / BASE_NAME     
    
    city_dir.mkdir(parents=True, exist_ok=True)
                                     
    download_calls(city_dir)
    download_geoms(city_dir)
                                    

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    
    # Download all data
    download_all()                              
                                     


from .city import City 

class LosAngeles(City):
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


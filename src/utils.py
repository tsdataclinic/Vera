import pandas as pd 
from pathlib import Path

PROJECT_DIR  =  Path(__file__).resolve().parents[1]
RAW_DATA_DIR =  PROJECT_DIR / 'data' / 'raw' 
INTERIM_DATA_DIR = PROJECT_DIR / 'data' / 'interim'
CLEAN_DATA_DIR = PROJECT_DIR  / 'data' / 'processed'
VIS_DIR  = PROJECT_DIR / 'reports'

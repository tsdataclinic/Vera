### 911 calls for service

In 2019 the Vera Institute of Justice (Vera) partnered with Two Sigma Data Clinic to produce a consolidated datasets of 911 data from 5 US cities. Each of these cities publish their the data on their respective open data portals however, the schema for each dataset, the units used for location and time, as well as the categories for each variable, vary wildly from city to city. This repo contains code that downloads, standardizes, and consolidates data from these different sources. Once standardized, we attached demographic information from the 2017 US Census American Community Survey (ACS) to provide additional context to each call.

In addition to the scripts used to standardize the data, we include code for descriptive statistics and visualizations of the data. See the end of the readme file for how to use this code.

To read about the process of creating this project, check out the blog series on Data Clinic's Medium page:

1. [Announcing a Consolidated Dataset of 911 Calls for Five US Cities (Part 1)](https://medium.com/dataclinic/announcing-a-consolidated-dataset-of-911-calls-for-five-us-cities-part-1-4320a1a31a88)
2. [Creating a consolidated taxonomy for 911 call data across different US Cities (Part 2)](https://medium.com/dataclinic/creating-a-consolidated-taxonomy-for-911-call-data-across-different-us-cities-part-2-9600cb09abfd)
3. Part 3 coming soon.

## The cities

The cities we have focused on for this project are:

1. New Orleans
2. Seattle
3. Dallas
4. Detroit
5. Charleston

These were selected because their 911 call data has the largest coverage of the variables of interest. The selection of specific variables (listed below) to focus on was driven by the research interests of Vera, as well as different questions we hoped to ask of the data. 

1. Call for Action (CFA) code (the reason for the call)
2. Disposition (the ultimate outcome of the call from an enforcement activity standpoint)
3. Response Time (how long it took to respond to each call)
4. Call Type (whether the call initiated from a 911 call, a police officer, or otherwise).

In addition to these variables, we attached the following socio-demographic variables from the 2017 ACS. These variables are assigned based on the tract in which the call was reported to originate in.

```
total_pop : B01003_001
median_age : B01002_001
white_pop : B03002_003
black_pop": B03002_004
amerindian_pop : B03002_005
asian_pop : B03002_006
other_race_pop : B03002_008
hispanic_pop : B03002_012
married_households : B11001_003
in_school : B14001_002
high_school_diploma : B15003_017
high_school_including_ged : B07009_003
poverty : B17001_002
median_income : B19013_001
gini_index : B19083_001
housing_units : B25002_001
vacant_housing_units : B25002_003
occupied_housing_units : B25003_001
median_rent : B25058_001
percent_income_spent_on_rent : B25071_001
pop_in_labor_force : B23025_002
employed_pop : B23025_004
unemployed_pop : B23025_005
```

## Acessing the data

The data can be downloaded directly from the following links. It comes in the following forms:

1. A csv of [all cities combined](https://dcvera.s3.amazonaws.com/all.zip) with demographic data attached.
2. A csv for each individual city with demographic data attached.
   - [New Orleans](https://dcvera.s3.amazonaws.com/NewOrleans_with_census.csv.zip)
   - [Dallas](https://dcvera.s3.amazonaws.com/Dallas_with_census.csv.zip)
   - [Detroit](https://dcvera.s3.amazonaws.com/Detroit_with_census.csv.zip)
   - [Charleston](https://dcvera.s3.amazonaws.com/Charleston_with_census.csv.zip)
   - [Seattle](https://dcvera.s3.amazonaws.com/Seattle_with_census.csv.zip)
3. A csv for each individual city with no demographic data.
   - [New Orleans](https://dcvera.s3.amazonaws.com/NewOrleans.csv.zip)
   - [Dallas](https://dcvera.s3.amazonaws.com/Dallas.csv.zip)
   - [Detroit](https://dcvera.s3.amazonaws.com/Detroit.csv.zip)
   - [Charleston](https://dcvera.s3.amazonaws.com/Charleston.csv.zip)
   - [Seattle](https://dcvera.s3.amazonaws.com/Seattle.csv.zip)

## Building the data

If you want to build the data from scratch, the easiest way is to use the docker container within this project. To do so run the following commands:

```bash
docker build -t vera .
docker run -it --rm -v $(pwd):/data /bin/bash
cd /data
python generate_dataset.py
```

This will download the datasets from the various open data portals, apply the standardization procedure, and output the results. Depending on your hardware / internet connection the process might take a few hours.

Once the script has run, you can find the data in data/processed. There should be one feather file and one csv file for each city.

## Analyzing the data

Once the data has been generated, you can use the included classes to easily summarize, visualize, and analyse the data. There is a class per city that can be accessed as follows:

```
from src.cities.new_orleans import NewOrleans

new_orleans  = NewOrleans()
data = new_orleans.clean_data()
```

In addition to simply accessing the data, you can use the following functions on each city to produce summaries of the data. For each function, if a variable such as year / call type is not used, the entire universe of that variable is used.

- disposition_by_tract(call_type, year, norm_by) : Make a summary of the call outcome (disposition) by census tract.
- self_initiated_by_call_type(year): Make a summary of the number of calls that are self initiated (officer initiated) vs not by the type of call

## Visualizing the data

A number of methods for visualizing the data can be found in the src.visualization module. Each of these takes a city object and some additional parameters as an argument and returns a matplotlib plot. For example:

```
from src.cities.new_orleans import NewOrleans
import src.visualization.visualize as vis

new_orleans = NewOrleans()
vis.plot_self_initiated_by_call_type(year=1995)
```

An easy way to do this is to start a jupyter lab session in the provided docker container:

```bash
docker build -t vera .
./start_notebook_docker.sh
```

then navigate to http://localhost:8888.

## Contributing to the project

If you find a bug in the data or the processing code, please feel free to open an issue on this repo describing the problem.

If you want to add a new city to the analysis, start by opening an issue on the repo declaring that you would like to do so, then take a look at how cities are specified by opening up one of the existing city config files in src/cities. This should give you an idea of the kinds of things that need to be specified for each city and how to override parts of processing pipeline where necessary.

If you would like to add a new feature to existing cities, take a look at the code in src/features.

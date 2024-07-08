# EgbertsTribometer
This repo contains work done by Liam Pond and Albert Kalayil on the oleic acid project in the Nanotribology Lab in 2024. Supervised by Drs. Philip Egberts and Vinay Saini. 

## Setup

Raw data will first need to be parsed with ```parse_tribometer.py```. All you need to do is set ```folder_path``` to the name of the subdirectory that contains your data. All files and subdirectories in ```folder_path``` will be parsed except directories listed in ```excluded_dirs```. Next, ```main.py``` will output .csv files and plot the results. <strong>Make sure that your directory contains folders called ```ParsedFiles```, ```FrictionCoefficientCSV```, and ```FrictionCoefficientGraphs```</strong>. This is where these files will be saved. 

## Common Errors

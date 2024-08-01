# EgbertsTribometer
This repo contains work done by Liam Pond and Albert Kalayil on the oleic acid project in the Nanotribology Lab in 2024. Supervised by Drs. Philip Egberts, Vinay Saini, and Kasimuthumaniyan Subramanian. 

## Setup
Note: The following commands are for Mac and Linux. Setup for Windows is slightly different.
1. Create a new project using your selected IDE (I use PyCharm). 
2. [Clone this repo.](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) Save it in the project directory you just created.
3. Change directories to the one you just created by typing ```cd <repodir>``` into the command line (replace <repodir> with the path to your directory).
4. Activate the venv by typing ```source bin/activate``` in Terminal.
5. Download required packages by typing ```pip install -e requirements.txt```.

Download relevant data [here](https://uofc.sharepoint.com/:f:/s/Nanotribology/EtoGu7vGsJZMtskWNr2DBOgBcGOyxEI-5rjUbJKRrB8v_g?e=wPcI27). If the link isn't working, email vinay.saini1@ucalgary.ca or pgsegber@ucalgary.ca.
Store data in the root directory of your project folder. The default name is ```Data```. If you wish to change it, remember to modify the name in ```parse_tribometer.py```.
Find information about the test procedure [here](https://uofc.sharepoint.com/:w:/s/Nanotribology/ESjDrQkJ6T5DqgAqq4mPkRIBXiINiYxcL5QqRma2VKqXUA?e=O2sIvo).

## Using the Scripts
Raw data will first need to be parsed with ```parse_tribometer.py```. Set ```folder_path``` to the name of the subdirectory that contains your data and verify that valid tests are correct by modifying ```entirely_valid_samples``` and the return statement of the ```test_validity``` function. All files and subdirectories in ```folder_path``` will be parsed except directories listed in ```excluded_dirs```. Next, ```main.py``` will output .csv files and plot the results. <strong>Make sure that your directory contains folders called ```ParsedFiles```, ```FrictionCoefficientCSV```, and ```FrictionCoefficientGraphs```</strong>. 

### Output Files by Directory
ParsedFiles/
* ```Master.csv```: Contains information about all parsed tests
* ```ValidMaster.csv```: Master, but only for tests specified as valid in the ```test_validity``` function in ```parse_tribometer.py```.

FrictionCoefficientCSV/
* ```FrictionCoefficientData.csv```: .csv that contains the average friction per cycle for each test. Average friction is calculated by averaging friction values in the <strong>middle 40%</strong> of both the outgoing and returning phase of each cycle.
* ```AverageFrictionCoefficientData.csv```: Same as above, but with per-cycle values further averaged to result in one number per test.

FrictionCoefficientGraphs/

Outdated — graphs are now generated in Origin using the .csv files above.

## Common Errors

<img width="854" alt="Screenshot 2024-07-08 at 12 42 23 PM" src="https://github.com/user-attachments/assets/4e05f2cd-009e-4b5c-9710-27af10dd2b07">

This means that a test parameter (in this case SampleNo) was unable to be read from the test filename. To fix this, modify either the regex code in ```parse_tribometer.py``` or your test's filename. If you're unfamiliar with regex expressions, ChatGPT is a good tool to build your own. For example, you can ask it to make regex that will return all numbers following the string 'SampleNo'. Remember that many test parameters are not recorded in the file itself and must be extracted from the filename. 

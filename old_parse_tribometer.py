import pandas as pd
import numpy as np
import os
import re

# Path that contains the folder with all the data
folder_path = 'ValidTribometerLogs'

# Parse all files?
parse_all = True
# If not, which test(s) should be analyzed?
parse_test_list = ['TribometerLogs/Sample 9 OA-1 - Feb 19/PAO4+OA-1_20N_20mms_test3_Feb19',
                   'TribometerLogs/Sample 9 OA-1 - Feb 19/PAO4+OA-1_20N_20mms_test4_Feb19',
                   'TribometerLogs/Sample 9 OA-1 - Feb 19/PAO4+OA-1_20N_100mms_test6_Feb19']


# Function to check if a test is valid
def sample_validity(testfile: pd.DataFrame):
    """
    Checks if the test is valid or not. Valid tests are defined manually.
    :param testfile: The output file of one test
    :return: True or False depending on test validity
    """

    sample_no = int(testfile['SampleNo'])
    oa_conc = int(testfile['OAConc'])
    test_no = int(testfile['TestNo'])

    # Test is also valid if SampleNo is 4 and OAConc is 0
    # Sample 6 is valid except tests 1, 2, 3
    # Sample 7 is valid except test 2
    entirely_valid_samples = [5, 8]
    return (sample_no == 4 and oa_conc == 0) or \
        (sample_no == 6 and test_no not in [1, 2, 3]) or \
        (sample_no == 7 and test_no not in [2]) or \
        (sample_no == 9 and test_no not in [2]) or \
        sample_no in entirely_valid_samples


# Create a list to collect information from all files to add to master later
full_list = []


# ------------
# FILE PARSING
# ------------

def parse_file(test_name: str):
    """
    Parses the information from one test. Returns a dictionary to be compiled into `master`
    :param test_name: A string containing the path to the file
    :return: A dictionary with the information associated with one test
    """

    # Get test parameter information from the filenames using regex

    # Define the regex patterns to look for
    patterns = {
        'OAConc': r'-(\d+)_',
        'Force': r'_(.*?)N',
        # Getting speed from the file header rather than the filename
        # 'Speed': r'_(\d+)mms',
        'SampleNo': r'Sample (\d+)',
        'TestNo': r'test(.*?)_',
        'Date': r'_([^_]*)$'
    }

    print("Processing file: ", test_name)

    # Create a dictionary with the information for one test to append to the master DataFrame
    test_row = {}

    # Use re.search to find each regex expression in the filename
    for key, pattern in patterns.items():
        match = re.search(pattern, test_name)

        # If there's no match, assume the filename is incorrect and assign None
        if match is None and key != 'OAConc':
            test_row[key] = None
        # If there is a match, add it to test_row
        elif match is not None:
            test_row[key] = match.group(1)
        # Filenames don't explicitly say 0% OA so if there is no match and the key is 'OAConc',
        # assume it's 0% OA
        else:
            test_row['OAConc'] = 0

    # Add validity (validation criteria defined at the beginning)
    test_row['Validity'] = sample_validity(test_row)

    # Add filename
    test_row['Filename'] = test_name

    # Add test parameters from the first line of the file
    params = pd.read_csv(test_name, nrows=1, delimiter='\t', header=None).iloc[0].tolist()
    # Maps desired variable name to index of the numerical value
    params_dict = dict(SampleRate=1, Speed=3, TrackLength=5, Cycles=7)

    for key in params_dict:
        test_row[key] = params[params_dict[key]]

    # Figure out the columns of the file
    file_headers = pd.read_csv(test_name, delimiter='\t', skiprows=1, nrows=1).columns.tolist()

    for header in file_headers:
        test_row[header] = pd.read_csv(test_name, delimiter='\t', skiprows=1)[header]

    # Add the information from the selected file to full_list
    full_list.append(test_row)

    return test_row


# parse_file('PAO4+OA-10_20N_100mms_test12_Feb6')


# Use os.walk to iterate through all subdirectories and files in folder_path
if parse_all:
    for root, dirs, files in os.walk(folder_path):

        # Exclude hidden files and directories (names starting with a dot)
        files = [f for f in files if not f.startswith('.')]
        dirs = [d for d in dirs if not d.startswith('.')]

        for file in files:
            # Get the full path of the file
            filename = os.path.join(root, file)

            parse_file(filename)

else:
    for parse_test in parse_test_list:
        parse_file(parse_test)

# Create a master dataframe with the following columns
master = pd.DataFrame(full_list,
                      columns=['OAConc', 'Force', 'SampleNo',
                               'TestNo', 'Date', 'Validity', 'Filename',
                               'SampleRate', 'Speed', 'TrackLength', 'Cycles',
                               'Fx', 'Fy', 'Fz', 'Tx', 'Ty',
                               'Tz', 'x-Position'])


def cycle_avg(test_name: str, split_cycle=True):
    """
    Find the average values for each semi-cycle (going there and back are considered separate)
    :param test_name: The test to be analyzed
    :param split_cycle: Set true if each cycle should be split into two phases (there and back)
    :return: A list containing the average values of the estimated friction coefficient for each semi-cycle
    """

    # -------------------------------
    # Find the indices of the extrema
    # -------------------------------

    print("Processing cycle_avg: ", test_name['Filename'])

    # TODO implement split_cycle

    pos_series = test_name['x-Position']
    endpoints_list = []
    # Counter so that only every other direction change is counted if split_cycle is True
    split_counter = True

    # Does the series start increasing or decreasing?
    if pos_series[0] <= pos_series[1]:
        old_dir = True
    elif pos_series[0] > pos_series[1]:
        old_dir = False

    # Do the values keep going in the same direction as before or different? (increasing or decreasing)
    for i in range(1, len(pos_series) - 1):
        if pos_series[i + 1] > pos_series[i]:
            current_dir = True
        elif pos_series[i + 1] < pos_series[i]:
            current_dir = False
        elif pos_series[i + 1] == pos_series[i]:
            current_dir = old_dir
        # If the direction changes, reset the old direction and add the index of the extrema to extrema_list
        if old_dir != current_dir:
            old_dir = current_dir
            if split_cycle:
                if split_counter:
                    endpoints_list.append(i)
                split_counter = not split_counter
            elif not split_cycle:
                endpoints_list.append(i)

    # -------------------------------------------------------------
    # Average estimated friction coefficient values between extrema
    # -------------------------------------------------------------

    avg_friction = []
    # Coefficient of friction is Fx / Fz — according to Brandon's thesis
    fric_series = test_name['Fx'] / test_name['Fz']

    # Note: Estimated friction coefficient values AT the extrema are being not considered

    for i in range(0, len(endpoints_list) - 1):
        local_avg = np.mean(fric_series[endpoints_list[i]:endpoints_list[i + 1]])
        avg_friction.append(local_avg)

    return avg_friction


# For each row in master, apply cycle_avg() to each row and create a new column 'Avg_Friction' with the results
master['Avg_Friction'] = master.apply(cycle_avg, axis=1)

# Select only valid tests
valid_master = master.loc[master['Validity']]

# Export files
master.to_csv('ParsedFiles/Master.csv', encoding='utf-8')
valid_master.to_csv('ParsedFiles/ValidMaster.csv', encoding='utf-8')

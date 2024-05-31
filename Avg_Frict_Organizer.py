import pandas as pd
from statistics import mean, stdev

"""
1. Remove test num and date -
2. Avg CoF for the tests with the same params
3. Calculate STDEV for the tests with the same params and add that to an adjacent column
4. Separate into oils df and grease df
5. Separate Oil df into 2 df
6. Separate Grease df into 3 df
7. Get 

"""

"""
samples = ['oils', 'greases'] # discriminators are PAO4 or not
OA_oil_discriminator = ['OA-0', 'OA-1', 'OA-10', 'OA-20']
OA_greases_discriminators = ['OA-2','TOCN'] # else then just C20A
force = ['10N', '20N']
speed = ['10mms', '20mms', '100mms']
num_dataframe = (len(samples)-1)*len(speed) + (len(speed)-1)*(len(samples)-1)

"""


#---------------------------------------------------------------------------------------------------------

def main():
    with open('AverageFrictionCoefficientData.csv', 'r') as opened_csv:
        csv_output(opened_csv)
        pass

def csv_output(csv_file:str):
    oil_set = set() # initialize local set <-- where unique oil name are to be stored
    grease_set = set() # initialize local set <-- where unique grease names are to be stored

    discriminators = {'oil discriminator':['OA-0', 'OA-1', 'OA-10', 'OA-20'], 'grease discriminator':['OA-2','TOCN']} # else then just C20A for grease discriminator
    parameters = {'force': ['10N', '20N'], 'speed':['10mms', '20mms', '100mms']}

    initial_average_cof = pd.read_csv(csv_file, header=None).transpose().rename(columns={0:'Name', 1:'CoF'}).dropna(how='any')
    # creates a dataframe without headers that reads the csv file, transposes it, renames the headers as Name and CoF, and drops all rows that contain NaN values

    initial_average_cof['Name'] = initial_average_cof['Name'].str.replace(r'mms.*', 'mms', regex=True)

    total_set = set(initial_average_cof['Name'])

    for name in total_set:
        if 'PAO' in name: # checks to see if PAO is in the name <-- indicator that it is an oil
            oil_set.add(name) # adds name and coefficent of friction as key value pairs to the oil_dict 
        else:
            grease_set.add(name) # adds name and coefficient of friction as key value pairs to the grease_dict

    total_dict = {'oil_set':list(oil_set), 'grease_set':list(grease_set)}
    processed_dataframes = avg_stdev_calc(total_dict, discriminators, parameters, initial_average_cof)

    #print(oil_set, '\n', len(oil_set), '\n\n', grease_set, '\n', len(grease_set))


    pass

def avg_stdev_calc(sample_dict:dict, discriminators:dict, parameters:dict, initial_dataframe:pd.DataFrame):
    """
    Params: 
    sample_dict = {'oil_set':oil_set, 'grease_set':grease_set} (each set containing unique names pertaining to the type of sample)
    discriminators = {'oil discriminator':['OA-0', 'OA-1', 'OA-10', 'OA-20'], 'grease discriminator':['OA-2','TOCN']} # else then just C20A for grease discriminator
    parameters = {'force': ['10N', '20N'], 'speed':['10mms', '20mms', '100mms']}
    initial dataframe: contains 2 columns: Name (containing all the sample names) and CoF (containing all the values for the CoF)
    
    returns: a dictionary of dataframes containing average value of the cof and the standard deviation of the sample to a dataframe
    Dataframes will be of the same speed

    1. Unique names in sample dict used for parsing through the initial data frame, 
    finding all with the unique name and averaging CoF and STDEV for unique name, and storing it into a new dataframe
    2. Take new dataframe and split into 4 dataframes that are 7 columned (name, 10N, STDEV 10, 10N % Reduction, 20N, STDEV 20, 20N % Reduction)

    """
    sample_types = ['Oils', 'Greases'] # 2 samples, 3 speeds therefore 6 dataframes outputted in dict
    sample_params_combinations = []
    for sample_type in sample_types:
        for spec_speed in parameters['speed'][1]:
            sample_params_combinations.append(f'{sample_type} {spec_speed}')
    dataframes_dict = {} # initializes output dictionary containing dataframes
    cof_list = []
    avg_cof_dict = {}

    

    for (key, value) in sample_dict.items(): # Iterates through key and values within a list
        for sample_name in range(len(value)):
            for _, column in initial_dataframe.iterrows(): # Iterates through the rows and columns of a dataframe
                name = column['Name'] # sets variable name to the name of the grease or oil
                cof = column['CoF'] # sets variable cof to the value of the coefficient of friction

                if name == value[sample_name]:
                    cof_list.append(cof)

            for speed in parameters['speed']:
                if speed in name:
                    for force in parameters['force']:
                        if force in name:
                            if key not in avg_cof_dict:
                                avg_cof_dict[key] = {}
                            if speed not in avg_cof_dict[key]:
                                avg_cof_dict[key][speed] = {}

                            avg_cof_dict[key][speed]['name'] = name
                            avg_cof_dict[key][speed][force].append(mean(cof_list))
                            avg_cof_dict[key][speed][f'STDEV {force}'].append(stdev(cof_list))
                            cof_list.clear()
    

    excel_worthy = pd.DataFrame(avg_cof_dict)
    print(excel_worthy)

if __name__ == "__main__":
    main()
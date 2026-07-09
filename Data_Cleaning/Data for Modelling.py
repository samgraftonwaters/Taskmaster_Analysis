import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, RobustScaler

input_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'
output_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'

data = pd.read_csv(input_path + 'Full Contestent Table.csv')
data = data.rename(columns = {'DQ' : 'Disqualifications'})

print(data.columns)

one_hot_encoder = OneHotEncoder()

def onehotcolumns(data_table, column_name : str):
    """
    Apply OHE method to a specific column of the data table

    Parameters:
    -----------
        data_table (DataFrame): contestent data table
        column_name (str): name of column to be apply OHE to
    
    Returns:
        Dataframe with OHE columns
    """
    data_ohe = one_hot_encoder.fit_transform(data_table[[column_name]]).toarray()
    column_names = one_hot_encoder.get_feature_names_out([column_name])
    ohe_data = pd.DataFrame(data=data_ohe, columns=column_names).astype(int)
    return(ohe_data)

teams = onehotcolumns(data_table = data, column_name = 'Team')

age_range = onehotcolumns(data_table = data, column_name = 'Age_Ranges')

gender = onehotcolumns(data_table = data, column_name = 'Gender')

seat = onehotcolumns(data_table = data, column_name = 'Seat')

concat_ohe_data = pd.concat([teams, age_range, gender, seat], axis=1)

data_merged = pd.concat([data, concat_ohe_data], axis = 1)

data_merged.to_csv(output_path + 'Full Contestent Table OHE.csv', sep = ',', index = False)


data_modelling_all = data_merged.drop(['Age_Ranges', 'Team', 'Gender', 'Seat', 
                                    'Episode Wins', 'Episode Losses', 'First_Air_Date'], axis = 1)

#'Team Score per Person', 'Team Score per Task',

print(data_modelling_all.columns)
#Removing first 4 as OHE, remving last 5 due to correlation analysis

data_modelling_all.to_csv(output_path + 'Full Contestent Table for Modelling.csv', sep = ',', index = False)

data_modelling = data_modelling_all.copy()

standard_scaling = StandardScaler()
robust_scaling = RobustScaler()

data_non_nums = data_modelling_all.select_dtypes(exclude=[float, int])


data_modelling = data_modelling[['Disqualifications', 'Episode Percentage Losses', 'Number of Tasks', 
            'Percent 1s Scored', 'Position', 'Score', 'Tie Break Losses', 
            'Tie Break Wins', 'Tie Breaks per series', 'Avg Score per Episodes', 
            'Avg Score per Tasks', 'Episode Percentage Wins', 'Number_Episodes', 
            'Number Team Tasks', 'Percent 5s Scored', 'Series Number', 
            'Team Score per Task', 'Team Score per Person']]

data_modelling.columns = data_modelling.columns.str.replace(' ', '_')

new_cols = data_modelling.columns

variables_scaled = robust_scaling.fit_transform(data_modelling)

variables_scaled = pd.DataFrame(variables_scaled, columns = new_cols)

data_modelling_scaled = pd.concat([data_non_nums, variables_scaled, concat_ohe_data], axis = 1)

print(variables_scaled.head())

data_modelling_scaled.to_csv(output_path + 'Full Contestent Table for Modelling Scaled.csv', sep = ',', index = False)
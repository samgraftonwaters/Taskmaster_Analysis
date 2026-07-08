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
                                   'Team Score per Person', 'Team Score per Task', 'Episode Wins',
                                   'Episode Losses', 'Series Number', 'First_Air_Date'], axis = 1)

print(data_modelling_all.columns)
#Removing first 4 as OHE, remving last 5 due to correlation analysis

data_modelling_all.to_csv(output_path + 'Full Contestent Table for Modelling.csv', sep = ',', index = False)

data_modelling = data_modelling_all.copy()

### Scaling Data
normal_variables = pd.read_csv(output_path + 'Normal Variable Comparison Table.csv')
normal_variables = normal_variables[~normal_variables['Normal Variable'].isin(['Episode Wins', 'Episode Losses', 'Team Score per Person', 'Team Score per Task'])]

non_normal_variables = pd.read_csv(output_path + 'Non-Normal Variable Comparison Table.csv')
non_normal_variables['Non Normal Variable'] = non_normal_variables['Non Normal Variable'].str.replace("Number Episodes", "Number_Episodes")
non_normal_variables = non_normal_variables[~non_normal_variables['Non Normal Variable'].isin(['Series Number', 'Seat Num'])]


standard_scaling = StandardScaler()
robust_scaling = RobustScaler()

normal_variables_scaled = standard_scaling.fit_transform(data_modelling_all[normal_variables['Normal Variable']])
non_normal_variables_scaled = robust_scaling.fit_transform(data_modelling_all[non_normal_variables['Non Normal Variable']])

normal_cols = normal_variables['Normal Variable']
non_normal_cols = non_normal_variables['Non Normal Variable']

normal_variables_scaled = pd.DataFrame(normal_variables_scaled, columns=normal_cols, 
                                       index=data_modelling_all.index)

non_normal_variables_scaled = pd.DataFrame(non_normal_variables_scaled, columns=non_normal_cols, 
                                           index=data_modelling_all.index)

data_non_nums = data_modelling_all.select_dtypes(exclude=[float, int])

data_modelling_all_scaled = pd.concat([data_non_nums, non_normal_variables_scaled, 
                         normal_variables_scaled, concat_ohe_data], axis = 1)

data_modelling_all_scaled.to_csv(output_path + 'Full Contestent Table for Modelling All Scaled.csv', sep = ',', index = False)

data_modelling = data_modelling[['Disqualifications', 'Episode Percentage Losses', 'Number of Tasks', 
                                 'Percent 1s Scored', 'Position', 'Score', 'Tie Break Losses', 
                                 'Tie Break Wins', 'Tie Breaks per series', 'Avg Score per Episodes', 
                                 'Avg Score per Tasks', 'Episode Percentage Wins', 'Number_Episodes', 
                                 'Number Team Tasks', 'Percent 5s Scored', 'Seat Number', 'Series Number', 
                                 'Team Score per Task', 'Team Score per Person']]

data_modelling.columns = data_modelling.columns.str.replace(' ', '_')

variables_scaled = robust_scaling.fit_transform(data_modelling)

data_non_nums = data_modelling.select_dtypes(exclude=[float, int])

data_modelling_scaled = pd.concat([data_non_nums, variables_scaled, concat_ohe_data], axis = 1)

data_modelling_scaled.to_csv(output_path + 'Full Contestent Table for Modelling Scaled.csv', sep = ',', index = False)
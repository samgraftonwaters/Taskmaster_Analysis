import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, RobustScaler

input_path = '../Data/'
output_path = '../Data/Script_Outputs/'

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

data_modelling_all = data_modelling_all[['Series', 'Name', 'Position', 'Score', 
                                         'Disqualifications', 'Episode Percentage Losses',
                                         'Number of Tasks', 'Percent 1s Scored', 'Tie Break Losses', 
            'Tie Break Wins', 'Tie Breaks per series', 'Avg Score per Episodes', 
            'Avg Score per Tasks', 'Episode Percentage Wins', 'Number_Episodes', 
            'Number Team Tasks', 'Percent 5s Scored', 'Series Number', 
            'Team Score per Task', 'Team Score per Person', 'Team_A', 'Team_B', 'Age_Ranges_20 - 29',
       'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59',
       'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male',
       'Gender_Non-Binary', 'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3',
       'Seat_Seat 4', 'Seat_Seat 5']]

data_modelling_all.columns = data_modelling_all.columns.str.replace(' ', '_').str.replace('_-_', '-')

print(data_modelling_all.columns)

data_modelling_all.to_csv(output_path + 'Full Contestent Table for Modelling.csv', sep = ',', index = False)

data_modelling = data_modelling_all.copy()

standard_scaling = StandardScaler()
robust_scaling = RobustScaler()

data_modelling_S21 = data_modelling[data_modelling['Series'] == 'S21'].reset_index(drop = True)
data_modelling = data_modelling[data_modelling['Series'] != 'S21'].reset_index(drop = True)

cols_to_model = ['Position', 'Score', 'Disqualifications', 'Episode_Percentage_Losses',
                'Number_of_Tasks', 'Percent_1s_Scored', 'Tie_Break_Losses', 
                'Tie_Break_Wins', 'Tie_Breaks_per_series', 'Avg_Score_per_Episodes', 
                'Avg_Score_per_Tasks', 'Episode_Percentage_Wins', 'Number_Episodes', 
                'Number_Team_Tasks', 'Percent_5s_Scored', 'Series_Number', 
                'Team_Score_per_Task', 'Team_Score_per_Person']

data_scaled_modelling = data_modelling[cols_to_model]#.select_dtypes(include=[float, int])

print(data_scaled_modelling.columns)

new_cols = data_scaled_modelling.columns

variables_scaled = robust_scaling.fit_transform(data_scaled_modelling)

variables_scaled = pd.DataFrame(variables_scaled, columns = new_cols)

data_modelling[cols_to_model] = variables_scaled

data_modelling_scaled = data_modelling.copy()

print(data_modelling_scaled.head())
print(data_modelling_scaled.tail())
print(data_modelling_scaled.columns)

#######################
#Series 21 only scaling

data_modelling_scaled_S21 = data_modelling_S21[cols_to_model]#.select_dtypes(include=[float, int])

new_cols_S21 = data_modelling_scaled_S21.columns

variables_scaled_S21 = robust_scaling.fit_transform(data_modelling_scaled_S21)

variables_scaled_S21 = pd.DataFrame(variables_scaled_S21, columns = new_cols_S21)

data_modelling_S21[cols_to_model] = variables_scaled_S21

print(data_modelling_S21)

data_modelling_scaled_S21 = data_modelling_S21.copy()


print(data_modelling_scaled_S21)

data_modelling_scaled = pd.concat([data_modelling_scaled, data_modelling_scaled_S21], 
                                  axis = 0).reset_index(drop = True)

print(data_modelling_scaled.head())
print(data_modelling_scaled.tail())
print(len(data_modelling_scaled))

data_modelling_scaled.to_csv(output_path + 'Full Contestent Table for Modelling Scaled.csv', sep = ',', index = False)
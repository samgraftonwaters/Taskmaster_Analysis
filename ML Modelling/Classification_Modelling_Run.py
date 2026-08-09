import pandas as pd
import Classification_Modelling as CM

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
scaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
unscaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')


model_columns_option_1 = ['Number_Episodes', 'Team_A', 'Team_B', 
           'Age_Ranges_20-29', 'Age_Ranges_30-39', 'Age_Ranges_40-49', 
           'Age_Ranges_50-59', 'Age_Ranges_60-69', 'Gender_Female', 'Gender_Male',
           'Seat_Seat_1', 'Seat_Seat_2', 'Seat_Seat_3', 'Seat_Seat_4', 'Seat_Seat_5']

model_columns_option_2 = ['Disqualifications',
       'Episode_Percentage_Losses', 'Number_of_Tasks', 'Percent_1s_Scored',
       'Tie_Break_Losses', 'Tie_Break_Wins', 'Tie_Breaks_per_series',
       'Avg_Score_per_Episodes', 'Avg_Score_per_Tasks',
       'Episode_Percentage_Wins', 'Number_Episodes', 'Number_Team_Tasks',
       'Percent_5s_Scored', 'Series_Number', 'Team_Score_per_Task',
       'Team_Score_per_Person', 'Team_A', 'Team_B', 'Age_Ranges_20-29',
       'Age_Ranges_30-39', 'Age_Ranges_40-49', 'Age_Ranges_50-59',
       'Age_Ranges_60-69', 'Gender_Female', 'Gender_Male',
       'Gender_Non-Binary', 'Seat_Seat_1', 'Seat_Seat_2', 'Seat_Seat_3',
       'Seat_Seat_4', 'Seat_Seat_5']

model_columns_option_3 = ['Disqualifications',
       'Episode_Percentage_Losses', 'Number_of_Tasks', 'Percent_1s_Scored',
       'Tie_Break_Losses', 'Tie_Break_Wins', 'Tie_Breaks_per_series',
       'Episode_Percentage_Wins', 'Number_Episodes', 'Number_Team_Tasks',
       'Percent_5s_Scored', 'Series_Number', 'Team_Score_per_Task',
       'Team_Score_per_Person', 'Team_A', 'Team_B', 'Age_Ranges_20-29',
       'Age_Ranges_30-39', 'Age_Ranges_40-49', 'Age_Ranges_50-59',
       'Age_Ranges_60-69', 'Gender_Female', 'Gender_Male',
       'Gender_Non-Binary', 'Seat_Seat_1', 'Seat_Seat_2', 'Seat_Seat_3',
       'Seat_Seat_4', 'Seat_Seat_5']



series_21_contestents = unscaled_data[scaled_data['Series'] == 'S21'].reset_index(drop = True)

data = unscaled_data[scaled_data['Series'] != 'S21']

feature_runs = ['run1', 'run2', 'run3']
model_columns = [model_columns_option_1, model_columns_option_2, model_columns_option_3]

series_21_contestents = data[data['Series'] == 'S21'].reset_index(drop = True)
series_21_contestents_names_series = series_21_contestents[name_series_cols]

series_21_contestents = series_21_contestents[model_columns]

print(series_21_contestents)

data = data[data['Series'] != 'S21']

data = data[model_columns + ["Position"]]

print(data.head())

data['Winner'] = CF.np.where(data['Position'] == 1, 1, 0)
data = data.drop('Position', axis = 1)

print(data.head())

model_data = data.copy()

print(model_data)

X = model_data.iloc[:,:-1]
y = model_data['Winner']

for (X_data, y_data) in zip(model_columns, y_columns):

    model_data = data[X_data]

    series_21_new_data = series_21_contestents[X_data]

    X = model_data
    y = y_data

    print(X)
    print(y)
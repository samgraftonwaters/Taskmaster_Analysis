
import pandas as pd
import Regression_Modelling as RM

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
scaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
unscaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

######

print(scaled_data.head())

model_columns_option_1 = ['Disqualifications',
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

model_columns_option_2 = ['Disqualifications',
       'Episode_Percentage_Losses', 'Number_of_Tasks', 'Percent_1s_Scored',
       'Tie_Break_Losses', 'Tie_Break_Wins', 'Tie_Breaks_per_series',
       'Episode_Percentage_Wins', 'Number_Episodes', 'Number_Team_Tasks',
       'Percent_5s_Scored', 'Series_Number', 'Team_Score_per_Task',
       'Team_Score_per_Person', 'Team_A', 'Team_B', 'Age_Ranges_20-29',
       'Age_Ranges_30-39', 'Age_Ranges_40-49', 'Age_Ranges_50-59',
       'Age_Ranges_60-69', 'Gender_Female', 'Gender_Male',
       'Gender_Non-Binary', 'Seat_Seat_1', 'Seat_Seat_2', 'Seat_Seat_3',
       'Seat_Seat_4', 'Seat_Seat_5']

model_columns_option_3 = ['Disqualifications', 'Position',
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

y_option_1 = data['Score']
y_option_2 = data['Avg_Score_per_Tasks']

feature_runs = ['run1', 'run2', 'run3', 'run4', 'run5']
model_columns = [model_columns_option_1, model_columns_option_2, model_columns_option_2, 
                 model_columns_option_3, model_columns_option_3]
y_columns = [y_option_1, y_option_1, y_option_2, y_option_1, y_option_2]
target_features = ["Avg_Score_per_Tasks",'Team_Score_per_Task', 'Team_Score_per_Task',
                   'Team_Score_per_Task', 'Team_Score_per_Task']
y_variable = ['Score', 'Score', 'Avg_Score_per_Tasks', 'Score', 'Avg_Score_per_Tasks']

for (X_data, y_data, feature_run, target_feature_feature, y_variable) in zip(model_columns, y_columns, feature_runs, target_features, y_variable):

    model_data = data[X_data]

    series_21_new_data = series_21_contestents[X_data]

    X = model_data
    y = y_data

    print(X)
    print(y)

    RM.regression_model_comparison_testing(X = X, y = y, file_path = file_path, feature_run = feature_run,
                                series_21_new_data = series_21_new_data, 
                                series_21_contestents = series_21_contestents,
                                target_feature_feature = target_feature_feature,
                                y_variable=y_variable)

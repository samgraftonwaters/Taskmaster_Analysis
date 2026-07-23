from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import pandas as pd

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
# 'Full Contestent Table for Modelling Scaled.csv'
print(data.head())

model_columns = ['Disqualifications',
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

series_21_contestents = data[data['Series'] == 'S21'].reset_index(drop = True)

series_21_contestents = series_21_contestents[model_columns]

data = data[data['Series'] != 'S21']

model_data = data[model_columns]

X = model_data
y = data['Score']

print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
print(len(X_train), len(X_test), len(y_train), len(y_test))

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

y_pred = linear_model.predict(X_test)

r2_value = r2_score(y_test, y_pred)

print("Model coefficient: \n", linear_model.coef_[0].round(2))
print("Model intercept: \n", linear_model.intercept_.round(2))


print(r2_value)


plt.scatter(y_pred, y_test, color="navy", label="Data")
plt.plot(y_pred, y_pred, color='red', linewidth=2.5)#, 
        #  label="Regression model:\nCount = {:.1f}{}Humidity + {:.1f}"\
        #          .format(linear_model.coef_[0], r"$\times$", 
        #              linear_model.intercept_))
# plt.title("Humidity Predicting Count")
# plt.xlabel("Standardised Humidity")
# plt.ylabel("Count")
plt.legend()
plt.show()

from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""
Model for:
    y = score per number of tasks
    X = GCA method
    X - remove score per number of tasks if y = total score
"""

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
# 'Full Contestent Table for Modelling Scaled.csv'
print(data.head())

model_columns = ['Disqualifications',
       'Episode_Percentage_Losses', 'Number_of_Tasks', 'Percent_1s_Scored',
       'Tie_Break_Losses', 'Tie_Break_Wins', 'Tie_Breaks_per_series',
    #    'Avg_Score_per_Episodes', 'Avg_Score_per_Tasks',
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

linear_model = LinearRegression()

cv_scores = cross_val_score(estimator=linear_model, X=X, y=y, cv=5, scoring="r2")

print(cv_scores)
print(cv_scores.mean())

linear_model.fit(X_train, y_train)

y_pred = linear_model.predict(X_test)

r2_value = r2_score(y_test, y_pred)

print(r2_value)

print("Model coefficient: \n", linear_model.coef_[0].round(2))
print("Model intercept: \n", linear_model.intercept_.round(2))

for i, col in enumerate(model_columns):
    print(f"{col} coefficient:", linear_model.coef_[i].round(2))


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


y_pred = cross_val_predict(estimator=linear_model, X=X, y=y, cv=5)

# We can then compare our predicted and true values using a plot.
fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(y, y_pred, edgecolors=(0, 0, 0), alpha=0.4)
ax.plot([0, y.max()], [0, y.max()], 'k--', lw=4)
ax.set_xlabel('Measured Count')
ax.set_ylabel('Predicted Count')
ax.set_title(r"True and Predicted $y_i$")
plt.show()


residual = y - y_pred

standard_residual = residual / residual.std()


def plot_residuals(residual_data, standardised = True):

    if standardised == True:

        standard_residual = residual_data / residual.std()

        res_mean = standard_residual.mean()
        res_median = np.median(standard_residual)

        print(f"Standared Residual Mean: {res_mean} \n Standard Residual Median: {res_median}")

        title = "Standardised Residual Distribution Plot of the Linear Model"

    else:
        res_mean = residual_data.mean()
        res_median = np.median(residual_data)

        print(f"esidual Mean: {res_mean} \n Residual Median: {res_median}")

        title = "Residual Distribution Plot of the Linear Model"

    plt.axvline(x=res_mean, label=f"mean: {res_mean.round(2)}", color="red", lw = 4)
    plt.axvline(x=res_median, label=f"median: {res_median.round(2)}", color = 'black', lw = 4)
    plt.hist(residual_data, bins=25, color="dodgerblue", alpha = 0.6)

    plt.title(title, fontsize = 20)
    plt.xlabel("Residual", fontsize = 16)
    plt.ylabel("Count", fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend(fontsize = 14)
    plt.show()


plot_residuals(residual_data = standard_residual, standardised = True)

plot_residuals(residual_data = residual, standardised = False)
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
scaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
unscaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')
# 'Full Contestent Table for Modelling Scaled.csv'
print(scaled_data .head())

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

series_21_contestents = unscaled_data[scaled_data['Series'] == 'S21'].reset_index(drop = True)

series_21_contestents = series_21_contestents[model_columns]

data = unscaled_data[scaled_data['Series'] != 'S21']

model_data = data[model_columns]

X = model_data
y = data['Score']

print(X)
print(y)

#####
#SINGLE MODEL (TEST)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

scaler = RobustScaler().set_output(transform="pandas")

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

y_pred = linear_model.predict(X_test)

cv_scores_r2 = cross_val_score(estimator=linear_model, X=X, y=y, cv=5, scoring="r2")
cv_scores_mae = cross_val_score(estimator=linear_model, X=X, y=y, cv=5, scoring="neg_mean_absolute_error")

print()
print("Cross Val R2 Scores:", cv_scores_r2)
print("Cross Val R2 Mean Score:", cv_scores_r2.mean())

print("Cross Val MAD Scores:", cv_scores_mae*-1)
print("Cross Val MAD Mean Score:", cv_scores_mae.mean()*-1)
r2_value = r2_score(y_test, y_pred)
mae_value = mean_absolute_error(y_test, y_pred)
MSE_value = mean_squared_error(y_test, y_pred)
RMSE_value = root_mean_squared_error(y_test, y_pred)
print()
print("Model R2 Score:", r2_value)
print("Model MAE Score:", mae_value)
print("Model MSE Score:", MSE_value)
print("Model RMSE Score:", RMSE_value)
print()

def model_coefficients(model_columns, model, x_cols, show_plot = True):

    print("Model intercept:", model.intercept_.round(3))
    for i, col in enumerate(model_columns):
        print(f"{i}. {col} coefficient:", model.coef_[i].round(3))

    if show_plot == True:
        coef = pd.Series(model.coef_, index=x_cols.columns)

        coef.sort_values().plot.barh(figsize=(8,6))
        plt.xlabel("Coefficient")
        plt.title("Feature Importance")
        plt.show()

model_coefficients(model_columns = model_columns, model = linear_model, x_cols = X_train, 
                   show_plot = True)

# coef = pd.Series(
#     model.named_steps["model"].coef_,
#     index=X_train.columns
# )


plt.scatter(y_pred, y_test, color="dodgerblue", label="Data")
# plt.plot(y_test, y_test, color='red', linewidth=3, label = 'Actual Score Line')
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]

plt.plot(lims, lims, color='red', linewidth=3, label = 'Actual Score Line')
plt.title("Predicted vs Actual (Standardised) Scores", fontsize = 20)
plt.xlabel("Predicted Score", fontsize = 16)
plt.ylabel("Actual Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 14)
# plt.xlim(-3, 2)
# plt.ylim(-3, 2)
plt.show()


# Feature to plot
feature = "Avg_Score_per_Tasks"

print(X_train)

x = np.linspace(X_train[feature].min(), X_train[feature].max(), 100)

# Create a DataFrame where every feature is fixed at its mean
X_plot = pd.DataFrame(np.tile(X_train.mean().values, (len(x), 1)), columns=X_train.columns)

X_plot[feature] = x

y_plot = linear_model.predict(X_plot)

plt.figure(figsize=(8,6))
plt.scatter(X_train[feature], y_train, color="dodgerblue", alpha=0.7, label="Data")
plt.plot(x, y_plot, color="red", linewidth=3,  label="Regression Line")
plt.title(f"{feature} Predicting Target")
plt.xlabel(feature)
plt.ylabel("Target")
plt.legend()
plt.show()

features = [
    "Avg_Score_per_Tasks",
    "Number_of_Tasks",
    "Team_Score_per_Person"
]

fig, ax = plt.subplots(figsize=(8, 6))
PartialDependenceDisplay.from_estimator(linear_model, X_test, features=features, ax = ax)

plt.show()

fig, ax = plt.subplots(figsize=(7, 6))

PartialDependenceDisplay.from_estimator(
    estimator=linear_model,
    X=X_test,
    features=[("Avg_Score_per_Tasks", "Number_of_Tasks")],
    ax = ax
)

plt.show()



y_pred_cv = cross_val_predict(estimator=linear_model, X=X, y=y, cv=5)

fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(y, y_pred_cv, edgecolors=(0, 0, 0), alpha=0.4)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured Count')
ax.set_ylabel('Predicted Count')
ax.set_title(r"True and Predicted $y_i$")
plt.show()

fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(y_test, y_pred, edgecolors=(0, 0, 0), alpha=0.4)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured Count')
ax.set_ylabel('Predicted Count')
ax.set_title(r"True and Predicted $y_i$")
plt.show()

def plot_residuals(residual_data, standardised = True):

    if standardised == True:

        standard_residual = residual_data / residual.std()

        res_mean = standard_residual.mean()
        res_median = np.median(standard_residual)

        print(f"Standard Residual Mean: {res_mean:.3f}\nStandard Residual Median: {res_median:.3f}")

        title = "Standardised Residual Distribution Plot of the Linear Model"

    else:
        res_mean = residual_data.mean()
        res_median = np.median(residual_data)

        print(f"Residual Mean: {res_mean:.3f}\nResidual Median: {res_median:.3f}")

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

residual = y_test - y_pred

standard_residual = residual / residual.std()

plot_residuals(residual_data = standard_residual, standardised = True)

plot_residuals(residual_data = residual, standardised = False)

plt.axhline(0, color="black", linestyle="--", lw = 4)
plt.scatter(y_pred, standard_residual, color="dodgerblue")
plt.title("Residual Plot of Predicted Values", fontsize = 20)
plt.xlabel("Predicted Value", fontsize = 16)
plt.ylabel("Residual", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

residual = y - y_pred_cv

standard_residual = residual / residual.std()

plot_residuals(residual_data = standard_residual, standardised = True)

plot_residuals(residual_data = residual, standardised = False)

plt.axhline(0, color="black", linestyle="--", lw = 4)
plt.scatter(y_pred_cv, standard_residual, color="dodgerblue")
plt.title("Residual Plot of Predicted Values", fontsize = 20)
plt.xlabel("Predicted Value", fontsize = 16)
plt.ylabel("Residual", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()


sm.qqplot(residual, line='45', fit=True)

plt.title("Q-Q Plot of Residuals")
plt.show()

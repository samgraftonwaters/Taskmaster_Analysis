from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

from Function_Scripts import Regression_Functions as RF

import warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.exceptions import FitFailedWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FitFailedWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
scaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
unscaled_data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

print(scaled_data.head())

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

print(len(series_21_contestents))

data = unscaled_data[scaled_data['Series'] != 'S21']

model_data = data[model_columns]

X = model_data
y = data['Score']

print(X)
print(y)

#####
#SINGLE MODEL (TEST)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# scaler = RobustScaler().set_output(transform="pandas")

# X_train_single = scaler.fit_transform(X_train)
# X_test_single = scaler.transform(X_test)

# linear_model = LinearRegression()

# linear_model.fit(X_train_single, y_train)

# y_pred = linear_model.predict(X_test_single)

# cv_scores_r2 = cross_val_score(estimator=linear_model, X=X, y=y, cv=5, scoring="r2")
# cv_scores_mae = cross_val_score(estimator=linear_model, X=X, y=y, cv=5, scoring="neg_mean_absolute_error")

# print()
# print("Cross Val R2 Scores:", cv_scores_r2)
# print("Cross Val R2 Mean Score:", cv_scores_r2.mean())

# print("Cross Val MAD Scores:", cv_scores_mae*-1)
# print("Cross Val MAD Mean Score:", cv_scores_mae.mean()*-1)




######
#Model Comparison
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

models = {
    "Linear Regression": Pipeline([
        ("scaler", RobustScaler()),
        ("model", LinearRegression())
    ]),

    "Ridge": Pipeline([
        ("scaler", RobustScaler()),
        ("model", Ridge())
    ]),

    "Lasso": Pipeline([
        ("scaler", RobustScaler()),
        ("model", Lasso())
    ]),

    "Elastic Net": Pipeline([
        ("scaler", RobustScaler()),
        ("model", ElasticNet())
    ]),

    # "Polynomial Ridge": Pipeline([ #Best option, but testing the rest
    #     ("poly", PolynomialFeatures(include_bias=False)),
    #     ("model", Ridge())
    # ]),

    # "Polynomial Lasso": Pipeline([
    # ("poly", PolynomialFeatures(include_bias=False)),
    # ("model", Lasso())
    # ]),

    # "Polynomial Elastic Net": Pipeline([
    # ("poly", PolynomialFeatures(include_bias=False)),
    # ("model", ElasticNet())
    # ]),

    "Decision Tree": DecisionTreeRegressor(random_state=42),

    "Random Forest": RandomForestRegressor(random_state=42)
}

param_grids = {

    "Linear Regression": {
        "model__fit_intercept": [True, False],
        "model__positive": [True, False]
    },

    "Ridge": {
        "model__alpha": np.logspace(-3, 3, 20),
        "model__solver": ["auto", "svd", "cholesky", "lsqr", "sag", "saga"],
        "model__max_iter": [10000, 20000, 50000],
        "model__tol": [1e-3, 1e-4, 1e-5],
        "model__fit_intercept": [True, False]
    },

    "Lasso": {
        "model__alpha": np.logspace(-3, 3, 20),
        "model__max_iter": [10000, 20000, 50000],
        "model__tol": [1e-3, 1e-4, 1e-5],
        "model__fit_intercept": [True, False],
        "model__selection": ["cyclic", "random"]
    },

    "Elastic Net": {
        "model__alpha": np.logspace(-3, 3, 20),
        "model__l1_ratio": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        "model__fit_intercept": [True, False],
        "model__max_iter": [5000, 10000, 20000, 50000],
        "model__tol": [1e-3, 1e-4],
        "model__selection": ["cyclic", "random"]
    },

    # "Polynomial Ridge": {
    #     "poly__degree": [2, 3],
    #     "model__alpha": np.logspace(-3, 3, 20),
    #     "model__solver": ["auto", "svd", "cholesky", "lsqr", "sag", "saga"],
    #     "model__max_iter": [10000, 20000, 50000],
    #     "model__tol": [1e-3, 1e-4, 1e-5],
    #     "model__fit_intercept": [True, False]
    # },

    # "Polynomial Lasso": {
    #     "poly__degree": [2, 3],
    #     "model__alpha": np.logspace(-3, 3, 20),
    #     "model__max_iter": [10000, 20000, 50000],
    #     "model__tol": [1e-3, 1e-4, 1e-5],
    #     "model__fit_intercept": [True, False],
    #     "model__selection": ["cyclic", "random"]
    # },

    # "Polynomial Elastic Net": {
    #     "poly__degree": [2, 3],
    #     "model__alpha": np.logspace(-3, 3, 20),
    #     "model__l1_ratio": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    #     "model__fit_intercept": [True, False],
    #     "model__max_iter": [5000, 10000, 20000, 50000],
    #     "model__tol": [1e-3, 1e-4],
    #     "model__selection": ["cyclic", "random"]
    # },

    "Decision Tree": {
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
    },

    "Random Forest": {
        "n_estimators": [100, 200, 500],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2]
    }
}

# results = []
# best_estimators = {}

# for model_name, model in models.items():

#     print(f"Running {model_name}...")

#     grid_search = GridSearchCV(
#         estimator=model,
#         param_grid=param_grids[model_name],
#         scoring="neg_mean_absolute_error",
#         cv=5,
#         n_jobs=-1
#     )

#     grid_search.fit(X_train, y_train)

#     print(f"\n{model_name} Best parameters: \n", grid_search.best_params_)

#     print(f"\nBest CV {model_name} MAE: \n", -grid_search.best_score_)

#     optimised_model = grid_search.best_estimator_
#     best_estimators[model_name] = grid_search.best_estimator_

#     y_pred = grid_search.predict(X_test)

#     print(optimised_model)

#     r2_value = r2_score(y_test, y_pred)
#     mae_value = mean_absolute_error(y_test, y_pred)
#     mse_value = mean_squared_error(y_test, y_pred)
#     rmse_value = root_mean_squared_error(y_test, y_pred)

#     residual = y_test - y_pred

#     res_stand_mean, res_stand_median = RF.plot_residuals(residual_data = residual, standardised = True, 
#                                                          show_plot = False)

#     res_mean, res_median = RF.plot_residuals(residual_data = residual, standardised = False, 
#                                              show_plot = False)

#     results.append({
#         "Model": model_name,
#         "Best MAE": -grid_search.best_score_,
#         "Best Hyperparameters": grid_search.best_params_,
#         "Best Estimator": grid_search.best_estimator_,
#         "R2 Score" : r2_value,
#         "MAE Score" : mae_value,
#         "MSE Score" : mse_value,
#         "RMSE Score" : rmse_value,
#         "Standard Residual Mean" : res_stand_mean,
#         "Standard Residual Median" :res_stand_median,
#         "Residual Mean" : res_mean,
#         "Residual Median" :res_median
#     })

# model_table = pd.DataFrame(results)

# print(type(model_table.loc[0, "Best Estimator"]))

# print(model_table)

# model_table.to_csv(file_path + 'Regression_Modelling_Comparison_Table.csv', sep = ',', index = False)

# model_table = pd.read_csv(file_path + 'Regression_Modelling_Comparison_Table.csv')

# best_model_row = model_table.loc[model_table["Best MAE"].idxmin()]

# best_model_name = best_model_row["Model"]
# best_params = best_model_row["Best Hyperparameters"]
# # best_regression_model = best_model_row["Best Estimator"]
# best_regression_model = best_estimators[best_model_name]

# print(f"Best model: {best_model_name}")
# print(f"Best CV MAE: {best_model_row['Best MAE']:.3f}")
# print("\nBest Hyperparameters:")
# print(best_params)

import joblib

# model_info = {
#     "model_name": best_model_name,
#     "best_params": best_params
# }

# joblib.dump(best_regression_model, "ML Modelling/best_regression_model.pkl")

# print("Model saved successfully.")

best_regression_model = joblib.load("ML Modelling/best_regression_model.pkl")

y_pred = best_regression_model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\nTest Set Performance")
print(f"R²   : {r2:.4f}")
print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")

# r2_value = r2_score(y_test, y_pred)
# mae_value = mean_absolute_error(y_test, y_pred)
# MSE_value = mean_squared_error(y_test, y_pred)
# RMSE_value = root_mean_squared_error(y_test, y_pred)
# print()
# print("Model R2 Score:", r2_value)
# print("Model MAE Score:", mae_value)
# print("Model MSE Score:", MSE_value)
# print("Model RMSE Score:", RMSE_value)
# print()

print(len(y_test))
print(len(y_pred))

plt.scatter(y_pred, y_test, color="dodgerblue", label="Data")
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]

plt.plot(lims, lims, color='red', linewidth=3, label = 'Actual Score Line')
plt.title("Predicted vs Actual (Standardised) Scores", fontsize = 20)
plt.xlabel("Predicted Score", fontsize = 16)
plt.ylabel("Actual Score", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.legend(fontsize = 14)
plt.show()


# Feature to plot
feature = "Avg_Score_per_Tasks"

x = np.linspace(X_train[feature].min(), X_train[feature].max(), 100)

# Create a DataFrame where every feature is fixed at its mean
X_plot = pd.DataFrame(np.tile(X_train.mean().values, (len(x), 1)), columns=X_train.columns)

X_plot[feature] = x

y_plot = best_regression_model.predict(X_plot)

plt.figure(figsize=(8,6))
plt.scatter(X_train[feature], y_train, color="dodgerblue", alpha=0.7, label="Data")
plt.plot(x, y_plot, color="red", linewidth=3,  label="Regression Line")
plt.title(f"{feature} Predicting Target")
plt.xlabel(feature)
plt.ylabel("Target")
plt.legend()
plt.show()


fig, ax = plt.subplots(figsize=(8, 6))
PartialDependenceDisplay.from_estimator(best_regression_model, X_test, features=model_columns, ax = ax)

plt.show()

fig, ax = plt.subplots(figsize=(7, 6))

PartialDependenceDisplay.from_estimator(
    estimator=best_regression_model,
    X=X_test,
    features=[("Avg_Score_per_Tasks", "Number_of_Tasks")],
    ax = ax
)

plt.show()



# y_pred_cv = cross_val_predict(estimator=best_regression_model, X=X, y=y, cv=5)

# fig, ax = plt.subplots(figsize=(6,6))
# ax.scatter(y, y_pred_cv, edgecolors=(0, 0, 0), alpha=0.4)
# ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
# ax.set_xlabel('Measured Count')
# ax.set_ylabel('Predicted Count')
# ax.set_title(r"True and Predicted $y_i$")
# plt.show()

fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(y_test, y_pred, edgecolors=(0, 0, 0), alpha=0.4)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured Count')
ax.set_ylabel('Predicted Count')
ax.set_title(r"True and Predicted $y_i$")
plt.show()


residual = y_test - y_pred

RF.plot_residuals(residual_data = residual, standardised = True)

RF.plot_residuals(residual_data = residual, standardised = False)


standard_residual = residual / residual.std()

plt.axhline(0, color="black", linestyle="--", lw = 4)
plt.scatter(y_pred, standard_residual, color="dodgerblue")
plt.title("Residual Plot of Predicted Values", fontsize = 20)
plt.xlabel("Predicted Value", fontsize = 16)
plt.ylabel("Residual", fontsize = 16)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

# residual = y - y_pred_cv

# standard_residual = residual / residual.std()

# RF.plot_residuals(residual_data = standard_residual, standardised = True)

# RF.plot_residuals(residual_data = residual, standardised = False)

# plt.axhline(0, color="black", linestyle="--", lw = 4)
# plt.scatter(y_pred_cv, standard_residual, color="dodgerblue")
# plt.title("Residual Plot of Predicted Values", fontsize = 20)
# plt.xlabel("Predicted Value", fontsize = 16)
# plt.ylabel("Residual", fontsize = 16)
# plt.xticks(fontsize = 14)
# plt.yticks(fontsize = 14)
# plt.show()


sm.qqplot(residual, line='45', fit=True)

plt.title("Q-Q Plot of Residuals")
plt.show()

##########
#Modelling Series 21 Data

series_21_contestents = series_21_contestents[model_columns]

X_new_data = series_21_contestents
y_new_data = series_21_contestents['Score']

print(X_new_data)

new_predictions = best_regression_model.predict(X_new_data)

print(new_predictions)

for i in range(1,6):
    print(i, new_predictions, y_new_data)

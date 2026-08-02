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

def model_coefficients(model_coef, model_intercept, x_cols, show_plot=True):

    print("Model intercept:", model_intercept.round(3))

    non_zero_coef = np.count_nonzero(model_coef)

    print(f"Non-zero coefficients: {non_zero_coef}/{len(x_cols.columns)}")
    print(f"Coefficients removed: {len(x_cols.columns) - non_zero_coef}")

    # for i, col in enumerate(x_cols.columns):
    #     print(f"{i}. {col} coefficient:", model_coef[i].round(3))

    for col, value in model_coef.items():
        print(f"{col} coefficient: {value:.3f}")

    if show_plot:
        model_coef.sort_values().plot.barh(figsize=(8,6))

        plt.xlabel("Coefficient")
        plt.title("Feature Importance")
        plt.show()

# def model_coefficients(model_columns, model_coef, model_intercept, x_cols, show_plot = True):

#     print("Model intercept:", model_intercept.round(3))

#     non_zero_coef = np.count_nonzero(model_coef)

#     print(f"Non-zero coefficients: {non_zero_coef}/{len(model_coef)}")
#     print(f"Coefficients removed: {len(model_coef) - non_zero_coef}")

#     for i, col in enumerate(model_columns):
#         print(f"{i}. {col} coefficient:", model_coef[i].round(3))

#     if show_plot == True:
#         coef = pd.Series(model_coef, index=x_cols.columns)

#         coef.sort_values().plot.barh(figsize=(8,6))
#         plt.xlabel("Coefficient")
#         plt.title("Feature Importance")
#         plt.show()
    # print("Model intercept:", model_intercept.round(3))
    # for i, col in enumerate(model_columns):
    #     print(f"{i}. {col} coefficient:", model_coef[i].round(3))

    # if show_plot == True:
    #     coef = pd.Series(model_coef, index=x_cols.columns)

    #     coef.sort_values().plot.barh(figsize=(8,6))
    #     plt.xlabel("Coefficient")
    #     plt.title("Feature Importance")
    #     plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.pipeline import Pipeline

# def plot_linear_coefficients(model, X, show_plot=True):
#     """
#     Prints and plots coefficients for Linear, Ridge, Lasso and Elastic Net models.
#     Works for both plain estimators and Pipelines.
#     """
#     if isinstance(model, Pipeline):
#         regressor = model.named_steps["model"]
#     else:
#         regressor = model

#     # Cannot plot coefficients for tree models
#     if not hasattr(regressor, "coef_"):
#         print(f"{type(regressor).__name__} has no coefficients.")
#         return

#     model_coef = regressor.coef_
#     model_intercept = regressor.intercept_

#     print(f"Model intercept: {model_intercept:.3f}\n")

#     for i, col in enumerate(X.columns):
#         print(f"{i}. {col}: {model_coef[i]:.3f}")

#     if show_plot:
#         coef = pd.Series(model_coef, index=X.columns)

#         plt.figure(figsize=(8, 6))
#         coef.sort_values().plot.barh()
#         plt.xlabel("Coefficient")
#         plt.title("Feature Coefficients")
#         plt.tight_layout()
#         plt.show()

def plot_residuals(residual_data, standardised = True, show_plot = True):

    if standardised == True:

        standard_residual = residual_data / residual_data.std()

        res_mean = standard_residual.mean()
        res_median = np.median(standard_residual)

        print(f"Standard Residual Mean: {res_mean:.3f}\nStandard Residual Median: {res_median:.3f}")

        title = "Standardised Residual Distribution Plot of the Linear Model"

    else:
        res_mean = residual_data.mean()
        res_median = np.median(residual_data)

        print(f"Residual Mean: {res_mean:.3f}\nResidual Median: {res_median:.3f}")

        title = "Residual Distribution Plot of the Linear Model"

    if show_plot == True:
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

    return(res_mean, res_median)


def plot_feature_dependancy(model, x_data, columns):

    fig, ax = plt.subplots(figsize=(8, 6))
    PartialDependenceDisplay.from_estimator(model, x_data,  features=columns, ax = ax)

    plt.show()
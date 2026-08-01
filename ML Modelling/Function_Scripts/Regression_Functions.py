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
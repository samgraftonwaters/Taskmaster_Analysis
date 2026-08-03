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

plt.rcParams['figure.figsize'] = (13, 7)

def model_coefficients(model_coef, model_intercept, x_cols, show_plot=True):

    print("Model intercept:", model_intercept.round(3))

    non_zero_coef = np.count_nonzero(model_coef)

    print(f"Non-zero coefficients: {non_zero_coef}/{len(x_cols.columns)}")
    print(f"Coefficients removed: {len(x_cols.columns) - non_zero_coef}")

    for (i, (col, value)) in enumerate(model_coef.items()):
        print(f"{i+1}. {col} coefficient: {value:.3f}")

    if show_plot:
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.2, right = 0.96)
        model_coef.sort_values().plot.barh()

        plt.title("Feature Importance", fontsize = 20)
        plt.xlabel("Coefficient", fontsize = 16)
        plt.ylabel("Feature", fontsize = 16)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
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
        plt.figure()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)
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


def plot_feature_dependancy(model, x_data, model_coef):

    coef = model_coef.sort_values()

    cols = []
    for col, value in coef.items():

        cols.append(col)

    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0.1, hspace=0.4, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)
    disp = PartialDependenceDisplay.from_estimator(model, x_data,  features=cols, ax = ax)    

    for ax, (feature, value) in zip(disp.axes_.ravel(), coef.items()):
        ax.text(x_data[feature].min(), 160, f"Coef = {value:.2f}", ha =  'left')
        plt.xlabel(feature, fontsize = 14)
        plt.ylabel('Partial Dependence', fontsize = 14)
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 12)

    plt.tight_layout()
    plt.show()


from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import RobustScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

plt.rcParams['figure.figsize'] = (13, 7)

def models_hyperparams():

    """
    Contains model pipelines and their respective hyperparameters
    """
    models = {
        "Linear Regression": Pipeline([
        ("scaler", RobustScaler()),
        ("model", LinearRegression())]),

        "Ridge": Pipeline([
        ("scaler", RobustScaler()),
        ("model", Ridge())]),

        "Lasso": Pipeline([
        ("scaler", RobustScaler()),
        ("model", Lasso())]),

        "Elastic Net": Pipeline([
        ("scaler", RobustScaler()),
        ("model", ElasticNet())]),

        "Decision Tree": DecisionTreeRegressor(random_state=42),

        "Random Forest": RandomForestRegressor(random_state=42) 
    }

    param_grids = {
        "Linear Regression": {
        "model__fit_intercept": [True, False],
        "model__positive": [True, False]},

        "Ridge": {
        "model__alpha": np.logspace(-3, 3, 20),
        "model__solver": ["auto", "svd", "cholesky", "lsqr", "sag", "saga"],
        "model__max_iter": [10000, 20000, 50000],
        "model__tol": [1e-3, 1e-4, 1e-5],
        "model__fit_intercept": [True, False]},

        "Lasso": {
        "model__alpha": np.logspace(-3, 3, 20),
        "model__max_iter": [10000, 20000, 50000],
        "model__tol": [1e-3, 1e-4, 1e-5],
        "model__fit_intercept": [True, False],
        "model__selection": ["cyclic", "random"]},

        "Elastic Net": {
        "model__alpha": np.logspace(-3, 3, 20),
        "model__l1_ratio": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        "model__fit_intercept": [True, False],
        "model__max_iter": [5000, 10000, 20000, 50000],
        "model__tol": [1e-3, 1e-4],
        "model__selection": ["cyclic", "random"]},

        "Decision Tree": {
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]},

        "Random Forest": {
        "n_estimators": [100, 200, 500],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2]}
    }
    return(models, param_grids)

def model_coefficients(model_coef, model_intercept, x_cols, show_plot=True):

    print("Model intercept:", model_intercept.round(3))

    non_zero_coef = np.count_nonzero(model_coef)

    print(f"Non-zero coefficients: {non_zero_coef}/{len(x_cols.columns)}")
    print(f"Coefficients removed: {len(x_cols.columns) - non_zero_coef}")

    for (i, (col, value)) in enumerate(model_coef.items()):
        print(f"{i+1}. {col} coefficient: {value:.3f}")

    if show_plot:
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.25, right = 0.96)
        model_coef.sort_values().plot.barh()

        plt.title("Feature Importance", fontsize = 20)
        plt.xlabel("Coefficient", fontsize = 16)
        plt.ylabel("Feature", fontsize = 16)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.show()


def plot_hist_residuals(residual_data, standardised = True, show_plot = True):

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
        plt.legend(fontsize = 16)
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
        ax.set_xlabel(feature, fontsize = 12)
        ax.tick_params(axis="x", labelsize=11)
        ax.tick_params(axis="y", labelsize=11)

    plt.tight_layout()
    plt.show()

def plot_target_feature(feature : str, x_data, y_data, model):

    """
    Scatter plot of target against specified feature, along with line of best fit.

    Parameters:
    -----------
        feature (str): column name of the feature to plot against the target variable
        x_data (DataFrame): DataFrame with all model variables
        y_data (array): target variable data
    
    """

    x = np.linspace(x_data[feature].min(), x_data[feature].max(), 100)

    X_plot = pd.DataFrame(np.tile(x_data.mean().values, (len(x), 1)), columns=x_data.columns)

    X_plot[feature] = x

    y_plot = model.predict(X_plot)

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

    plt.scatter(x_data[feature], y_data, color="dodgerblue", alpha=0.8, label="Data", s = 60)
    plt.plot(x, y_plot, color="red", linewidth=3,  label="Regression Line")

    plt.title(f"{feature} Predicting Target", fontsize = 20)
    plt.xlabel(feature, fontsize = 16)
    plt.ylabel("Target", fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend(fontsize = 16)

    plt.show()


def plot_qq(residuals):

    """
    Plot Q-Q plot with 45 degree line

    Parameters:
    -----------
        residuals (array): calculated residuals - difference between y_pred and y_test
    """

    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

    sm.qqplot(residuals, line='45', fit=True, ax = ax, color = 'dodgerblue')

    plt.title("Q-Q Plot of Residuals", fontsize = 20)
    plt.xlabel('Theoretial Quartiles', fontsize = 16)
    plt.ylabel('Actual Quartiles', fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)

    plt.show()  

def plot_residuals(y_data, residuals):

    """
    Plot residuals for predicted values

    Parameters:
    ----------
        y_data (array): target variable (e.g. y_pred or y_test)
        residuals: calculated residuals
    """
    
    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

    plt.axhline(0, color="black", linestyle="--", lw = 4)
    plt.scatter(y_data, residuals, color="dodgerblue", alpha = 0.8, s = 60)
    plt.title("Residual Plot of Predicted Values", fontsize = 20)
    plt.xlabel("Predicted Value", fontsize = 16)
    plt.ylabel("Residual", fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.show()
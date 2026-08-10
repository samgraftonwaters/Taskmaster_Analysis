from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, root_mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
import joblib

from Function_Scripts import Regression_Functions as RF

import warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.exceptions import FitFailedWarning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FitFailedWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

plt.rcParams['figure.figsize'] = (13, 7)

######
#Model Comparison

def regression_model_comparison_testing(X, y, file_path, feature_run, series_21_new_data, 
                             series_21_contestents, target_feature_feature, y_variable):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    models, parameters = RF.models_hyperparams()

    results = []
    best_estimators = {}

    for model_name, model in models.items():

        print(f"Running {model_name}...")

        grid_search = GridSearchCV(estimator=model, param_grid=parameters[model_name],
                                scoring="neg_mean_absolute_error",  cv=5,  n_jobs=-1)

        grid_search.fit(X_train, y_train)

        print(f"\n{model_name} Best parameters: \n", grid_search.best_params_)

        print(f"\nBest CV {model_name} MAE: \n", -grid_search.best_score_)

        optimised_model = grid_search.best_estimator_
        best_estimators[model_name] = grid_search.best_estimator_

        y_pred = grid_search.predict(X_test)

        print(optimised_model)

        r2_value = r2_score(y_test, y_pred)
        mae_value = mean_absolute_error(y_test, y_pred)
        mse_value = mean_squared_error(y_test, y_pred)
        rmse_value = root_mean_squared_error(y_test, y_pred)

        residual = y_test - y_pred

        res_stand_mean, res_stand_median = RF.plot_hist_residuals(residual_data = residual, standardised = True, 
                                                            show_plot = False)

        res_mean, res_median = RF.plot_hist_residuals(residual_data = residual, standardised = False, 
                                                show_plot = False)

        results.append({
            "Model": model_name,
            "Best MAE": -grid_search.best_score_,
            "Best Hyperparameters": grid_search.best_params_,
            "Best Estimator": grid_search.best_estimator_,
            "R2 Score" : r2_value,
            "MAE Score" : mae_value,
            "MSE Score" : mse_value,
            "RMSE Score" : rmse_value,
            "Standard Residual Mean" : res_stand_mean,
            "Standard Residual Median" :res_stand_median,
            "Residual Mean" : res_mean,
            "Residual Median" :res_median
        })

    model_table = pd.DataFrame(results)

    print(model_table)

    model_table.to_csv(file_path + f'Regression_Modelling_Comparison_Table_{feature_run}.csv', sep = ',', index = False)

    model_table = pd.read_csv(file_path + f'Regression_Modelling_Comparison_Table_{feature_run}.csv')

    best_model_row = model_table.loc[model_table["Best MAE"].idxmin()]

    best_model_name = best_model_row["Model"]
    best_params = best_model_row["Best Hyperparameters"]
    best_regression_model = best_estimators[best_model_name]

    print(f"Best model: {best_model_name}")
    print(f"Best CV MAE: {best_model_row['Best MAE']:.3f}")
    print("\nBest Hyperparameters:")
    print(best_params)

    joblib.dump(best_regression_model, f"ML Modelling/best_regression_model_{feature_run}.pkl")

    print("Model saved successfully.")

    best_regression_model = joblib.load(f"ML Modelling/best_regression_model_{feature_run}.pkl")

    print("Model loaded successfully.")

    print(best_regression_model)

    regressor = best_regression_model.named_steps["model"]

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
    print()

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

    plt.scatter(y_pred, y_test, color="dodgerblue", label="Data", s = 60, alpha = 0.8)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]

    plt.plot(lims, lims, color='red', linewidth=3, label = 'Actual Score Line')
    plt.title("Predicted vs Actual (Standardised) Scores", fontsize = 20)
    plt.xlabel("Predicted Score", fontsize = 16)
    plt.ylabel("Actual Score", fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend(fontsize = 16)
    plt.savefig(f"Plots/Predict_Actual_test_{feature_run}.png", dpi=300, bbox_inches="tight")
    plt.show()

    RF.plot_target_feature(x_data = X_train, y_data = y_train, feature = target_feature_feature,
                        model = best_regression_model, fig_name = f'feature_target_train_{feature_run}')

    RF.plot_target_feature(x_data = X_test, y_data = y_test, feature = target_feature_feature,
                        model = best_regression_model, fig_name = f'feature_target_test_{feature_run}')

    coef = pd.Series(regressor.coef_, index=X_train.columns)
    threshold = 1e-4
    important_coef = coef[coef.abs() > threshold]

    intercept = regressor.intercept_

    RF.model_coefficients(model_coef = important_coef, model_intercept = intercept, 
                        x_cols = X_train, show_plot = True, fig_name = f'Important_Features_{feature_run}')

    if len(important_coef) <= 12:
        RF.plot_feature_dependancy(model = best_regression_model, x_data = X_test.astype(float), 
                                model_coef = important_coef, fig_name = f'Important_Features_subplots_{feature_run}')

    else:
        split = int(round(len(important_coef)/2, 0))
        RF.plot_feature_dependancy(model = best_regression_model, x_data = X_test[0:split].astype(float), 
                                    model_coef = important_coef, fig_name = f'Important_Features_subplots_{feature_run}_0-{split}')

        RF.plot_feature_dependancy(model = best_regression_model, x_data = X_test[split:].astype(float), 
                                        model_coef = important_coef, 
                                        fig_name = f'Important_Features_subplots_{feature_run}_{split}')


    residual = y_test - y_pred

    RF.plot_hist_residuals(residual_data = residual, standardised = True, 
                           fig_name = f'standard_residual_hist_{feature_run}')

    RF.plot_hist_residuals(residual_data = residual, standardised = False, fig_name = f'residual_hist_{feature_run}')

    standard_residual = residual / residual.std()

    RF.plot_residuals(y_data = y_pred, residuals = residual, fig_name = f'residual_predict_{feature_run}',
                      title = "Residual Plot of Predicted Values")

    RF.plot_residuals(y_data = y_pred, residuals = standard_residual, 
                      fig_name = f'standard_residual_predict_{feature_run}',
                      title = "Standardised Residual Plot of Predicted Values")


    RF.plot_qq(residuals = residual, fig_name = f'Q-Q_plot_residual_{feature_run}')
    RF.plot_qq(residuals = standard_residual, fig_name = f'Q-Q_plot_standard_residual_{feature_run}')

    ##########
    #Modelling Series 21 Data

    X_new_data = series_21_new_data
    y_new_data = series_21_contestents[y_variable]

    if (feature_run == 'run6' | 'run7'):
        y_new_data = np.log(y_new_data)

    print(series_21_new_data.columns.equals(X_train.columns))

    new_predictions = best_regression_model.predict(X_new_data)

    ratio = (new_predictions - y_new_data)/y_new_data

    print(' ', 'Pred', ' ', 'Act', ' ', 'Rat')
    for i in range(5):
        print(i+1, f'{new_predictions[i]:.4f}', y_new_data[i], f'{ratio[i]:.4f}')

    plt.figure()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.1, top = 0.94, left = 0.08, right = 0.96)

    plt.scatter(new_predictions, y_new_data, color="dodgerblue", label="Data", s = 60)
    lims = [min(y_new_data.min(), new_predictions.min()), max(y_new_data.max(), new_predictions.max())]

    plt.plot(lims, lims, color='red', linewidth=3, label = 'Actual Score Line')
    plt.title("Predicted vs Actual (Standardised) Scores for Series 21", fontsize = 20)
    plt.xlabel("Predicted Series 21 Score", fontsize = 16)
    plt.ylabel("Actual Series 21 Score", fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend(fontsize = 16)
    plt.savefig(f"Plots/Predict_Actual_S21_{feature_run}.png", dpi=300, bbox_inches="tight")
    plt.show()

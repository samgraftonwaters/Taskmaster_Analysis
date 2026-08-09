from Function_Scripts import Classification_Functions as CF
import warnings
from sklearn.exceptions import ConvergenceWarning
import joblib

warnings.filterwarnings("ignore", category=FutureWarning, module=r"sklearn")

warnings.filterwarnings("ignore", category=UserWarning,
                          module=r"sklearn\.linear_model\._logistic")

warnings.filterwarnings("ignore", category=ConvergenceWarning)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
data = CF.pd.read_csv(file_path + 'Full Contestent Table for Modelling Scaled.csv')
# 'Full Contestent Table for Modelling Scaled.csv'
print(data.head())

name_series_cols = ['Name', 'Series', 'Position', 'Score']

########
#To Change

def classification_model_comparison_testing(X, y, file_path, feature_run, series_21_new_data, 
                                            series_21_contestents_names_series):

    X_train, X_test, y_train, y_test = CF.train_test_split(X, y, test_size=0.2, random_state=123)

    models, parameters = CF.models_hyperparams()

    # hyperparameters = [log_reg_param_grid, nb_param_grid, nb_param_grid, svm_linear_param_grid, 
    #                 svc_param_grid, nu_svc_param_grid, decision_tree_param_grid]

    # model_names = ['Logistic Regression', 'Bernoulli NB', 'Multinomial NB', 'SVM Linear', 'SVC', 
    #             'NuSVC', 'Decision Tree']




    # if (data.select_dtypes(include="number") < 0).any().any() == True:
    #     del hyperparameters[2]
    #     del model_names[2]
    #     del classification_models[2]
    #     print(model_names)

    Best_Params = []
    Threshold = []
    F1_Score = []
    Precision = []
    Recall = []
    ROC_AUC = []
    Precision_Recall_AUC = []

    results = []
    best_estimators = {}

    for model_name, model in models.items():

        print(f"Running {model_name}...")

        labels = [1, 0]
        tick_labels = ["Winner", "Non-Winner"]
        
        grid_search = CF.GridSearchCV(estimator=model, param_grid=parameters[model_name], 
                                        scoring="f1", cv=5)

        grid_search.fit(X_train, y_train)

        print(f"\n{model_name} Best parameters: \n", grid_search.best_params_)

        print(f"\nBest CV {model_name} F1: \n", grid_search.best_score_)

        Best_Params.append(grid_search.best_params_)

        optimised_model = grid_search.best_estimator_
        best_estimators[model_name] = grid_search.best_estimator_

        #find best threshold
        y_train_probs = CF.cross_val_predict(optimised_model, X_train, y_train, cv=5,
                                        method="predict_proba")[:, 1]

        best_threshold_train = CF.determine_best_threshold(y_train, y_train_probs)

        Threshold.append(best_threshold_train)

        optimised_model.fit(X_train, y_train)

        y_test_probs = optimised_model.predict_proba(X_test)[:, 1]
        y_test_pred = (y_test_probs >= best_threshold_train).astype(int)

        conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred)

        CF.plot_confusion_matrix(model_matrix = conf_matrix, tick_labels = tick_labels,
                                title = f'{model_name} Model Confusion Matrix', save_plot = False)

        classif_report = CF.classification_report(y_test, y_test_pred, target_names=tick_labels,
                                                labels=labels, zero_division=0)

        print(f"Final {model_name} Model Report: \n", classif_report)

        precision, recall, f1 = CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

        Precision.append(precision)
        Recall.append(recall)
        F1_Score.append(f1)

        roc_auc = CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_pred, 
                        title = f'{model_name} Model ROC Curve', save_plot = False)

        pr_auc = CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                                    title = f'{model_name} Model Precision Recall Curve',
                                    model_precision = CF.precision_score(y_test, y_test_pred), 
                                    model_recall = CF.recall_score(y_test, y_test_pred),
                                    save_plot = False)
        
        ROC_AUC.append(roc_auc)
        Precision_Recall_AUC.append(pr_auc)

        results.append({
            "Model Name" : model_name,
            "Best F1": grid_search.best_score_,
            "Best Hyperparameters": grid_search.best_params_,
            "Best Estimator": grid_search.best_estimator_,
            "Best Hyperparameters" : Best_Params,
            "Threshold" : Threshold,
            "F1 Score" : F1_Score,
            "precision" : Precision,
            "Recall" : Recall,
            "ROC AUC" : roc_auc, #ROC_AUC, 
            "Precision Recall AUC" : pr_auc  #Precision_Recall_AUC
        })

    model_table = CF.pd.DataFrame(results)

    print(model_table)
    print(model_table.info())

    model_table.to_csv(file_path + f'Classification_Modelling_Comparison_Table_{feature_run}.csv', sep = ',', index = False)

    best_model_row = model_table.sort_values(by=["Best F1", "F1 Score", "ROC AUC", 
                                                 "Precision Recall AUC"], ascending=False).iloc[0]

    best_model_name = best_model_row["Model"]
    best_params = best_model_row["Best Hyperparameters"]
    best_classification_model = best_estimators[best_model_name]

    print(f"Best model: {best_model_name}")
    print(f"Best CV MAE: {best_model_row['Best MAE']:.3f}")
    print("\nBest Hyperparameters:")
    print(best_params)


    # best_model_table = model_table.loc[best_model_index]

    # print(best_model_table)

    # best_classification_model = classification_models[best_model_index]

    # best_classification_model.set_params(**best_model_table['Best Hyperparameters'])

    # best_classification_model.fit(X_train, y_train)

    joblib.dump(best_classification_model, f"ML Modelling/best_classification_model_{feature_run}.pkl")

    print("Model saved successfully.")

    best_classification_model = joblib.load(f"ML Modelling/best_classification_model_{feature_run}.pkl")

    print("Model loaded successfully.")


    if hasattr(best_classification_model, "predict_proba"):
        y_test_probs = best_classification_model.predict_proba(X_test)[:, 1]
    else:
        y_test_probs = best_classification_model.decision_function(X_test)

    y_test_pred = (y_test_probs >= best_model_row['Threshold']).astype(int)

    conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred)

    precision, recall, f1 = CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

    CF.plot_confusion_matrix(model_matrix = conf_matrix, tick_labels = tick_labels,
                            title = f'{best_model_row['Model Name']} Model Confusion Matrix', save_plot = True)

    CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_pred, 
                        title = f'{best_model_row['Model Name']} Model ROC Curve', save_plot = True)

    CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                                title = f'{best_model_row['Model Name']} Model Precision Recall Curve',
                                model_precision = CF.precision_score(y_test, y_test_pred), 
                                model_recall = CF.recall_score(y_test, y_test_pred),
                                save_plot = True)
    ###
    # # Predictions with Series 21
    # ####

    print(series_21_new_data.columns)

    predict_data = series_21_new_data#.iloc[:, 2:]
    print(predict_data)

    y_predict_probs = best_classification_model.predict_proba(predict_data)[:, 1]
    y_predict_pred = (y_predict_probs >= best_model_row['Threshold']).astype(int)

    print(y_predict_probs)
    print(y_predict_pred)

    series_21_new_data = CF.pd.concat([series_21_new_data, series_21_contestents_names_series], axis = 1)

    series_21_new_data['Probability'] = y_predict_probs
    series_21_new_data['Prediction'] = y_predict_pred

    print(series_21_new_data[series_21_new_data['Prediction'] == 1]['Name'])

    series_21_new_data[['Name', 'Series', 'Position', 'Score', 
                        'Prediction', 'Probability']].to_csv(file_path + f'Classification_Modelling_Comparison_Table_{feature_run}_Predicton.csv', 
                                sep = ',', index = False)
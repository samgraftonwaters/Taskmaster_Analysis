from Function_Scripts import Classification_Functions as CF
import warnings
from sklearn.exceptions import ConvergenceWarning

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

final_table_file_name = "Classification Modelling Table.csv"

model_columns = ['Number_Episodes', 'Team_A', 'Team_B', 
           'Age_Ranges_20 - 29', 'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 
           'Age_Ranges_50 - 59', 'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male',
           'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5']

# model_columns = ['Disqualifications',
#        'Episode_Percentage_Losses', 'Number_of_Tasks', 'Percent_1s_Scored',
#        'Tie_Break_Losses', 'Tie_Break_Wins', 'Tie_Breaks_per_series',
#        'Avg_Score_per_Episodes', 'Avg_Score_per_Tasks',
#        'Episode_Percentage_Wins', 'Number_Episodes', 'Number_Team_Tasks',
#        'Percent_5s_Scored', 'Series_Number', 'Team_Score_per_Task',
#        'Team_Score_per_Person', 'Team_A', 'Team_B', 'Age_Ranges_20 - 29',
#        'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59',
#        'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male',
#        'Gender_Non-Binary', 'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3',
#        'Seat_Seat 4', 'Seat_Seat 5']
######



series_21_contestents = data[data['Series'] == 'S21'].reset_index(drop = True)
series_21_contestents_names_series = series_21_contestents[name_series_cols]

series_21_contestents = series_21_contestents[model_columns]

print(series_21_contestents)

data = data[data['Series'] != 'S21']

data = data[model_columns + ["Position"]]

print(data.head())

data['Winner'] = CF.np.where(data['Position'] == 1, 1, 0)
data = data.drop('Position', axis = 1)

print(data.head())

model_data = data.copy()

print(model_data)

X = model_data.iloc[:,:-1]
y = model_data['Winner']

X_train, X_test, y_train, y_test = CF.train_test_split(X, y, test_size=0.2, random_state=123)

labels = [1, 0]
tick_labels = ["Winner", "Non-Winner"]

log_reg_param_grid = [
    {
        "solver": ["lbfgs", "newton-cg"],
        "penalty": ["l2", None],
        "C": [0.1, 1, 10, 100],
        "tol": [0.0001, 0.001, 0.01, 0.1, 1]
    },
    {
        "solver": ["liblinear"],
        "penalty": ["l1", "l2"],
        "C": [0.1, 1, 10, 100],
        "tol": [0.0001, 0.001, 0.01, 0.1, 1]
    },
    {
    "solver": ["saga"],
    "penalty": ["l1", "l2"],
    "C": [0.1, 1, 10, 100],
    "tol": [0.0001, 0.001, 0.01, 0.1, 1]
    },
    {
    "solver": ["saga"],
    "penalty": ["elasticnet"],
    "C": [0.1, 1, 10, 100],
    "tol": [0.0001, 0.001, 0.01, 0.1, 1],
    "l1_ratio": [0.5]
    }
]

nb_param_grid = {
    "alpha": [0.001, 0.01, 0.1, 0.5, 1, 2]
}

svm_linear_param_grid = [
    { "C" :  [0.1, 1, 10, 100],
     "tol": [0.0001, 0.001, 0.01, 0.1, 1],
     "penalty" : ["l1", "l2"],
     "loss": ["hinge",  "squared_hinge"],
    }
]

svc_param_grid = [
    {"C" :  [0.1, 1, 10, 100],
     "tol": [0.0001, 0.001, 0.01, 0.1, 1],
     "kernel" : ["linear", "poly", "rbf", "sigmoid"],
     "gamma": ["scale", "auto"]
    }
]

nu_svc_param_grid = [
    {"tol": [0.0001, 0.001, 0.01, 0.1, 1],
     "nu": [0.01, 0.02, 0.05, 0.1, 0.2, 0.5],
     "kernel" : ["linear", "poly", "rbf", "sigmoid"],
      "gamma": ["scale", "auto"]
    }
]

decision_tree_param_grid = {
    "criterion": ["gini", "entropy", "log_loss"],
    "splitter" : ['best', 'random'],
    "max_features": [None, "sqrt", "log2"]
}

hyperparameters = [log_reg_param_grid, nb_param_grid, nb_param_grid, svm_linear_param_grid, 
                   svc_param_grid, nu_svc_param_grid, decision_tree_param_grid]

model_names = ['Logistic Regression', 'Bernoulli NB', 'Multinomial NB', 'SVM Linear', 'SVC', 
               'NuSVC', 'Decision Tree']

classification_models = [CF.LogisticRegression(class_weight="balanced"), CF.BernoulliNB(), CF.MultinomialNB(),
          CF.LinearSVC(class_weight = 'balanced'),  CF.SVC(class_weight = 'balanced', probability=True),
          CF.NuSVC(class_weight = 'balanced', probability=True),
          CF.DecisionTreeClassifier(class_weight = 'balanced')]


if (data.select_dtypes(include="number") < 0).any().any() == True:
    del hyperparameters[2]
    del model_names[2]
    del classification_models[2]
    print(model_names)

Best_Params = []
Threshold = []
F1_Score = []
Precision = []
Recall = []
ROC_AUC = []
Precision_Recall_AUC = []

for model, model_name, parameters_to_search in zip(classification_models, model_names, hyperparameters):

    grid_search = CF.GridSearchCV(estimator=model, param_grid=parameters_to_search, 
                                      scoring="f1", cv=5)

    grid_search.fit(X_train, y_train)

    print(f"\n{model_name} Best parameters: \n", grid_search.best_params_)

    print(f"\nBest CV {model_name} F1: \n", grid_search.best_score_)

    Best_Params.append(grid_search.best_params_)

    optimised_model = grid_search.best_estimator_

    if model_name == 'SVM Linear':
        optimised_model = CF.CalibratedClassifierCV(optimised_model, method="sigmoid", cv=5)

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

model_table = CF.pd.DataFrame({
    "Model Name" : model_names,
    "Classification Model" : classification_models,
    "Best Hyperparameters" : Best_Params,
    "Threshold" : Threshold,
    "F1 Score" : F1_Score,
    "precision" : Precision,
    "Recall" : Recall,
    "ROC AUC" : ROC_AUC, 
    "Precision Recall AUC" : Precision_Recall_AUC
    }
)

print(model_table)
print(model_table.info())

model_table.to_csv(file_path + final_table_file_name, sep = ',', index = False)

# best_model = model_table[model_table['F1 Score'].max()]

best_model_index = (model_table.sort_values(by=["F1 Score", "ROC AUC", "Precision Recall AUC"],
                                      ascending=False).index[0])

best_model_table = model_table.loc[best_model_index]

print(best_model_table)

best_classification_model = classification_models[best_model_index]

best_classification_model.set_params(**best_model_table['Best Hyperparameters'])

best_classification_model.fit(X_train, y_train)

y_test_probs = best_classification_model.predict_proba(X_test)[:, 1]
y_test_pred = (y_test_probs >= best_model_table['Threshold']).astype(int)

conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred)

precision, recall, f1 = CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

CF.plot_confusion_matrix(model_matrix = conf_matrix, tick_labels = tick_labels,
                        title = f'{best_model_table['Model Name']} Model Confusion Matrix', save_plot = True)

CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_pred, 
                    title = f'{best_model_table['Model Name']} Model ROC Curve', save_plot = True)

CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                            title = f'{best_model_table['Model Name']} Model Precision Recall Curve',
                            model_precision = CF.precision_score(y_test, y_test_pred), 
                            model_recall = CF.recall_score(y_test, y_test_pred),
                            save_plot = True)

# series_21_contestents = CF.pd.read_csv('/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Series 21 Predictions Table.csv')
###
# Predictions with Series 21
####

print(series_21_contestents.columns)

predict_data = series_21_contestents#.iloc[:, 2:]
print(predict_data)

y_predict_probs = best_classification_model.predict_proba(predict_data)[:, 1]
y_predict_pred = (y_predict_probs >= best_model_table['Threshold']).astype(int)

print(y_predict_probs)
print(y_predict_pred)

series_21_contestents = CF.pd.concat([series_21_contestents, series_21_contestents_names_series], axis = 1)

series_21_contestents['Prediction'] = y_predict_pred

print(series_21_contestents[series_21_contestents['Prediction'] == 1]['Name'])
import Classification_Functions as CF


file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
data = CF.pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

print(data.head())

data = data[['Series', 'Name', 'Position', 'Number_Episodes', 'Team_A', 'Team_B', 'Age_Ranges_20 - 29', 
                   'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59', 
                   'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male', 'Gender_Non-Binary', 
                   'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5']]

data['Winner'] = CF.np.where(data['Position'] == 1, 1, 0)

print(data.head())

model_data = data[['Number_Episodes', 'Team_A', 'Team_B', 'Age_Ranges_20 - 29', 
                   'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59', 
                   'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male', 'Gender_Non-Binary', 
                   'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5', 
                   'Winner']]

X = model_data.iloc[:,:-1]
y = model_data['Winner']

X_train, X_test, y_train, y_test = CF.train_test_split(X, y, test_size=0.2, random_state=123)

labels = [1, 0]
tick_labels = ["Winner", "Non-Winner"]



######
#1. Logistic Regression Model
######
parameters_to_search = [
    {
        "solver": ["lbfgs", "newton-cg"],
        "penalty": ["l2", None],
        "C": [0.1, 1, 10, 100],
        "tol": [0.0001, 0.001, 0.01, 0.1]
    },
    {
        "solver": ["liblinear"],
        "penalty": ["l1", "l2"],
        "C": [0.1, 1, 10, 100],
        "tol": [0.0001, 0.001, 0.01, 0.1]
    },
    {
    "solver": ["saga"],
    "penalty": ["l1", "l2"],
    "C": [0.1, 1, 10, 100],
    "tol": [0.0001, 0.001, 0.01, 0.1]
    },
    {
    "solver": ["saga"],
    "penalty": ["elasticnet"],
    "C": [0.1, 1, 10, 100],
    "tol": [0.0001, 0.001, 0.01, 0.1],
    "l1_ratio": [0.5]
    }
]


#Hyperparameter grid search
optimised_model = CF.GridSearchCV(estimator=CF.LogisticRegression(class_weight="balanced"),
                               param_grid=parameters_to_search, scoring="f1", cv=5)

optimised_model.fit(X_train, y_train)

print("\nBest parameters: \n\n", optimised_model.best_params_)

logistic_regression_best = optimised_model.best_estimator_

#find best threshold
y_train_probs = CF.cross_val_predict(logistic_regression_best, X_train, y_train, cv=5,
                                  method="predict_proba")[:, 1]

best_threshold_train = CF.determine_best_threshold(y_train, y_train_probs)

logistic_regression_best.fit(X_train, y_train)

y_test_probs = logistic_regression_best.predict_proba(X_test)[:, 1]
y_test_pred = (y_test_probs >= best_threshold_train).astype(int)

logistic_regression_conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred,
                                                           labels = labels)

CF.plot_confusion_matrix(model_matrix = logistic_regression_conf_matrix, tick_labels = tick_labels)

classif_report = CF.classification_report(y_test, y_test_pred, target_names=tick_labels)

print("Final Model Report: \n", classif_report)

CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

y_pred_scores = logistic_regression_best.decision_function(X_test)

CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_pred, title = 'Logistic Regression Model ROC Curve')

CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                            title = 'Logistic Regression Model Precision Recall Curve',
                            model_precision = CF.precision_score(y_test, y_test_pred), 
                            model_recall = CF.recall_score(y_test, y_test_pred))



######
#2. Naive Bayes
######











######
#3. SVM
######

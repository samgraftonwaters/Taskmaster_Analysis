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
                                                        #stratify=y)

labels = [1, 0]
tick_labels = ["Winner", "Non-Winner"]



######
#1. Logistic Regression Model
######

print('\n Logistic Regression Method: \n')

parameters_to_search = [
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


#Hyperparameter grid search
optimised_model = CF.GridSearchCV(estimator=CF.LogisticRegression(class_weight="balanced"),
                               param_grid=parameters_to_search, scoring="f1", cv=5)

optimised_model.fit(X_train, y_train)

print("\nBest parameters: \n", optimised_model.best_params_)

print("\nBest CV Logistic regression F1: \n", optimised_model.best_score_)

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

CF.plot_confusion_matrix(model_matrix = logistic_regression_conf_matrix, tick_labels = tick_labels,
                         title = f'Logistic Regression Model Confusion Matrix')

classif_report = CF.classification_report(y_test, y_test_pred, target_names=tick_labels,
                                          labels=labels)

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

print('\n Naive Bayes Method: \n')
param_grid = {
    "alpha": [0.001, 0.01, 0.1, 0.5, 1, 2]
}

#Hyperparameter grid search
multi_optimised_model = CF.GridSearchCV(estimator=CF.MultinomialNB(),
                               param_grid=param_grid, scoring="f1", cv=5)

multi_optimised_model.fit(X_train, y_train)

print("Best parameters for MultinomialNB: \n", multi_optimised_model.best_params_)

print("Best CV MultinomialNB F1: ", multi_optimised_model.best_score_)


bern_optimised_model = CF.GridSearchCV(estimator=CF.BernoulliNB(),
                               param_grid=param_grid, scoring="f1", cv=5)

bern_optimised_model.fit(X_train, y_train)

print("\nBest parameters for BernoulliNB: \n\n", bern_optimised_model.best_params_)

print("Best CV BernoulliNB F1: ", bern_optimised_model.best_score_)

nb_models = [bern_optimised_model.best_estimator_, multi_optimised_model.best_estimator_]
nb_model_names = ['Bernoulli', 'Multinomial']

for nb_model, nb_name in zip(nb_models, nb_model_names):
    y_train_probs = CF.cross_val_predict(nb_model, X_train, y_train, cv=5,
                                    method="predict_proba")[:, 1]

    best_threshold_train = CF.determine_best_threshold(y_train, y_train_probs)

    nb_model.fit(X_train, y_train)

    y_test_probs = nb_model.predict_proba(X_test)[:, 1]
    y_test_pred = (y_test_probs >= best_threshold_train).astype(int)

    naive_bayes_conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred,
                                                            labels = labels)

    CF.plot_confusion_matrix(model_matrix = naive_bayes_conf_matrix, tick_labels = tick_labels,
                             title = f'Naive Bayes {nb_name} Model Confusion Matrix')

    classif_report = CF.classification_report(y_test, y_test_pred, target_names=tick_labels,
                                            labels=labels)

    print(f"Final {nb_name} Model Report: \n", classif_report)

    CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

    CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_probs, title = f'Naive Bayes {nb_name} Model ROC Curve')

    CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                                title = f'Naive Bayes {nb_name} Model Precision Recall Curve',
                                model_precision = CF.precision_score(y_test, y_test_pred), 
                                model_recall = CF.recall_score(y_test, y_test_pred))


######
#3. SVM
######

svm_linear_parameters_grid = [
    { "C" :  [0.1, 1, 10, 100],
     "tol": [0.0001, 0.001, 0.01, 0.1, 1],
     "penalty" : ["l1", "l2"],
     "loss": ["hinge",  "squared_hinge"],
    }
]

svc_parameters_grid = [
    {"C" :  [0.1, 1, 10, 100],
     "tol": [0.0001, 0.001, 0.01, 0.1, 1],
     "kernel" : ["linear", "poly", "rbf", "sigmoid"],
     "gamma": ["scale", "auto"]
    }
]

nu_svc_parameter_grid = [
    {"tol": [0.0001, 0.001, 0.01, 0.1, 1],
     "nu": [0, 0.2, 0.4, 0.6, 0.8, 1],
     "kernel" : ["linear", "poly", "rbf", "sigmoid"],
      "gamma": ["scale", "auto"]
    }
]

#Hyperparameter grid search
svm_linear_optimised_model = CF.GridSearchCV(estimator=CF.LinearSVC(class_weight = 'balanced'),
                               param_grid=svm_linear_parameters_grid, scoring="f1", cv=5)

svm_linear_optimised_model.fit(X_train, y_train)

print("Best parameters for MultinomialNB: \n", svm_linear_optimised_model.best_params_)

print("Best CV MultinomialNB F1: ", svm_linear_optimised_model.best_score_)

svm_linear_best = svm_linear_optimised_model.best_estimator_

svc_optimised_model = CF.GridSearchCV(estimator=CF.SVC(class_weight = 'balanced', probability=True),
                               param_grid=svc_parameters_grid, scoring="f1", cv=5)

svc_optimised_model.fit(X_train, y_train)

print("Best parameters for MultinomialNB: \n", svc_optimised_model.best_params_)

print("Best CV MultinomialNB F1: ", svc_optimised_model.best_score_)

svc_best = svc_optimised_model.best_estimator_


nu_svc_optimised_model = CF.GridSearchCV(estimator=CF.NuSVC(class_weight = 'balanced', probability=True),
                               param_grid=nu_svc_parameter_grid, scoring="f1", cv=5)

nu_svc_optimised_model.fit(X_train, y_train)

print("Best parameters for MultinomialNB: \n", nu_svc_optimised_model.best_params_)

print("Best CV MultinomialNB F1: ", nu_svc_optimised_model.best_score_)

nu_svc_best = nu_svc_optimised_model.best_estimator_

###

linear_model = CF.CalibratedClassifierCV(
    svm_linear_optimised_model.best_estimator_,
    method="sigmoid",
    cv=5
)

svm_models = [linear_model, 
              svc_optimised_model.best_estimator_,
              nu_svc_optimised_model.best_estimator_
              ]
svm_model_names = ['SVM Linear', 'SVC', 'NuSVC']

for svm_model, svm_name in zip(svm_models, svm_model_names):

    y_train_probs = CF.cross_val_predict(svm_model, X_train, y_train, cv=5,
                                    method="predict_proba")[:, 1]

    best_threshold_train = CF.determine_best_threshold(y_train, y_train_probs)

    svm_model.fit(X_train, y_train)

    y_test_probs = svm_model.predict_proba(X_test)[:, 1]
    y_test_pred = (y_test_probs >= best_threshold_train).astype(int)

    svm_model_conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred,
                                                            labels = labels)

    CF.plot_confusion_matrix(model_matrix = svm_model_conf_matrix, tick_labels = tick_labels,
                             title = f'{svm_name} Model Confusion Matrix')

    classif_report = CF.classification_report(y_test, y_test_pred, target_names=tick_labels,
                                            labels=labels)

    print(f"Final {svm_name} Model Report: \n", classif_report)

    CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

    CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_probs, title = f'{svm_name} Model ROC Curve')

    CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                                title = f'{svm_name} Model Precision Recall Curve',
                                model_precision = CF.precision_score(y_test, y_test_pred), 
                                model_recall = CF.recall_score(y_test, y_test_pred))




######
#4. Decision Tree
######

decision_tree_param_grid = {
    "criterion": ["gini", "entropy", "log_loss"],
    "splitter" : ['best', 'random'],
    "max_features": [None, "sqrt", "log2"]
}

#Hyperparameter grid search
tree_optimised_model = CF.GridSearchCV(estimator=CF.DecisionTreeClassifier(class_weight = 'balanced'),
                               param_grid=decision_tree_param_grid, scoring="f1", cv=5)

tree_optimised_model.fit(X_train, y_train)

print("Best parameters for MultinomialNB: \n", tree_optimised_model.best_params_)

print("Best CV MultinomialNB F1: ", tree_optimised_model.best_score_)

tree_best = tree_optimised_model.best_estimator_


y_train_probs = CF.cross_val_predict(tree_best, X_train, y_train, cv=5,
                                method="predict_proba")[:, 1]

best_threshold_train = CF.determine_best_threshold(y_train, y_train_probs)

tree_best.fit(X_train, y_train)

y_test_probs = tree_best.predict_proba(X_test)[:, 1]
y_test_pred = (y_test_probs >= best_threshold_train).astype(int)

tree_conf_matrix = CF.calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred,
                                                        labels = labels)

CF.plot_confusion_matrix(model_matrix = tree_conf_matrix, tick_labels = tick_labels,
                         title = 'Decision Tree Model Confusion Matrix')

classif_report = CF.classification_report(y_test, y_test_pred, target_names=tick_labels,
                                        labels=labels)

print(f"Final Decision Tree Classifier Model Report: \n", classif_report)

CF.return_model_metrics(y_true = y_test, y_pred = y_test_pred)

CF.plot_ROC_curve(y_true = y_test, y_scores = y_test_probs, title = f'Decision Tree Classifier Model ROC Curve')

CF.plot_precision_recall_curve(y_true = y_test, y_prob_scores = y_test_probs, 
                            title = f'Decision Tree Classifier Model Precision Recall Curve',
                            model_precision = CF.precision_score(y_test, y_test_pred), 
                            model_recall = CF.recall_score(y_test, y_test_pred))
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, RobustScaler
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.linear_model import LogisticRegression



plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/Script_Outputs/'
data = pd.read_csv(file_path + 'Full Contestent Table for Modelling.csv')

print(data.head())

data = data[['Series', 'Name', 'Position', 'Number_Episodes', 'Team_A', 'Team_B', 'Age_Ranges_20 - 29', 
                   'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59', 
                   'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male', 'Gender_Non-Binary', 
                   'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5']]

data['Winner'] = np.where(data['Position'] == 1, 1, 0)

print(data.head())

model_data = data[['Number_Episodes', 'Team_A', 'Team_B', 'Age_Ranges_20 - 29', 
                   'Age_Ranges_30 - 39', 'Age_Ranges_40 - 49', 'Age_Ranges_50 - 59', 
                   'Age_Ranges_60 - 69', 'Gender_Female', 'Gender_Male', 'Gender_Non-Binary', 
                   'Seat_Seat 1', 'Seat_Seat 2', 'Seat_Seat 3', 'Seat_Seat 4', 'Seat_Seat 5', 
                   'Winner']]

X = model_data.iloc[:,:-1]
y = model_data['Winner']

print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)


# # Fit the model
# logistic_regression_model.fit(X_train, y_train)

# # Predict values using the test data.
# y_pred = logistic_regression_model.predict(X_test)

# # Compare predicted and true values to yield the accuracy.
# logistic_regression_acc = f1_score(y_test, y_pred)

# print("Logistic Regression Model F1-Score: \n", logistic_regression_acc)

# # Predicting Probabilities
# y_pred_prob = logistic_regression_model.predict_proba(X_test)
# print(y_pred_prob[:5])
# print(y_pred[:5])

# classif_report = classification_report(y_test, y_pred)

# print(classif_report)

labels = [1, 0]
tick_labels = ["Winner", "Non-Winner"]

def calculate_conf_matrix( y_test, y_pred):

    conf_matrix_values = confusion_matrix(y_test, y_pred, labels=labels)
    print("Confusion matrix (count): \n", conf_matrix_values)

    return(conf_matrix_values)

def plot_confusion_matrix(model_matrix):
    fig, ax = plt.subplots()
    plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.95)

    sns.heatmap(
        model_matrix, annot=True, fmt="d", cmap="coolwarm", xticklabels=tick_labels,
        yticklabels=tick_labels, annot_kws={"size": 16}, cbar_kws={"shrink": 1.0},
        linewidths=1, linecolor="black")

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=14)

    plt.xlabel('Predicted', fontsize = 16)
    plt.ylabel('True', fontsize = 16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.xaxis.set_label_position('top') 

    plt.show()

def determine_best_threshold(y, y_probs):
    thresholds = np.arange(0.05, 0.95, 0.01)
    f1_scores = []

    for t in thresholds:
        preds = (y_probs >= t).astype(int)
        f1_scores.append(f1_score(y, preds))

    best_threshold = thresholds[np.argmax(f1_scores)]
    print("Best threshold:", best_threshold)

    return(best_threshold)

def predict_with_threshold(model, X, threshold):
    probs = model.predict_proba(X)[:, 1]
    return (probs >= threshold).astype(int)


#Logistic Regression Model

# parameters_to_search = {"solver":["lbfgs", "liblinear", "newton-cg"], "C":[0.1, 1, 10, 100],
#                         "tol":[0.001, 0.001, 0.01, 0.1], "penalty":['l1', 'l2', 'elasticnet', None]}

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
        "penalty": ["l1", "l2", "elasticnet"],
        "C": [0.1, 1, 10, 100],
        "tol": [0.0001, 0.001, 0.01, 0.1],
        "l1_ratio": [0.5]  # required for elasticnet
    }
]


logistic_regression_model = LogisticRegression(class_weight="balanced")

optimised_model = GridSearchCV(estimator=logistic_regression_model, \
                               param_grid=parameters_to_search, scoring="f1", cv=5)

optimised_model.fit(X_train, y_train)

print("\nThe best parameters found are: \n\n", optimised_model.best_params_)

y_pred = optimised_model.best_estimator_.predict(X_test)

classif_report = classification_report(y_test, y_pred, target_names=tick_labels)

print("Optimised parameter report: \n", classif_report)

logistic_regression_conf_matrix = calculate_conf_matrix(y_test = y_test, y_pred = y_pred)

plot_confusion_matrix(model_matrix = logistic_regression_conf_matrix)

best_params = optimised_model.best_params_

logistic_regression_best = LogisticRegression(
    class_weight="balanced",
    **best_params
)

logistic_regression_best.fit(X_train, y_train)

# y_pred = logistic_regression_best.predict(X_test)

# classif_report = classification_report(y_test, y_pred, target_names=tick_labels)

# print("Optimised parameter report: \n", classif_report)

# logistic_regression_conf_matrix = calculate_conf_matrix(y_test = y_test, y_pred = y_pred)

# plot_confusion_matrix(model_matrix = logistic_regression_conf_matrix)

# y_probs = logistic_regression_best.predict_proba(X_test)[:, 1]

#find best threshold
y_train_probs = cross_val_predict(
    logistic_regression_best,
    X_train,
    y_train,
    cv=5,
    method="predict_proba"
)[:, 1]

best_threshold_train = determine_best_threshold(y_train, y_train_probs)

logistic_regression_best.fit(X_train, y_train)

y_test_probs = logistic_regression_best.predict_proba(X_test)[:, 1]
y_test_pred = (y_test_probs >= best_threshold_train).astype(int)

logistic_regression_conf_matrix = calculate_conf_matrix(y_test = y_test, y_pred = y_test_pred)

plot_confusion_matrix(model_matrix = logistic_regression_conf_matrix)

classif_report = classification_report(y_test, y_test_pred, target_names=tick_labels)

print("Optimised parameter report: \n", classif_report)

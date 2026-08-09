from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, RobustScaler
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score, classification_report, precision_score, recall_score
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, precision_recall_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC, SVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

plt.rcParams['figure.figsize'] = (13, 7)

def models_hyperparams():

    """
    Contains model pipelines and their respective hyperparameters
    """
    models = {
        "Logistic Regression": Pipeline([
        ("scaler", RobustScaler()),
        ("model", LogisticRegression(class_weight="balanced"))]),

        "BernoulliNB": Pipeline([
        ("scaler", RobustScaler()),
        ("model", BernoulliNB())]),

        "MultinomialNB": Pipeline([
        ("scaler", RobustScaler()),
        ("model", MultinomialNB())]),

        "LinearSVM": Pipeline([
        ("scaler", RobustScaler()),
        ("model", LinearSVC(class_weight = 'balanced'))]),

        "SVC": Pipeline([
        ("scaler", RobustScaler()),
        ("model", SVC(class_weight = 'balanced', probability=True))]),

        "NuSCV": Pipeline([
        ("scaler", RobustScaler()),
        ("model", NuSVC(class_weight = 'balanced', probability=True))]),

        "DecisionTree": Pipeline([
        ("scaler", RobustScaler()),
        ("model", DecisionTreeClassifier(class_weight = 'balanced'))]),
    }

    param_grids = {
        "Logistic Regression": {
        "model__solver": ["lbfgs", "newton-cg"],
        "model__penalty": ["l2", None],
        "model__C": [0.1, 1, 10, 100],
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1]
        },
        "Logistic Regression": {
        "model__solver": ["liblinear"],
        "model__penalty": ["l1", "l2"],
        "model__C": [0.1, 1, 10, 100],
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1]
        },
        "Logistic Regression": {
        "model__solver": ["saga"],
        "model__penalty": ["l1", "l2"],
        "model__C": [0.1, 1, 10, 100],
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1]
        },
        "Logistic Regression": {
        "model__solver": ["saga"],
        "model__penalty": ["elasticnet"],
        "model__C": [0.1, 1, 10, 100],
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1],
        "model__l1_ratio": [0.5]
        },

        "BernoulliNB" : {
        "model__alpha": [0.001, 0.01, 0.1, 0.5, 1, 2]
        },

        "MultinomialNB" : {
        "model__alpha": [0.001, 0.01, 0.1, 0.5, 1, 2]
        },

        "LinearSVM" : { 
        "model__C" :  [0.1, 1, 10, 100],
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1],
        "model__penalty" : ["l1", "l2"],
        "model__loss": ["hinge",  "squared_hinge"],
        },

        "SVC" : {
        "model__C" :  [0.1, 1, 10, 100],
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1],
        "model__kernel" : ["linear", "poly", "rbf", "sigmoid"],
        "model__gamma": ["scale", "auto"]
        },

        "NuSCV" : {
        "model__tol": [0.0001, 0.001, 0.01, 0.1, 1],
        "model__nu": [0.01, 0.02, 0.05, 0.1, 0.2, 0.5],
        "model__kernel" : ["linear", "poly", "rbf", "sigmoid"],
        "model__gamma": ["scale", "auto"]
        },

        "DecisionTree": {
        "model__criterion": ["gini", "entropy", "log_loss"],
        "model__splitter" : ['best', 'random'],
        "model__max_features": [None, "sqrt", "log2"]
        }
    }

    return(models, param_grids)


def calculate_conf_matrix(y_test, y_pred):

    """
    Calculates the confidence matrix of a classfication model

    Parameters:
    -----------
        y_test (): array of target values from the test portion of the train_test_split method
        y_pred (): predicted target values based on the X_test and classification model
    
    Returns:
    --------
        Returns the confusion matrix of the classification model. 
    """

    conf_matrix_values = confusion_matrix(y_test, y_pred, labels=[1,0])
    print("Confusion matrix (count): \n", conf_matrix_values)

    return(conf_matrix_values)

def plot_confusion_matrix(model_matrix, tick_labels, title : str, save_plot = False):

    """
   Plots the confidence matrix of a classfication model

    Parameters:
    -----------
        model_matrix: confusion matrix calculated from previous function. 
        tick_labels: names of the classes
        title (str): Title of confusion matrix
        save_plot (boolean): Set to save the plot. Default is False
    
    Returns:
    --------
        Returns the confusion matrix plot of the classification model. 
    """
    if save_plot == True:
        fig, ax = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.05, top = 0.85, left = 0.1, right = 0.95)

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
        plt.title(title, fontsize = 20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        
        plt.show()
    else:
        None

def determine_best_threshold(y, y_probs):

    """
    Determines the best threshold from the F1 score for the given classification model

    Parameters:
    -----------
        y: target variables from training data
        y_probs: model probabilities for y data

    Returns:
    --------
        Best threshold value for classification model
    """
    thresholds = np.arange(0.1, 0.9, 0.01)
    f1_scores = []

    for t in thresholds:
        preds = (y_probs >= t).astype(int)
        f1_scores.append(f1_score(y, preds))

    best_threshold = thresholds[np.argmax(f1_scores)]
    print("Best threshold:", best_threshold)

    return(best_threshold)

def predict_with_threshold(model, X, threshold):
    """
    Classification model predictions based on new "best" threshold value

    Parameters:
    -----------
        model: best fit classification model
        X: test variables to calculate the probabilities of y
        threshold: best threshold value from the previous function

    Returns:
    --------
        list of probabilities that are greater than or equal to the new threshold value
    
    """

    probs = model.predict_proba(X)[:, 1]
    return (probs >= threshold).astype(int)

def return_model_metrics(y_true, y_pred):
    """
    Prints and returns Precision, Recall and F1 Score classification model

    Parameters:
    -----------
        y_true: actual class values
        y_pred: predicted class values
    
    Returns:
    --------
        precision, recall, f1
    """

    print('The Precision, Recall and F1 Score values are:\n')
    precision = round(precision_score(y_true, y_pred), 2)
    recall = round(recall_score(y_true, y_pred), 2)
    f1 = round(f1_score(y_true, y_pred), 2)

    print('Precision: ', precision)
    print('Recall: ', recall)
    print('F1 Score: ', f1)

    return(precision, recall, f1)

def plot_ROC_curve(y_true, y_scores, title, save_plot = False):

    """
    Plots an ROC curve for the given classification model

    Parameters:
    -----------
        y_true: actual y values from the train_test_split
        y_scores: predicted y-values using the X_test values and new threshold
        title (str): title of the plot
        save_plot (boolean): Set to save the plot. Default is False
    
    Returns:
    --------
        Plots ROC curve
        AUC_Score (float): the ROC area under the curve value
    """

    fpr, tpr, _thresholds = roc_curve(y_true, y_scores, pos_label=1)

    AUC_score = roc_auc_score(y_true, y_scores)

    print(AUC_score)

    if save_plot == True:
        fig, ax = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.95)

        plt.plot(fpr, tpr, color='firebrick', lw = 3, label="ROC curve area: {:.3f}".format(AUC_score))
        plt.plot([0, 1], [0, 1], color='dodgerblue', linestyle='--', lw = 3, label="Expected Random Model")
        plt.title(title, fontsize = 20)
        plt.legend(loc="best", fontsize = 18)
        plt.xlabel('False Positive Rate', fontsize = 16)
        plt.ylabel('True Positive Rate', fontsize = 16)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.show()
    return(AUC_score)

def plot_precision_recall_curve(y_true, y_prob_scores, title, model_precision, model_recall, 
                                save_plot = False):

    """
    Plots a precision-recall curve for the given classification model

    Parameters:
    -----------
        y_true: actual y values from the train_test_split
        y_prob_scores: predicted probabilities using the X_test values and new threshold
        title (str): title of the plot
        model_precision (float): the precision score of the model
        model_recall (float): the recall score of the model
        save_plot (boolean): Set to save the plot. Default is False
    
    Returns:
    --------
        Plots Precision-Recall curve
        AUC_Score (float): the Precision-Recall area under the curve value
    """

    precision, recall, _thresholds = precision_recall_curve(y_true, y_prob_scores)

    AUC_score = auc(recall, precision)

    print(AUC_score)

    if save_plot == True:

        fig, ax = plt.subplots()
        plt.subplots_adjust(wspace=0, hspace=0, bottom = 0.08, top = 0.9, left = 0.1, right = 0.95)

        plt.plot(recall, precision, color='dodgerblue', lw = 3, label="PR AUC: {:.3f}".format(AUC_score))
        plt.plot(model_recall, model_precision, 'o', color='firebrick', markersize = 16, label="Model Precision-Recall")
        plt.title(title, fontsize = 20)
        plt.legend(loc="best", fontsize = 18)
        plt.xlabel('Recall', fontsize = 16)
        plt.ylabel('Precision', fontsize = 16)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 14)
        plt.show()
    return(AUC_score)

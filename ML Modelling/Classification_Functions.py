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

plt.rcParams['figure.figsize'] = (13, 7)

def calculate_conf_matrix( y_test, y_pred, labels):

    conf_matrix_values = confusion_matrix(y_test, y_pred, labels=labels)
    print("Confusion matrix (count): \n", conf_matrix_values)

    return(conf_matrix_values)

def plot_confusion_matrix(model_matrix, tick_labels):
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
    thresholds = np.arange(0.1, 0.9, 0.01)
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

def return_model_metrics(y_true, y_pred):
    print('The Precision, Recall and F1 Score values are:\n')
    print('Precision: ', round(precision_score(y_true, y_pred), 2))
    print('Recall: ', round(recall_score(y_true, y_pred), 2))
    print('F1 Score: ', round(f1_score(y_true, y_pred), 2))

def plot_ROC_curve(y_true, y_scores, title):

    fpr, tpr, _thresholds = roc_curve(y_true, y_scores, pos_label=1)

    AUC_score = roc_auc_score(y_true, y_scores)

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

def plot_precision_recall_curve(y_true, y_prob_scores, title, model_precision, model_recall):

    precision, recall, _thresholds = precision_recall_curve(y_true, y_prob_scores)

    AUC_score = auc(recall, precision)

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

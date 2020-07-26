#Data-Handling Libraries
import pandas as pd 
from sklearn import svm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from class_performance_metrics import PerformanceMetrics

 
#Selecting which files to load.
Directory_Labelled_Emails = (
        "D:/"
        "Bachelor_Thesis/"
        "Labelled_Emails_Features_Only/"
        "Word_Vectors/"
        )

df_train = pd.read_csv(
        Directory_Labelled_Emails 
        + "part_1_augmented.csv"
        )

df_test = pd.read_csv(
        Directory_Labelled_Emails 
        + "part_2.csv"
        )

X_train = df_train.iloc[:, 1:302]
y_train = df_train.iloc[:, 0]
X_test = df_test.iloc[:, 1:302]
y_test = df_test.iloc[:, 0]

##### TRAINING PART
classifiers = [
        svm.SVC(kernel = "rbf", 
                gamma = "scale"),
                
        RandomForestClassifier(n_estimators = 1000, 
                               max_depth = 200),
                               
        MLPClassifier(solver = "lbfgs", 
                      alpha = 0.3, 
                      hidden_layer_sizes = (500,20), 
                      random_state = 3),
                      
        LogisticRegression(solver = "lbfgs"),
        
        AdaBoostClassifier(n_estimators=500, 
                           learning_rate=0.0005)
        ]

SCORE_ATTRIBUTES = [
        "classifier",
        "random_state",
        "test_size",
        "accuracy",
        "precision",
        "recall",
        "f1_score"
        ]

df_scores = pd.DataFrame(columns = SCORE_ATTRIBUTES)

for clf in classifiers:
    clf_position = classifiers.index(clf)
    clf.fit(X_train, y_train.ravel())
    y_pred = clf.predict(X_test)
    scores_for_run = PerformanceMetrics(clf, 1, y_test, y_pred)
    for attribute, value in scores_for_run.__dict__.items():
        df_scores.loc[clf_position, attribute] = value

"""
for index in range(Start, End):
    print(index)
    for clf in classifiers:
        clf_position = classifiers.index(clf)
        clf.fit(X_train, y_train)
"""
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier

def train_svm(X_train, y_train, C = 1, kernel = "rbf", gamma = "scale"):
    clf = svm.SVC(C = C, kernel = kernel, gamma = gamma)

    clf.fit(X_train, y_train.ravel())
    return clf

def train_rf(X_train, y_train, n_estimators = 1000, max_depth = 200):
    clf = RandomForestClassifier(
            n_estimators = n_estimators, 
            max_depth = max_depth
            )

    clf.fit(X_train, y_train.ravel())
    return clf

def train_mlp(
            X_train, y_train, 
            solver = "lbfgs", 
            alpha = 0.3, 
            hidden_layer_sizes = (500,20),
            random_state = 0
            ):
    clf = MLPClassifier(
            solver = solver, 
            alpha = alpha, 
            hidden_layer_sizes = hidden_layer_sizes, 
            random_state = random_state
            )

    clf.fit(X_train, y_train.ravel())
    return clf

def train_logreg(X_train, y_train, penalty = "l2", solver = "lbfgs", C = 1):
    clf = LogisticRegression(penalty = penalty, solver = solver, C = C)

    clf.fit(X_train, y_train.ravel())
    return clf

def train_adaboost(X_train, y_train, n_estimators = 50, learning_rate = 0.05):
    clf = AdaBoostClassifier(
            n_estimators = n_estimators, 
            learning_rate = learning_rate)

    clf.fit(X_train, y_train.ravel())
    return clf
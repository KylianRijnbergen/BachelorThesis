import os
import pandas as pd
from timeit import default_timer as timer
from augmentation import augment
from classification import train_svm, train_rf, train_mlp, train_logreg, train_adaboost, evaluate, load_data
from preprocessing import train_test_split
from experiments import SEEDS, TO_AUGMENT, AUGMENTATION_PERCENTAGE, AUGMENTATION_FREQUENCY, \
                        TO_CLASSIFY, TO_CSV, \
                        TRAIN_SVM, svm_combined, \
                        TRAIN_RANDOM_FOREST, rf_combined, \
                        TRAIN_MLP, mlp_combined, \
                        TRAIN_LOGREG, logreg_combined, \
                        TRAIN_ADABOOST, ada_combined
import warnings
warnings.filterwarnings("ignore")
current_dir = os.getcwd().replace('\\', '/')

metrics_list = ["accuracy", "precision", "recall", "f1_score"]
pd_svm = pd.DataFrame(columns = ["kernel", "gamma"] + metrics_list)
pd_rf = pd.DataFrame(columns = ["n_estimators", "max_depth"] + metrics_list)
pd_mlp = pd.DataFrame(columns = ["solver", "alpha", "layers", "state"] + metrics_list)
pd_logreg = pd.DataFrame(columns = ["penalty", "solver", "C"] + metrics_list)
pd_ada = pd.DataFrame(columns = ["n_estimators", "learning_rate"] + metrics_list)

def write_to_df(df, entries, y_test, y_pred):
    accuracy, precision, recall, f1_score = evaluate(y_test, y_pred)
    columns = metrics_list
    row = df.shape[0]
    for item in columns:
        df.loc[row, item] = locals()[item]
    for item in entries:
        df.loc[row, item] = entries[item]
    return


def main(seed):
    train_test_split(random_state = seed)

    if TO_AUGMENT:
        augment(current_dir + "/data/Labelled_Emails_Features_Only/Word_Vectors/",
                "part_1.csv", 
                AUGMENTATION_PERCENTAGE, 
                AUGMENTATION_FREQUENCY, 
                current_dir + "/data/Labelled_Emails_Features_Only/Word_Vectors/"
                )
    
    if TO_CLASSIFY:
        #Load data
        (X_train, y_train, X_test, y_test) = load_data()
        if TRAIN_SVM:
            for kernel, gamma in svm_combined:
                clf = train_svm(X_train, y_train, kernel, gamma)
                y_pred = clf.predict(X_test)
                accuracy = evaluate(y_test, y_pred)[0]
                print("SVM: Seed: {}, kernel: {}, gamma: {}, accuracy: {}.".format(seed, kernel, gamma, accuracy))
                entries = {}
                entries["kernel"] = kernel
                entries["gamma"] = gamma
                write_to_df(pd_svm, entries, y_test, y_pred)


        if TRAIN_RANDOM_FOREST:
            for n_estimators, max_depth in rf_combined:
                clf = train_rf(X_train, y_train, n_estimators, max_depth)
                y_pred = clf.predict(X_test)
                accuracy = evaluate(y_test, y_pred)[0]
                print("Random Forests: Seed: {}, n_estimators: {}, max_depth: {}, accuracy: {}.".format(seed, n_estimators, max_depth, accuracy))
                entries = {}
                entries["n_estimators"] = n_estimators
                entries["max_depth"] = max_depth
                write_to_df(pd_rf, entries, y_test, y_pred)
        
        if TRAIN_MLP:
            for solver, alpha, layers, state in mlp_combined:
                clf = train_mlp(X_train, y_train, solver, alpha, layers, state)
                y_pred = clf.predict(X_test)
                accuracy = evaluate(y_test, y_pred)[0]
                print("MultiLayer Perceptron: Seed: {}, solver: {}, alpha: {}, layers: {}, state: {}, accuracy: {}.".format(seed, solver, alpha, layers, state, accuracy))
                entries = {}
                entries["solver"] = solver
                entries["alpha"] = alpha
                entries["layers"] = layers
                entries["state"] = state
                write_to_df(pd_mlp, entries, y_test, y_pred)
                
        if TRAIN_LOGREG:
            for penalty, solver, C in logreg_combined:
                clf = train_logreg(X_train, y_train, penalty = penalty, solver = solver, C = C)
                y_pred = clf.predict(X_test)
                accuracy = evaluate(y_test, y_pred)[0]
                print("Logistic Regression: Seed: {}, penalty: {}, solver: {}, C: {}, accuracy: {}.".format(seed, penalty, solver, C, accuracy))
                entries = {}
                entries["penalty"] = penalty
                entries["solver"] = solver
                entries["C"] = C
                write_to_df(pd_logreg, entries, y_test, y_pred)
        
        if TRAIN_ADABOOST:
            for n_estimators, learning_rate in ada_combined:
                clf = train_adaboost(X_train, y_train, n_estimators = n_estimators, learning_rate = learning_rate)
                y_pred = clf.predict(X_test)
                accuracy = evaluate(y_test, y_pred)[0]
                print("Adaptive Boosting: Seed: {}, n_estimators: {}, learning_rate: {}, accuracy: {}.".format(seed, n_estimators, learning_rate, accuracy))
                entries = {}
                entries["n_estimators"] = n_estimators
                entries["learning_rate"] = learning_rate
                write_to_df(pd_ada, entries, y_test, y_pred)


        if TO_CSV:
            if TRAIN_SVM:
                pd_svm.to_csv("{}/experimentresults/svm/seed{}.csv".format(current_dir, seed), index = False)
            if TRAIN_RANDOM_FOREST:
                pd_rf.to_csv("{}/experimentresults/rf/seed{}.csv".format(current_dir, seed), index = False)
            if TRAIN_MLP:
                pd_mlp.to_csv("{}/experimentresults/mlp/seed{}.csv".format(current_dir, seed), index = False)
            if TRAIN_LOGREG:
                pd_logreg.to_csv("{}/experimentresults/logreg/seed{}.csv".format(current_dir, seed), index = False)
            if TRAIN_ADABOOST:
                pd_ada.to_csv("{}/experimentresults/ada/seed{}.csv".format(current_dir, seed), index = False)



if __name__ == "__main__":
    for seed in SEEDS:
        main(seed)
    
    print("Program finished. Runtime was {} seconds.".format(timer()))
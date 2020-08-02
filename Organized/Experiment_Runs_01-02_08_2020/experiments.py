#GLOBAL
SEEDS = [0]
TO_AUGMENT = True
AUGMENTATION_PERCENTAGE = [1.005, 1.01, 1.015, 1.02, 1.025, 1.03, 1.035, 1.04, 1.045, 1.05]
AUGMENTATION_FREQUENCY = 20
TO_CLASSIFY = True
TO_CSV = True

#SUPPORT VECTOR MACHINE
TRAIN_SVM = True
SVM_C = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1, 1.1, 1.2, 1.25, 1.3, 1.4, 1.5, 1.75, 2, 2.5, 3, 4, 5, 7.5, 10]
SVM_KERNEL = ["linear", "rbf"]
SVM_GAMMA = ["scale"]
svm_combined = [(C, kernel, gamma) for C in SVM_C for kernel in SVM_KERNEL for gamma in SVM_GAMMA]

#RANDOM FORESTS
TRAIN_RANDOM_FOREST = True
RF_ESTIMATORS = [100, 250, 500] 
RF_MAX_DEPTH = [10, 50, 100, 200]
rf_combined = [(n_estimators, max_depth) for n_estimators in RF_ESTIMATORS for max_depth in RF_MAX_DEPTH]

#MULTILAYER PERCEPTRON
TRAIN_MLP = True
MLP_SOLVER = ["lbfgs"] #, "sgd", "adam"] 
MLP_ALPHA = [0.1, 0.25, 0.5]
layer_1 = [50, 100, 250, 500]
layer_2 = [5, 10, 20, 50]
combination_constructor = [(one, two) for one in layer_1 for two in layer_2]
MLP_HIDDEN_LAYERS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500]
for one, two in combination_constructor:
    MLP_HIDDEN_LAYERS.append((one, two))    
MLP_RANDOM_STATE = [0]
mlp_combined = [(solver, alpha, layers, state) for solver in MLP_SOLVER for alpha in MLP_ALPHA for layers in MLP_HIDDEN_LAYERS for state in MLP_RANDOM_STATE]

#LOGISTIC REGRESSION
TRAIN_LOGREG = True
LOGREG_PENALTY = ["l2"]
LOGREG_SOLVER = ["lbfgs"]
LOGREG_C = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1]
logreg_combined = [(penalty, solver, C) for penalty in LOGREG_PENALTY for solver in LOGREG_SOLVER for C in LOGREG_C]

#ADAPTIVE BOOSTING
TRAIN_ADABOOST = True
ADA_ESTIMATORS = [1, 5, 10, 20, 30, 40, 50, 75, 100] 
ADA_LEARNING_RATE = [0.001, 0.002, 0.003, 0.004, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.25, 1.5, 1.75, 2]
ada_combined = [(n_estimators, learning_rate) for n_estimators in ADA_ESTIMATORS for learning_rate in ADA_LEARNING_RATE]
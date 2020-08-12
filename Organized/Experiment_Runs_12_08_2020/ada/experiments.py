#GLOBAL
SEEDS = list(range(0,10))
TO_AUGMENT = True
AUGMENTATION_PERCENTAGE = [1.015, 1.02, 1.025, 1.03, 1.035]
AUGMENTATION_FREQUENCY = 20
TO_CLASSIFY = True
TO_CSV = True

#SUPPORT VECTOR MACHINE
TRAIN_SVM = False
SVM_C = [0.15, 0.75, 1, 1.1]
SVM_KERNEL = ["linear", "rbf"]
SVM_GAMMA = ["scale"]
svm_combined = [(C, kernel, gamma) for C in SVM_C for kernel in SVM_KERNEL for gamma in SVM_GAMMA]

#RANDOM FORESTS
TRAIN_RANDOM_FOREST = False
RF_ESTIMATORS = [100, 250, 500] 
RF_MAX_DEPTH = [10, 50, 100, 200]
rf_combined = [(n_estimators, max_depth) for n_estimators in RF_ESTIMATORS for max_depth in RF_MAX_DEPTH]

#MULTILAYER PERCEPTRON
TRAIN_MLP = False
MLP_SOLVER = ["lbfgs"] #, "sgd", "adam"] 
MLP_ALPHA = [0.1, 0.25, 0.5]
MLP_HIDDEN_LAYERS = [20, 40, 60, (50,5), (50,10), (100, 10), (100, 20), (250, 10)]  
MLP_RANDOM_STATE = [0]
mlp_combined = [(solver, alpha, layers, state) for solver in MLP_SOLVER for alpha in MLP_ALPHA for layers in MLP_HIDDEN_LAYERS for state in MLP_RANDOM_STATE]

#LOGISTIC REGRESSION
TRAIN_LOGREG = False
LOGREG_PENALTY = ["l2"]
LOGREG_SOLVER = ["lbfgs"]
LOGREG_C = [0.4, 0.5, 0.75, 1]
logreg_combined = [(penalty, solver, C) for penalty in LOGREG_PENALTY for solver in LOGREG_SOLVER for C in LOGREG_C]

#ADAPTIVE BOOSTING
TRAIN_ADABOOST = True
ADA_ESTIMATORS = [40, 50, 75, 100] 
ADA_LEARNING_RATE = [0.6, 0.7, 0.8, 1, 1.5]
ada_combined = [(n_estimators, learning_rate) for n_estimators in ADA_ESTIMATORS for learning_rate in ADA_LEARNING_RATE]
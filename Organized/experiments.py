#GLOBAL
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
TO_AUGMENT = True
AUGMENTATION_PERCENTAGE = 1.01
AUGMENTATION_FREQUENCY = 3
TO_CLASSIFY = True
TO_CSV = True

#SUPPORT VECTOR MACHINE
TRAIN_SVM = True
SVM_KERNEL = ["linear", "poly", "rbf", "sigmoid"]
SVM_GAMMA = ["scale", "auto"]
svm_combined = [(kernel, gamma) for kernel in SVM_KERNEL for gamma in SVM_GAMMA]

#RANDOM FORESTS
TRAIN_RANDOM_FOREST = True
RF_ESTIMATORS = [1, 10, 100] 
RF_MAX_DEPTH = [1, 10, 100]
rf_combined = [(n_estimators, max_depth) for n_estimators in RF_ESTIMATORS for max_depth in RF_MAX_DEPTH]

#MULTILAYER PERCEPTRON
TRAIN_MLP = True
MLP_SOLVER = ["lbfgs", "sgd", "adam"] 
MLP_ALPHA = [0.0001, 0.001, 0.01, 0.1]
layer_1 = [1, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
layer_2 = [1, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
layer_3 = [1, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
combination_constructor = [(one, two, three) for one in layer_1 for two in layer_2 for three in layer_3]
MLP_HIDDEN_LAYERS = []
for one, two, three in combination_constructor:
    MLP_HIDDEN_LAYERS.append((one, two, three))    
MLP_RANDOM_STATE = [0]
mlp_combined = [(solver, alpha, layers, state) for solver in MLP_SOLVER for alpha in MLP_ALPHA for layers in MLP_HIDDEN_LAYERS for state in MLP_RANDOM_STATE]

#LOGISTIC REGRESSION
TRAIN_LOGREG = True
LOGREG_PENALTY = ["l2"]
LOGREG_SOLVER = ["lbfgs"]
LOGREG_C = [0.01, 0.1, 1]
logreg_combined = [(penalty, solver, C) for penalty in LOGREG_PENALTY for solver in LOGREG_SOLVER for C in LOGREG_C]

#ADAPTIVE BOOSTING
TRAIN_ADABOOST = True
ADA_ESTIMATORS = [1, 10, 100] 
ADA_LEARNING_RATE = [0.1, 1, 10]
ada_combined = [(n_estimators, learning_rate) for n_estimators in ADA_ESTIMATORS for learning_rate in ADA_LEARNING_RATE]
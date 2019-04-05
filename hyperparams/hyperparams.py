criterion = ["gini", "entropy"]
splitter = ["best", "random"]
max_depth = list(range(5, 40))
max_depth.append(None)
min_samples_split = [2, 5, 10, 20]
min_samples_leaf = [1, 2, 4, 8, 16]
max_features = ['log2', 'sqrt', None]
random_state = [13]

dectree_hyperparams_grid = {'max_depth': max_depth,
                            'splitter': splitter,
                            'max_features': max_features,
                            'max_depth': max_depth,
                            'min_samples_split': min_samples_split,
                            'min_samples_leaf': min_samples_leaf,
                            'criterion': criterion,
                            'random_state': random_state}



n_estimators = list(range(100, 1100, 100))
max_features = ['log2', 'sqrt', None]
max_depth = list(range(5, 100))
max_depth.append(None)
min_samples_split = [2, 5, 10, 20, 50]
min_samples_leaf = [1, 2, 4, 8, 16]
bootstrap = [True, False]
criterion = ["gini", "entropy"]
random_state = [13]

randf_hyperparams_grid = {'n_estimators': n_estimators,
                          'max_features': max_features,
                          'max_depth': max_depth,
                          'min_samples_split': min_samples_split,
                          'min_samples_leaf': min_samples_leaf,
                          'bootstrap': bootstrap,
                          'criterion': criterion,
                          'random_state': random_state}




n_estimators = list(range(100, 1100, 100))
learning_rate = [0.01, 0.05, 0.1, 0.3, 1]
base_estimator__criterion = ["gini", "entropy"]
base_estimator__splitter = ["best", "random"]
base_estimator__max_depth = list(range(5, 100))
base_estimator__max_depth.append(None)
base_estimator__min_samples_split = [2, 5, 10, 20, 50]
base_estimator__min_samples_leaf = [1, 2, 4, 8, 16]
base_estimator__max_features = ['sqrt', 'log2', None]
random_state = [13]

ada_hyperparams_grid = {'n_estimators' : n_estimators,
                        'learning_rate' : learning_rate,
                        'base_estimator__criterion' : base_estimator__criterion,
                        'base_estimator__splitter' : base_estimator__splitter,
                        'base_estimator__max_depth' : base_estimator__max_depth,
                        'base_estimator__min_samples_split' : base_estimator__min_samples_split,
                        'base_estimator__min_samples_leaf' : base_estimator__min_samples_leaf,
                        'base_estimator__max_features' : base_estimator__max_features,
                        'random_state': random_state}




learning_rate = [0.01, 0.05, 0.1, 0.3, 1]
n_estimators = list(range(100, 600, 100))
max_depth = list(range(3, 12, 2))
min_child_weight = list(range(1, 6, 2))
gamma = [i/10.0 for i in range(0, 6)]
subsample = [i/10.0 for i in range(6, 11)]
colsample_bytree = [i/10.0 for i in range(6, 11)]
reg_alpha = [1e-5, 1e-2, 0.1, 1, 100]
random_state = [13]

xgb_hyperparams_grid = {'learning_rate': learning_rate,
                        'n_estimators': n_estimators,
                        'max_depth': max_depth,
                        'min_child_weight': min_child_weight,
                        'gamma': gamma,
                        'subsample': subsample,
                        'colsample_bytree': colsample_bytree,
                        'reg_alpha': reg_alpha,
                        'random_state': random_state}
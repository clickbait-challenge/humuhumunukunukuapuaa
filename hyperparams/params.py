small_randf_params = {}
small_randf_params['max_depth'] = 7
small_randf_params['n_estimators'] = 500
small_randf_params['min_samples_leaf'] = 4
small_randf_params['min_samples_split'] = 8
small_randf_params['random_state'] = 13
small_randf_w = 2.5
# weight = 2.5

large_randf_params = {}
large_randf_params['max_depth'] = 9
large_randf_params['n_estimators'] = 1000
large_randf_params['min_samples_leaf'] = 8
large_randf_params['min_samples_split'] = 10
large_randf_params['random_state'] = 13
large_randf_w = 4
# weight = 4



small_ada_params = {}
small_ada_params['base_estimator__max_depth'] = 7
small_ada_params['n_estimators'] = 80
small_ada_params['base_estimator__min_samples_leaf'] = 2
small_ada_params['base_estimator__min_samples_split'] = 4
small_ada_params['random_state'] = 13
small_ada_w = 3
# weight = 3

large_ada_params = {}
large_ada_params['base_estimator__max_depth'] = 9
large_ada_params['n_estimators'] = 100
large_ada_params['base_estimator__min_samples_leaf'] = 2
large_ada_params['base_estimator__min_samples_split'] = 4
large_ada_params['random_state'] = 13
large_ada_w = 3.5
# weight = 3.5



small_xgb_params = {}
small_xgb_params['max_depth'] = 6   
small_xgb_params['n_estimators'] = 100
small_xgb_params['learning_rate'] = 0.01
small_xgb_params['reg_alpha'] = 0.001
small_xgb_params['min_child_weight'] = 3
small_xgb_params['gamma'] = 0.5
small_xgb_params['random_state'] = 13
small_xgb_w = 2.5
# weight = 2.5

large_xgb_params = {}
large_xgb_params['max_depth'] = 8   
large_xgb_params['n_estimators'] = 250
large_xgb_params['learning_rate'] = 0.001
large_xgb_params['reg_alpha'] = 1e-05
large_xgb_params['min_child_weight'] = 4
large_xgb_params['gamma'] = 0.5
large_xgb_params['random_state'] = 13
large_xgb_w = 4
# weight = 4



small_dect_params = {}
small_dect_params['max_depth'] = 6
small_dect_params['min_samples_leaf'] = 2
small_dect_params['min_samples_split'] = 3
small_dect_params['random_state'] = 13
small_dect_w = 2.5
# weight = 2.5

large_dect_params = {}
large_dect_params['max_depth'] = 10
large_dect_params['min_samples_leaf'] = 2
large_dect_params['min_samples_split'] = 4
large_dect_params['random_state'] = 13
large_dect_w = 3.5
# weight = 3.5
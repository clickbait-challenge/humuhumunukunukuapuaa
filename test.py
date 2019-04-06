import numpy.ma as ma



d = {
'param_kernel' : ma.masked_array(data = ['rbf', 'rbf', 'rbf'], mask = False),
'param_gamma'  : ma.masked_array(data = [0.1, 0.2, 0.3], mask = False),
'split0_test_score'  : [0.80, 0.90, 0.70],
'split1_test_score'  : [0.82, 0.50, 0.70],
'mean_test_score'    : [0.81, 0.70, 0.70],
'std_test_score'     : [0.01, 0.20, 0.00],
'rank_test_score'    : [3, 1, 1],
'split0_train_score' : [0.80, 0.92, 0.70],
'split1_train_score' : [0.82, 0.55, 0.70],
'mean_train_score'   : [0.81, 0.74, 0.70],
'std_train_score'    : [0.01, 0.19, 0.00],
'mean_fit_time'      : [0.73, 0.63, 0.43],
'std_fit_time'       : [0.01, 0.02, 0.01],
'mean_score_time'    : [0.01, 0.06, 0.04],
'std_score_time'     : [0.00, 0.00, 0.00],
'params'             : [{'kernel' : 'rbf', 'gamma' : 0.1}],
}

import pandas as pd

d.pop('params', None)

df = pd.DataFrame(d)
print(df)
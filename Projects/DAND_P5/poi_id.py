#!/usr/bin/python

import sys
import pickle
import pprint
import numpy as np
import final_projects_helper_functions as hf
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.feature_selection import RFE
from sklearn.pipeline import Pipeline
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi',
                 'bonus',
                 'deferral_payments',
                 'deferred_income',
                 'director_fees',
                 'exercised_stock_options',
                 'expenses',
                 'from_messages',
                 'from_poi_to_this_person',
                 'from_this_person_to_poi',
                 'loan_advances',
                 'long_term_incentive',
                 'other',
                 'restricted_stock',
                 'salary',
                 'shared_receipt_with_poi',
                 'to_messages',
                 'total_payments',
                 'total_stock_value']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict['TOTAL']
del data_dict['THE TRAVEL AGENCY IN THE PARK']

### Task 3: Create new feature(s)
data_dict = hf.add_poi_mail_features(data_dict)
# features_list.append('from_poi_pct')
# features_list.append('to_poi_pct')

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract all features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

### Dimensions of the data are computed below
# print np.array(data).shape
# print np.sum(labels)

### Plot all original variables
# hf.plot_features(features_list, data_all)

### Print top 5 extreme observations for "loan_advances" and "total_payments"
# pprint.pprint(hf.return_sorted_values(data_dict, "loan_advances", 5))
# pprint.pprint(hf.return_sorted_values(data_dict, "total_payments", 5))

### Plot Lasso selection
# hf.lasso_selection(features, labels, features_list)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
random_seed = 1303
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=random_seed)
cv = StratifiedShuffleSplit(labels_train,
                            n_iter=20,
                            test_size=0.5,
                            random_state=random_seed)

ada=AdaBoostClassifier(random_state=random_seed)
selector=RFE(ada,step=1)
pipe_ada= Pipeline(steps=[('RFE', selector), ('ada', ada)])
params_ada_gs = {"RFE__n_features_to_select": np.arange(11,15,2),
                 "ada__learning_rate" : np.arange(0.3,0.7,0.2),
                 "ada__n_estimators" : [50,100]
                }

# pipe_ada= Pipeline(steps=[('RFE', selector), ('ada', ada)])
# params_ada_gs = {"RFE__n_features_to_select": [15],
#                  "ada__learning_rate" : [0.5],
#                  "ada__n_estimators" : [50]
#                 }

gs = GridSearchCV(pipe_ada, params_ada_gs, scoring='f1', cv=cv)
gs.fit(features_train, labels_train)
model_best = gs.best_estimator_
print model_best

clf = model_best.named_steps['ada']
features_best = model_best.named_steps['RFE'].get_support()
features_all = features_list[1:]
features_chosen=[]
for feature_name, feature_boo in zip(features_all, features_best):
    if feature_boo:
        features_chosen.append(feature_name)

features_list=features_list[0:1] + features_chosen
# features_list = ['poi',
#                 'bonus',
#                 'deferred_income',
#                 'exercised_stock_options',
#                 'expenses', 'from_messages',
#                 'from_this_person_to_poi',
#                 'other',
#                 'restricted_stock',
#                 'salary',
#                 'shared_receipt_with_poi',
#                 'to_messages',
#                 'total_payments',
#                 'total_stock_value',
#                 'from_poi_pct',
#                 'to_poi_pct']

# Recreate data with the chosen features

data = featureFormat(my_dataset, features_list, sort_keys=True)
labels_final, features_final = targetFeatureSplit(data)
features_train, features_test, labels_train, labels_test = \
    train_test_split(features_final, labels_final, test_size=0.3, random_state=random_seed)

# clf=AdaBoostClassifier(learning_rate=0.5, n_estimators=50, random_state=random_seed)
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
print ""
pprint.pprint("Performance of tuned AdaBoost")
pprint.pprint(hf.evaluate_estimator(pred, labels_test))

# The best model is refit to all the available data
clf.fit(features_final, labels_final)

hf.plot_feature_importance(clf,features_final,labels_final, features_list)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

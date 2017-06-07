def plot_features(features_array, data):
    '''
    Behavior:   Shows scatterplots of data
    Input:      feature_array (list of strings), data (array)
    Output:     Return None, shows plot
    '''
    import matplotlib.pyplot as plt
    import math
    import numpy as np

    dependent = data[:, 0]
    dependent_name = features_array[0]
    independent = data[:, 1:]
    independent_names = features_array[1:]
    max_columns = 6
    plots = int(len(independent_names))
    max_rows = int(math.ceil(float(plots) / max_columns))
    plt.figure(1)
    for index, variable in enumerate(independent.T):
        variable_name = independent_names[index]
        plt.subplot(max_rows, max_columns, int(index+1))
        for point_x, point_y in zip(dependent, variable):
            x = point_x
            y = point_y
            plt.scatter(x, y)
        plt.xlabel(dependent_name)
        plt.ylabel(variable_name)
        plt.xticks(np.arange(0, 1.5, 1))
        plt.yticks(fontsize=1)
    plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    plt.show()
    return None


def return_sorted_values(data_dictionary, feature, top_n):
    '''
    Behavior:   Finds extreme values of the variable "feature" in
                "data_diciontary", and returns the "top_n" of these
    Input:      data_dictionary (list of dictionaries), feature (string),
                top_n (integer)
    Output:     tuple of top_n extreme values and their key.
    '''
    import numpy as np
    import numbers

    feature_array = []
    key_array = []
    for key in data_dictionary.keys():
        if data_dictionary[key][feature] != 'NaN':
            feature_array.append(data_dictionary[key][feature])
            key_array.append(key)
    feature_array = np.array(feature_array)
    key_array = np.array(key_array)
    sort_index = np.flip(np.array(feature_array).argsort(), axis=0)
    feature_array_sorted = feature_array[sort_index]
    key_array_sorted = key_array[sort_index]
    if top_n > len(key_array):
        top_n = len(key_array)
    return zip(key_array_sorted[0:top_n], feature_array_sorted[0:top_n])


def add_poi_mail_features(data_dict):
    '''
    Behavior:   Calculates new variables and returns new dictionary with
                these variables included
    Input:      data_dict (list of dicionaries)
    Output:     data_dict (list of dicionaries)
    '''
    from numbers import Number

    for key in data_dict.keys():
        if isinstance(data_dict[key]['from_poi_to_this_person'], Number):
            from_poi_pct = float(data_dict[key]['from_poi_to_this_person']) / \
                            data_dict[key]['from_messages']
        else:
            from_poi_pct = 'NaN'

        if isinstance(data_dict[key]['from_this_person_to_poi'], Number):
            to_poi_pct = float(data_dict[key]['from_this_person_to_poi']) / \
                data_dict[key]['to_messages']
        else:
            from_poi_pct = 'NaN'
        data_dict[key]['from_poi_pct'] = from_poi_pct
        data_dict[key]['to_poi_pct'] = to_poi_pct
    return data_dict


def count_nans(features, data):
    '''
    Behavior:   caounts if non-numerical values are present in data.
    Input:      features (list of strings), data (array)
    Output:     list of tuples showing how many NaN each variable contains.
    '''
    from numbers import Number
    import numpy as np

    nan_array = []
    for index, variable in enumerate(data.T):
        variable_name = features[index]
        nan = 0
        for obs in variable:
            print obs
            nan += 1
        nan_array.append(nan)
    return zip(features, nan_array)


def evaluate_estimator(pred_label, true_label):
    '''
    Behavior:   takes predictions and true labels and returns score metrics
    Input:      pred_label (list), true_label (list)
    Output:     dictionary of rounded score metrics values
    '''
    import sklearn.metrics as m

    acuracy = round(m.accuracy_score(true_label, pred_label), 3)
    precision = round(m.precision_score(true_label, pred_label), 3)
    recall = round(m.recall_score(true_label, pred_label), 3)
    return ({"acuracy": acuracy, "precision": precision, "recall": recall})


def lasso_selection(features_train, labels_train, features_list):
    '''
    Behavior:   Plots coefficients from a Lasso regression
    Input:      features_train (array), labels_train (array),
                features list (list of strings)
    Output:     None, shows plot
    '''
    from sklearn.linear_model import Lasso
    import matplotlib.pyplot as plt
    import numpy as np

    from sklearn.model_selection import GridSearchCV
    parameters = {'alpha': np.arange(0.1, 2, 0.1)}
    Lasso = Lasso()
    Lasso_search = GridSearchCV(Lasso, parameters)
    Lasso_search.fit(features_train, labels_train)
    print Lasso_search.best_estimator_
    Lasso_best = Lasso_search.best_estimator_
    plt.barh(range(len(Lasso_best.coef_)), Lasso_best.coef_,
             color="b", align='center')
    plt.yticks(range(len(Lasso_best.coef_)), features_list[1:])
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    plt.show()
    return None


def plot_feature_importance(clf, X, y, features_list):
    '''
    Altered the code from: http://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
    Behavior:   Plots features importance from AdaBoostClassifier
    Input:      clf (AdaBoostClassifier instance),
                X (array), y (array), feature_list (list of strings)
    Output:     None, shows plot
    '''
    from sklearn.ensemble import AdaBoostClassifier
    import matplotlib.pyplot as plt
    import numpy as np

    X = np.array(X)
    labels = features_list[1:]
    importances = clf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    plt.figure()
    plt.title("Feature importances")
    plt.barh(range(X.shape[1]), importances[indices], color="b",
             xerr=std[indices], align="center")
    plt.yticks(range(X.shape[1]), np.array(labels)[indices])
    plt.ylim([-1, X.shape[1]])
    plt.tight_layout(pad=0., w_pad=0., h_pad=0.)
    plt.show()
    return None

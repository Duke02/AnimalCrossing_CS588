import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC, LinearSVC

from constants import RANDOM_STATE, SVM_ITERATIONS, N_JOBS


def get_linear_svm_classifier():
    params = {'linearsvc__C': np.arange(0.125, 0.375, .025),
              'linearsvc__fit_intercept': [True, False],
              'linearsvc__tol': np.arange(.000001, .00001, .000005)}

    # need to scale data using Standard Scaler
    return 'Linear SVM', \
           make_pipeline(MinMaxScaler(), LinearSVC(random_state=RANDOM_STATE, max_iter=SVM_ITERATIONS)), \
           params


def get_rbf_svm_classifier():
    params = {
        'svc__gamma': ['scale', 'auto'],
        'svc__shrinking': [True, False],
        'svc__tol': np.arange(.00001, .00005, .000005),
        'svc__C': np.arange(.125, .375, .025)
    }

    return 'RBF SVM', \
           make_pipeline(MinMaxScaler(), SVC(kernel='rbf', random_state=RANDOM_STATE, max_iter=SVM_ITERATIONS)), \
           params


def get_naive_bayes_classifier():
    params = {
        'var_smoothing': np.arange(10 ** -12, 10 ** -10, 5 * 10 ** - 12)
    }
    return 'Naive Bayes', GaussianNB(), params


def get_random_forest_classifier():
    params = {
        'ccp_alpha': np.arange(.01, .03, .005),
        'max_features': ['auto', None, 'sqrt'],
        'max_depth': [None] + list(range(3, 11, 2)),
        'n_estimators': list(range(50, 150, 10))
    }
    return 'Random Forest', RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=N_JOBS), params

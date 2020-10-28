import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC

from constants import RANDOM_STATE, SVM_ITERATIONS, N_JOBS


def get_linear_svm_classifier():
    params = {'linearsvc__C': np.arange(0.25, 1.0, .05),
              'linearsvc__fit_intercept': [True, False],
              'linearsvc__tol': np.arange(10 ** -5, 5 * 10 ** -4, 25 * 10 ** -6)}

    # need to scale data using Standard Scaler
    return 'Linear SVM', \
           make_pipeline(StandardScaler(), LinearSVC(random_state=RANDOM_STATE, max_iter=SVM_ITERATIONS)), \
           params


def get_rbf_svm_classifier():
    params = {
        'svc__gamma': ['scale', 'auto'],
        'svc__shrinking': [True, False],
        'svc__tol': np.arange(.5 * 10 ** -4, .5 * 10 ** -2, 5 * 10 ** -3),
        'svc__C': np.arange(.25, 2.5)
    }

    return 'RBF SVM', \
           make_pipeline(StandardScaler(), SVC(kernel='rbf', random_state=RANDOM_STATE, max_iter=SVM_ITERATIONS)), \
           params


def get_naive_bayes_classifier():
    params = {
        'var_smoothing': np.arange(10 ** -10, 10 ** -8)
    }
    return 'Naive Bayes', GaussianNB(), params


def get_random_forest_classifier():
    params = {
        'ccp_alpha': np.arange(0, .04, .01),
        'max_features': ['auto', None, 'sqrt'] + list(np.arange(.1, .75, .225)),
        'max_depth': [None] + list(range(3, 10, 2)),
        'n_estimators': [10, 50, 100, 150]
    }
    return 'Random Forest', RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=N_JOBS), params

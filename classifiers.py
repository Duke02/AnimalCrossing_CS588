from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC

from constants import RANDOM_STATE


def get_linear_svm_classifier():
    # need to scale data using Standard Scaler
    return make_pipeline([StandardScaler(), LinearSVC(random_state=RANDOM_STATE)])


def get_rbf_svm_classifier():
    return make_pipeline([StandardScaler(), SVC(kernel='rbf', random_state=RANDOM_STATE)])


def get_naive_bayes_classifier():
    return GaussianNB()


def get_random_forest_classifier():
    return RandomForestClassifier(random_state=RANDOM_STATE)

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

def compare_classifiers(data, targets):
    classifiers = ['GaussianNB', 'SVC', 'KNeighborsClassifier', 'DecisionTreeClassifier']
    max_score = 0

    for alg in classifiers:
        clf = eval(alg)()
        score = cross_val_score(clf, data, targets, cv=10).mean()
        if score > max_score:
            max_score = score
            max_alg = alg

    return max_alg, max_score
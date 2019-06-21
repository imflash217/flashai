"""
A standard machine learning task using sacred's magic
"""

from sacred import Experiment
from sacred.observers import FileStorageObserver
from sklearn import svm, datasets, model_selection

ex = Experiment("magicML")

ex.observers.append(
        FileStorageObserver.create("my_runs_magicML")
        )

# configuration is defined through local variables
@ex.config
def cfg():
    C = 1.0
    gamma = 0.7
    kernel = "rbf"
    seed = 217

@ex.capture
def get_model(C, gamma, kernel):
    return svm.SVC(C=C, kernel=kernel, gamma=gamma)

# Using automain to enable command-line integration
@ex.automain
def run():
    X, y = datasets.load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = model.selection.train_test_split(X, y, test_size=0.2)
    clf = get_model()   #Parameters as injected automatically due to @ex.capture decoration
    clf.fit(X,_train, y_train)
    return clf.score(X_test, y_test)

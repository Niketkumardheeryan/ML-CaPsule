from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingClassifier


class Ensemble:
    def __init__(self):
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self):
        x, y = load_breast_cancer(return_X_y=True)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.25, random_state=23)

    @staticmethod
    def __Classifiers__(name=None):
        # See for reproducibility
        random_state = 23
        
        if name == 'decision_tree':
            return DecisionTreeClassifier(random_state=random_state)
        if name == 'kneighbors':
            return KNeighborsClassifier()
        if name == 'logistic_regression':
            return LogisticRegression(random_state=random_state)

    def __DecisionTreeClassifier__(self):
        
        # Decision Tree Classifier
        decision_tree = Ensemble.__Classifiers__(name='decision_tree')
        
        # Train Decision Tree
        decision_tree.fit(self.x_train, self.y_train)

    def __KNearestNeighborsClassifier__(self):
        
        # K-Nearest Neighbors Classifier
        knn = Ensemble.__Classifiers__(name='kneighbors')
        
        # Train K-Nearest Neighbos
        knn.fit(self.x_train, self.y_train)

    def __LogisticRegression__(self):
        
        # Decision Tree Classifier
        logistic_regression = Ensemble.__Classifiers__(name='logistic_regression')
        
        # Init Grid Search
        logistic_regression.fit(self.x_train, self.y_train)
    
    def __VotingClassifier__(self):

        # Instantiate classifiers
        decision_tree = Ensemble.__Classifiers__(name='decision_tree')
        knn = Ensemble.__Classifiers__(name='kneighbors')
        logistic_regression = Ensemble.__Classifiers__(name='logistic_regression')

        # Voting Classifier initialization
        vc = VotingClassifier(estimators=[('decision_tree', decision_tree), 
                                        ('knn', knn), ('logistic_regression', 
                                        logistic_regression)], voting='soft')
        
        # Init Grid Search
        vc.fit(self.x_train, self.y_train)

if __name__ == "__main__":

    ensemble = Ensemble()
    ensemble.load_data()
    ensemble.__StackingClassifier__()
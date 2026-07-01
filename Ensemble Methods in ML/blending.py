import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

class Ensemble:
    def __init__(self):
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self):
        x, y = load_breast_cancer(return_X_y=True)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.15, random_state=23)
        self.x_train, self.x_val, self.y_train, self.y_val = train_test_split(self.x_train, self.y_train, test_size=0.3, random_state=23)
    
    def BlendingClassifier(self):

        # Define weak learners
        weak_learners = [('dt', DecisionTreeClassifier()),
                        ('knn', KNeighborsClassifier()),
                        ('rf', RandomForestClassifier()),
                        ('gb', GradientBoostingClassifier()),
                        ('gn', GaussianNB())]
        
        # Finaler learner or meta model
        final_learner = LogisticRegression()

        train_meta_model = None
        test_meta_model = None

        # Start stacking
        for clf_id, clf in weak_learners:
            
            # Predictions for each classifier based on k-fold
            val_predictions, test_predictions = self.train_level_0(clf)
            
            # Stack predictions which will form 
            # the inputa data for the data model
            if isinstance(train_meta_model, np.ndarray):
                train_meta_model = np.vstack((train_meta_model, val_predictions))
            else:
                train_meta_model = val_predictions

            # Stack predictions from test set
            # which will form test data for meta model
            if isinstance(test_meta_model, np.ndarray):
                test_meta_model = np.vstack((test_meta_model, test_predictions))
            else:
                test_meta_model = test_predictions
        
        # Transpose train_meta_model
        train_meta_model = train_meta_model.T

        # Transpose test_meta_model
        test_meta_model = test_meta_model.T
        
        # Training level 1
        self.train_level_1(final_learner, train_meta_model, test_meta_model)


    def train_level_0(self, clf):
        # Train with base x_train
        clf.fit(self.x_train, self.y_train)
        
        # Generate predictions for the holdout set (validation)
        # These predictions will build the input for the meta model
        val_predictions = clf.predict(self.x_val)
        
        # Generate predictions for original test set
        # These predictions will be used to test the meta model
        test_predictions = clf.predict(self.x_test)

        return val_predictions, test_predictions

    def train_level_1(self, final_learner, train_meta_model, test_meta_model):
        # Train is carried out with final learner or meta model
        final_learner.fit(train_meta_model, self.y_val)
       
        # Getting train and test accuracies from meta_model
        print(f"Train accuracy: {final_learner.score(train_meta_model,  self.y_val)}")
        print(f"Test accuracy: {final_learner.score(test_meta_model, self.y_test)}")
        

if __name__ == "__main__":
    ensemble = Ensemble()
    ensemble.load_data()
    ensemble.BlendingClassifier()
import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from .Datas_for_train import DataPrep
from sklearn.feature_extraction.text import TfidfVectorizer
from .liwc_vectorizer import LIWCVectorizer

class Model():
    def __init__(self, type='tfidf'):
        self.rfr = RandomForestRegressor(bootstrap=True,
         max_features='sqrt',
         min_samples_leaf=1,
         min_samples_split=2,
         n_estimators= 200)
        self.type = type         
        self.rfc = RandomForestClassifier(max_features='sqrt', n_estimators=110)
        self.tfidf = TfidfVectorizer(stop_words='english', strip_accents='ascii')
        self.liwc = LIWCVectorizer()

    def fit(self, X, y, regression=True):
        if self.type == 'tfidf':
            X = self.tfidf.fit_transform(X) # devuelve la matriz termino documento
        elif self.type == 'liwc':
            X = self.liwc.vectorize_docs(X)
        else:
            raise Exception('Error!!!!!!!!!!!!!!!!')
            
        if regression:
            self.rfr = self.rfr.fit(X, y)
        else:
            self.rfc = self.rfc.fit(X, y)

    def predict(self, X, regression=True):
        if self.type == 'tfidf':
            X = self.tfidf.transform(X) # devuelve la matriz termino documento
        elif self.type == 'liwc':
            X = self.liwc.vectorize(X)
        else:
            raise Exception('Error!!!!!!!!!!!!!!!!')

        if regression:
            return self.rfr.predict(X)
        else:
            return self.rfc.predict(X)
    
    def predict_proba(self, X, regression=False):
        X = self.tfidf.transform(X)
      
        if regression:
            raise ValueError('Cannot predict probabilites of a regression!')
        else:
            return self.rfc.predict_proba(X)
        
def train_models(vectorizer='tfidf'):
    traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
    print('Vectorizer = {0}'.format(vectorizer))
    model = Model(vectorizer)

    for trait in traits:
        dp = DataPrep()
        X_regression, y_regression = dp.prep_data(trait, regression=True, model_comparison=False)        
        X_categorical, y_categorical = dp.prep_data(trait, regression=False, model_comparison=False)
        
        
        print('Fitting trait ' + trait + ' regression model...')
        model.fit(X_regression, y_regression, regression=True)
        print('Done!')
        print('Fitting trait ' + trait + ' categorical model...')
        model.fit(X_categorical, y_categorical, regression=False)
        print('Done!')
        with open('logic/models/{1}_categorical_model_{0}.pkl'.format(vectorizer, trait), 'wb') as f:
            pickle.dump(model, f)
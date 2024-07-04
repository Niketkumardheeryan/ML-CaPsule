from plotters import learning_curves
from Model import Model
from Datas_for_train import DataPrep
from sklearn.model_selection import ShuffleSplit

traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
vectorizers = {True:'tfidf', False:'liwc'}
dp = DataPrep()
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0) 

for vectorizer in vectorizers:
    for trait in traits:
        model = Model(vectorizers[vectorizer])
        X, y = dp.prep_data(trait, regression=False)
        score = learning_curves(model, X, y, cv, trait, vectorizers[vectorizer])
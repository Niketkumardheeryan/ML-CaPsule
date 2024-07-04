from .Model import Model, train_models
import pickle
import numpy as np
import os, sys

class Predictor():
    def __init__(self, vetorice='tfidf'):
        self.traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
        self.models = {}
        self.modelsreg = {}
        self.vetorice = vetorice        
        self.load_models()
        self.dicname = {'sOPN': " Score de Apertura ", 'cOPN': " Clasification de Apertura ", 'sCON': " Score de Conciencia ", 'cCON': " Clasification de Conciencia ", 
        'sEXT': " Score de Extraverión ", 'cEXT': " Clasification de Extraverión ", 'sAGR': " Score de Amabilidad ", 'cAGR': " Clasification de Amabilidad ", 
        'sNEU': " Score de Neurotimos ", 'cNEU': " Clasification de Neurotismo "

        }

    def load_models(self):
        r = ['categorical', 'regression']
        for trait in self.traits:
            with open('logic/models/{1}_categorical_model_{0}.pkl'.format(self.vetorice, trait), 'rb') as f:
                self.models[trait] = pickle.load(f)

    def predict(self, X, traits='All', predictions='All'):
        predictions = {}
        if traits == 'All':
            for trait in self.traits:
                pkl_model = self.models[trait]
                
                trait_scores = pkl_model.predict(X, regression=True).reshape(1, -1)
                predictions['pred_s'+trait] = trait_scores.flatten()[0]

                
                trait_categories = pkl_model.predict(X, regression=False)
                predictions['pred_c'+trait] = str(trait_categories[0])

               
                trait_categories_probs = pkl_model.predict_proba(X)
                predictions['pred_prob_c'+trait] = trait_categories_probs[:, 1][0]
            
            result = self.print_Pred(predictions, X)

        return result
    
    def print_Pred(self, prediction, X):
        result = []
        result.append("Evaluated Text: " + X[0])
        for t, v in prediction.items():
            s = t.split('_')
            try:
                k = s[2]
            except:
                k = s[1]
            text = '*Predicting the ' +str(self.dicname[k]) + ' The Result ->:  ' +  str(v) 
            print(text + ': \n' + '\n')
            result.append(text)
        return result


if __name__ == '__main__':
    P = Predictor()
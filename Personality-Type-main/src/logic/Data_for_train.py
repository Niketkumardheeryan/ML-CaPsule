import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataPrep():
    def __init__(self):
        self.trait_cat_dict = { 
            'O': 'cOPN',
            'C': 'cCON',
            'E': 'cEXT',
            'A': 'cAGR',
            'N': 'cNEU',
            'OPN': 'cOPN',
            'CON': 'cCON',
            'EXT': 'cEXT',
            'AGR': 'cAGR',
            'NEU': 'cNEU',
            'Openness': 'cOPN',
            'Conscientiousness': 'cCON',
            'Extraversion': 'cEXT',
            'Agreeableness': 'cAGR',
            'Neuroticism': 'cNEU'
            }
        self.trait_score_dict = {
            'O': 'sOPN',
            'C': 'sCON',
            'E': 'sEXT',
            'A': 'sAGR',
            'N': 'sNEU',
            'OPN': 'sOPN',
            'CON': 'sCON',
            'EXT': 'sEXT',
            'AGR': 'sAGR',
            'NEU': 'sNEU',
            'Openness': 'sOPN',
            'Conscientiousness': 'sCON',
            'Extraversion': 'sEXT',
            'Agreeableness': 'sAGR',
            'Neuroticism': 'sNEU'
            }
        self.LIWC_features = [
            'WPS', 'Unique', 'Dic', 'Sixltr', 'Negate', 'Assent', 'Article', 'Preps', 'Number',
            'Pronoun', 'I', 'We', 'Self', 'You', 'Other',
            'Affect', 'Posemo', 'Posfeel', 'Optim', 'Negemo', 'Anx', 'Anger', 'Sad',
            'Cogmech', 'Cause', 'Insight', 'Discrep', 'Inhib', 'Tentat', 'Certain',
            'Senses', 'See', 'Hear', 'Feel',
            'Social', 'Comm', 'Othref', 'Friends', 'Family', 'Humans',
            'Time', 'Past', 'Present', 'Future',
            'Space', 'Up', 'Down', 'Incl', 'Excl', 'Motion',
            'Occup', 'School', 'Job', 'Achieve',
            'Leisure', 'Home', 'Sports', 'TV', 'Music',
            'Money',
            'Metaph', 'Relig', 'Death', 'Physcal', 'Body', 'Sexual', 'Eating', 'Sleep', 'Groom',
            'Allpct', 'Period', 'Comma', 'Colon', 'Semic', 'Qmark', 'Exclam', 'Dash', 'Quote', 'Apostro', 'Parenth', 'Otherp',
            'Swear', 'Nonfl', 'Fillers',
        ]

    def prep_data(self, trait, regression=False, model_comparison=False):
        df_status = self.extract_text_from_corpus()
        X = df_status['STATUS']

        if regression:
            y_column = self.trait_score_dict[trait]
        else:
            y_column = self.trait_cat_dict[trait]
            
        y = df_status[y_column]

        return X, y

    def extract_text_from_corpus(self):
        df = pd.read_csv('logic/data/myPersonality/mypersonality_final.csv', encoding="ISO-8859-1")
        df = self.convert_traits_to_boolean(df)
        return df

    def convert_traits_to_boolean(self, df):
        trait_columns = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']
        d = {'y': True, 'n': False}

        for trait in trait_columns:
            df[trait] = df[trait].map(d)

        return df

    def load_data(self, filepath):
        return pd.read_csv(filepath, encoding="ISO-8859-1")

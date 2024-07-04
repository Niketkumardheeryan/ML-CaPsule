from Datas_for_train import DataPrep
from sklearn.feature_extraction.text import TfidfVectorizer
from liwc_vectorizer import LIWCVectorizer
from scipy.sparse.csr import csr_matrix
from scipy.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
import time, numpy
import pandas as pd
from info_gain import info_gain
from utils import write_to_xlsx

traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
dp = DataPrep()


def extract_vectorized_elements(tfidf_features):
    corpus = dp.extract_text_from_corpus()['STATUS']

    mx = None
    features = None
    xlabel = None

    if tfidf_features:
        tfidf = TfidfVectorizer(stop_words='english', strip_accents='ascii')
        mx = tfidf.fit_transform(corpus).toarray()
        features = tfidf.get_feature_names()
        xlabel = 'Tfidf_features'
    else:
        liwc = LIWCVectorizer()
        mx = liwc.vectorize_docs(corpus)
        features = liwc.features
        xlabel = 'LIWC_features'

    return mx, features, xlabel

def correlate(mx, features_names, xlabel, regression = False):
    matrix, pvalues, start = [], [], time.time()

    for i in range(0,len(features_names)):
        matrix.append([])
        pvalues.append([])
        col = mx[:,i]
        for trait in traits:
            _, y = dp.prep_data(trait, regression=regression)
            r, pval = pearsonr(col,y) #spearmanr(col,y).correlation

            print('r={0}  pval={1}'.format(r,pval))

            matrix[i].append(r)
            pvalues[i].append(pval)

    matrix = pd.DataFrame(matrix, columns=traits, index=features_names)
    pvalues = pd.DataFrame(pvalues, columns=traits, index=features_names)


    for trait in traits:
        cor = matrix.loc[:, trait].to_numpy()
        pv = pvalues.loc[:, trait].to_numpy()

        final = pd.DataFrame({'cor':cor,'pvalue':pv}, index=features_names)
        final = final[final.pvalue < 0.1]
        print('Trait: {0}'.format(trait))
        final = final.sort_values(ascending = False, by = 'cor')
        print(final[0:10])
        print('\n\n')

    print('time = {0}'.format(time.time() - start)) 
    return (matrix, None)

def make_matrix(vectorize_like_tfidf):
    mx, features, xlabel = extract_vectorized_elements(vectorize_like_tfidf)
    matrix, infogain = correlate(mx, features, xlabel)
    vector_type = 'tfidf' if vectorize_like_tfidf else 'liwc'
    write_to_xlsx(matrix, traits, features, 'correlation_{0}.xlsx'.format(vector_type))
    #write_to_xlsx(infogain, traits, features, 'infogain_{0}.xlsx'.format(vector_type))
    return (matrix, infogain)

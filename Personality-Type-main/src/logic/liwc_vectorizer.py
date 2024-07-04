from liwc.liwc import Liwc
import pandas as pd
import time 

class LIWCVectorizer:
    def __init__(self):
        self.liwc = Liwc('logic/data/LIWC2007_English100131.dic')
        self.features = list(self.liwc.categories.values())
        self.featuresidx = dict([(f,i) for i,f in enumerate(self.features)])

    def vectorize(self, doc):
        doc = doc.lower().split(' ')
        parse = self.liwc.parse(doc)
        vector = [0]*len(self.features)
        for v in parse:
            vector[self.featuresidx[v]] = parse[v]/len(doc)
        return vector

    def vectorize_docs(self, documents):
        vectors = []
        for doc in documents:
            vectors.append(self.vectorize(doc))
        return vectors

    def make_corpus_liwc(self, corpus_path):
        df_essays = pd.read_csv(corpus_path, encoding="ISO-8859-1")
        corpus = df_essays['STATUS']
        vector = self.vectorize_docs(corpus)

        dataframe = pd.DataFrame(vector, columns=self.features)
        
        scores = df_essays.loc[:, ['sEXT','sNEU','sAGR','sCON','sOPN','cEXT','cNEU','cAGR','cCON','cOPN']]
        dataframe = dataframe.join(scores)

        writer = pd.ExcelWriter('./data/liwc_corpus.xlsx', engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='Sheet1')
        writer.save()

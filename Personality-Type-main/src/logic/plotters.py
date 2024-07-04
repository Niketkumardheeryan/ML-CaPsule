import pandas as pd
import time, os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import learning_curve


def show(data, foobar, feature_id=None, verbose=0, solid=False, random_seed=43):
    """
    Show clusters of data using john as clusterer algorithm.
    """
    samples, features = data.shape
    
    if feature_id is None:
        feature_id = [i for i in range(features)]
        
    features = len(feature_id)
    
    clusterid = foobar.fit_predict(data)
    
    clusters = max(clusterid) + 1
    
    np.random.seed(43)
    colors = [ [np.random.random() for _ in range(3)]  for f in range(clusters)]
    colors.append("white") # Color -1
    
    if verbose >= 1:
        print("Samples:", samples)
        print("Features:", features)
        print("Clusters:", clusters)

    for i in range(features):
        for j in range(i + 1, features):
            fi, fj = feature_id[i], feature_id[j]
            for col in range(-1, clusters):
                value = data[clusterid==col]

                plt.subplot(features - 1,features - 1, i * (features-1) + j)


                
                if solid:
                    kwargs = {'color' : colors[col]}
                else:
                    kwargs = {'facecolor' : colors[col]}
                
                plt.scatter(value[:,fi], value[:,fj], **kwargs)     
    plt.show()

def plot_to2(X, y):
    to_plot = PCA(2).fit_transform(X)

    plt.scatter(to_plot[:,0], to_plot[:,1], c=y, cmap=plt.cm.Paired)
    plt.title('Actual labels')
    plt.show()

def learning_curves(estimator, X, y, cv, trait, vectorizer):
    start = time.time()
    train_sizes, train_scores, validation_scores = learning_curve(
    estimator, X, y, cv = cv, scoring = 'accuracy', verbose=1)
    end = time.time()

    train_scores_mean = train_scores.mean(axis = 1)
    validation_scores_mean = validation_scores.mean(axis = 1)

    train_series_mean = pd.Series(train_scores_mean, index = train_sizes)
    validation_series_mean = pd.Series(validation_scores_mean, index = train_sizes)

    '''
    print('train_size = {0}'.format(train_sizes))
    print('Mean training scores\n\n', train_series_mean)
    print('-' * 20)
    print('\nMean validation scores\n\n', validation_series_mean)
    '''

    m1 = train_scores_mean.mean()
    m2 = validation_scores_mean.mean()
    model_score = (m1 + m2)/2

    delay = start -  end

    
    plt.plot(train_sizes, train_scores_mean, label = 'Training error')
    plt.plot(train_sizes, validation_scores_mean, label = 'Validation error')

    plt.ylabel('Accuracy', fontsize = 14)
    plt.xlabel('Training set size', fontsize = 14)
    title = 'Learning curves for a ' + str(estimator).split('(')[0] + ' model for {0} trait vectorizing with {1} score = {2}'.format(trait,vectorizer, model_score)
    plt.title(title, fontsize = 18, y = 1.03)
    plt.legend()
    plt.ylim(-2,3)
    plt.savefig('{0}_{1}_chart.png'.format(trait,vectorizer))
    plt.show()

    return model_score

# Evaluate model performance.

from train import model_training
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score


def evaluate():
    models, X_test, y_test = model_training()
    
    metric_calculation_results = { model : {
        'prediction':'',
        'accuracy':0,
        'precision':0,
        'recall':0,
        'f1':0        
    } for model in models}
    
    print("="*50)
    for model in models:
        print(f"Prediction on test data by {model}")
        prediction  =  models[model].predict(X_test)
        
        accuracy = round(accuracy_score(y_test,prediction),2)
        f1 = round(f1_score(y_test,prediction),2)
        precision = round(precision_score(y_test,prediction),2)
        recall = round(recall_score(y_test,prediction),2)
        
        print(f"    Accuracy Score : {accuracy}")
        print(f"    F1 Score : {f1}")
        print(f"    Recall Score : {recall}")
        print(f"    Precison Score : {precision}")
        
        metric_calculation_results[model]['prediction'] = prediction
        metric_calculation_results[model]['accuracy'] = accuracy
        metric_calculation_results[model]['precision'] = precision
        metric_calculation_results[model]['f1'] = f1
        metric_calculation_results[model]['recall'] = recall
        
    return y_test, metric_calculation_results

if __name__ == "__main__":
    evaluate()
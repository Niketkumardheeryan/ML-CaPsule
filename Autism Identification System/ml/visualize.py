# All graphs and plots.

from evaluate import evaluate
import matplotlib.pyplot as plt 
import os
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# bar chart for accuracy ,precision, recall, f1 in order
def create_bar_chart(models,metric,metric_name):
    plt.bar(x =models, height=metric )
    plt.title(f"{metric_name} Scores of Models")
    path = os.path.join('charts',f'model_{metric_name.lower()}_chart.png')
    plt.savefig(
        path
    )
    print(f"Path for {metric_name} graph : {str(path)}")
    plt.close()
    
    
def get_bar_charts(evaluation_results):
    print()
    print("="*50)
    print("Creating and Saving bar charts for Accuracy, Precision, Recall, F1 Scores")
    
    accuracy = []
    precision  = []
    f1 = []
    recall = []
    
    models = []
    
    for model in evaluation_results:
        models.append(model)
        accuracy.append(evaluation_results[model]['accuracy'])
        recall.append(evaluation_results[model]['recall'])
        f1.append(evaluation_results[model]['f1'])
        precision.append(evaluation_results[model]['precision'])
        
    
    if not os.path.exists('charts'):
        os.mkdir('charts')
    
    create_bar_chart(
        models=models,
        metric=precision,
        metric_name='Precision'
        )
    
    create_bar_chart(
        models=models,
        metric=accuracy ,
        metric_name='Accuracy'
        ) 
    
    create_bar_chart(
        models=models,
        metric=f1,
        metric_name='F1' 
        )
    
    create_bar_chart(
        models=models,
        metric=recall,
        metric_name='Recall'
        )
    
    
    print("Saved charts successfully!!")

# confusion matrix heatmaps
def get_confusion_matrix(y_true,y_pred,model_name,classes = ['No','Yes']):
    
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
    disp.plot(cmap=plt.cm.Blues)
    
    plt.xlabel('Prediction', fontsize=11)
    plt.ylabel('Actual', fontsize=11)
    plt.gca().xaxis.set_label_position('top')
    plt.gca().xaxis.tick_top()
    plt.gca().figure.subplots_adjust(bottom=0.2)
    plt.gca().figure.text(0.5, 0.05, f'Confusion Matrix for {model_name}', ha='center', fontsize=13)
    
    if not os.path.exists('charts'):
        os.mkdir('charts')
    
    path = os.path.join('charts',f'confusion_matrix_{"_".join(model_name.split(" ")).lower()}.png')
    plt.savefig(path)
    print(f"Saved Confusion matrix for {model_name}")
    print(f"Path for {model_name} confusion matrix : {str(path)}")
    print()
    plt.close()
    
def get_confusion_matrix_for_all_models(y_test,results):
    print()
    print("="*50)
    models = results.keys()
    print(f"Creating and saving confusion matrix for {', '.join(models)}")
    print()
    for model in models:
        get_confusion_matrix(
            y_true=y_test,
            y_pred=results[model]['prediction'],
            model_name=model
            )
    print(f"Saved confusion matrix for {', '.join(models)} successfully!! ")
    
    
# Optional ROC curves, precision recall curve, feature importance  


if __name__ == "__main__":

    y_test, results = evaluate()

    get_bar_charts(results)
    models = results.keys()
    
    get_confusion_matrix_for_all_models(
        y_test=y_test,
        results=results
        )
    
    
    

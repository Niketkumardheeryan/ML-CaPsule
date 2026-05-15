"""
Save and load trained models.
"""

from train import model_training
import joblib
import os

def save_models():
    models,_,_ = model_training()
    
    print()
    print("="*50)
    if not os.path.exists('saved_models'):
            os.mkdir('saved_models')
    for model in models:
        print(f"Saving {model} after training")
        
        
            
        path = os.path.join('saved_models',f'{'_'.join(model.split(" ")).lower()}.pkl')
        joblib.dump(
            value=models[model],
            filename=path
        )
        print(f"Path for {model} : {str(path)}")
        print()
    print(f"Saved {', '.join(models.keys())} successfully !!")

def load_model(model_name='random_forest'):
    models = {}
    if not os.path.exists('saved_models'):
        os.mkdir('saved_models')
        
    for _,_,files in os.walk("saved_models"):
        for file in files:
            models[file.split('.pkl')[0]] = os.path.join('saved_models',file)
            
    if model_name not in models.keys():
        print(f"{model_name} not in saved_models folder")
        return 
    
    return joblib.load(models[model_name])

def load_scaler():
    if not os.path.exists('saved_others'):
        print(f"Model not saved in or as {os.path.exists('saved_others')}")
        return 
    return joblib.load(
        os.path.join('saved_others','scaler.pkl')
    )
    
def load_feature_columns_name():
    if not os.path.exists('saved_others'):
        print(f"Model not saved in or as {os.path.exists('saved_others')}")
        return 
    return joblib.load(
       os.path.join('saved_others','feature_columns.pkl') 
    )
    
if __name__ == "__main__":
    # save_models()
    load_model()
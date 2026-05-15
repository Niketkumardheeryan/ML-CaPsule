# Train all models.

from models import get_models
from preprocessing import preprocessing_result 

def model_training():
    
    X_train,X_test,y_train, y_test = preprocessing_result()

    models = get_models()
    print()
    print("="*50)
    print("Model Training in process .... ")
    print()


    for model in models:
        print(f"Training Model {model}")
        
        models[model].fit(X_train,y_train)
                            
        print(f"Completed Training {model}")
        print()
        
    return models,X_test,y_test
    

if __name__  == "__main__":
    model_training()
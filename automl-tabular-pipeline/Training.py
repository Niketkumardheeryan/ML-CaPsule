import optuna
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

optuna.logging.set_verbosity(optuna.logging.WARNING)

class AutoMLTrainer:
    def __init__(self, preprocessor, n_trials=15):
        self.preprocessor = preprocessor
        self.n_trials = n_trials
        self.best_pipeline = None

    def optimize_and_fit(self, X, y):
        """Finds the best model configuration and parameters using Optuna optimization trials."""
        def objective(trial):
            classifier_name = trial.suggest_categorical("classifier", ["LogReg", "RandomForest", "GradientBoosting"])
            
            if classifier_name == "LogReg":
                c = trial.suggest_float("C", 1e-4, 10.0, log=True)
                model = LogisticRegression(C=c, max_iter=1000)
            elif classifier_name == "RandomForest":
                n_estimators = trial.suggest_int("n_estimators", 10, 100)
                max_depth = trial.suggest_int("max_depth", 2, 12)
                model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
            else:
                n_estimators = trial.suggest_int("gb_estimators", 10, 100)
                lr = trial.suggest_float("learning_rate", 0.01, 0.2, log=True)
                model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=lr, random_state=42)

            current_pipeline = Pipeline(steps=[
                ('preprocessor', self.preprocessor),
                ('classifier', model)
            ])
            
            return cross_val_score(current_pipeline, X, y, cv=3, scoring='accuracy').mean()

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=self.n_trials)
        
        best_params = study.best_params
        print(f"\n[AutoML Engine] Best Architecture Selected: {best_params['classifier']}")
        
        if best_params["classifier"] == "LogReg":
            best_model = LogisticRegression(C=best_params["C"], max_iter=1000)
        elif best_params["classifier"] == "RandomForest":
            best_model = RandomForestClassifier(n_estimators=best_params["n_estimators"], max_depth=best_params["max_depth"], random_state=42)
        else:
            best_model = GradientBoostingClassifier(n_estimators=best_params["gb_estimators"], learning_rate=best_params["learning_rate"], random_state=42)
            
        self.best_pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', best_model)
        ])
        
        self.best_pipeline.fit(X, y)
        return self.best_pipeline

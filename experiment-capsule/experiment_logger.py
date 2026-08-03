import json
from datetime import datetime
import os


class ExperimentLogger:
    def __init__(self, log_file="experiment_logs.json"):
        self.log_file = log_file

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def log_experiment(self, model_name, dataset, accuracy, parameters):
        experiment = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_name": model_name,
            "dataset": dataset,
            "accuracy": accuracy,
            "parameters": parameters
        }

        with open(self.log_file, "r") as f:
            data = json.load(f)

        data.append(experiment)

        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Experiment logged successfully!")



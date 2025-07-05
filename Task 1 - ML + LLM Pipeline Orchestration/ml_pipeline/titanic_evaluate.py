import os
import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score, f1_score
import mlflow.sklearn

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

# Use the MLflow tracking server
mlflow.set_tracking_uri("http://mlflow:5000")

mlflow.set_experiment("Titanic")

print("Tracking URI:", mlflow.get_tracking_uri())
experiment = mlflow.get_experiment_by_name("Titanic")
print("Experiment:", experiment)
if experiment is None:
    raise RuntimeError("MLflow experiment not found or not created!")

X_test = pd.read_csv(f'{DATA_PREFIX}/titanic_X_test.csv')
y_test = pd.read_csv(f'{DATA_PREFIX}/titanic_y_test.csv').values.ravel()

model = mlflow.sklearn.load_model("models:/titanic_rf_model/Latest")
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# LOG METRICS INSIDE THE RUN CONTEXT
with mlflow.start_run(run_name="Titanic_Eval"):
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("f1_score", f1)
    print(f"Accuracy: {acc:.3f}, F1: {f1:.3f}")
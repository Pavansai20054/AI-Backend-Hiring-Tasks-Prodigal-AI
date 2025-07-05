import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

# Use the Docker network MLflow tracking URI
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Titanic")
experiment = mlflow.get_experiment_by_name("Titanic")
print("Tracking URI:", mlflow.get_tracking_uri())
print("Experiment:", experiment)

X_train = pd.read_csv(f'{DATA_PREFIX}/titanic_X_train.csv')
y_train = pd.read_csv(f'{DATA_PREFIX}/titanic_y_train.csv').values.ravel()

with mlflow.start_run(run_name="Titanic_RF") as run:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    mlflow.sklearn.log_model(clf, "titanic_rf_model")
    mlflow.log_param("n_estimators", 100)
    print("Titanic model trained and logged.")
    # Register the model in the Model Registry
    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/titanic_rf_model"
    mlflow.register_model(model_uri, "titanic_rf_model")
    print("Titanic model registered to MLflow Model Registry.")
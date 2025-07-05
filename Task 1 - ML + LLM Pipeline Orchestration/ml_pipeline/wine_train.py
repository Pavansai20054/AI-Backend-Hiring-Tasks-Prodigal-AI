import os
import pandas as pd
import mlflow
import mlflow.sklearn
from xgboost import XGBRegressor

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("WineQuality")
experiment = mlflow.get_experiment_by_name("WineQuality")
print("Tracking URI:", mlflow.get_tracking_uri())
print("Experiment:", experiment)

X_train = pd.read_csv(f'{DATA_PREFIX}/wine_X_train.csv')
y_train = pd.read_csv(f'{DATA_PREFIX}/wine_y_train.csv').values.ravel()

with mlflow.start_run(run_name="Wine_XGB") as run:
    model = XGBRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    mlflow.sklearn.log_model(model, "wine_xgb_model")
    mlflow.log_param("n_estimators", 100)
    print("Wine model trained and logged.")
    # Register the model in the Model Registry
    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/wine_xgb_model"
    mlflow.register_model(model_uri, "wine_xgb_model")
    print("Wine model registered to MLflow Model Registry.")
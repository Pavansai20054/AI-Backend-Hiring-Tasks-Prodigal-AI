import os
import pandas as pd
import mlflow
import mlflow.sklearn
from xgboost import XGBRegressor
import glob

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("WineQuality")
experiment = mlflow.get_experiment_by_name("WineQuality")
print("Tracking URI:", mlflow.get_tracking_uri())
print("Experiment:", experiment)

def load_spark_csv_as_df(path):
    csv_files = glob.glob(f"{path}/part-*.csv")
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

X_train = load_spark_csv_as_df(f'{DATA_PREFIX}/wine_X_train.csv')
y_train = load_spark_csv_as_df(f'{DATA_PREFIX}/wine_y_train.csv').values.ravel()

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
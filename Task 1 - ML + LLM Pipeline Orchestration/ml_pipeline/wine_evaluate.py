import os
import pandas as pd
import mlflow
from sklearn.metrics import mean_squared_error, r2_score
import mlflow.sklearn
import glob

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

mlflow.set_tracking_uri("http://mlflow:5000")

mlflow.set_experiment("WineQuality")
experiment = mlflow.get_experiment_by_name("WineQuality")
print("Tracking URI:", mlflow.get_tracking_uri())
print("Experiment:", experiment)

def load_spark_csv_as_df(path):
    # If Spark output is a directory, load the part-*.csv file(s)
    if os.path.isdir(path):
        csv_files = glob.glob(f"{path}/part-*.csv")
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {path}")
        return pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)
    else:
        return pd.read_csv(path)

X_test = load_spark_csv_as_df(f'{DATA_PREFIX}/wine_X_test.csv')
y_test = load_spark_csv_as_df(f'{DATA_PREFIX}/wine_y_test.csv').values.ravel()

model = mlflow.sklearn.load_model("models:/wine_xgb_model/Latest")
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

with mlflow.start_run(run_name="Wine_Eval"):
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2_score", r2)
    print(f"MSE: {mse:.3f}, R2: {r2:.3f}")
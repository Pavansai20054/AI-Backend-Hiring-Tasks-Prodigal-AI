import os
import pandas as pd
import mlflow
from sklearn.metrics import mean_squared_error, r2_score
import mlflow.sklearn

DATA_PREFIX = os.environ.get('DATA_PREFIX', '/data')

# Use the MLflow tracking server
mlflow.set_tracking_uri("http://mlflow:5000")

mlflow.set_experiment("WineQuality")
experiment = mlflow.get_experiment_by_name("WineQuality")
print("Tracking URI:", mlflow.get_tracking_uri())
print("Experiment:", experiment)

X_test = pd.read_csv(f'{DATA_PREFIX}/wine_X_test.csv')
y_test = pd.read_csv(f'{DATA_PREFIX}/wine_y_test.csv').values.ravel()

model = mlflow.sklearn.load_model("models:/wine_xgb_model/Latest")
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

with mlflow.start_run(run_name="Wine_Eval"):
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2_score", r2)
    print(f"MSE: {mse:.3f}, R2: {r2:.3f}")
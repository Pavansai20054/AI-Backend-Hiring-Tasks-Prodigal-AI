from flask import Flask, request, jsonify
import mlflow
import mlflow.sklearn
import pandas as pd

# Always set the MLflow tracking URI
mlflow.set_tracking_uri("http://mlflow:5000")

app = Flask(__name__)

@app.route("/")
def home():
    return "ML Service is running!"

@app.route("/predict_titanic", methods=["POST"])
def predict_titanic():
    data = request.json
    model = mlflow.sklearn.load_model("models:/titanic_rf_model/Latest")
    df = pd.DataFrame([data])
    pred = model.predict(df)
    return jsonify({"prediction": int(pred[0])})

@app.route("/predict_wine", methods=["POST"])
def predict_wine():
    data = request.json
    model = mlflow.sklearn.load_model("models:/wine_xgb_model/Latest")
    df = pd.DataFrame([data])
    pred = model.predict(df)
    return jsonify({"prediction": float(pred[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
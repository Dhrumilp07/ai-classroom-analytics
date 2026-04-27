import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Create or set experiment
mlflow.set_experiment("Classroom Analytics Experiment")

@mlflow.trace(name="load_and_prepare_data")
def load_and_prepare_data():
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2
    )
    return X_train, X_test, y_train, y_test

@mlflow.trace(name="train_and_evaluate_model")
def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    return model, accuracy

with mlflow.start_run():
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    model, accuracy = train_and_evaluate_model(X_train, X_test, y_train, y_test)

    mlflow.log_param("model", "LogisticRegression")
    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "model")

    print("Model trained with accuracy:", accuracy)
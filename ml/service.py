# ml/service.py

from ml.algorithms.perceptron import Perceptron
from ml.utilis import load_training_data


def get_perceptron_results():
    X_train, y_train, X_val, y_val = load_training_data("train.csv")

    model = Perceptron(
        n_features=len(X_train[0]),
        learning_rate=0.01,
        epochs=30,
        threshold=0.0
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_val)
    accuracy = model.accuracy(X_val, y_val)
    confusion_matrix = model.confusion_matrix(X_val, y_val)

    comparison = []
    for i in range(min(10, len(y_val))):
        comparison.append({
            "index": i + 1,
            "predicted": predictions[i],
            "actual": y_val[i]
        })

    return {
        "accuracy": accuracy,
        "confusion_matrix": confusion_matrix,
        "epoch_errors": model.epoch_errors,
        "comparison": comparison
    }
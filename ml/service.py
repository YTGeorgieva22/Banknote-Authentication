import os

from ml.algorithms.perceptron import (Perceptron)
from ml.utilis import load_training_data, prepare_single_input, standardize_apply

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRAIN_FILE_PATH = os.path.join(BASE_DIR, "data/train.csv")

X_train, y_train, X_val, y_val, FEATURE_MEANS, FEATURE_STDS, DATA_MEAN_AGE, DATA_MEAN_FARE = load_training_data(TRAIN_FILE_PATH)

perceptron = Perceptron(
    n_features=len(X_train[0]),
    learning_rate=0.01,
    epochs=50
)
perceptron.fit(X_train, y_train)


def predict_passenger(form_data):
    raw_features = prepare_single_input(
        form_data=form_data,
        mean_age=DATA_MEAN_AGE,
        mean_fare=DATA_MEAN_FARE
    )

    scaled_features = standardize_apply([raw_features], FEATURE_MEANS, FEATURE_STDS)
    features = scaled_features[0]

    result = perceptron.predict([features])[0]
    score = perceptron.weighted_sum(features)

    return result, score

def get_perceptron_results():
    accuracy = perceptron.accuracy(X_val, y_val)
    confusion = perceptron.confusion_matrix(X_val, y_val)

    comparison = {
        "perceptron": round(accuracy * 100, 2),
        "baseline": 61.6,  # majority class baseline for Titanic
        "target": 80.0
    }

    return {
        "accuracy": accuracy,
        "epoch_errors": perceptron.epoch_errors,
        "confusion_matrix": confusion,
        "comparison": comparison
    }
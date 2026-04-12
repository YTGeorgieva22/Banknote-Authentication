# app/ml/utils.py

import csv
import random


def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def encode_sex(value):
    if value.strip().lower() == "female":
        return 1.0
    return 0.0


def encode_embarked(value):
    value = value.strip().upper()
    if value == "C":
        return 1.0
    elif value == "Q":
        return 2.0
    return 0.0  # S or missing


def read_csv_rows(file_path):
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def compute_means(rows):
    age_sum = 0.0
    age_count = 0
    fare_sum = 0.0
    fare_count = 0

    for row in rows:
        if row["Age"].strip() != "":
            age_sum += float(row["Age"])
            age_count += 1

        if "Fare" in row and row["Fare"].strip() != "":
            fare_sum += float(row["Fare"])
            fare_count += 1

    mean_age = age_sum / age_count if age_count > 0 else 0.0
    mean_fare = fare_sum / fare_count if fare_count > 0 else 0.0

    return mean_age, mean_fare


def row_to_features(row, mean_age, mean_fare):
    age = safe_float(row["Age"], mean_age) if row["Age"].strip() != "" else mean_age
    fare = safe_float(row["Fare"], mean_fare) if row["Fare"].strip() != "" else mean_fare

    embarked_value = row["Embarked"].strip() if "Embarked" in row and row["Embarked"] is not None else ""
    if embarked_value == "":
        embarked_value = "S"

    features = [
        float(row["Pclass"]),              # passenger class
        encode_sex(row["Sex"]),            # male/female
        age,                               # age
        float(row["SibSp"]),               # siblings/spouses
        float(row["Parch"]),               # parents/children
        fare,                              # fare
        encode_embarked(embarked_value)    # embarked port
    ]

    return features


def standardize_train_test(X_train, X_test):
    if not X_train:
        return X_train, X_test

    n_features = len(X_train[0])
    means = []
    stds = []

    for j in range(n_features):
        column = [row[j] for row in X_train]
        mean = sum(column) / len(column)

        variance = 0.0
        for value in column:
            variance += (value - mean) ** 2
        variance /= len(column)

        std = variance ** 0.5
        if std == 0:
            std = 1.0

        means.append(mean)
        stds.append(std)

    def transform(X):
        result = []
        for row in X:
            new_row = []
            for j in range(n_features):
                new_value = (row[j] - means[j]) / stds[j]
                new_row.append(new_value)
            result.append(new_row)
        return result

    return transform(X_train), transform(X_test)


def load_training_data(file_path, test_size=0.2, seed=42):
    rows = read_csv_rows(file_path)
    mean_age, mean_fare = compute_means(rows)

    X = []
    y = []

    for row in rows:
        features = row_to_features(row, mean_age, mean_fare)
        label = int(row["Survived"])

        X.append(features)
        y.append(label)

    combined = list(zip(X, y))
    random.seed(seed)
    random.shuffle(combined)

    split_index = int(len(combined) * (1 - test_size))
    train_part = combined[:split_index]
    val_part = combined[split_index:]

    X_train = [item[0] for item in train_part]
    y_train = [item[1] for item in train_part]

    X_val = [item[0] for item in val_part]
    y_val = [item[1] for item in val_part]

    X_train, X_val = standardize_train_test(X_train, X_val)

    return X_train, y_train, X_val, y_val


def load_test_data(file_path, train_file_path):
    train_rows = read_csv_rows(train_file_path)
    test_rows = read_csv_rows(file_path)

    mean_age, mean_fare = compute_means(train_rows)

    passenger_ids = []
    X_test = []

    for row in test_rows:
        passenger_ids.append(int(row["PassengerId"]))
        features = row_to_features(row, mean_age, mean_fare)
        X_test.append(features)

    # standardize test data using statistics from training-style transformation
    X_train_raw = []
    for row in train_rows:
        X_train_raw.append(row_to_features(row, mean_age, mean_fare))

    X_train_scaled, X_test_scaled = standardize_train_test(X_train_raw, X_test)

    return passenger_ids, X_test_scaled


def save_predictions(file_path, passenger_ids, predictions):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PassengerId", "Survived"])

        for i in range(len(passenger_ids)):
            writer.writerow([passenger_ids[i], predictions[i]])
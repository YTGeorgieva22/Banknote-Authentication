import csv
import random


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
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
    return 0.0


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
        float(row["Pclass"]),
        encode_sex(row["Sex"]),
        age,
        float(row["SibSp"]),
        float(row["Parch"]),
        fare,
        encode_embarked(embarked_value)
    ]

    return features


def standardize_fit(X):
    if not X:
        return [], [], []

    n_features = len(X[0])
    means = []
    stds = []

    for j in range(n_features):
        column = [row[j] for row in X]
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

    X_scaled = standardize_apply(X, means, stds)
    return X_scaled, means, stds


def standardize_apply(X, means, stds):
    result = []

    for row in X:
        new_row = []
        for j in range(len(row)):
            new_value = (row[j] - means[j]) / stds[j]
            new_row.append(new_value)
        result.append(new_row)

    return result


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

    X_train_raw = [item[0] for item in train_part]
    y_train = [item[1] for item in train_part]

    X_val_raw = [item[0] for item in val_part]
    y_val = [item[1] for item in val_part]

    X_train, means, stds = standardize_fit(X_train_raw)
    X_val = standardize_apply(X_val_raw, means, stds)

    return X_train, y_train, X_val, y_val, means, stds, mean_age, mean_fare


def prepare_single_input(form_data, mean_age, mean_fare):
    row = {
        "Pclass": str(form_data["pclass"]),
        "Sex": str(form_data["sex"]),
        "Age": str(form_data["age"]) if str(form_data["age"]).strip() != "" else str(mean_age),
        "SibSp": str(form_data["sibsp"]),
        "Parch": str(form_data["parch"]),
        "Fare": str(form_data["fare"]) if str(form_data["fare"]).strip() != "" else str(mean_fare),
        "Embarked": str(form_data["embarked"]) if str(form_data["embarked"]).strip() != "" else "S",
    }

    return row_to_features(row, mean_age, mean_fare)


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

    X_train_raw = []
    for row in train_rows:
        X_train_raw.append(row_to_features(row, mean_age, mean_fare))

    _, means, stds = standardize_fit(X_train_raw)
    X_test_scaled = standardize_apply(X_test, means, stds)

    return passenger_ids, X_test_scaled


def save_predictions(file_path, passenger_ids, predictions):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PassengerId", "Survived"])

        for i in range(len(passenger_ids)):
            writer.writerow([passenger_ids[i], predictions[i]])
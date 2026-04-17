class Perceptron:
    def __init__(self, n_features, learning_rate=0.01, epochs=50, threshold=0.0):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.threshold = threshold

        self.weights = [0.0 for _ in range(n_features)]
        self.bias = 0.0
        self.epoch_errors = []

    def weighted_sum(self, x):
        total = self.bias
        for i in range(len(x)):
            total += self.weights[i] * x[i]
        return total

    def activation(self, x):
        return 1 if self.weighted_sum(x) >= self.threshold else 0

    def predict_one(self, x):
        return self.activation(x)

    def predict(self, X):
        predictions = []
        for x in X:
            predictions.append(self.predict_one(x))
        return predictions

    def fit(self, X, y):
        self.epoch_errors = []

        for _ in range(self.epochs):
            errors = 0

            for i in range(len(X)):
                x_i = X[i]
                target = y[i]

                prediction = self.predict_one(x_i)
                update = self.learning_rate * (target - prediction)

                if update != 0:
                    errors += 1

                for j in range(len(self.weights)):
                    self.weights[j] += update * x_i[j]

                self.bias += update

            self.epoch_errors.append(errors)

    def accuracy(self, X, y):
        predictions = self.predict(X)
        correct = 0

        for i in range(len(y)):
            if predictions[i] == y[i]:
                correct += 1

        return correct / len(y) if len(y) > 0 else 0.0

    def confusion_matrix(self, X, y):
        predictions = self.predict(X)

        tp = tn = fp = fn = 0

        for i in range(len(y)):
            if y[i] == 1 and predictions[i] == 1:
                tp += 1
            elif y[i] == 0 and predictions[i] == 0:
                tn += 1
            elif y[i] == 0 and predictions[i] == 1:
                fp += 1
            elif y[i] == 1 and predictions[i] == 0:
                fn += 1

        return {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn
        }
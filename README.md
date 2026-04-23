# 🚢 Titanic Predictor – Flask ML Web Application

## 📌 Project Overview
This project is a Flask web application that demonstrates a machine learning algorithm implemented from scratch. The application allows users to interact with a Perceptron model to predict whether a passenger would survive the Titanic disaster.

The goal of this project is to combine web development, database systems, and core machine learning understanding in one structured application.

---

## 🧠 Machine Learning Model
The chosen algorithm is:

### 👉 Perceptron (Binary Classification)

The model is implemented manually using Python and includes:
- Weighted sum calculation
- Activation function (threshold)
- Weight updates
- Training through multiple epochs
- Binary classification output (Survived / Not Survived)

No machine learning libraries (like sklearn) are used.

---

## 📊 Dataset
Dataset used: Titanic Dataset (Kaggle)

Files:
- train.csv
- test.csv
- gender_submission.csv

### Features used:
- Passenger class (Pclass)
- Sex
- Age
- Fare

### Target:
- Survived (0 = No, 1 = Yes)

Basic preprocessing was applied:
- Missing values handled
- Categorical values encoded

---

## ⚙️ Technologies Used

### Backend:
- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy

### Machine Learning:
- Python
- pandas
- random

### Frontend:
- HTML / CSS

---

## 🔐 Features

### Authentication
- User registration
- User login and logout
- Password hashing
- Protected routes

### Dashboard
- User-specific statistics
- Model accuracy
- Number of predictions
- Training activity

### Machine Learning
- Train perceptron model
- Make predictions
- View results:
  - Accuracy
  - Confusion matrix
  - Training errors

### Database
Stores:
- Users
- Model training history
- Predictions per user

---

## 🧩 Project Structure

project/
│
├── app/
│   ├── auth/
│   ├── main/
│   ├── ml/
│   ├── errors/
│   ├── static/
│   └── templates/
│
├── data/
├── docs/
├── migrations/
├── config.py
├── run.py
├── requirements.txt
└── README.md

---

## ▶️ How to Run the Project

1. Install dependencies:
pip install -r requirements.txt

2. Run the application:
python run.py

3. Open in browser:
http://127.0.0.1:5000

---

## 🧪 How to Use the App

1. Register an account  
2. Log in  
3. Go to Dashboard  
4. Train the model  
5. Make predictions  
6. View results  

---

## 📈 Results Display
The application shows:
- Model accuracy
- Training error per epoch
- Confusion matrix (TP, FP, FN, TN)
- Prediction history

---

## 🎯 Project Goal
The purpose of this project is not to achieve maximum accuracy, but to demonstrate:
- Understanding of machine learning algorithms
- Manual implementation of a model
- Integration of ML into a Flask web application

---

## 👩‍💻 Author
Yoana Georgieva

---

## 📌 Notes
- The Perceptron model is implemented from scratch
- No external ML libraries were used
- Each user has their own stored results and predictions

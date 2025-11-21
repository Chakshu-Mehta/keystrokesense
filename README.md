📌 KeystrokeSense – Typing-Based Stress Prediction using Machine Learning

KeystrokeSense is a Python & Machine Learning project that predicts a user’s stress level (Calm / Normal / Stressed) based on typing behavior, including typing speed, mistakes, accuracy, difficulty score, and sleep hours.

The project uses real-world data from 53 users, includes feature engineering, model training, visualizations, and both manual and live automatic prediction modes.

⭐ Features
✔ Data Collection Module

Shows a reference text

User types it

Automatically measures:

Time taken

Characters typed

Accuracy

Mistakes

Difficulty score

User enters:

Stress level (label for ML)

Sleep hours

Stored in raw_sessions.csv

✔ Feature Engineering Module

Adds the following features:

chars_per_sec

mistakes_per_char

difficulty_score

word_mistake_rate

accuracy_percent

sleep_hours

Output stored in sessions_with_features.csv.

✔ Machine Learning Model

Two models tested:

Model	Accuracy
Logistic Regression	68.75%
Random Forest	75%

Random Forest performed best and is used as the final model.

Model saved as:

models/stress_model.pkl

✔ Live Automatic Prediction (New!)

Script: live_predict.py

Shows a reference sentence

User types it live

System automatically extracts:

Speed

Mistakes

Accuracy

Word errors

Difficulty score

Asks only sleep hours

Predicts stress AUTOMATICALLY using trained model

This makes the system feel like a real-world product.

✔ Manual Prediction Module

Script: predict_stress.py

Useful when you already know feature values or want rapid testing.

✔ Professional Data Visualizations

Graphs included:

Typing speed vs stress

Mistakes vs stress

Accuracy vs stress

Sleep vs stress

Feature importance (Random Forest)

These make the project scientifically strong.

📁 Project Structure
keystrokesense/
│
├── data/
│   ├── raw_sessions.csv
│   ├── sessions_with_features.csv
│
├── models/
│   ├── stress_model.pkl
│
├── src/
│   ├── typing_logger.py          # Collect training data
│   ├── feature_engineering.py    # Generate features
│   ├── train_model.py            # Train ML model
│   ├── predict_stress.py         # Manual prediction
│   ├── live_predict.py           # NEW — automatic prediction
│
├── graphs/                       # Visualizations
│   ├── speed_vs_stress.png
│   ├── mistakes_vs_stress.png
│   ├── accuracy_vs_stress.png
│   ├── sleep_vs_stress.png
│   ├── feature_importance.png
│
├── requirements.txt
└── README.md

🔧 Tech Stack

Python 3.x

Pandas

Scikit-Learn

Matplotlib

Joblib

🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/Chakshu-Mehta/keystrokesense.git
cd keystrokesense

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Collect Training Data
python -m src.typing_logger


This creates entries inside:

data/raw_sessions.csv

4️⃣ Generate Features
python -m src.feature_engineering


Creates:

data/sessions_with_features.csv

5️⃣ Train Machine Learning Model
python -m src.train_model


Outputs accuracy and confusion matrix.

Saves model to:

models/stress_model.pkl

6️⃣ Predict Stress (Manual Inputs)
python -m src.predict_stress


This mode is useful for quick testing.

7️⃣ Live Automatic Stress Prediction
python -m src.live_predict


This mode:

Gives a sentence

You type it

System auto-computes all typing metrics

Only asks for sleep hours

Predicts stress level

Shows full summary + result

🧠 Why Ask for Sleep Hours?

Sleep duration is not visible directly from typing behavior.
Since sleep strongly affects stress, and since it was used as a real input during training, the model expects it at prediction time too.

This keeps the prediction:

Accurate

Consistent with training

Scientifically valid

Easy for the user (one simple question)

Future improvement: Build a sleep-hours predictor model.

📊 Key Insights from Data

Low sleep → low accuracy → high stress

High mistakes_per_char → high stress

High word mistake rate → high stress

Calm users show stable typing behavior

Feature importance:

Sleep Hours

Mistakes per char

Accuracy

Difficulty score

Word mistake rate

Typing speed

The model’s logic matches real cognitive patterns.

🎯 Conclusion

KeystrokeSense successfully demonstrates:

Behavioral biometrics

Real-world data collection

Machine learning feature engineering

Model training & evaluation

Live automatic prediction

Clean modular architecture

Interactive demo capability

This makes it a strong academic + applied ML project.

🔮 Future Enhancements

Predict sleep hours automatically

Larger dataset (100–500 users)

Real-time keystroke logging

Deep learning (LSTM for sequential typing data)

Full web dashboard (Flask/Streamlit)

Mobile typing stress app

🙌 Author

Chakshu Mehta
B.Tech CSE (DSAI)
Typing Behavior & Machine Learning Research Enthusiast

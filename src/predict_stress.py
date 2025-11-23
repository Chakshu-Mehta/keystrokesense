import joblib
import pandas as pd
import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "stress_model.pkl")
model = joblib.load(MODEL_PATH)
def predict_stress():
    print("\n=== Stress Prediction Using Typing Behavior ===")
    chars_per_sec = float(input("Enter chars per second: "))
    mistakes_per_char = float(input("Enter mistakes per char: "))
    difficulty_score = float(input("Enter difficulty score: "))
    word_mistake_rate = float(input("Enter word mistake rate: "))
    accuracy_percent = float(input("Enter accuracy percent: "))
    sleep_hours = float(input("Enter sleep hours: "))
    user_data = pd.DataFrame([{
        "chars_per_sec": chars_per_sec,
        "mistakes_per_char": mistakes_per_char,
        "difficulty_score": difficulty_score,
        "word_mistake_rate": word_mistake_rate,
        "accuracy_percent": accuracy_percent,
        "sleep_hours": sleep_hours
    }])
    prediction = model.predict(user_data)[0]
    labels = {
        0: "Calm",
        1: "Normal",
        2: "Stressed"
    }
    print(f"\n🧠 Predicted Stress Level: {labels[prediction]}\n")
if __name__ == "__main__":
    predict_stress()

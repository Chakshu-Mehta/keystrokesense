import time
import random
import os
import joblib
import pandas as pd
REFERENCE_TEXTS = [
    "Python makes data science fun and powerful.",
    "Typing speed and accuracy can reflect our focus.",
    "Machine learning finds patterns in noisy data.",
    "College projects are a great way to learn real skills.",
    "Typing speed and accuracy during a test can reflect how focused or distracted a student is at that moment.",
    "Machine learning models can discover hidden patterns in noisy data, helping us make better predictions about the real world."
]
def choose_reference_text():
    return random.choice(REFERENCE_TEXTS)
def calculate_accuracy(reference, typed):
    """Return (accuracy_percent, mistake_count)."""
    ref = reference.strip()
    t = typed.strip()
    max_len = max(len(ref), len(t))

    mistakes = 0
    for i in range(max_len):
        ref_char = ref[i] if i < len(ref) else ""
        t_char = t[i] if i < len(t) else ""
        if ref_char != t_char:
            mistakes += 1
    if max_len == 0:
        return 0.0, mistakes
    accuracy = ((max_len - mistakes) / max_len) * 100
    return round(accuracy, 2), mistakes
def word_level_mistakes(ref, typed):
    ref_words = str(ref).split()
    typed_words = str(typed).split()
    mistakes = sum(1 for rw, tw in zip(ref_words, typed_words) if rw != tw)
    mistakes += abs(len(ref_words) - len(typed_words))
    return mistakes
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "stress_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    return joblib.load(model_path)
def run_live_prediction():
    print("\n=== KeystrokeSense: Live Stress Prediction ===\n")
    reference_text = choose_reference_text()
    print("Type the following sentence as accurately and quickly as you can:\n")
    print("-->", reference_text)
    input("\nPress ENTER when you are ready to start...")
    print("\nStart typing and press ENTER when done:")
    start_time = time.time()
    typed_text = input("> ")
    end_time = time.time()
    time_taken_sec = round(end_time - start_time, 2)
    reference_len = len(reference_text.strip())
    typed_len = len(typed_text.strip())
    accuracy_percent, mistake_count = calculate_accuracy(reference_text, typed_text)
    difficulty_score = max(0, (reference_len - typed_len) + mistake_count)
    chars_per_sec = typed_len / time_taken_sec if time_taken_sec > 0 else 0.0
    mistakes_per_char = mistake_count / reference_len if reference_len > 0 else 0.0
    word_mistake_count = word_level_mistakes(reference_text, typed_text)
    word_mistake_rate = word_mistake_count / reference_len if reference_len > 0 else 0.0
    sleep_raw = input("\nHow many hours did you sleep last night? (just press ENTER to skip): ").strip()
    if sleep_raw == "":
        sleep_hours = 0.0
    else:
        try:
            sleep_hours = float(sleep_raw)
        except ValueError:
            sleep_hours = 0.0
    print("\n=== Typing Session Summary ===")
    print(f"Time taken (sec):        {time_taken_sec}")
    print(f"Reference length:        {reference_len}")
    print(f"Typed length:            {typed_len}")
    print(f"Accuracy (%):            {accuracy_percent}")
    print(f"Mistakes (char-level):   {mistake_count}")
    print(f"Word-level mistakes:     {word_mistake_count}")
    print(f"Chars per second:        {round(chars_per_sec, 3)}")
    print(f"Mistakes per char:       {round(mistakes_per_char, 4)}")
    print(f"Difficulty score:        {difficulty_score}")
    print(f"Word mistake rate:       {round(word_mistake_rate, 4)}")
    print(f"Sleep hours:             {sleep_hours}")
    model = load_model()
    feature_row = pd.DataFrame([{
        "chars_per_sec": chars_per_sec,
        "mistakes_per_char": mistakes_per_char,
        "difficulty_score": difficulty_score,
        "word_mistake_rate": word_mistake_rate,
        "accuracy_percent": accuracy_percent,
        "sleep_hours": sleep_hours
    }])
    pred = model.predict(feature_row)[0]
    labels = {
        0: "Calm",
        1: "Normal",
        2: "Stressed"
    }
    print("\n=== Model Prediction ===")
    print(f"🧠 Predicted Stress Level: {labels.get(pred, 'Unknown')}")
    print("\n(0 = Calm, 1 = Normal, 2 = Stressed)\n")
if __name__ == "__main__":
    run_live_prediction()

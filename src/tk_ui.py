import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import random
import os
import joblib
import pandas as pd

# ---------- REFERENCE TEXTS (same style as typing_logger) ----------
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

# ---------- HELPER FUNCTIONS (same logic as live_predict) ----------

def calculate_accuracy(reference, typed):
    """Return (accuracy_percent, mistake_count) based on character comparison."""
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

# ---------- TKINTER APP ----------

class KeystrokeSenseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("KeystrokeSense - Stress Prediction")
        self.master.geometry("800x600")

        # Colors / theme
        self.bg_color = "#edf3ff"       # light bluish background
        self.panel_color = "#ffffff"    # white panels
        self.accent_color = "#4a6cf7"   # primary blue for button
        self.master.configure(bg=self.bg_color)

        # Load model once
        try:
            self.model = load_model()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load model:\n{e}")
            self.master.destroy()
            return

        self.reference_text = ""
        self.start_time = None

        # Build UI
        self.create_widgets()
        self.new_test()  # Load first sentence

    def create_widgets(self):
        # App title
        self.app_title = tk.Label(
            self.master,
            text="KeystrokeSense – Typing-based Stress Detector",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_color,
            fg="#111111"
        )
        self.app_title.pack(pady=(10, 5))

        # Reference sentence title
        self.ref_label_title = tk.Label(
            self.master,
            text="Reference Sentence",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg="#222222"
        )
        self.ref_label_title.pack(pady=(5, 0))

        # Reference sentence panel
        self.ref_frame = tk.Frame(self.master, bg=self.panel_color, bd=1, relief="solid")
        self.ref_frame.pack(pady=(5, 10), padx=20, fill="x")

        self.ref_label = tk.Label(
            self.ref_frame,
            text="",
            wraplength=730,
            justify="left",
            font=("Segoe UI", 11),
            bg=self.panel_color,
            fg="#333333",
            anchor="w"
        )
        self.ref_label.pack(padx=10, pady=8, fill="x")

        # Typing area label
        self.typing_label = tk.Label(
            self.master,
            text="Type the above sentence in the box below, then click 'Predict Stress':",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#333333"
        )
        self.typing_label.pack()

        # Typing text area
        self.text_area = scrolledtext.ScrolledText(
            self.master,
            height=6,
            width=90,
            font=("Consolas", 11),
            bg="#ffffff",
            fg="#222222",
            insertbackground="#222222",  # cursor color
            relief="solid",
            borderwidth=1
        )
        self.text_area.pack(pady=(5, 10), padx=20)

        # Sleep hours frame
        self.sleep_frame = tk.Frame(self.master, bg=self.bg_color)
        self.sleep_frame.pack(pady=(5, 10))

        self.sleep_label = tk.Label(
            self.sleep_frame,
            text="Sleep hours last night:",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#333333"
        )
        self.sleep_label.pack(side=tk.LEFT)

        self.sleep_entry = tk.Entry(
            self.sleep_frame,
            width=10,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1
        )
        self.sleep_entry.pack(side=tk.LEFT, padx=5)
        self.sleep_entry.insert(0, "7")  # default

        # Buttons row
        self.button_frame = tk.Frame(self.master, bg=self.bg_color)
        self.button_frame.pack(pady=(5, 10))

        self.new_test_button = tk.Button(
            self.button_frame,
            text="New Sentence",
            command=self.new_test,
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#333333",
            activebackground="#e1e7ff",
            activeforeground="#000000",
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=3
        )
        self.new_test_button.pack(side=tk.LEFT, padx=5)

        self.predict_button = tk.Button(
            self.button_frame,
            text="Predict Stress",
            command=self.predict_stress,
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_color,
            fg="#ffffff",
            activebackground="#324ad9",
            activeforeground="#ffffff",
            relief="flat",
            padx=12,
            pady=4
        )
        self.predict_button.pack(side=tk.LEFT, padx=8)

        # Results title
        self.result_label = tk.Label(
            self.master,
            text="Results",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg="#222222"
        )
        self.result_label.pack(pady=(10, 0))

        # Results panel
        self.result_frame = tk.Frame(self.master, bg=self.panel_color, bd=1, relief="solid")
        self.result_frame.pack(pady=(5, 10), padx=20, fill="both", expand=True)

        self.result_text = tk.Label(
            self.result_frame,
            text="",
            justify="left",
            font=("Consolas", 10),
            bg=self.panel_color,
            fg="#222222",
            anchor="nw"
        )
        self.result_text.pack(padx=10, pady=8, fill="both", expand=True)

        # Footer / status
        self.footer_label = tk.Label(
            self.master,
            text="Model: RandomForest (accuracy ≈ 75% on 53 samples)",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#555555"
        )
        self.footer_label.pack(pady=(0, 8))

    def new_test(self):
        """Start a new typing test with a fresh sentence."""
        self.reference_text = choose_reference_text()
        self.ref_label.config(text=self.reference_text)
        self.text_area.delete("1.0", tk.END)
        self.sleep_entry.delete(0, tk.END)
        self.sleep_entry.insert(0, "7")
        self.result_text.config(text="")
        self.start_time = time.time()

    def predict_stress(self):
        """Compute features from typed text and predict stress."""
        if not self.reference_text:
            messagebox.showwarning("Warning", "No reference text loaded.")
            return

        typed_text = self.text_area.get("1.0", tk.END).strip()
        if not typed_text:
            messagebox.showwarning("Warning", "Please type the sentence before predicting.")
            return

        end_time = time.time()
        time_taken_sec = round(end_time - self.start_time, 2) if self.start_time else 0.0

        reference_len = len(self.reference_text.strip())
        typed_len = len(typed_text.strip())

        accuracy_percent, mistake_count = calculate_accuracy(self.reference_text, typed_text)
        difficulty_score = max(0, (reference_len - typed_len) + mistake_count)
        chars_per_sec = typed_len / time_taken_sec if time_taken_sec > 0 else 0.0
        mistakes_per_char = mistake_count / reference_len if reference_len > 0 else 0.0
        word_mistake_count = word_level_mistakes(self.reference_text, typed_text)
        word_mistake_rate = word_mistake_count / reference_len if reference_len > 0 else 0.0

        # Sleep hours
        sleep_raw = self.sleep_entry.get().strip()
        try:
            sleep_hours = float(sleep_raw) if sleep_raw else 0.0
        except ValueError:
            messagebox.showwarning("Warning", "Invalid sleep hours. Using 0.")
            sleep_hours = 0.0

        # Prepare feature row
        feature_row = pd.DataFrame([{
            "chars_per_sec": chars_per_sec,
            "mistakes_per_char": mistakes_per_char,
            "difficulty_score": difficulty_score,
            "word_mistake_rate": word_mistake_rate,
            "accuracy_percent": accuracy_percent,
            "sleep_hours": sleep_hours
        }])

        # Predict
        pred = self.model.predict(feature_row)[0]
        labels = {0: "Calm", 1: "Normal", 2: "Stressed"}
        stress_label = labels.get(pred, "Unknown")

        # Show results
        result_str = (
            f"Predicted Stress Level: {stress_label}\n"
            f"----------------------------------------\n"
            f"Time taken (sec):      {time_taken_sec}\n"
            f"Reference length:      {reference_len}\n"
            f"Typed length:          {typed_len}\n"
            f"Accuracy (%):          {accuracy_percent}\n"
            f"Mistakes (chars):      {mistake_count}\n"
            f"Word mistakes:         {word_mistake_count}\n"
            f"Chars per second:      {round(chars_per_sec, 3)}\n"
            f"Mistakes per char:     {round(mistakes_per_char, 4)}\n"
            f"Difficulty score:      {difficulty_score}\n"
            f"Word mistake rate:     {round(word_mistake_rate, 4)}\n"
            f"Sleep hours:           {sleep_hours}"
        )
        self.result_text.config(text=result_str)

def main():
    root = tk.Tk()
    app = KeystrokeSenseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

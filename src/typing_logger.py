import time
import csv
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw_sessions.csv")

REFERENCE_TEXTS = [
    # Short / warm-up
    "Python makes data science fun and powerful for students who love logic.",
    
    # Medium
    "Typing speed and accuracy during a test can reflect how focused or distracted a student is at that moment.",
    
    # Medium-long
    "Machine learning models can discover hidden patterns in noisy data, helping us make better predictions about the real world.",
    
    # Long
    "College projects are a great way to learn real skills, because they force us to combine theory, problem solving, teamwork, and clear communication in one place.",
    
    # Longer
    "When students track their daily habits, such as sleep, screen time, and study hours, they can often see clear trends that explain why their performance improves or drops over time.",
    
    # Longer – more like a paragraph
    "Stress does not always reduce productivity immediately, but over time it can increase mistakes, reduce focus, and make even simple tasks feel much harder than they actually are."
]

def choose_reference_text():
    import random
    # To encourage variety, avoid repeating the last chosen text if possible
    if not hasattr(choose_reference_text, "last_text"):
        choose_reference_text.last_text = None

    candidates = [t for t in REFERENCE_TEXTS if t != choose_reference_text.last_text] or REFERENCE_TEXTS
    text = random.choice(candidates)
    choose_reference_text.last_text = text
    return text

'''REFERENCE_TEXTS = [
    "Python makes data science fun and powerful.",
    "Typing speed and accuracy can reflect our focus.",
    "Machine learning finds patterns in noisy data.",
    "College projects are a great way to learn real skills."
]

def choose_reference_text():
    import random
    return random.choice(REFERENCE_TEXTS)'''

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

def init_csv_if_needed():
    """Create the CSV file with header if it does not exist."""
    if not os.path.exists(os.path.dirname(DATA_FILE)):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "session_id",
                "user_id",
                "reference_text",
                "reference_text_len",
                "typed_text",
                "typed_text_len",
                "time_taken_sec",
                "accuracy_percent",
                "mistake_count",
                "backspace_estimate",
                "date_time",
                "self_stress_level",
                "sleep_hours",
                "notes"
            ])

def get_next_session_id():
    """Find the next session id based on existing rows."""
    if not os.path.isfile(DATA_FILE):
        return 1
    with open(DATA_FILE, mode="r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
        if len(rows) <= 1:
            return 1
        last_row = rows[-1]
        try:
            return int(last_row[0]) + 1
        except Exception:
            return 1

def run_typing_session():
    print("=== KeystrokeSense: Typing Session Logger ===")
    user_id = input("Enter user id (e.g., user1): ").strip() or "user1"

    reference = choose_reference_text()
    print("\nType the following sentence as accurately and quickly as you can:")
    print(f"--> {reference}")
    input("\nPress ENTER when you are ready to start...")

    start_time = time.time()
    typed_text = input("\nStart typing and press ENTER when done:\n> ")
    end_time = time.time()

    time_taken_sec = round(end_time - start_time, 2)
    accuracy_percent, mistake_count = calculate_accuracy(reference, typed_text)

    # Simple proxy for backspaces: difference in length + mistakes
    reference_len = len(reference.strip())
    typed_len = len(typed_text.strip())
    backspace_estimate = max(0, (reference_len - typed_len) + mistake_count)

    print("\n=== Session Summary ===")
    print(f"Time taken (sec): {time_taken_sec}")
    print(f"Accuracy (%):     {accuracy_percent}")
    print(f"Mistakes:         {mistake_count}")

    print("\nLabel your current stress level:")
    print("  0 = Calm")
    print("  1 = Normal")
    print("  2 = Stressed")
    while True:
        try:
            self_stress_level = int(input("Enter stress level (0/1/2): ").strip())
            if self_stress_level in [0, 1, 2]:
                break
            else:
                print("Please enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a valid number (0/1/2).")

    sleep_input = input("How many hours did you sleep last night? (optional, just press ENTER to skip): ").strip()
    sleep_hours = float(sleep_input) if sleep_input else ""

    notes = input("Any notes (e.g., exam tomorrow, not feeling well)? (optional): ").strip()

    init_csv_if_needed()
    session_id = get_next_session_id()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_id,
            user_id,
            reference,
            reference_len,
            typed_text,
            typed_len,
            time_taken_sec,
            accuracy_percent,
            mistake_count,
            backspace_estimate,
            date_time,
            self_stress_level,
            sleep_hours,
            notes
        ])

    print("\n✅ Session saved successfully!")
    print(f"Saved as session_id = {session_id} in {DATA_FILE}")

if __name__ == "__main__":
    run_typing_session()

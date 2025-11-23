import pandas as pd
import os
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw_sessions.csv")
df = pd.read_csv(DATA_FILE)
df["chars_per_sec"] = df["typed_text_len"] / df["time_taken_sec"]
df["mistakes_per_char"] = df["mistake_count"] / df["reference_text_len"]
df["difficulty_score"] = df["backspace_estimate"]
def word_level_mistakes(ref, typed):
    ref_words = str(ref).split()
    typed_words = str(typed).split()
    mistakes = sum(1 for rw, tw in zip(ref_words, typed_words) if rw != tw)
    mistakes += abs(len(ref_words) - len(typed_words))
    return mistakes
df["word_mistake_count"] = df.apply(
    lambda row: word_level_mistakes(row["reference_text"], row["typed_text"]),
    axis=1
)
df["word_mistake_rate"] = df["word_mistake_count"] / df["reference_text_len"]
df["sleep_hours"] = df["sleep_hours"].fillna(0)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sessions_with_features.csv")
df.to_csv(OUTPUT_FILE, index=False)
print("✅ Feature engineering complete.")
print(f"Saved file: {OUTPUT_FILE}")
print("Here are the first few rows with new columns:")
print(df.head())

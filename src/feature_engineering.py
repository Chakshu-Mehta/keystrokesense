import pandas as pd
import os

# 1. Load the raw data
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raw_sessions.csv")
df = pd.read_csv(DATA_FILE)

# 2. Create smart features

# typing speed: characters per second
df["chars_per_sec"] = df["typed_text_len"] / df["time_taken_sec"]

# character level error density
df["mistakes_per_char"] = df["mistake_count"] / df["reference_text_len"]

# keep difficulty_score same as backspace_estimate (our rough proxy)
df["difficulty_score"] = df["backspace_estimate"]

# word-level mistake count (human-friendly)
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

# normalize word mistakes (so long/short sentences are comparable)
df["word_mistake_rate"] = df["word_mistake_count"] / df["reference_text_len"]

# 3. Fill any missing sleep_hours with 0 (just to be safe)
df["sleep_hours"] = df["sleep_hours"].fillna(0)

# 4. Save a new CSV with features
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sessions_with_features.csv")
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Feature engineering complete.")
print(f"Saved file: {OUTPUT_FILE}")
print("Here are the first few rows with new columns:")
print(df.head())

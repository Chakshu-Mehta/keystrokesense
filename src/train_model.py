import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# Load the feature-engineered CSV
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sessions_with_features.csv")
df = pd.read_csv(DATA_FILE)

# ML Features we will use
features = [
    "chars_per_sec",
    "mistakes_per_char",
    "difficulty_score",
    "word_mistake_rate",
    "accuracy_percent",
    "sleep_hours"
]

X = df[features]
y = df["self_stress_level"]

# Handle missing values
X = X.fillna(0)

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42
)

# --------------------------
# Logistic Regression Model
# --------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_model = LogisticRegression(max_iter=300)
log_model.fit(X_train_scaled, y_train)
log_pred = log_model.predict(X_test_scaled)
log_acc = accuracy_score(y_test, log_pred)

print("\n=== Logistic Regression Results ===")
print("Accuracy:", log_acc)
print(confusion_matrix(y_test, log_pred))
print(classification_report(y_test, log_pred))

# --------------------------
# Random Forest Model
# --------------------------
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

print("\n=== Random Forest Results ===")
print("Accuracy:", rf_acc)
print(confusion_matrix(y_test, rf_pred))
print(classification_report(y_test, rf_pred))

# Save the best model
best_model = rf if rf_acc >= log_acc else log_model

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "stress_model.pkl")
joblib.dump(best_model, MODEL_PATH)

print(f"\n✅ Best model saved to: {MODEL_PATH}")

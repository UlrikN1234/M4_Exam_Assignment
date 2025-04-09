import sqlite3
from pathlib import Path

# Ensure directory exists
Path("database").mkdir(exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect("database/theft_risk.db")
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# --- 1. STORES: The only table not model-related ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS STORES (
    store_id INTEGER PRIMARY KEY AUTOINCREMENT,
    postal_code TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    store_type TEXT,
    area_m2 REAL,
    employee_count INTEGER,
    turnover_last_year REAL,
    theft_occurred INTEGER CHECK(theft_occurred IN (0, 1)),
    imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# --- 2. MODELS: Metadata about trained models ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS MODELS (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    algorithm TEXT NOT NULL,
    hyperparameters TEXT,
    training_data_size INTEGER,
    accuracy REAL,
    precision REAL,
    recall REAL,
    f1_score REAL
);
''')

# --- 3. MODEL_TRAINING_SETS: Link between model_id and store_id used during training ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS MODEL_TRAINING_SETS (
    model_id INTEGER,
    store_id INTEGER,
    PRIMARY KEY (model_id, store_id),
    FOREIGN KEY (model_id) REFERENCES MODELS(model_id),
    FOREIGN KEY (store_id) REFERENCES STORES(store_id)
);
''')

# --- 4. PREDICTIONS: What the model predicted vs actual theft ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS PREDICTIONS (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    store_id INTEGER,
    predicted_risk INTEGER CHECK(predicted_risk IN (0, 1)),
    actual_risk INTEGER CHECK(actual_risk IN (0, 1)),
    correct INTEGER CHECK(correct IN (0, 1)),
    predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES MODELS(model_id),
    FOREIGN KEY (store_id) REFERENCES STORES(store_id)
);
''')

# --- 5. MODEL_EVALUATIONS: Stores evaluation performance separately ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS MODEL_EVALUATIONS (
    evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    dataset_label TEXT NOT NULL,
    evaluated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    accuracy REAL,
    precision REAL,
    recall REAL,
    f1_score REAL,
    FOREIGN KEY (model_id) REFERENCES MODELS(model_id)
);
''')

# Finalize
conn.commit()
conn.close()

print("✅ SQLite database with full schema created at 'database/theft_risk.db'")

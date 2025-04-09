# 🐧 Penguin Species Prediction NEW DATA— MLOps Exercise

This exercise is designed to simulate an end-to-end MLOps workflow using a penguin classification task. We will work with a dataset of penguin features to build, evaluate, and monitor ML models, using SQLite as a lightweight metadata store.

---

## 📦 Project Structure

```text
theft-risk-mlops/
├── data/
│   └── original_data.csv     
│   └── new_data.csv                   
│
├── database/
│   └── theft_risk.db
│
│── images/│
│
├── models/
│   ├── model_1.pkl               
│   └── model_2.pkl                  
│
├── scripts/
│   ├── db/
│   │   ├── 1_create_db.py     
│   │   ├── 2_import_original_data.py
│   │   └── 4_import_new_data.py
│   │    
│   ├── model/
│   │   ├── 3_train_and_evaluate_original_data.py(model_id = 1)
│   │   ├── 5_test_first_model_on_new_data.py
│   │   └── 6_train_second_model_new_data.py(model_id = 2)
│   │
│   ├── monitoring/
│   │   └── check_imported_at_counts.py    # Shows summary of original vs new data
│
├── README.md                        
└── requirements.txt                
```


## 🧠 Learning Objectives

- Understand the lifecycle of ML models in production
- Track metadata for datasets, training, predictions, and evaluations
- Use SQLite to persist:
  - Model configurations and metrics (`MODELS`)
  - Dataset versions (`imported_at`)
  - Predictions per sample (`PREDICTIONS`)
  - Train/test splits (`MODEL_TRAINING_SETS`)
  - Evaluation results over time (`MODEL_EVALUATIONS`)

![Schema](images/schema_new.PNG)


---

## ✅ Steps

1. **Create database and tables**  

scripts/db/1_create_db.py

2. **Import original data**

scripts/db/2_import_original_data_to_db.py

3. **Preprocess data**

scripts/models/3_train_and_evaluate_original_data.py

4. **Import new data**

scripts/db/4_import_new_data_to_db.py

5. **Test first model on new data**

scripts/models/5_test_first_model_on_new_data.py

6. **Train second model on new data**

scripts/models/6_train_second_model_new_data.py








# Mental Health Classifier

This project is a machine learning web application for classifying mental health conditions based on survey data. It uses a trained ensemble model and provides a user-friendly web interface built with Flask.

## Features
- Predicts mental health conditions: Bipolar Type-1, Bipolar Type-2, Depression, or Normal
- Clean, modern UI with dropdowns for all features
- Handles categorical and numeric data
- Model trained with label encoding and SMOTE for class balance

## Project Structure
```
mental-health-classifier/
├── app.py                  # Flask web app
├── best_model.pkl          # Trained ML model
├── cleaned_dataset.csv     # Cleaned dataset
├── dataset/
│   └── Dataset-Mental-Disorders.csv
├── static/
│   └── style.css           # App styling
├── templates/
│   └── index.html          # Web form
├── model.ipynb             # Model training notebook
└── README.md               # Project documentation
```

## Setup Instructions
1. **Clone the repository and install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or manually install: flask, numpy, pandas, scikit-learn, imbalanced-learn, matplotlib, seaborn
   ```
2. **Train the model (optional):**
   - Run `model.ipynb` to preprocess data and train the model.
   - The trained model is saved as `best_model.pkl`.
3. **Run the Flask app:**
   ```bash
   python app.py
   ```
   - Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
- Fill in the form with the required features (dropdowns for categorical, numbers for scores).
- Click "Predict" to see the predicted mental health condition.

## Notes
- The model uses label encoding for all categorical features. The web form options match the encoded values.
- Only the training set is oversampled with SMOTE to avoid data leakage.
- The app is for educational/demo purposes and not for real medical diagnosis.

## License
MIT
# mental_health_classifier

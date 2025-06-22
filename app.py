from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)

# LabelEncoder mappings (must match training)
category_maps = {
    'Sadness': {'Most-Often': 0, 'Seldom': 1, 'Sometimes': 2, 'Usually': 3},
    'Euphoric': {'Most-Often': 0, 'Seldom': 1, 'Sometimes': 2, 'Usually': 3},
    'Exhausted': {'Most-Often': 0, 'Seldom': 1, 'Sometimes': 2, 'Usually': 3},
    'Sleep dissorder': {'Most-Often': 0, 'Seldom': 1, 'Sometimes': 2, 'Usually': 3},
    'Mood Swing': {'NO': 0, 'YES': 1},
    'Suicidal thoughts': {'NO': 0, 'YES': 1},
    'Anorxia': {'NO': 0, 'YES': 1},
    'Authority Respect': {'NO': 0, 'YES': 1},
    'Try-Explanation': {'NO': 0, 'YES': 1},
    'Aggressive Response': {'NO': 0, 'YES': 1},
    'Ignore & Move-On': {'NO': 0, 'YES': 1},
    'Nervous Break-down': {'NO': 0, 'YES': 1},
    'Admit Mistakes': {'NO': 0, 'YES': 1},
    'Overthinking': {'NO': 0, 'YES': 1},
    # The following are numeric, use as int
    'Sexual Activity': None,
    'Concentration': None,
    'Optimisim': None
}

# Add this mapping for the target class
class_map = {
    0: 'Bipolar Type-1',
    1: 'Bipolar Type-2',
    2: 'Depression',
    3: 'Normal'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_features = []
    for feature in category_maps:
        val = request.form.get(feature)
        if category_maps[feature] is None:
            input_features.append(int(val))
        else:
            input_features.append(category_maps[feature][val])
    features = np.array(input_features).reshape(1, -1)
    pred_idx = model.predict(features)[0]
    prediction = class_map.get(pred_idx, str(pred_idx))
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)

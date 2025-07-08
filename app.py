import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection config (update with your XAMPP credentials)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'mental_health'

def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, cursorclass=pymysql.cursors.DictCursor)

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

class_map = {
    0: 'Bipolar Type-1',
    1: 'Bipolar Type-2',
    2: 'Depression',
    3: 'Normal'
}

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
            if cursor.fetchone():
                flash('Username already exists!')
                conn.close()
                return redirect(url_for('signup'))
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
        conn.close()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
            user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('menu'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # ✅ Move category_maps to the top
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
        'Sexual Activity': None,
        'Concentration': None,
        'Optimisim': None
    }

    class_map = {
        0: 'Bipolar Type-1',
        1: 'Bipolar Type-2',
        2: 'Depression',
        3: 'Normal'
    }

    prediction = None

    if request.method == 'POST':
        input_features = []
        input_dict = {}
        for feature in category_maps:
            val = request.form.get(feature)
            input_dict[feature] = val
            if category_maps[feature] is None:
                input_features.append(int(val))
            else:
                input_features.append(category_maps[feature][val])

        features = np.array(input_features).reshape(1, -1)
        pred_idx = model.predict(features)[0]
        prediction = class_map.get(pred_idx, str(pred_idx))

        # Save to history
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO history (user_id, input_data, prediction) VALUES (%s, %s, %s)',
                (session['user_id'], str(input_dict), prediction)
            )
            conn.commit()
        conn.close()

    # ✅ Pass category_maps into template
    return render_template('predict.html', prediction=prediction, category_maps=category_maps)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM history WHERE user_id=%s', (session['user_id'],))
        user_history = cursor.fetchall()
    conn.close()
    return render_template('history.html', history=user_history)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

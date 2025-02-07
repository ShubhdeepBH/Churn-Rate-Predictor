import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from t3 import ChurnPredictor
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


VALID_EMAIL = "user@example.com"
VALID_PASSWORD = "password123"

@app.route('/upload', methods=['POST'])
def upload_file():
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    try:
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        
        predictor = ChurnPredictor()
        result = predictor.analyze_dataset(file_path)

        
        return jsonify({
            'message': result.get('message', 'Analysis complete! You can now view the results.'),
            'churn_rate': f"{result.get('churn_rate', 0):.2f}%",
            'churn_users_count': result.get('churn_users_count', 0),
            'churn_user_ids': result.get('churn_user_ids', [])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return redirect(url_for('about'))

@app.route('/result')
def result_page():
    return render_template('result.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        
        if email == VALID_EMAIL and password == VALID_PASSWORD:
            return redirect(url_for('index'))  
        else:
            
            return render_template('login.html', error_message="Invalid email or password")
    
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            
            return render_template('signup.html', error_message="Passwords do not match.")
        
        
        
        print(f"User {email} signed up with password {password}")
        
        
        return redirect(url_for('login'))

    
    return render_template('signup.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/home')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

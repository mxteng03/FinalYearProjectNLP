from flask import Flask, request, redirect, url_for, render_template
from flask_cors import CORS
from auth import auth as auth_blueprint
from text_processing import text_processing as text_processing_blueprint
from history import history as history_blueprint
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='frontend/public', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
CORS(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(text_processing_blueprint)
app.register_blueprint(history_blueprint, url_prefix='/history')


@app.route('/')
def home():
    return redirect(url_for('auth.signup_page'))

@app.route('/main')
def main_page():
    email = request.cookies.get('email')
    if not email:
        return redirect(url_for('auth.login_page'))
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)

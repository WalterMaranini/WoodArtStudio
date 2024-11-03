from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import User  # Importa il modello

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia la chiave segreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione completata con successo!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login eseguito con successo!')  # Messaggio di login riuscito
            return redirect(url_for('gallery'))
        else:
            flash('Credenziali non valide. Riprova.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sei stato disconnesso con successo.')  # Messaggio di logout
    return redirect(url_for('login'))

@app.route('/')
@login_required
def gallery():
    images = []
    image_folder = 'static/images'
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}

    for filename in os.listdir(image_folder):
        if filename.split('.')[-1].lower() in allowed_extensions:
            images.append(f'/{image_folder}/{filename}')

    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea il database e le tabelle
    app.run(debug=True)

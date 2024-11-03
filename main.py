from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Crea un'istanza di SQLAlchemy
db = SQLAlchemy()

# Crea un'istanza di LoginManager
login_manager = LoginManager()

# Definisci il modello User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia la chiave segreta
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inizializza SQLAlchemy e LoginManager con l'app
    db.init_app(app)
    login_manager.init_app(app)

    # Registrazione delle route
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)

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
                flash('Login eseguito con successo!')
                return redirect(url_for('gallery'))
            else:
                flash('Credenziali non valide. Riprova.')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sei stato disconnesso con successo.')
        return redirect(url_for('login'))

    @app.route('/')
        def gallery():
        images = []
        image_folder = 'static/images'
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}

        for filename in os.listdir(image_folder):
            if filename.split('.')[-1].lower() in allowed_extensions:
                images.append(f'/{image_folder}/{filename}')

        return render_template('gallery.html', images=images)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Crea il database e le tabelle
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()  # Crea l'app utilizzando la funzione
    app.run(host='0.0.0.0', port=5000, debug=True)


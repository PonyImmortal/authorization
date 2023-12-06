from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from models import db
from models.user import User, Application

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/vhod')
def vhod():
    return render_template('vhod.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['register_login']
        password = request.form['register_password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Пароли не совпадают', 'danger')
            return render_template('registration.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user is not None:
            flash('Пользователь с таким логином уже существует', 'danger')
            return render_template('registration.html')

        new_user = User(username=username)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        flash(f'Пользователь "{username}" успешно зарегистрирован, можете выполнить вход', 'success')
        return redirect(url_for('login'))

    return render_template('registration.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        remember = 'remember' in request.form

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return render_template('vhod.html')


@app.route('/dashboard')
@login_required
def dashboard():
    apps = current_user.applications
    return render_template('dashboard.html', apps=apps)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

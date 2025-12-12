from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (LoginManager,
                         UserMixin,
                         login_user,
                         logout_user,
                         login_required)
import datetime
from forms import LoginForm
from models import Setting, User

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@app.context_processor
def inject():
    return {'current_year': datetime.datetime.now(datetime.timezone.utc).year}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(
            username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)

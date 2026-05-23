from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)
class User(db.Model):
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(40), unique = True, primary_key=True)
    password = db.Column(db.String(50))
    
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
  
with app.app_context():
    db.create_all() 
@app.route("/")
def home():
    return "hi"
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name = name, email = email, password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("login")
    return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect("dashboard")
        else:
            render_template("login.html", error = "invalid user")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if session["name"]:
        user = User.query.filter_by(email = session["email"]).first()
        return render_template("dashboard.html", user = user)
    return redirect("login.html")
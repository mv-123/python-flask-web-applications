from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"

db = SQLAlchemy(app)
class File(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    filename = db.Column(db.String(100), nullable = False)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    files = File.query.all()
    return render_template('upload_img.html', files = files)

@app.route("/uploads", methods = ["POST"])
def uploads():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            newfile = File(filename = filename)
            db.session.add(newfile)
            db.session.commit()
            return redirect("/")
    return "if something is wrong, please try again"

@app.route("/uploaded_file/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/download/<int:file_id>")
def download(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(app.config["UPLOAD_FOLDER"], file.filename, as_attachment = True)

@app.route("/delete/<int:file_id>")
def delete(file_id):
    file = File.query.get_or_404(file_id)
    filename = file.filename
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    return redirect("/")

@app.route("/refresh")
def refresh():
    all_files = app.config["UPLOAD_FOLDER"]
    for filename in os.listdir(all_files):
        file_path = os.path.join(all_files, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    File.query.delete()
    db.session.commit()
    return redirect("/")

# if __name__ == "main":
#     app.run(debug = True, port = 8000)
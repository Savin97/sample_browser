from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to browse files
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

# Route to upload files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

# Route to download files
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
# db = SQLAlchemy(app)
#
# # Define Report model
# class Report(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(100), nullable=False)
#     date_uploaded = db.Column(db.DateTime, nullable=False)
#     file_type = db.Column(db.String(20), nullable=False)
#
# # Initialize database
# db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
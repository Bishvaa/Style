import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stylesense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/wardrobe')
def wardrobe():
    return "Wardrobe Page (To be implemented)"

@app.route('/generator')
def generator():
    return "Generator Page (To be implemented)"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

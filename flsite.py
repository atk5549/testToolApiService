import os
import psycopg2
import requests
from datetime import datetime
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


URLDB = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = URLDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connection = psycopg2.connect(URLDB)
if connection:
    print("========================================================================")
    print("connection sucessfully!!!")
    print("========================================================================")


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class QuestionForDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer)
    text_question = db.Column(db.String(1024), unique=True, nullable=False)
    text_answer = db.Column(db.String(1024), nullable=False)
    airdate_question = db.Column(db.DateTime, nullable=False)
    saved_question = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<QuestionForDB %r>' % self.text_question

@app.route("/api/posts/<int:post_number>")
def postsItem(post_number):
    
    try:
        
        response = requests.get(f"https://jservice.io/api/random?count={post_number}",
                                headers={"Content-Type": "application/json"})
        res = response.json()

        for item in res:
            # print("========================================================================")
            # print(type(item))
            # print(item["id"])
            # print(item["question"])
            # print(item["answer"])
            # print(item["airdate"])
            # print("========================================================================")

            idQuestion: int = item["id"],
            textQuestion: str = item["question"],
            textAnswer: str = item["answer"],
            airdateQuestion: str = item["airdate"]

        
            ins = QuestionForDB(
                id_question = idQuestion,
                text_question = textQuestion,
                text_answer = textAnswer,
                airdate_question = airdateQuestion
            )
            db.session.add(ins)
            
        db.session.commit()
    except ValueError:
        print("Одинаковые данные !!!")
    
    return res

@app.route("/")
def index():
    return render_template("index.html",
                           title="Главная",
                           data=QuestionForDB.query.all())


if __name__ == "__main__":
    app.run(debug=True)
    
    
## if you have a proplem installation flask-sqlalchemy
## https://stackoverflow.com/questions/76159927/error-could-not-build-wheels-for-greenlet-which-is-required-to-install-pyproje



# I got the some issue when I was trying to download Flask-SQLAlchemy; I used the code below in my terminal and it worked:

# pip install --only-binary :all: greenlet
# pip install --only-binary :all: Flask-SQLAlchemy

# Python packages are often distributed as "wheels" (.whl files), which are pre-compiled binary packages. Try installing "greenlet" and "Flask-SQLAlchemy" using wheels instead of source distribution

### команда для миграции субд
### dependency:
### create environment var:
### 
### Flask-Migrate==3.1.0
### flask db init 
### flask db migrate
### flask db upgrade
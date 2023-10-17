import os
import requests
import psycopg2
from datetime import datetime
from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import sqlalchemy
load_dotenv()


app = Flask(__name__)


URLDB = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = URLDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connection = psycopg2.connect(URLDB)
# if connection:
#     print("========================================================================")
#     print("connection sucessfully!!!")
#     print("========================================================================")


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

@app.route("/api/posts/<int:post_number>", methods=['GET'])
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
            
            # idQuestion:      int = 146781
            # textQuestion:    str = "Summer in this country lasts from December to February"
            # textAnswer:      str = "Australia"
            # airdateQuestion: str = "2012-07-03T19:00:00.000Z"

            idQuestion:      int = item["id"],
            textQuestion:    str = item["question"],
            textAnswer:      str = item["answer"],
            airdateQuestion: str = item["airdate"]
        
            ins = QuestionForDB(
                id_question = idQuestion,
                text_question = textQuestion,
                text_answer = textAnswer,
                airdate_question = airdateQuestion
            )
            db.session.add(ins)
            
        db.session.commit()
        
    # except psycopg2.errors.UniqueViolation as err:
    except sqlalchemy.exc.IntegrityError as err:
        print("========================================================================================")
        print("Caught UniqueViolation error || Обнаружена ошибка в Нарушении уникальности данных:")
        print("========================================================================================")
        print(err)
        print("========================================================================================")
        db.session.rollback()
        redirectBeforeURL = url_for('postsItem', post_number=post_number)
        # print("редирекаемся на: ", queryURL)
        return redirect(redirectBeforeURL)
        
        
    
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


# https://stacktuts.com/how-to-catch-a-psycopg2-errors-uniqueviolation-error-in-a-python-flask-app
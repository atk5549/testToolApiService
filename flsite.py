import os
import requests
from datetime import datetime
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from dotenv import load_dotenv
import sqlalchemy
load_dotenv()


app = Flask(__name__)
api = Api(app)


URLDB = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = URLDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create model
class QuestionForDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer)
    text_question = db.Column(db.String(1024), unique=True, nullable=False)
    text_answer = db.Column(db.String(1024), nullable=False)
    airdate_question = db.Column(db.DateTime, nullable=False)
    saved_question = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<QuestionForDB %r>' % self.text_question
    
    
    
    
    
class QuestionList(Resource):
    def post(self):
        data = request.get_json()
        if 'questions_num' in data:
            post_number = data['questions_num']
            try:
                response = requests.get(f"https://jservice.io/api/random?count={post_number}",
                                        headers={"Content-Type": "application/json"})
                res = response.json()

                for item in res:

                    # type annotation
                    idQuestion:      int = item["id"],
                    textQuestion:    str = item["question"],
                    textAnswer:      str = item["answer"],
                    airdateQuestion: str = item["airdate"]

                    # prepare data and insert to database
                    ins = QuestionForDB(
                        id_question = idQuestion,
                        text_question = textQuestion,
                        text_answer = textAnswer,
                        airdate_question = airdateQuestion
                    )
                    db.session.add(ins)
                    
                db.session.commit()

            # catching uniqueviolation error 
            except sqlalchemy.exc.IntegrityError as err:
                print("========================================================================================")
                print("Caught UniqueViolation error || Обнаружена ошибка в Нарушении уникальности данных:")
                print("========================================================================================")
                print(err)
                print("========================================================================================")
                db.session.rollback()
                redirectBeforeURL = url_for('postsItem', post_number=post_number)
                
                # if the question not unique then redirect to postItem url
                return redirect(redirectBeforeURL)
            
            
            
            return {'questions_num': post_number}, 200
        else:
            return 'questions_num is required', 400

api.add_resource(QuestionList, '/api/v1/questions/')




# get questions via GET method
@app.route("/api/v1/questions/<int:post_number>", methods=['GET'])
def postsItem(post_number):
    if request.method == 'GET':
        try:
            
            response = requests.get(f"https://jservice.io/api/random?count={post_number}",
                                    headers={"Content-Type": "application/json"})
            res = response.json()

            for item in res:

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

        except sqlalchemy.exc.IntegrityError as err:
            print("========================================================================================")
            print("Caught UniqueViolation error || Обнаружена ошибка в Нарушении уникальности данных:")
            print("========================================================================================")
            print(err)
            print("========================================================================================")
            db.session.rollback()
            redirectBeforeURL = url_for('postsItem', post_number=post_number)
            # print("редирекаемся заново на: ", queryURL)
            return redirect(redirectBeforeURL)
        return res

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
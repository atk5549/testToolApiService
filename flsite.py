import os
from datetime import datetime
from flask import Flask, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

from dotenv import load_dotenv
load_dotenv()


# DESERIALAZED DATA
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec

import requests


app = Flask(__name__)

URLDB = os.getenv("DATABASE_URL")
connection = psycopg2.connect(URLDB)
if connection:
    print("connection suessfully!!!")


app.config['SQLALCHEMY_DATABASE_URI'] = URLDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

### команда для миграции субд
### dependency:
### create environment var:
### 
### Flask-Migrate==3.1.0
### flask db init 
### flask db migrate
### flask db upgrade

class QuestionForDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_question = db.Column(db.String(1024), unique=False, nullable=False)
    text_answer = db.Column(db.String(1024), nullable=False)
    pub_question = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<QuestionForDB %r>' % self.text_question


docs = FlaskApiSpec()
docs.init_app(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})

headers = {
    "Content-Type": "application/json",
}



postinfo = [
    
    {
    "id": 0,
    "post": "postinfo1"
    },
    {
    "id": 1,
    "post": "postinfo2"
    }
]


@app.route("/")
def index():
    return render_template("index.html", title="Главная", data=QuestionForDB.query.all())

@app.route("/api/posts/")
def posts():
    return jsonify(postinfo)



@app.route("/api/posts/<int:post_number>")
def postsItem(post_number):
    response = requests.get(f"https://jservice.io/api/random?count={post_number}", headers=headers)
    res = response.json()
    print(res[0]["id"])
    print(res[0]["question"])
    print(res[0]["answer"])
    
    # ins = QuestionForDB(
    #     id=post_number,
    #     text_question="my first text question",
    #     text_answer="my first text answer"
    # )
    # db.session.add(ins)
    # db.session.commit()
    
    return res


if __name__ == "__main__":
    app.run(debug=True)
    
    
## if you have a proplem installation flask-sqlalchemy
## https://stackoverflow.com/questions/76159927/error-could-not-build-wheels-for-greenlet-which-is-required-to-install-pyproje



# I got the some issue when I was trying to download Flask-SQLAlchemy; I used the code below in my terminal and it worked:

# pip install --only-binary :all: greenlet
# pip install --only-binary :all: Flask-SQLAlchemy

# Python packages are often distributed as "wheels" (.whl files), which are pre-compiled binary packages. Try installing "greenlet" and "Flask-SQLAlchemy" using wheels instead of source distribution
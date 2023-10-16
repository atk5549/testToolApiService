from flask import Flask, jsonify, render_template

app = Flask(__name__)


answer = {
    "name": "Roman",
    "surename": "Kovalchuk",
    "title_index": "Главная страница"
}

postinfo = [
    {
    "id": 0,
    "post": "postinfo1"
    },
    {
    "id": 1,
    "post": "postinfo2"
    },
]


@app.route("/")
def index():
    return render_template("index.html", data=answer)



@app.route("/api/posts/<int:post_number>")
def posts(post_number):
    mypost = postinfo[post_number]
    return jsonify(mypost)


if __name__ == "__main__":
    app.run(debug=True)
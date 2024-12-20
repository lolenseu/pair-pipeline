from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to Pair-Pipeline!"


@app.route('/pair/')
def pair():
    pass

@app.route('/pipeline/')
def pipeline():
    pass


if __name__ == '__main__':
    app.run(debug=True)
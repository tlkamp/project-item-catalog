import flask

app = flask.Flask(__name__)


@app.route('/')
@app.route('/catalog')
def default():
    return 'Hello World!'


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
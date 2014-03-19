from flask import Flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    manager.run()

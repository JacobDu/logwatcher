from flask import Flask, render_template
from watcher import Watcher
import json

app = Flask(__name__)
app.config.from_object('config.MyConfig')
watcher = Watcher(app.config.get('LOG_PATH'))
watcher.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<timestamp>', methods=['POST'])
def fetch(timestamp):
    return json.dumps(watcher.fetch(float(timestamp)))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, Response, request
from flask_cors import CORS
from redis import StrictRedis
from collections import namedtuple, Counter

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
Tile = namedtuple("Tile", ["x", "y", "z"])
tile_counter = Counter()
db = StrictRedis(host="localhost", port=6379, db=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tile")
def tile():
    tilex = request.args['x']
    tiley = request.args['y']
    zoom = request.args['z']
    t = Tile(tilex, tiley, zoom)
    try:
        result = db.get("%s_%s_%s" % (zoom, tilex, tiley))
    except:
        pass
    tile_counter[t] += 1
    return Response(result, mimetype='image/png')


if __name__ == "__main__":
    app.run()


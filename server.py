import math
from flask_cors import CORS
from redis import StrictRedis
from flask import Flask, render_template, Response, request

from utils.utils import GlobalMercator, deg2num
from utils import utm, gps_transform

MAXZOOMLEVEL = 32
GM = GlobalMercator()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# db = StrictRedis(host="localhost", port=6380, db=0)
# db = StrictRedis(host="localhost", port=6380, db=1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tile")
def tile():
    tilex = int(request.args['x'])
    tiley = int(request.args['y'])
    zoom = int(request.args['z'])

    # with open("sample.tfw", "r") as fr:
    #     content = fr.read()
    #     laty, lonx = content.splitlines()[4:]  # 506745.528140000068, 4062749.627380000427
    # lat, lon = utm.to_latlon(float(laty), float(lonx), 50, "U")  # 36.710400756495844, 117.07552736231953
    # lon, lat = gps_transform.gcj02tobd09(lon, lat)  # 36.71619511543831, 117.08480138258149

    # lat, lon = 36.710400756495844, 117.07552736231953
    lat, lon = 36.711608315232034, 117.08250959049264
    # lat, lon = 36.71619511543831, 117.08480138258149
    # ori_x, ori_y = deg2num(lat, lon, zoom)

    lat_m, lon_m = GM.LatLonToMeters(lat, lon)
    lat_t, lon_t = GM.MetersToTile(lat_m, lon_m, zoom)
    ori_x, ori_y = GM.GoogleTile(lat_t, lon_t, zoom)
    print ("ori_x=%s\tori_y=%s" % (ori_x, ori_y))
    try:
        with open("../../nkyt2/%s/%s/%s.png" % (zoom - 15, tilex-ori_x, tiley-ori_y-1), "rb") as fr:
            result = fr.read()
    except:
        result = None
    return Response(result, mimetype='image/png')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")

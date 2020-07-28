from flask import Flask, request,jsonify
import requests
import pandas as pd
from geopy import distance
import itertools
import io

app = Flask(__name__)


def get_distance_for_pair_of_points(point1,point2):
    return {
        "name": point1["Point"]+point2["Point"],
        "distance":1000*distance.distance(
        (point1["Latitude"],point1["Longitude"]),
        (point2["Latitude"],point2["Longitude"])

    ).km
    }

@app.route("/api/getAddresses", methods=['POST'])
def getAddresses():

    # read file
    f = request.files['filedata']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), 
    )

    list_of_points = pd.read_csv(stream)[['Point', 'Latitude', 'Longitude']].to_dict(orient="records")

    # get addresses
    res = []
    for item in list_of_points:
        latitude,longitude = item['Latitude'],item['Longitude']
        url = f"http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location={longitude}%2C{latitude}&langCode=en&outSR=&forStorage=false&f=pjson"
        address = requests.get(url).json()["address"]["LongLabel"]
        res.append({
            "name":item["Point"],
            "address":address
        })

    # calculate distance for every possible pair
    list_of_pairs = list(itertools.combinations(list_of_points, 2))
    return jsonify(
        {
            "points":res,
            "links":[get_distance_for_pair_of_points(x,y) for x,y in list_of_pairs]

        }
        
        )    



if __name__ == "__main__":
    app.run(host='0.0.0.0')
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
import requests
import googlemaps
import string
import gmaps
from flask import Flask
from flask_googlemaps import GoogleMaps
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from flask import redirect
from flask import url_for
from flask import request



def TSP_algorithm(distanse_matrix):
    permutation, distance = solve_tsp_dynamic_programming(distanse_matrix)
    return permutation



def distance(locations):
    gmaps = googlemaps.Client(key='AIzaSyBEgfYV03Mr6v5ve6TZ2NnZr0V7CP83Nvc')
    api_key = "AIzaSyBEgfYV03Mr6v5ve6TZ2NnZr0V7CP83Nvc"
    x = len(locations)
    matrix_locations = np.empty([x, x])

    for i in range(len(locations)):
        row_time = []
        for loc in locations:
            # base url
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
            # get response
            r = requests.get(url + "origins=" + locations[i] + "&destinations=" + loc + "&key=" + api_key)
            # return time as text and as seconds
            seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]
            row_time.append(seconds)
        matrix_locations[i] = row_time



    arr_ideal = TSP_algorithm(matrix_locations)

    # returns the cordinata of locations
    cordinata_location = []
    for loc in arr_ideal:
        cor = locations[loc]
        result = gmaps.geocode(str(cor))
        cordinata_location.append(result[0]['geometry']['location'])
    return cordinata_location





app = Flask(__name__, template_folder="./templates")
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBEgfYV03Mr6v5ve6TZ2NnZr0V7CP83Nvc"

# Initialize the extension

GoogleMaps(app)

@app.route("/map", methods=['POST', 'GET'])
def map():
    #locations=request.form['locations']
    locations=request.args.get('cities').split(',')
    #locations = ["בת ים", "רחובות","תל אביב"]
    #print(locations)
    order = distance(locations)
    marks=[]

    for (loc, index) in zip(order, string.ascii_uppercase):
        mark={}
        mark['icon']='http://www.google.com/mapfiles/marker'+index+'.png'
        mark['lng']=loc['lng']
        mark['lat']=loc['lat']
        #mark['infobox']="1"
        marks.append(mark)

    mymap = Map(
    identifier="view-side",
    lat=31.7833302,
    lng=35.2166658,
    zoom=7,
        markers=marks
            #{
                #icons.dots.blue: [(37.4419, -122.1419), (37.4500, -122.1350)]
            #icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
                #'icon': icons.alpha.A,
                #'lng': order[0]['lng'],
                #'lat': order[0]['lat'],
            #'label': "X"
            #}#for loc in order
        #],
    )

    return render_template('map.html', mymap=mymap, )


# location=distance(l)



    #for i in locations:
        #order.append((di))
    # creating a map in the view





@app.route("/")
def index():
    return render_template('Web.html')


if __name__=="__main__":
    app.run(debug=True)
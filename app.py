from flask import Flask, render_template, request
import pickle
import warnings
import pandas as pd
from geopy.distance import geodesic
import json
from urllib.request import urlopen

df = pd.read_csv('zone.csv')
data = pd.read_csv('newdata.csv')
zones = []

def distance(user_coords, earthquake_coords):
    res = geodesic(user_coords, earthquake_coords).km
    res = round(res,2)
    return res

app = Flask(__name__)
warnings.filterwarnings("ignore")
with open('rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/map', methods=['POST'])

# def distance(user_coords, earthquake_coords):
#     res = geodesic(user_coords, earthquake_coords).km
#     res = round(res,2)
#     return res

def loc():
    lat = (float)(request.form['lat'])
    long = (float)(request.form['long'])
    magnitude = model.predict([[lat, long]])

    # if magnitude >= 6:
    #     zone = "red"
    # elif magnitude >=4 and magnitude <6 :
    #     zone = "yellow"
    # elif magnitude < 4:
    #     zone = "green"

    user_coords = [lat,long]
    df['distance'] = df.apply(lambda x: distance(user_coords,[x['lat'], x['lon']]), axis=1)
    data['distance'] = data.apply(lambda x: distance(user_coords, [x['Lat'], x['Long']]), axis=1)
    # nearest_lat= df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['lat']
    # nearest_long = df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['lon']
    # nearest_distance = df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['distance']
    nearest_lat= data.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['Lat']
    nearest_long = data.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['Long']
    nearest_distance = data.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['distance']
    nearest_coords = [nearest_lat, nearest_long]
    nearest_zone = df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['Zone']
    zones.append(nearest_zone)
    

    return render_template('distance_map_tooltip.html', zone=nearest_zone , lat=lat, long=long, nearest_coords=nearest_coords, nearest_distance=nearest_distance)

@app.route('/current_loc')
def current_loc():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    location = json.load(response)
    lat, long = (location['loc']).split(",")
    lat = float(lat)
    long = float(long)
    magnitude = model.predict([[lat, long]])
    user_coords = [lat,long]
    df['distance'] = df.apply(lambda x: distance(user_coords,[x['lat'], x['lon']]), axis=1)
    data['distance'] = data.apply(lambda x: distance(user_coords, [x['Lat'], x['Long']]), axis=1)
    # nearest_lat= df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['lat']
    # nearest_long = df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['lon']
    # nearest_distance = df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['distance']
    nearest_lat= data.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['Lat']
    nearest_long = data.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['Long']
    nearest_distance = data.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['distance']
    nearest_coords = [nearest_lat, nearest_long]
    nearest_zone = df.sort_values(by=['distance'], axis=0, ascending=True).iloc[0]['Zone']
    zones.append(nearest_zone)
    return render_template('distance_map_tooltip.html', zone=nearest_zone , lat=lat, long=long, nearest_coords=nearest_coords, nearest_distance=nearest_distance)

@app.route('/precaution')
def precaution():
    nearest_zone = zones[len(zones) - 1]
    if nearest_zone == "II":
        return render_template('zone2.html')
    elif nearest_zone == "III":
        return render_template('zone3.html')
    elif nearest_zone == "IV":
        return render_template('zone4.html')
    elif nearest_zone == "V":
        return render_template('zone5.html')

@app.route('/bzone2')
def bzone2():
    return render_template('bzone2.html')

@app.route('/bzone3')
def bzone3():
    return render_template('bzone3.html')

@app.route('/bzone4')
def bzone4():
    return render_template('bzone4.html')

@app.route('/bzone5')
def bzone5():
    return render_template('bzone5.html')

if __name__ == '__main__':
    app.run(debug=True)
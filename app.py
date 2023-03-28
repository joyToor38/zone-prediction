from flask import Flask, render_template, request
import pickle
import warnings
import pandas as pd
from geopy.distance import geodesic
import json
from urllib.request import urlopen
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
# import os

# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


# Latitude & Longitude input
def get_city(Latitude, Longitude):
    Latitude = str(Latitude)
    Longitude = str(Longitude)

    location = geolocator.reverse(Latitude+","+Longitude)

    address = location.raw['address']

    # traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    return city


df = pd.read_csv('zone.csv')
data = pd.read_csv('newdata.csv')
graph_df = pd.read_csv('graphdata.csv')
zones = []
lats=[]
longs=[]



def distance(user_coords, earthquake_coords):
    res = geodesic(user_coords, earthquake_coords).km
    res = round(res,2)
    return res

app = Flask(__name__)
warnings.filterwarnings("ignore")
with open('random_forest.pkl', 'rb') as f:
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
    lats.append(lat)
    longs.append(long)
    

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
    ans = model.predict([[lat,long,10]])
    ans = str(ans)
    final_ans = ans.replace("[", "").replace("'", "").replace("]", "")
    final_ans = final_ans.capitalize()


    return render_template('distance_map_tooltip.html', ans=final_ans, zone=nearest_zone , lat=lat, long=long, nearest_coords=nearest_coords, nearest_distance=nearest_distance)

@app.route('/current_loc')
def current_loc():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    location = json.load(response)
    lat, long = (location['loc']).split(",")
    lat = float(lat)
    long = float(long)
    lats.append(lat)
    longs.append(long)
    
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
    ans = model.predict([[lat,long,10]])
    ans = str(ans)
    ans = ans.replace("[", "").replace("'", "").replace("]", "")
    ans = ans.capitalize()
    return render_template('distance_map_tooltip.html', ans=ans, zone=nearest_zone , lat=lat, long=long, nearest_coords=nearest_coords, nearest_distance=nearest_distance)

@app.route('/graph')
def graph():
    lat = lats[len(lats) - 1]
    long = longs[len(longs) - 1]
    # lat = request.form['lat']
    # long = request.form['long']

    city = get_city(lat,long)

    # graph_df = pd.read_csv("graphdata.csv")
    city_data = graph_df[graph_df["CITY"] == city]

    # Group the data by year and count the earthquakes
    year_counts = city_data.groupby("Year").size()

    # Create a bar plot of the earthquake counts by year
    plt.bar(year_counts.index, year_counts.values, color='lightblue')
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title(f"Earthquake Counts in {city} by Year")

    # Add labels to the bars
    for i, v in enumerate(year_counts.values):
        plt.text(year_counts.index[i], v, str(v), ha='center', va='bottom')

    # Add a horizontal line for the maximum count
    # max_count = year_counts.max()
    # plt.axhline(y=max_count, color='red', linestyle='--', alpha=0.5)
    # plt.text(year_counts.index[-1], max_count, f"Max: {max_count}", ha='right', va='center', color='red')

    
#     plt.savefig('graph.png')
    plt.savefig(f'static/{city}.png')

    return render_template('graph.html', city=city)


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

@app.route('/final')
def final():
    lat = lats[len(lats) - 1]
    long = longs[len(longs) - 1]
    city = get_city(lat,long)
    source = str(f"static/{city}.png")
    return render_template('image.html', source = source)

if __name__ == '__main__':
    app.run(debug=True)
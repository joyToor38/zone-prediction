from flask import Flask, render_template, request
import pickle
import warnings

app = Flask(__name__)
warnings.filterwarnings("ignore")
with open('rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/map', methods=['POST'])
def loc():
    lat = (float)(request.form['lat'])
    long = (float)(request.form['long'])
    magnitude = model.predict([[lat, long]])

    if magnitude >= 6:
        zone = "red"
    elif magnitude >=4 and magnitude <6 :
        zone = "yellow"
    elif magnitude < 4:
        zone = "green"

    return render_template('output2.html', lat=lat, long=long, magnitude=magnitude, zone=zone)

if __name__ == '__main__':
    app.run(debug=True)
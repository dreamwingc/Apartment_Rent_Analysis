from flask import Flask, render_template, request
from sklearn.externals import joblib
from sklearn import linear_model, preprocessing
import memcache
import pickle
import os

web = Flask(__name__)


@web.route("/", methods=['GET', 'POST'])
def web_page():
    geo_location = {'san_jose_south': [37.260051, -121.836636],
                    'san_jose_north': [37.387622, -121.893933],
                    'san_jose_west': [37.302557, -121.983071],
                    'san_jose_east': [37.335163, -121.807102],
                    'milpitas': [37.435165, -121.896299],
                    'santa_clara': [37.365837, -121.966180],
                    'sunnyvale': [37.381047, -122.025153],
                    'los gatos': [37.229648, -121.949819],
                    'campbell': [37.282795, -121.950746],
                    'cupertino': [37.317918, -122.039611],
                    'mountain_view': [37.401455, -122.082126]}

    memcacheClient = memcache.Client(['127.0.0.1:11211'], debug=1)
    if request.method == 'POST':
        queryLocation = request.form.get('location')
        queryBedroom = request.form.get('bedroom')

        queryMLocation = request.form.get('mlocation')
        queryMBedroom= request.form.get('mbedroom')
        queryMSqr = request.form.get('msquarefeet')

        if queryLocation:
            queryLocation = queryLocation.replace(' ', '_')
            results = memcacheClient.get(queryLocation)
            results = sorted(results, key=lambda x: int(x[1]))
            return render_template("googlemap.html", data=results, coordinate=geo_location[queryLocation])
        elif queryBedroom:
            results = memcacheClient.get(queryBedroom + 'br')
            results = sorted(results, key=lambda x: int(x[1]))
            return render_template("result.html", data=results)
        elif queryMBedroom and queryMLocation and queryMSqr:
            dirlocal = os.path.dirname(os.path.abspath(__file__))
            file_name = os.path.join(dirlocal, 'location_dict.pkl')
            location_file = open(file_name, "rb")
            location_dict = pickle.load(location_file)
            location_file.close()

            location = location_dict[" " + queryMLocation]
            query_data = [location, int(queryMBedroom), int(queryMSqr)]

            scaler_name = os.path.join(dirlocal, 'scaler.pkl')
            scaler = joblib.load(scaler_name)
            query_data = scaler.transform([query_data])

            trained_name = os.path.join(dirlocal, 'linear_regression_trained.pkl')
            linear_regression_trained = joblib.load(trained_name)
            prediction = linear_regression_trained.predict(query_data)

            queryMLocation = queryMLocation.replace(' ', '_')
            results = memcacheClient.get(queryMLocation)
            output = []

            for item in results:
                if item[3][0] == queryMBedroom and abs(prediction - int(item[1])) < 50:
                    output.append(item)

            output = sorted(output, key=lambda x: int(x[1]))
            return render_template("machinelearning.html", data=output, pre=[int(prediction[0])],
                                   coordinate=geo_location[queryMLocation])
        else:
            return "Error"
    return render_template("initial.html", name=None)


if __name__ == "__main__":
    web.run()
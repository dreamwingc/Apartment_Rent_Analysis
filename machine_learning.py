import mysql.connector
from sklearn import linear_model, preprocessing
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.externals import joblib
import pickle

class ResultAnalysis():
    def __init__(self):
        self.mysqlPool = mysql.connector.connect(user='root', password='mypassword', host='127.0.0.1',
                                                 database='web_crawler')

    def machine_learning(self):
        cursor_all = self.mysqlPool.cursor(buffered=True)

        cursor_all.execute("select price, location, floor_plan from web_crawler")

        self.mysqlPool.commit()
        all_all = cursor_all.fetchall()

        feature_all = []
        location_dict = {}
        location_index = 0
        for feature in all_all:
            if int(feature[0]) > 10000 or feature[1].lower() == 'none' or '-' not in feature[2] or 'ft' not in feature[2]:
                continue
            feature_all.append(feature)
            location = feature[1].lower()
            if location not in location_dict:
                location_dict[location] = location_index
                location_index += 1

        location_file = open("location_dict.pkl", "wb")
        pickle.dump(location_dict, location_file)
        location_file.close()

        label = []
        location_all = []
        bedroom_all = []
        sqr_feet_all = []
        training_data = []
        for i in range(len(feature_all)):
            label.append(int(feature_all[i][0]))

            location = location_dict[feature_all[i][1].lower()]
            location_all.append(location)

            floor_plan = feature_all[i][2].split('-')

            bedroom = int(floor_plan[0][0:-2])
            bedroom_all.append(bedroom)

            sqr_feet = int(floor_plan[1][0:-2])
            sqr_feet_all.append(sqr_feet)

            training_data.append([location, bedroom, sqr_feet])

        scaler = preprocessing.MinMaxScaler()
        scaler.fit(training_data)

        joblib.dump(scaler, 'scaler.pkl')

        training_data = scaler.transform(training_data)

        print label
        print training_data

        # linear regression
        linear_regression = linear_model.LinearRegression()
        linear_regression.fit(training_data, label)

        joblib.dump(linear_regression, 'linear_regression_trained.pkl')

        prediction = linear_regression.predict(training_data)

        plt.scatter(location_all, label, color='black')

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(bedroom_all, sqr_feet_all, label, c='b', marker='o')
        ax.scatter(bedroom_all, sqr_feet_all, prediction, c='r', marker='^')

        ax.set_xlabel('Number of bedrooms')
        ax.set_ylabel('Square feet')
        ax.set_zlabel('Monthly rent')

        plt.show()

if __name__ == '__main__':
    result = ResultAnalysis()
    result.machine_learning()

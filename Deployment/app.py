import numpy as np
import pandas as pd 
import joblib
import lightgbm as lgb
from flask import Flask, jsonify, request,render_template
import flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    clf= joblib.load('final_model.pkl')
    to_predict_list = request.form.to_dict()
    to_predict_list = list(to_predict_list.values())
    to_predict_list = np.array(list(map(float, to_predict_list))).reshape(1, -1)
    print(to_predict_list)
    pred = clf.predict(to_predict_list)

    if pred == [0]:
        print('Hard Drive: Running')
        status= 'Running'

    else:
        print('Hard Drive: Fail')
        status= 'Fail'

    print(pred)

    return jsonify({'prediction': str(status)})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
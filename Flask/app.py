
from flask import Flask, request
import json
import numpy as np
import pickle

def load_models():
    file_name = "models/salary_model.pkl"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

app = Flask(__name__)
@app.route('/predict-salary', methods=['GET'])
def predict():
    # stub input features
    request_json = request.get_json()

    x_list = request_json['input']
    predictions = []
    for x in x_list:
        x_in = np.array(x).reshape(1,-1)
        # load model
        model = load_models()
        prediction = model.predict(x_in)[0]
        predictions.append(prediction.tolist())

    print(predictions)
    response = json.dumps({'response': predictions}) 
    return response, 200

if __name__ == '__main__':
    application.run(debug=True)
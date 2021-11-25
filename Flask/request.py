import requests 
from data_input_parse import parset_input_data, get_dummy_header
from pdb import set_trace as bp

if __name__ == "__main__":
    data_path = "test_data.csv" # data example

    URL = 'http://127.0.0.1:5000/predict-salary'
    headers = {"Content-Type": "application/json"}
    data = {"input": parset_input_data(data_path)}

    r = requests.get(URL,headers=headers, json=data) 

    print(r.json())
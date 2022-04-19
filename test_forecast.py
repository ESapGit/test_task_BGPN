import requests
import time
import json
import os


host = "https://api.open-meteo.com/"


def test_minimal_parameters():
    url = "v1/forecast"
    payload = {'latitude': 51.5002, 'longitude': -0.1262, 'timeformat':'unixtime','timezone':'Europe/London'}
    response = requests.get(host+url, params=payload)
    with open('responses/minimal_parameters' + str(time.time()) + '.json', 'w') as f:
        json.dump(response.json(), f)
    assert response.status_code == 200


def test_maximal_parameters():
    url = "v1/forecast"
    with open('maximal_parameters.json') as fp:
        data = fp.read()
        params = json.loads(data)
        payload = ""
        for k, v in params.items():
            print(k, v)
            print(type(k), type(v))
            if type(v) == list:
                payload = payload + k + "=" + ",".join(v) + "&"
            else:
                payload = payload + k + "=" + str(v) + "&"
    response = requests.get(host+url, params=payload)
    with open('responses/maximal_parameters' + str(time.time()) + '.json', 'w') as f:
        json.dump(response.json(), f)
    assert response.status_code == 200


def test_custom_parameters():
    url = "v1/forecast"
    directory = 'custom_body_parameters'
    for filename in os.listdir(directory):
        fcustom = os.path.join(directory, filename)
        with open(fcustom) as fp:
            data = fp.read()
            params = json.loads(data)
            payload = ""
            for k, v in params.items():
                print(k, v)
                print(type(k), type(v))
                if type(v) == list:
                    payload = payload + k + "=" + ",".join(v) + "&"
                else:
                    payload = payload + k + "=" + str(v) + "&"
        response = requests.get(host+url, params=payload)
        with open('responses/data' + filename + str(time.time()) + '.json', 'w') as fw:
            json.dump(response.json(), fw)
        assert response.status_code == 200


def test_response_code_400():
    url = "v1/forecast"
    payload = {'latitude': 351.5002, 'longitude': -0.1262, 'timeformat': 'unixtime', 'timezone': 'Europe/London'}
    response = requests.get(host + url, params=payload)
    json_response = json.loads(response.content)
    assert response.status_code == 400
    assert json_response['reason'][0:47] == 'Latitude must be in rang of -90 to 90°. Given: '
    assert json_response['error'] == True


def test_response_code_404():
    url = "v2/forecast"
    payload = {'latitude': 351.5002, 'longitude': -0.1262, 'timeformat': 'unixtime', 'timezone': 'Europe/London'}
    response = requests.get(host + url, params=payload)
    json_response = json.loads(response.content)
    assert response.status_code == 404
    assert json_response['reason'] == 'Not Found'
    assert json_response['error'] == True




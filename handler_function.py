import json
import joblib
import sklearn

model_name = 'model_1636456626.6694472.joblib'
model = joblib.load(model_name)

def predict(event, context):
    body = {
        "message": 'ok'
    }
    params = event['queryStringParameters']

    medinc = float(params['medinc'])/100000
    houseage = float(params['houseage'])
    aveRooms = float(params['aveRooms'])
    aveBedrms = float(params['aveBedrms'])
    population = float(params['population'])
    aveOccup = float(params['aveOccup'])
    lat = float(params['lat'])
    long = float(params['long'])

    inputvector = [medinc, houseage, aveRooms, aveBedrms, population, aveOccup, lat, long]
    data = [inputvector]
    predictedprice = model.predict(data)[0] *100000
    predictedprice = round(predictedprice,2)
    body['predictedprice'] = predictedprice

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Origin": "*"
        }
    }
    return response

def do_main():
    event = {
        'queryStringParameters': {
            'medinc': 200000,
            'houseage': 10,
            'aveRooms': 4,
            'aveBedrms': 1,
            'population': 800,
            'aveOccup': 3,
            'lat': 37.54,
            'long': -121.72
                }
    }

    response = predict(event,None)
    body = json.loads(response['body'])
    print('price:', body['predictedprice'])

    with open('event.json','w') as event_file:
        event_file.write(json.dumps(event))

#do_main()
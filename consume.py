import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "Inputs": {
    "data": [
      {
        "age": 0,
        "job": "example_value",
        "marital": "example_value",
        "education": "example_value",
        "default": "example_value",
        "housing": "example_value",
        "loan": "example_value",
        "contact": "example_value",
        "month": "example_value",
        "day_of_week": "example_value",
        "duration": 0,
        "campaign": 0,
        "pdays": 0,
        "previous": 0,
        "poutcome": "example_value",
        "emp.var.rate": 0,
        "cons.price.idx": 0,
        "cons.conf.idx": 0,
        "euribor3m": 0.0,
        "nr.employed": 0
      }
    ]
  },
  "GlobalParameters": {
    "method": "predict"
  }
}

input_data = json.dumps(data)
with open("data.json", "w") as _f:
    _f.write(input_data)

body = str.encode(json.dumps(data))

url = 'http://bada2cad-8726-4e3a-9e51-35a68dcedd76.francecentral.azurecontainer.io/score'
api_key = 'jubrDJWeEA2TUuQf5BamWXVhjWi8zBID' # Replace this with the API key for the web service

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
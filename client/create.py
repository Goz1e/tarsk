import requests, json

auth_endpoint = 'http://127.0.0.1:8000/api/token/'
auth_response = requests.post(auth_endpoint,data={"username":"passdjango","email":"x@django.com"})

# print(json.loads(auth_response),  auth_response.status_code)
print(auth_response.status_code) 
print(auth_response.json()) 
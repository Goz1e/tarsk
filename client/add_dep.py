import requests

endpoint = "http://localhost:8000/api/brother-in-so-many-ways-man-cant-tell/add-comment/"

data = {
    'text':'new comment from terminal'
}

get_response = requests.post(endpoint, json=data)

print(get_response.status_code)
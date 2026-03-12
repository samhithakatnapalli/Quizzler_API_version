import requests

def fetch_questions():
    parameters = {
        'amount' : 50,
        'type' : 'boolean',
    }

    response = requests.get("https://opentdb.com/api.php",params=parameters)
    response.raise_for_status()
    json_data = response.json()

    return json_data['results']
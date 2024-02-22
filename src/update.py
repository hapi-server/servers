import json
import requests

def get_about(about_url):

    # Send a GET request and check for errors
    try:
        response = requests.get(about_url)
        response.raise_for_status()  # Raise an error if response code is not 2xx
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        exit(1)

    # Parse the JSON data
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        exit(1)

    return data

about = get_about("https://imag-data.bgs.ac.uk/GIN_V1/hapi/about")
id = about['id']
del about['status']
del about['HAPI']
about['contact'] = "Hello"

with open('../all.json') as f:
  all = json.load(f)

for server in all['servers']:
  if server['id'] != id:
    continue
  server = {**server, **about}
  print(json.dumps(server, indent=2))
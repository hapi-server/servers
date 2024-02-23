import json
import datetime
import requests

def get_about(about_url):

  print(f"Fetching {about_url}")
  try:
    response = requests.get(about_url, timeout=5)
    response.raise_for_status()  # Raise an error if response code is not 2xx
  except requests.exceptions.RequestException as e:
    print(f"  {e}")
    return e
  print(f"  Fetched {about_url}")

  try:
    data = json.loads(response.text)
  except json.JSONDecodeError as e:
    print(f"  Error parsing JSON from {about_url}:\n  {e}")
    return e

  return data

def equivalent_dicts(d1, d2):
  # Based on https://stackoverflow.com/a/10480904
  for k1, v1 in d1.items():
    if not k1.startswith("x_") and (k1 not in d2 or d2[k1] != v1):
      return False
  for k2, v2 in d2.items():
    if k1.startswith("x_") and k2 not in d1:
      return False
  return True

def write(fname, data):
  print(f"Writing {fname}")
  with open(fname, 'w') as f:
    f.write(data)

with open('../all.json') as f:
  all = json.load(f)

changed = False
all_file_str1 = ""
all_file_str2 = ""
for server in all['servers']:

  about = get_about(server['url'] + '/about') 
  server['x_LastUpdateAttempt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
  if isinstance(about, Exception):
    server['x_LastUpdateError'] = str(about)
  else:
    server['x_LastUpdateError'] = False
    del about["HAPI"]
    del about["status"]
    server_new = {**server, **about}
    if not equivalent_dicts(server, about):
      changed = True
      print(f"  Difference between all.json and {server['url']}")
      server["x_LastUpdateChange"] = server["x_LastUpdateAttempt"]
    else:
      print(f"  No difference between all.json and {server['url']}")

  all_file_str1 += f"{server['url']}, {server['title']}, {server['id']}, {server['contact']}, {server['contactID']}\n"
  all_file_str2 += f"{server['url']}\n"

write('../all.json.new', json.dumps(all, ensure_ascii=False, separators=(',', ': '), indent=2))

if changed == True:
  write('../all_.txt.new', all_file_str1)
  write('../all.txt.new', all_file_str2)
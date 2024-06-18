def logger(file_name=None):
  import os
  import time
  import inspect
  import logging

  # Print to stdout and file_name

  if file_name is None:
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    file_name = os.path.splitext(module.__file__)[0] + ".log"

  mkdir(os.path.dirname(file_name))

  if os.path.exists(file_name):
    os.remove(file_name)

  conf = {
    'handlers': [logging.FileHandler(file_name, 'w', 'utf-8'),
                 logging.StreamHandler()
              ],
    'level': logging.INFO,
    'format': u'%(asctime)s.%(msecs)03dZ %(message)s',
    'datefmt': '%Y-%m-%dT%H:%M:%S',
  }
  logging.basicConfig(**conf)

  logging.Formatter.converter = time.gmtime

  return logging.getLogger(__name__)

def utc_now():
  import datetime
  return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def mkdir(dirname, log=None):
  import os
  if not os.path.exists(dirname):
    if log is not None:
      log.info(f"Creating dir {dirname}")
    os.makedirs(dirname, exist_ok=True)

def get(url, log=None):
  assert log is not None, "log keyword argument must be provided"
  # TODO: Handle log=None

  import json
  import requests

  log.info(f"Getting {url}")
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an error if response code is not 2xx
  except requests.exceptions.RequestException as e:
    log.info(f"  {e}")
    return e
  log.info(f"  Got {url}")

  try:
    data = json.loads(response.text)
  except json.JSONDecodeError as e:
    log.info(f"  Error parsing JSON from {url}:\n  {e}")
    return e
  return data

def write(fname, data, log=None):
  import os

  mkdir(os.path.dirname(fname))

  if '.json' == os.path.splitext(fname)[1]:
    import json
    data = json.dumps(data, indent=2, ensure_ascii=False)

  if log is not None:
    log.info(f"Writing {fname}")

  # TODO: Catch open exception
  with open(fname, 'w', encoding='utf-8') as f:
    f.write(data)
    if log is not None:
      log.info(f"  Wrote {fname}")

def read(fname, log=None):
  import os
  import json

  if log is not None:
    log.info(f"Reading {fname}")
  try:
    f = open(fname, encoding='utf-8')
  except Exception as e:
    exit(f"Error opening {fname}: {e}")

  if '.json' == os.path.splitext(fname)[1]:
    try:
      data = json.load(f)
    except:
      if log is not None:
        log.info(f"Error parsing {fname}")
      exit(f"Error parsing {fname}: {e}")
  else:
    try:
      data = f.readlines()
    except:
      exit(f"Error reading {fname}: {e}")
  f.close()

  if log is not None:
    log.info(f"  Read {fname}")
  return data

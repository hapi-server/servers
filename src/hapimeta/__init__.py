def version():
  import os
  import json
  fname = open(os.path.join(os.path.dirname(__file__),'version.json'))
  return json.load(fname)['version']

__version__ = version()

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

def get(url, log=None, timeout=10):
  assert log is not None, "log keyword argument must be provided"
  # TODO: Handle log=None

  import json
  import requests

  log.info(f"Getting {url}")
  headers = {'User-Agent': f'hapibot-mirror/{version()}; https://github.com/hapi-server/data-specification/wiki/hapi-bots.md#hapibot-mirror'}
  try:
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()  # Raise an error if response code is not 2xx
  except Exception as e:
    log.error(f"  Error: {e}")
    raise e
  log.info(f"  Got {url}")

  try:
    data = json.loads(response.text)
  except json.JSONDecodeError as e:
    log.error(f"  Error parsing JSON from {url}:\n  {e}")
    raise e
  return data

def write(fname, data, log=None):
  import os

  mkdir(os.path.dirname(fname))

  if '.json' == os.path.splitext(fname)[1]:
    import json
    data = json.dumps(data, indent=2, ensure_ascii=False)

  if log is not None:
    log.info(f"Writing {fname}")

  try:
    f = open(fname, 'w', encoding='utf-8')
  except Exception as e:
    msg = f"Error opening {fname}: {e}"
    if log is not None:
      log.error(msg)
    raise e

  try:
    f.write(data)
  except:
    msg = f"Error writing {fname}: {e}"
    if log is not None:
      log.error(msg)
    raise e

  if log is not None:
    log.info(f"  Wrote {fname}")

def read(fname, log=None, exit_on_error=False):
  import os
  import json

  if log is not None:
    log.info(f"Reading {fname}")

  try:
    f = open(fname, encoding='utf-8')
  except Exception as e:
    msg = f"Error opening {fname}: {e}"
    if log is not None:
      log.error(msg)
    raise e

  if '.json' == os.path.splitext(fname)[1]:
    try:
      data = json.load(f)
      if log is not None:
        log.info(f"  Read and parsed {fname}")
    except Exception as e:
      msg = f"json.load({fname}) raised: {e}"
      if log is not None:
        log.info(msg)
      raise e
  else:
    try:
      data = f.readlines()
      if log is not None:
        log.info(f"  Read {fname}")
    except:
      msg = f"Error reading {fname}: {e}"
      if log is not None:
        log.error(msg)
      raise e

  f.close()

  return data

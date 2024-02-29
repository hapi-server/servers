import json
import logging

import pickle as pickle
from hapiclient import hapi

format = "%(asctime)s.%(msecs)03d %(message)s"
datefmt = "%Y-%m-%dT%H:%M:%S"
level = logging.INFO # Use WARNING or ERROR to suppress messages
logging.basicConfig(level=level, format=format, datefmt=datefmt)

fname = '../servers.json'
logging.info(f'Reading {fname}')
with open(fname) as f:
  all = json.load(f)
logging.info(f'Read {fname}')

s = 0
for server in all['servers']:
  url = server["url"]
  if 'TestData3.2' in url:
    continue
  if s > 2:
    break

  s = s + 1
  logging.info(f'{url}')

  logging.info(f' Getting /catalog')
  catalog = hapi(url, logging=False)
  datasets = catalog['catalog']
  logging.info(f' Got {len(datasets)} datasets')

  server["datasets"] = datasets
  for idx, dataset in enumerate(datasets):
    logging.info(f'  Getting /info?id={dataset["id"]}')
    try:
      info = hapi(url, dataset["id"], logging=False)
      logging.info(f'  Got {len(info["parameters"])} parameters')
    except Exception as e:
      pass

    server["datasets"][idx]["info"] = info

    if idx > 2:
      break

if False:
  fname = 'metadata.pkl'
  with open(fname, 'wb') as f:
    logging.info(f'Saving {fname}')
    pickle.dump(all, f)
    logging.info(f'Saved {fname}')

all = json.dumps(all, ensure_ascii=False, separators=(',', ': '), indent=2)
fname = '../metadata.json'
logging.info(f"Writing {fname}")
with open(fname, 'w') as f:
  f.write(all)
logging.info(f"Wrote {fname}")

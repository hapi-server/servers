import json

data_dir =  '../data'
max_infos = 2

files = {
  'servers': '../servers.json',
  'catalogs': '../data/catalogs.json',
  'catalogs_all': '../data/catalogs-all.json',
}

from hapimeta import logger, get, read, write, utc_now
log = logger()

servers = read(files['servers'], log=log)

def get_infos(url, datasets, max_infos=None):
  n = 1
  for dataset in datasets:
    info = get(url + "/info?id=" + dataset['id'], log=log)
    if isinstance(info, Exception):
      dataset['info'] = {'x_LastUpdateError': str(info)}
      continue
    dataset['info'] = info
    for parameter in dataset['info']['parameters']:
      if 'bins' in parameter:
        del parameter['bins']
    if max_infos is not None and n >= max_infos:
      return datasets
    n = n + 1
  return datasets

def get_catalogs(servers):
  catalogs = {}
  for obj in servers['servers']:
    log.info(obj['id'])
    catalog = get(obj['url'] + '/catalog', log=log)

    if isinstance(catalog, Exception):
      catalog = {
        'x_LastUpdateAttempt': utc_now(),
        'x_LastUpdateError': str(catalog)
      }
      continue

    if not 'catalog' in catalog:
      catalog = {
        'x_LastUpdateAttempt': utc_now(),
        'x_LastUpdateError': "No catalog node in JSON response."
      }
      continue

    if not 'x_LastUpdateError' in catalog:
      catalog['x_LastUpdate'] = utc_now()

    catalog['x_URL'] = obj['url']
    catalogs[obj['id']] = catalog
    write(f"{data_dir}/catalogs/{obj['id']}.json", catalog, log=log)

  return catalogs

catalogs = get_catalogs(servers)
write(files['catalogs'], catalogs, log=log)

for id, catalog in catalogs.items():
  # catalog['catalog'] is an array of dataset objects with at least a key of
  # 'id' (dataset id). The following adds an 'info' key to each dataset object.
  if 'x_LastUpdateError' in catalog['catalog']:
    msg = f"Skipping {id} because of error: {catalog['catalog']['x_LastUpdateError']}."
    log.info(msg)
    # TODO: read last info file: ../infos/{id}.json.
    continue
  get_infos(catalog['x_URL'], catalog['catalog'], max_infos=max_infos)
  write(f"{data_dir}/infos/{id}.json", catalog, log=log)

write(files['catalogs_all'], catalogs, log=log)

data_dir =  '../data'
max_infos = None # Set to None to get all infos.
timeout = 20 # Set to small value to force failures.
max_workers = 10
files = {
  'servers': '../servers.json',
  'catalogs': '../data/catalogs.json',
  'catalogs_all': '../data/catalogs-all.json',
}

from hapimeta import logger, get, read, write, utc_now
log = logger()

try:
  servers = read(files['servers'], log=log)
except Exception as e:
  log.error(f"Error reading {files['servers']}: {e}")
  exit(1)

def get_infos(cid, catalog, max_infos=None):

  if 'catalog' not in catalog:
    msg = f"Skipping {cid} because no catalog array."
    log.info(msg)
    return

  n = 1
  for dataset in catalog['catalog']:
    id = dataset['id']
    try:
      info = get(f"{catalog['x_URL']}/info?id={id}", timeout=timeout, log=log)
      info['x_LastUpdate'] = utc_now()
    except Exception as e:
      info = {
        'x_LastUpdateError': str(e),
        'x_LastUpdateAttempt': utc_now()
      }

    if 'parameters' not in info:
      info = {
        'x_LastUpdateAttempt': utc_now(),
        'x_LastUpdateError': "No parameters node in JSON response."
      }

    fname = f"{data_dir}/infos/{cid}/{id}.json"
    if 'x_LastUpdateError' in info:
      log.info("  Attempting to read last successful /info response.")
      try:
        info_last = read(fname, log=log)
        log.info("  Read last successful /info response.")
        # Overwrites x_LastUpdate{Attempt,Error}
        info = {**info_last, **info}
      except:
        log.info("  No last successful /info response found.")
        continue
    else:
      info['x_LastUpdate'] = utc_now()

    try:
      write(fname, info, log=log)
    except:
      log.error(f"Error writing {fname}")

    if 'parameter' in info['parameters']:
      for parameter in info['parameters']:
        if 'bins' in parameter:
          if 'centers' in parameter['bins']:
            del parameter['bins']['centers']
          if 'ranges' in parameter['ranges']:
            del parameter['bins']['ranges']

    if max_infos is not None and n >= max_infos:
      return
    n = n + 1

def get_catalogs(servers):
  catalogs = {}
  for obj in servers['servers']:
    log.info(obj['id'])
    try:
      catalog = get(obj['url'] + '/catalog', timeout=timeout, log=log)
    except Exception as e:
      catalog = {
        'x_LastUpdateAttempt': utc_now(),
        'x_LastUpdateError': str(e)
      }

    if 'catalog' not in catalog:
      catalog = {
        'x_LastUpdateAttempt': utc_now(),
        'x_LastUpdateError': "No catalog node in JSON response."
      }

    fname = f"{data_dir}/catalogs/{obj['id']}.json"
    if 'x_LastUpdateError' in catalog:
      log.info("  Attempting to read last successful /catalog response.")
      try:
        catalog_last = read(fname, log=log)
        log.info("  Read last successful /catalog response.")
        # Overwrites x_LastUpdate{Attempt,Error}
        catalog = {**catalog_last, **catalog}
      except:
        log.info("  No last successful /catalog response found.")
        continue
    else:
      catalog['x_LastUpdate'] = utc_now()

    catalog['x_URL'] = obj['url']

    catalogs[obj['id']] = catalog

    try:
      write(fname, catalog, log=log)
    except:
      log.error(f"Error writing {fname}")
      exit(1)
  return catalogs

catalogs = get_catalogs(servers)

try:
  write(files['catalogs'], catalogs, log=log)
except:
  log.error(f"Error writing {files['catalogs']}")
  exit(1)

# catalog['catalog'] is an array of dataset objects with at least a key of
# 'id' (dataset id). The following adds an 'info' key to each dataset object.

if max_workers == 1:
  for cid, catalog in catalogs.items():
    get_infos(cid, catalog, max_infos=max_infos)
else:
  # Build infos for each server in parallel. (/info requests for a each server are sequential.)
  from concurrent.futures import ThreadPoolExecutor
  def call(cid):
    get_infos(cid, catalogs[cid], max_infos=max_infos)
  with ThreadPoolExecutor(max_workers=max_workers) as pool:
    pool.map(call, catalogs.keys())

try:
  write(files['catalogs_all'], catalogs, log=log)
except:
  log.error(f"Error writing {files['catalogs_all']}")

try:
  catalogs_all_pkl = files['catalogs_all'].replace(".json", ".pkl")
  write(catalogs_all_pkl, catalogs, log=log)
except:
  log.error(f"Error writing {catalogs_all_pkl}")
import json
import datetime

from hapimeta import logger, get, read, write, utc_now
log = logger()

fname_in   = '../servers.json'
fname_out  = '../servers.updated.json'
fname_all1 = '../all_.updated.txt'
fname_all2 = '../all.updated.txt'

def equivalent_dicts(servers, about):
  diff = False
  for k1, v1 in servers.items():
    if k1.startswith("x_"): continue
    if k1 not in about:
      log.info(f"  key '{k1}' not in /about response")
      #diff = True
  log.info("  ---")
  for k2, v2 in about.items():
    if k2.startswith("x_"): continue
    if k2 not in servers:
      log.info(f"  key '{k2}' not in /about response")
      diff = True
    if diff == False and servers[k2] != v2:
      log.info(f"  servers[{k2}] != about[{k2}]")
      diff = True
  return diff

servers = read(fname_in, log=log)

changed = False
all_file_str1 = ""
all_file_str2 = ""
for idx in range(len(servers['servers'])):
  server = servers['servers'][idx]
  try:
    about = get(server['url'] + '/about', log=log)
  except Exception as e:
    server['x_LastUpdateAttempt'] = utc_now()
    server['x_LastUpdateError'] = str(type(e)) + " " + str(e)
    continue

  server['x_LastUpdate'] = utc_now()
  del about["HAPI"]
  del about["status"]
  if not equivalent_dicts(server, about):
    log.info(f"  No difference between servers.json[{server['id']}] and {server['url']}")
  else:
    changed = True
    log.info(f"  Difference between servers.json[{server['id']}] and {server['url']}/about")
    server["x_LastUpdateChange"] = utc_now()
    log.info(f"servers.json[{server['id']}]")
    log.info(json.dumps(server, indent=2, ensure_ascii=False))
    log.info(f"{server['url']}/about")
    log.info(json.dumps(about, indent=2, ensure_ascii=False))
    servers['servers'][idx] = {**server, **about}

  all_file_str1 += f"{server['url']}, {server['title']}, {server['id']}, {server['contact']}, {server['contactID']}\n"
  all_file_str2 += f"{server['url']}\n"

if not changed:
  log.info("No changes to servers.json. Updating only x_ fields.")

write(fname_out, servers, log=log)

if changed:
  write(fname_all1, all_file_str1, log=log)
  write(fname_all2, all_file_str2, log=log)
else:
  msg = f"No changes to servers.json. Not writing {fname_all1} or {fname_all2}."
  log.info(msg)
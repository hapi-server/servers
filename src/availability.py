# Usage:
#   python availability.py [server_id1,server_id2,...]

# TODO: Create service
#  meta/catalog?include=all
#  meta/availability?start=START&stop=stop
#  meta/availability?start=START&stop=stop
#  server, dataset, start, stop, cadence, x_lat, x_long, regions

import os
import sys
import json
import pickle

from datetime import datetime, timedelta, timezone

from hapimeta import logger
from hapiclient import hapitime2datetime

max_workers    = 1    # Number of servers to process in parallel
lines_per_plot = 50   # Number of time range plots per page
savefig_fmts = ['png'] # File formats to save. 'png' and 'svg' are supported.

dpi            = 300
fig_width      = 3840  # pixels
fig_height     = 2160  # pixels
fig_width      = fig_width/dpi   # inches
fig_height     = fig_height/dpi  # inches

catalogs_all = '../data/catalogs-all.pkl' # Input file
out_dir      = '../data/availability'     # Output directory

# Only do these servers
all = True
if len(sys.argv) > 1:
  all = False
  servers_only = sys.argv[1].split(',')
  print(f"Only doing servers '{servers_only}'")

log = logger()

with open(catalogs_all, 'rb') as f:
  catalogs_all = pickle.load(f)

def plot(server, title, datasets, starts, stops,
         lines_per_plot=lines_per_plot,
         fig_width=fig_width, fig_height=fig_height):

  import math
  import numpy

  import matplotlib
  import matplotlib.pyplot as plt
  #matplotlib.set_loglevel('warning')

  from datetick import datetick

  def newfig():
    plt.close('all')
    fig, ax = plt.subplots()
    fig.set_figheight(fig_height)
    fig.set_figwidth(fig_width)
    return fig, ax

  def config(ax, starts_min, stops_max, title, n_plots, fn_padded=None, left_margin=None, right_margin=None):

    if fn_padded is not None:
      title = f'{title}    page {fn_padded}/{n_plots}'
    ax.set_title(title)
    ax.set_xlim([starts_min, stops_max])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', which='minor', alpha=0.5, linestyle=':')
    ax.grid(axis='x', which='major', color='k', alpha=0.5)
    ax.set_yticks(ticks=[])
    datetick('x')
    if left_margin is not None and right_margin is not None:
      plt.subplots_adjust(left=left_margin, right=right_margin)
    plt.subplots_adjust(top=0.93, bottom=0.05)

  def write(fn):
    fname = f"{out_dir}/{server}/{server}.{fn}"

    if not os.path.exists(os.path.dirname(fname)):
      os.makedirs(os.path.dirname(fname))

    if 'svg' in savefig_fmts:
      _fname = f"{fname}.svg"
      log.info(f'Writing {_fname}')
      plt.savefig(f"{_fname}")
      log.info(f'Wrote   {_fname}')

    if 'png' in savefig_fmts:
      _fname = f"{fname}.png"
      log.info(f'Writing {_fname}')
      plt.savefig(f"{_fname}", dpi=dpi)
      log.info(f'Wrote   {_fname}')

    return _fname

  def draw(ax, n, starts, stops, datasets, start_text, max_len):
    line, = ax.plot([starts[n], stops[n]], [n, n], linewidth=5)
    label = f'{datasets[n]:{max_len}s}'

    text_kwargs = {
      'family': 'monospace',
      'color': line.get_color(),
      'verticalalignment': 'center',
      'size': 8,
    }

    ax.text(stops[n], n, label, **text_kwargs)
    if start_text[n] is not None:
      text_kwargs['horizontalalignment'] = 'right'
      text_kwargs['size'] = 8
      ax.text(starts[n], n, start_text[n], **text_kwargs)

  n_plots = math.ceil(len(datasets)/lines_per_plot)
  pad = math.ceil(math.log10(n_plots))
  starts_min = numpy.min(starts)
  stops_max = datetime.now(timezone.utc) + timedelta(days=5*365)
  starts_min = datetime(1960, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
  max_len = 0
  start_text = []
  for ds in range(len(datasets)):
    datasets[ds] = f" {datasets[ds]}"
    if stops[ds] > stops_max:
      stops[ds] = numpy.array([stops_max])
      datasets[ds] = f"→{datasets[ds]}"
    if starts[ds] < starts_min:
      starts[ds] = numpy.array([starts_min])
      start_text.append("←")
    else:
      start_text.append(None)
    max_len = max(max_len, len(datasets[ds]))

  fig, ax = newfig()
  for n in range(len(datasets)):
    draw(ax, n, starts, stops, datasets, start_text, max_len)

  debug = False
  config(ax, starts_min, stops_max, title, n_plots)
  l, b, w, h = ax.get_position().bounds
  if debug:
    file = write('all-before-tight-layout')
    print(f"Left margin: {l}")
    print(f"Bottom margin: {b}")
    print(f"Width: {w}")
    print(f"Height: {h}")
  fig.tight_layout()
  l, b, w, h = ax.get_position().bounds
  if debug:
    file = write('all-after-tight-layout')
    print(f"Left margin: {l}")
    print(f"Bottom margin: {b}")
    print(f"Width: {w}")
    print(f"Height: {h}")
  # 2*l instead of l so we have the same margin on the right as on the left
  # (instead of zero on right)
  right_margin = w+l
  left_margin = l

  fn = 0
  files = []
  fig, ax = newfig()
  for n in range(len(datasets)):
    draw(ax, n, starts, stops, datasets, start_text, max_len)
    if (n + 1) % lines_per_plot == 0:
      fn = fn + 1
      fn_padded = f"{fn:0{pad}d}"
      config(ax, starts_min, stops_max, title, n_plots, fn_padded, left_margin, right_margin)
      file = write(fn_padded)
      files.append(file)

      fig, ax = newfig()

  # Finish last plot, if needed
  if (n + 1) % lines_per_plot != 0:
    fn = fn + 1
    fn_padded = f"{fn:0{pad}d}"
    config(ax, starts_min, stops_max, title, n_plots, fn_padded, left_margin, right_margin)
    file = write(fn)
    files.append(file)

  return files

def html(files):
  import base64

  # Create the HTML content with the embedded PNG data
  html_content = """
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>TITLE</title>
  </head>
  <body>
      DIVS
  </body>
  </html>
  """

  # Remove leading and trailing whitespace from each line
  html_content = "\n".join([line.strip() for line in html_content.split("\n")])

  divs = ""
  for file in files:
    with open(file, "rb") as png_file:
      png_data = png_file.read()
      png_base64 = base64.b64encode(png_data).decode('utf-8')
      divs += f'<img width="100%" src="data:image/png;base64,{png_base64}" alt="{file}">\n'

  html_content = html_content.replace("DIVS", divs)
  html_content = html_content.replace("TITLE", server)

  # Write the HTML content to the output file
  fname = f"{out_dir}/{server}/{server}.html"
  with open(fname, "w") as html_file:
    log.info(f"Writing {fname}")
    html_file.write(html_content)
    log.info(f"Wrote   {fname}")

def process_server(server, catalogs_all):

  def extract_time(info, key):
    if key not in info:
      log.error(f"{server}/{dataset['id']}: key '{key}' not in info")
      return None, None

    if info[key].strip() == "":
      log.error(f"{server}/{dataset['id']}: info[{key}].strip() = ''")
      return None, None

    hapitime = info[key]
    try:
      dt = hapitime2datetime(hapitime, allow_missing_Z=True)
    except e:
      import traceback
      trace = traceback.format_exc()
      log.error(f"{server}/{dataset['id']}: hapitime2datetime({hapitime}) returned:\n{trace}")
      return hapitime, None

    return info[key], dt

  if not all and server not in servers_only:
    return

  lines = []
  datasets = []
  starts = []
  stops = []
  for dataset in catalogs_all['catalog']:
    if 'info' not in dataset:
      log.error(f'No info node for {server}/{dataset["id"]}')
      print(server, dataset['id'], None, None)
      continue

    info = dataset['info']

    startDate, startDate_datetime = extract_time(info, 'startDate')
    if startDate is None:
      startDate = 'Error'
    stopDate, stopDate_datetime = extract_time(info, 'stopDate')
    if stopDate is None:
      stopDate = 'Error'

    line = f"{server},{dataset['id']},{startDate},{stopDate}"
    lines.append(line)
    log.info(line.replace(",", "\t"))

    if startDate_datetime is not None and stopDate_datetime is not None:
      stops.append(stopDate_datetime)
      starts.append(startDate_datetime)
      datasets.append(dataset['id'])

  fname = f"{out_dir}/{server}/{server}.csv"
  if not os.path.exists(os.path.dirname(fname)):
    os.makedirs(os.path.dirname(fname))
  with open(fname, 'w') as f:
    log.info(f"Writing to {fname}")
    f.write("\n".join(lines))

  if len(datasets) == 0:
    return

  log.info(f"Plotting availability for {server}")
  server_url = catalogs_all['x_URL']
  x_LastUpdate = catalogs_all['x_LastUpdate']
  title = f"{server}: {server_url}   {len(datasets)} datasets\n{x_LastUpdate}"
  files = plot(server, title, datasets, starts, stops,
               lines_per_plot=lines_per_plot,
               fig_width=fig_width, fig_height=fig_height)

  for savefig_fmt in savefig_fmts:
    fname = f"{out_dir}/{server}/{server}-plots.{savefig_fmt}.json"
    log.info(f"Writing {fname}")
    with open(fname, 'w') as f:
      json.dump(files, f, indent=2)
      log.info(f"Wrote   {fname}")

  html(files)

if max_workers == 1:
  for server in catalogs_all.keys():
    process_server(server, catalogs_all[server])
else:
  from concurrent.futures import ThreadPoolExecutor
  def call(server):
    process_server(server, catalogs_all[server])
  with ThreadPoolExecutor(max_workers=max_workers) as pool:
    pool.map(call, catalogs_all.keys())

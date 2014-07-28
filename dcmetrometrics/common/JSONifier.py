"""
Methods to convert an oect to json for the web.
"""
from json import JSONEncoder, dumps
import datetime
import os
from .utils import mkdir_p


from ..eles.models import (Unit, UnitStatus, KeyStatuses, Station)

class WebJSONEncoder(JSONEncoder):
  """JSON Encoder for DC Metro Metrics data types.
  """

  def default(self, o):

    # Convert dates to string
    if isinstance(o, datetime.datetime) or \
       isinstance(o, datetime.date):
       return o.isoformat()

    # Convert ELES models
    elif isinstance(o, (Unit, UnitStatus, Station, KeyStatuses)):
      return o.to_web_json()

    # Let the base class default method raise the TypeError
    return JSONEncoder.default(self, o)


class JSONWriter(object):
  """Write Unit and Station JSON static files.
  """

  def __init__(self, basedir = None):
    self.basedir = os.path.abspath(basedir) if basedir else os.getcwd()

  def write_unit(self, unit):

    # Get the statuses for the unit
    statuses = unit.get_statuses()

    # Get the key statuses
    key_statuses = unit.get_key_statuses()

    data = {'unit' : unit,
            'key_statuses' : key_statuses,
            'statuses' : statuses}
    
    jdata = dumps(data, cls = WebJSONEncoder)

    # Create the directory if necessary
    outdir = os.path.join(self.basedir, 'json', 'units')
    mkdir_p(outdir)

    fname = '%s.json'%(unit.unit_id)
    outpath = os.path.join(outdir, fname)

    with open(outpath, 'w') as fout:
      fout.write(jdata)






import sys

slips = False
if len(sys.argv) < 5:
    print "mwdrealtime.py type timeStamp value"
    sys.exit()

import status
import datetime

type = sys.argv[1]

value = float(sys.argv[2])

timestamp = " ".join(sys.argv[3:])

print type, value, timestamp

#django setup code
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#setting up the slip model

from tdsurface.depth.models import MWDRealTime

#get the latest run

kwargs = {'run':status.current_run(),
          'time_stamp':timestamp}

if type == 'gx':
    kwargs['type'] = 'G'
    kwargs['value_x'] = value
elif type == 'gy':
    kwargs['type'] = 'G'
    kwargs['value_y'] = value
elif type == 'gz':
    kwargs['type'] = 'G'
    kwargs['value_z'] = value
elif type == 'hx':
    kwargs['type'] = 'H'
    kwargs['value_x'] = value
elif type == 'hy':
    kwargs['type'] = 'H'
    kwargs['value_y'] = value
elif type == 'hz':
    kwargs['type'] = 'H'
    kwargs['value_z'] = value
else:
    kwargs['type'] = type
    kwargs['value'] = value

t = MWDRealTime(**kwargs)

t.save()

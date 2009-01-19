import sys

slips = False
if len(sys.argv) != 2:
    raise Exception("First argument must be block position.")

try:
    pos = float(sys.argv[1])
except Exception, e: 
    print e
    raise Exception("There was an error converting the block position!")

import datetime

slips = 0
if sys.argv[1] == 'in':
    slips = 1

#django setup code
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#setting up the slip model

from tdsurface.depth.models import BlockPosition, Settings

t = Settings()
#get the latest run


kwargs = {'run':t.get_active_run(),
          'time_stamp':datetime.datetime.now(),
          'position':str(pos),
          'position_units':'ft'}


t = BlockPosition(**kwargs)

t.save()

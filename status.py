#django setup code
from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

#setting up the slip model

from tdsurface.depth.models import Slip
from tdsurface.depth.models import Run


def current_run():
    """Get the current system run."""
    #get all runs
    runs = Run.objects.all()
    #return the latest one
    return runs[len(runs)-1]

def current_bore():
    return "Bore1"
def current_rig():
    return "Rig1"
def current_well():
    return "Well1"

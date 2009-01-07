from django.core.management import setup_environ

from tdsurface import settings

setup_environ(settings)

from tdsurface.depth.models import Rig

print Rig.objects.all()

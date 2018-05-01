# WSGI-configuration for apache2 and temp-pi
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from tempserver import app as application

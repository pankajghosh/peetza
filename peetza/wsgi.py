"""
Entrypoint module for WSGI containers.

"""
from peetza.app import create_app


app = create_app().app

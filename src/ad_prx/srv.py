"""
AD PRX Helper to forward ldap requests via https
"""
import os
import ldap

from sanic import Sanic
from sanic.request import Request

app = Sanic("AD_PRX")


PFX = os.environ.get("AD_PRX_PREFIX", "") # prefix for web server
objects = {}  # lsit of persistant objects

def check_auth(request):
    """ is request authenticated """
    return True


@app.get(f"{PFX}/")
async def index(request: Request):
    check_auth(request)
    return text("", status=200)

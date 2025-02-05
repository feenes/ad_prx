"""
AD PRX Helper to forward ldap requests via https
"""
import os
import ldap
import uuid

from datetime import datetime
from datetime import timedelta

from sanic import Sanic
from sanic.request import Request
from sanic.response import text
from sanic.response import json


app = Sanic("AD_PRX")


PFX = os.environ.get("AD_PRX_PREFIX", "") # prefix for web server


class Object:
    objects = {}
    def __init__(self, value, typ=None):
        self.id = self._gen_id()
        self.val = value
        self.type = typ
        self.created = datetime.now()
        self.add_obj()
        cls = type(self)
        cls.purge_objects()

    def _add_obj(self):
        """
        adds object to object store
        """
        cls = type(self)
        cls.objects[obj.id] = self

    @staticmethod
    def gen_obj_id():
        # Generate a random UUID (Universally Unique Identifier)
        unique_id = uuid.uuid4()
        return unique_id

    def purge(self, seconds=300):
        t_keep = datetime.now() - timedelta(seconds=seconds)
        cls = type(self)
        objects = cls.objects
        to_purge = [obj.id for obj in objects.values() if obj.created < t_keep]
        for id_ in to_purge:
            del objects[id_]


def check_auth(request):
    """ is request authenticated """
    return True


@app.get(f"{PFX}/")
async def index(request: Request):
    check_auth(request)
    return text(f"{PFX}", status=200)

@app.post(f"{PFX}/initialize")
async def initialize(request: Request):
    check_auth(request)
    data = request.json
    print(f"{data=}")
    args = data["args"]
    kwargs = data["kwargs"]
    con = ldap.initialize(*args, **kwargs)
    id_ = gen_obj_id()
    obj = Object(value=con, typ="connection")
    
    rslt = {
        "id": obj.id,
        "typ": typ,
    }
    return json(rslt)
    

# To IMPLEMENT

# con = ldap.initialize()
# meth = ldap.sasl.digest.md5()
# ctrl = ldap.controls.SimplePagedResultsControl(
# 
# # 
# con.set_option()
# con.simple_bind_s(uid, passwd)
# con.sasl_interactive_bind_s("", meth)
# con.search_ext()
# con.result3()


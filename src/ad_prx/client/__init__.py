import os

from unittest.mock import patch

from pathlib import Path

import ldap
import ldap.sasl
import requests


class ProxyObj:
    def __init__(self, url, cert, id_):
        self.url = url
        self.cert = cert
        self.id = id_


class ConnectionProxy(ProxyObj):
    """ proxy connection object """
    # con.set_option()
    # con.simple_bind_s(uid, passwd)
    # con.sasl_interactive_bind_s("", meth)
    # con.search_ext()
    # con.result3()


class PrxClient:
    def __init__(self, fqdn, port=None, prefix="/ad_prx/"):
        self.url = f"https://{fqdn}"
        if port:
            self.url += ":port"
        self.url += prefix
        self.certpath = Path(
            os.environ.get("MHCLNT_CERT")
            or Path.home() / ".ssl" / "cert" / "client.crt"
        )
        self.cert = (
            str(self.certpath),
            str(self.certpath.with_suffix(".key")),
        )

    def post(self, rel_url, data):
        url = f"{self.url}{rel_url}"
        print(f"post to {url} {data}")
        rslt = requests.post(url, cert=self.cert, json=data)
        print(f"{rslt=}")

    def initialize(self, *args, **kwargs):
        """
        handle  con = ldap.initialize()
        """
        print(f"ldap.initialize({args}, {kwargs})")
        data = {
            "args": args,
            "kwargs": kwargs,
        }
        self.post("initialize", data=data)
        id_ = 1
        connection = ConnectionProxy(self.url, self.cert, id_)

    def sasl_dig_md5(self, *args, **kwargs):
        """
        handle meth = ldap.sasl.digest_md5()
        """

    def  ctrls_simple_paged_results_ctrl(self, *args, **kwargs):
        """
        handle ctrl = ldap.controls.SimplePagedResultsControl(
        """


client = None

def patch_ldap_w_proxy(fqdn, port=None, prefix="/ad_prx/"):
    """
    patches ldap with proxy objects
    """
    global client
    client = PrxClient(fqdn, port=port, prefix=prefix)

    ldap.initialize = client.initialize
    ldap.controls.SimplePagedResultsControl = client.ctrls_simple_paged_results_ctrl
    ldap.sasl.digest_md5 = client.sasl_dig_md5


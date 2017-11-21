#/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import requests
import json
import subprocess
from urllib.parse import urljoin

GITHUB_API = "https://api.github.com"

def get_token():
    user = input("Your Github username: ")
    password = getpass.getpass("Your password: ")
    note = "Requesting 0AuthToken."
    url = urljoin(GITHUB_API, "authorizations")
    payload = {}
    if note:
        payload["note"] = note
    res = requests.post(
        url,
        auth = (user, password),
        data = json.dumps(payload),
        )
    j_obj = json.loads(res.text)
    if res.status_code >= 400:
        print("An error occurred: %d"%res.status_code)
        sys.exit(1)
    return j_obj['token']

def retrieve_json(address, auth_token, addrr_is_url=False):
    cmd = "curl -l -H 'Authorization: token %s' \
            %s/%s"%(auth_token, GITHUB_API, address)
    if addrr_is_url:
        cmd = "curl -l -H 'Authorization: token %s'\
            %s"%(auth_token, address)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return json.loads(out.decode("utf-8"))

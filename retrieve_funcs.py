#/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import requests
import json
import subprocess
import sys
import select
import copy
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

def acqu_users(user_set, auth_token):
    tmp = copy.deepcopy(user_set)
    iter_set = copy.deepcopy(user_set)
    for old_user in iter_set:
        for repo in retrieve_json("users/%s/repos"%old_user, auth_token):
            try:
                new_users = retrieve_json(repo["contributors_url"], auth_token, addrr_is_url=True)
                for new_user in new_users:
                    tmp.add(new_user["login"])
                    print("added %s to user_set"%new_user["login"])
                    print("Press ENTER if you wish to start with data retrieval of the present %d users."%len(tmp))
                    inp, outp, err = select.select([sys.stdin], [], [], 5)
                    if inp:
                        return tmp
                    else:
                        continue
            except ValueError:
                continue
    new_set = user_set | tmp
    if new_set == user_set:
        print("No new acquisitions have been made. Now starting data retrieval.")
        return new_set
    else:
        print("Acquired %d users."%len(new_set))
        print("Now continuing acquisition with updated user_set.")
        return acqu_users(new_set, auth_token)

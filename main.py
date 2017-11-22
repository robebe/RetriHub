#/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from repo_commits import UserRepoCommits
from retrieve_funcs import get_token, acqu_users
from multiprocessing import Pool

user_name = sys.argv[1]
try:
    auth_token = sys.argv[2]
except IndexError:
    auth_token = get_token()

if not os.path.exists("log_files"):
    os.makedirs("log_files")

def data_retrieval(user_name):
    urc = UserRepoCommits(user_name, auth_token)
    urc.get_repos()

initial_set = set()
initial_set.add(user_name)
retrieved_user_set = acqu_users(initial_set, auth_token, 5) | initial_set

print("Now starting data retrieval for acquired users: %s. This may take several years."%retrieved_user_set)
p = Pool(len(retrieved_user_set))
p.map(data_retrieval, retrieved_user_set)

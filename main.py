#/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from repo_commits import UserRepoCommits
from retrieve_funcs import get_token, acqu_users

def main():
    user_name = sys.argv[1]
    try:
        auth_token = sys.argv[2]
    except IndexError:
        auth_token = get_token()

    #urc = UserRepoCommits(user_name, auth_token)
    #urc.get_repos()

    initial_set = set()
    initial_set.add(user_name)
    retrieved_user_set = acqu_users(initial_set, auth_token) | initial_set
    print("Now starting data retrieval for acquired users: %s. This may take several years."%retrieved_user_set)
    for user_name in retrieved_user_set:
        urc = UserRepoCommits(user_name, auth_token)
        urc.get_repos()

    """
    def _data_retrieval(user_name):
        urc = UserRepoCommits(user_name, auth_token)
        urc.get_repos()

    #p = pool(len(retrieved_user_set))
    #p.map(_data_retrieval, retrieved_user_set)
    p = process(_data_retrieval, retrieved_user_set)
    p.start()
    p.join()
    """


if __name__=="__main__":
    main()

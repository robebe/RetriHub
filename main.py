#/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
from repo_commits import UserRepoCommits
from retrieve_funcs import get_token

def main():
    user_name = sys.argv[1]
    try:
        auth_token = sys.argv[2]
    except IndexError:
        auth_token = get_token()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("log_files/user_%s_retrieval.log" %user_name, mode='a', encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    urc = UserRepoCommits(user_name, auth_token)
    urc.get_repos()

if __name__=="__main__":
    main()

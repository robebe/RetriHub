#/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import json
import csv
from random import shuffle
from retrieve_funcs import retrieve_json

class UserRepoCommits(object):

    def __init__(self, user_name, auth_token, max_repos=20):
        self.user_name = user_name
        self.auth_token = auth_token
        self.max_repos = max_repos
        self.logger_setup()
        self.commits_path = "data/%s/"%self.user_name
        if not os.path.exists(self.commits_path):
            os.makedirs(self.commits_path)

    def logger_setup(self):
        self.logger = logging.getLogger(__name__+"_"+self.user_name)
        self.logger.setLevel(logging.INFO)
        log_to = os.path.join("log_files", "user_%s_retrieval.log"%self.user_name)
        fh = logging.FileHandler(log_to)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s: %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.info("Init class UserData with user_name: %s"%self.user_name)

    def get_repos(self):
        repo_names = []
        for repo in retrieve_json("users/%s/repos"%self.user_name, self.auth_token):
            repo_names.append(repo["name"])
        shuffle(repo_names)
        repos = repo_names[:self.max_repos]
        self.repo_count = len(repos)
        self.logger.info("%s total repo_count: %s"%(self.user_name, self.repo_count))
        for repo in repos:
            self.get_branch_commits(repo)

    def get_branch_commits(self, repo):
        commit_list = []
        for branch in retrieve_json("repos/%s/%s/branches"%(self.user_name, repo), self.auth_token):
            branch = branch["name"]
            for commit in retrieve_json("repos/%s/%s/commits?sha=%s"%(self.user_name, repo, branch), self.auth_token):
                data_dict = self._get_commit_data(commit["url"])
                #commit_list.append(data_dict)
                commit_list = [data_dict] + commit_list
        with open(os.path.join(self.commits_path, "%s_commit_data.csv"%repo), "w", newline="") as outf:
            out = csv.DictWriter(outf, commit_list[0].keys())
            out.writeheader()
            for dic in commit_list:
                out.writerow(dic)
        self.logger.info("Retrieved commit data from git folder: %s"%repo)
        self.repo_count -= 1
        self.logger.info("%d repos to go."%self.repo_count)

    def _get_commit_data(self, commit_url):
        data_dict = retrieve_json(commit_url, self.auth_token, addrr_is_url=True)
        tmp_dict = dict()
        tmp_dict["user_date"] = "%s (%s)"%(data_dict["commit"]["committer"]["name"], data_dict["commit"]["committer"]["date"])
        tmp_dict["additions"] = data_dict["stats"]["additions"]
        tmp_dict["deletions"] = data_dict["stats"]["deletions"]
        """
        tmp_dict["committer_name"] = data_dict["commit"]["committer"]["name"]
        tmp_dict["commit_committer_date"] = data_dict["commit"]["committer"]["date"]
        try:
            tmp_dict["committer_login"] = data_dict["committer"]["login"]
        except:
            tmp_dict["committer_login"] = "null"
        tmp_dict["additions"] = data_dict["stats"]["additions"]
        tmp_dict["deletions"] = data_dict["stats"]["deletions"]
        tmp_dict["file_count"] = len(data_dict["files"])
        """
        return tmp_dict

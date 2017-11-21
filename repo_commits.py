#/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import json
from retrieve_funcs import retrieve_json

class UserRepoCommits(object):

    def __init__(self, user_name, auth_token):
        self.user_name = user_name
        self.auth_token = auth_token
        self.logger = logging.getLogger("__main__")
        self.logger.info("Init class UserData with user_name: %s"%self.user_name)
        self.commits_path = "retrieved_data/%s/"%self.user_name
        if not os.path.exists(self.commits_path):
            os.makedirs(self.commits_path)

    def get_repos(self):
        repo_names = []
        contrib_url = []
        for repo in retrieve_json("users/%s/repos"%self.user_name, self.auth_token):
            repo_names.append(repo["name"])
            contrib_url.append(repo["contributors_url"])
        self.repo_count = len(repo_names)
        self.logger.info("repos of %s: %s"%(self.user_name, repo_names))
        self.logger.info("urls of contributors: %s"%contrib_url)
        for repo in repo_names:
            self.get_branch_commits(repo)

    def get_branch_commits(self, repo):
        #print(repo)
        repo_dict = dict()
        for branch in retrieve_json("repos/%s/%s/branches"%(self.user_name, repo), self.auth_token):
            branch = branch["name"]
            #print(branch)
            for commit in retrieve_json("repos/%s/%s/commits?sha=%s"%(self.user_name, repo, branch), self.auth_token):
                #print(commit["url"])
                sha2data_dict = self._get_commit_data(commit["url"])
                for sha, data in sha2data_dict.items():
                    repo_dict[sha] = data
        with open(os.path.join(self.commits_path, "%s_commit_data.json"%repo), "w") as outf:
            json.dump(repo_dict, outf, indent=4)
        print("done with repository: %s"%repo)
        self.repo_count -= 1
        print("%d repos to go."%self.repo_count)
        self.logger.info("Retrieved commit data from git folder: %s"%repo)

    def _get_commit_data(self, commit_url):
        ret = dict()
        data_dict = retrieve_json(commit_url, self.auth_token, addrr_is_url=True)
        tmp_dict = dict()
        tmp_dict["author_name"] = data_dict["commit"]["author"]["name"]
        tmp_dict["commit_author_date"] = data_dict["commit"]["author"]["date"]
        tmp_dict["committer_name"] = data_dict["commit"]["committer"]["name"]
        tmp_dict["commit_committer_date"] = data_dict["commit"]["committer"]["date"]
        try:
            tmp_dict["author_login"] = data_dict["author"]["login"]
        except:
            self.logger.error("author_login linking to null at: %s"%commit_url)
            tmp_dict["author_login"] = "null"
        try:
            tmp_dict["committer_login"] = data_dict["committer"]["login"]
        except:
            self.logger.error("committer_login linking to null at: %s"%commit_url)
            tmp_dict["committer_login"] = "null"
        tmp_dict["committer_is_admin"] = str(data_dict["committer"]["site_admin"])
        tmp_dict["stats"] = data_dict["stats"]
        tmp_dict["file_count"] = len(data_dict["files"])
        ret[data_dict["sha"]] = tmp_dict
        return ret

import json
import subprocess
import os
import sys
import getpass
from urllib.parse import urljoin
import logging


class UserRepoCommits(object):
    """
    retrieve all git repositories of specified user_name and store commits
    to each repo in /data/user_name/repo
    """
    def __init__(self, user_name, auth_token=None):
        self.user_name = user_name
        self.auth_token = auth_token
        if not self.auth_token:
            self.auth_token = self.get_token()
        self.user_path = "data/%s"%user_name
        if not os.path.exists(self.user_path):
            os.makedirs(self.user_path)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init class UserData with user_name: %s"%self.user_name)

    def get_repos(self, save_data=True):
        cmd = "curl -l -H 'Authorization: token %s' \
                https://api.github.com/users/%s/repos" %(self.auth_token,self.user_name)
        self.repos = self._retrieve_json(cmd)
        self.logger.info("loading repository data")
        if save_data:
            repo_path = os.path.join(self.user_path, "repos.json")
            with open(repo_path, "w") as outf:
                json.dump(self.repos, outf, indent=4)

    def get_token(self):
        user = raw_input("Your Github username: ")
        password = getpass.getpass("Your password: ")
        note = raw_input("Note (eg. testing): ")
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

    def filter_repos(self):
        repo_names = []
        self.contrib_urls = []
        for repo in self.repos:
            repo_names.append(repo["name"])
            self.contrib_urls.append(repo["contributors_url"])
        self.logger.info("repos of %s: %s"%(self.user_name, repo_names))
        #print(contrib_urls)
        self._get_repo_branches(repo_names)


    def _get_repo_branches(self, repo_names):
        for repo in repo_names:
            self._get_branches(repo)

    def _get_branches(self, repo):
        cmd = "curl -l -H 'Authorization: token %s' \
                https://api.github.com/repos/%s/%s/branches" %(self.auth_token, self.user_name, repo)
        branches = [branch['name'] for branch in self._retrieve_json(cmd)]
        self._get_commits(branches, repo)

    def _get_commits(self, branches, repo):
        repo_path = os.path.join(self.user_path, repo)
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
        for branch in branches:
            cmd = "curl -l -H 'Authorization: token %s' \
                    https://api.github.com/repos/%s/%s/commits?sha=%s" %(self.auth_token, self.user_name, repo, branch)
            commit_tmp = self._retrieve_json(cmd)
            commit_file = os.path.join(repo_path, "%s_commits.json" %branch)
            with open(commit_file, "w") as outf:
                json.dump(commit_tmp, outf, indent=4)
            self.logger.info("loading commits of branch %s into %s"%(branch, repo_path))


    def _retrieve_json(self,cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return json.loads(out.decode("utf-8"))



if __name__=="__main__":
    user_name = "defunkt"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("user_%s_retrieval.log" %user_name, mode='a', encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ud = UserData(user_name, auth_token="10753b8277ae8c9d284bf42470d0d0c5bf62b58c")
    ud.get_repos(save_data=True)
    ud.filter_repos()

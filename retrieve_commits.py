import json
import subprocess
from retrieve_repos import retrieve_json
import sys
import os


class RepoCommitData(object):

    def __init__(self, user_name):
        self.user_name = user_name
        self.auth_token = sys.argv[1]
        self.user_path = "data/%s"%user_name
        self.commits_path = "retrieved_data/%s/"%self.user_name
        if not os.path.exists(self.commits_path):
            os.makedirs(self.commits_path)

    def walk_dirs(self):
        #get all directories listed in data/user_name and skip the first one (=data/user_name)
        dirs = [(direc[0], direc[-1]) for direc in os.walk(self.user_path)][1:]
        for dir_path, commits_files in dirs:
            commit_dict = self.call_commits(dir_path, commits_files)
            proj_name = dir_path.split("/")[-1]
            with open(os.path.join(self.commits_path, "%s_commit_data.json"%proj_name), "w") as outf:
                json.dump(commit_dict, outf, indent=4)
            print("done with path: %s" %dir_path)

    def call_commits(self, path_to_files, commits_files):
        ret = dict()
        for commits_file in commits_files:
            with open(os.path.join(path_to_files, commits_file)) as infile:
                print(path_to_files, commits_file)
                commits = json.load(infile)
                for commit in commits:
                    sha2data_dict = self._get_commit_data(commit["url"])
                    for sha, data in sha2data_dict.items():
                        ret[sha] = data
        return ret

    def _get_commit_data(self, commit_url):
        ret = dict()
        cmd = "curl -l -H 'Authorization: token %s' \
                %s" %(self.auth_token, commit_url)
        data_dict = retrieve_json(cmd)
        tmp_dict = dict()
        tmp_dict["author_name"] = data_dict["commit"]["author"]["name"]
        tmp_dict["commit_author_date"] = data_dict["commit"]["author"]["date"]
        tmp_dict["committer_name"] = data_dict["commit"]["committer"]["name"]
        tmp_dict["commit_committer_date"] = data_dict["commit"]["committer"]["date"]
        try:
            tmp_dict["author_login"] = data_dict["author"]["login"]
            tmp_dict["committer_login"] = data_dict["committer"]["login"]
        except:
            #self.logger.error("author_login and/or committer_login linking to Null: %s"%commit_url)
            print("could not retrieve author_login and/or committer_login for: %s"%commit_url)
            tmp_dict["author_login"] = "null"
            tmp_dict["committer_login"] = "null"
        tmp_dict["stats"] = data_dict["stats"]
        tmp_dict["file_count"] = len(data_dict["files"])
        ret[data_dict["sha"]] = tmp_dict
        return ret

if __name__=="__main__":
    rcd = RepoCommitData("defunkt")
    rcd.walk_dirs()

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

    def walk_dirs(self):
        for directory in os.walk(self.user_path):
            self.commit_dict = {}#dict for each repo to store commit data
            dir_path = directory[0]
            commits_files = directory[-1]
            for commits_file in commits_files:
                self.call_commits(dir_path, commits_file)
            json_obj = json.dumps(self.commit_dict)
            with open(os.path.join(dir_path, "commit_data.json")) as f:
                json.dump(json_obj, f, indent=4)

    def call_commits_actual(self, path_to_file, com_file):
        #with open(os.path.join(path_to_file, com_file)) as infile:
        #test only with one project
        test_path = "data/defunkt/ace/master_commits.json"
        with open(test_path) as infile:
            commits = json.load(infile)
            for commit in commits:
                #print(commit["url"])
                self._get_commit_data(commit["url"])
    -> hier weiter machen!! nicht alles speichen sondern direct ansprechen und
    dann mit _get_commit_data weiter

    def call_commits(self,path_to_file,com_file):
        self._get_commit_data("testing")

    def _get_commit_data(self, commit_url):
        cmd = "curl -l -H 'Authorization: token %s' \
                %s" %(self.auth_token, commit_url)
        #com_data = retrieve_json(cmd) takes wayyy to long!!
        #test with existing file:
        #print(com_data)
        with open("tmp.json", "r") as infile:
            for single_commit in json.load(infile):#change to for single_commit in com_data
                tmp_dict = {}
                tmp_dict["commit_author_date"] = single_commit["commit"]["author"]["date"]
                tmp_dict["commit_committer_date"] = single_commit["commit"]["committer"]["date"]
                tmp_dict["author_login"] = single_commit["author"]["login"]
                tmp_dict["committer_login"] = single_commit["committer"]["login"]
                tmp_dict["stats"] = single_commit["stats"]
                tmp_dict["file_count"] = len(single_commit["files"])
                self.commit_dict[single_commit["sha"]] = tmp_dict






if __name__=="__main__":
    rcd = RepoCommitData("defunkt")
    rcd.walk_dirs()

"""

for each project
    for each commit in _commitsfile:
        call commit["url"]:

append to global file for project:

for commit:
    [sha] -> existing?
    [commit][author][date]
    [commit][committer][date]
    [author][login] = author
    [committer][login] = committer
    bool isEqual(author, committer)

    [stats][total]
    [stats][additions]
    [stats][deletions]
    len of [files] (how many)

"""

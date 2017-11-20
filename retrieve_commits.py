import json
import subprocess

"""
todo: _retrieve_json as modular function!

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

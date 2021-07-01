import requests
import os
import sys
from pprint import pprint

sourceuser = sys.argv[0]
sourcetoken = sys.argv[1]
targetuser = sys.argv[2]
targettoken = sys.argv[3]
orgname = sys.argv[4]
reponame = ["bh-cfn-templates"]


# Get All Issues from source
gs = Github(sourcetoken)
for repo in reponame: 
    r = gs.get_repo(repo)
    issues = r.get_issues()
    pprint(issues)
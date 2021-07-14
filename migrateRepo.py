# Migrate Repo's and Code Base

import subprocess
import settings
import common
import requests

def cloneSource(org, repo, user, pat):
    sourceuser = f"{user}:{pat}"
    sourcerepo = f"{settings.source_instance_url}"
    cloneurl = f"https://{sourceuser}@{sourcerepo}/{org}/{repo}"
    subprocess.run(f'git clone {cloneurl}.git --mirror', shell=True)

def rewriteRefs(repo): 
    file = open(f"{repo}.git/packed-refs", "rt", newline="\n")
    data = file.read()
    data = data.replace('refs/pull', 'refs/pr')
    file.close()
    file = open(f"{repo}.git/packed-refs", "wt", newline="\n")
    file.write(data)
    file.close()


def pushTarget(org, repo, user, pat):
    targetuser = f"{user}:{pat}"
    targetrepo = f"{settings.target_instance_url}"
    cloneurl = f"https://{targetuser}@{targetrepo}/{org}/{repo}"
    common.create_repo(org, repo)
    subprocess.run(f'git push {cloneurl} --mirror', cwd=f'.\{repo}.git', shell=True)

def delete_repo(org, repo):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}"
    d = requests.request("DELETE", query_url, headers=settings.target_headers, verify=False)
    return d
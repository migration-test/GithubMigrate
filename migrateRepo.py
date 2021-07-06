# Migrate Repo's and Code Base

import subprocess
import settings
import common

def cloneSource(org, repo, user, pat):
    sourceuser = f"{user}:{pat}"
    sourcerepo = f"{settings.source_repo_url}"
    cloneurl = f"https://{sourceuser}@{sourcerepo}/{org}/{repo}"
    subprocess.run(f'git clone {cloneurl}.git --mirror', shell=True)

def rewriteRefs(repo): 
    file = open(f"{repo}.git/packed-refs", "rt")
    data = file.read()
    data = data.replace('pull', 'pr')
    file.close()
    file = open(f"{repo}.git/packed-refs", "wt")
    file.write(data)
    file.close()


def pushTarget(org, repo, user, pat):
    targetuser = f"{user}:{pat}"
    targetrepo = f"{settings.target_repo_url}"
    cloneurl = f"https://{targetuser}@{targetrepo}/{org}/{repo}"
    common.create_repo(org, repo)
    subprocess.run(f'git push {cloneurl} --mirror', cwd=f'./{repo}.git', shell=True)
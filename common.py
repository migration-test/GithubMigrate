# Common utilities for Migrate Program

import requests, os, sys, json, time, random, time, subprocess, urllib3, shutil, stat
import settings
from datetime import timedelta

urllib3.disable_warnings()

# Check for API request rate 
def get_rate_reset():
    r = requests.get(f"{settings.target_api_url}/rate_limit", headers=settings.headers, verify=False)
    rate = json.loads(r.text)
    if rate["resources"]["core"]["remaining"] >= 2:
        print(f'{rate["resources"]["core"]["remaining"]} API calls until I have to take a break.')
        return rate 
    else:
        reset_time = rate["resources"]["core"]["reset"] - time.time()
        print(f'Waiting for rate API rate limit to reset... Sleeping for {reset_time} seconds.')
        time.sleep(reset_time)

# Get list of repo names
def get_repos(filename):
    f = filename 
    try:
        file = open(f"{f}", 'r')
        repos = file.readlines()
    except ValueError as e:
        print(f"Cannot open file {f}")
    return repos 

# Create repo in target
def create_repo(org, repo, source):
    reponame = repo
    orgname = org
    source = source 
    if source['visibility'] == "public":
        visibility = "internal"
    else: 
        visibility = source['visibility']
    query_url = f"https://{settings.target_api_url}/orgs/{orgname}/repos"
    try:
        payload = {}
        payload['name'] = f'{reponame}'
        payload['org'] = f'{orgname}'
        payload['description'] = source['description']
        payload['homepage'] = source['homepage']
        payload['private'] = source['private']
        payload['visibility'] = visibility
        payload['has_issues'] = source['has_issues']
        payload['has_projects'] = source['has_projects']
        payload['has_wiki'] = source['has_wiki']
        payload['allow_squash_merge'] = source['allow_squash_merge']
        payload['allow_merge_commit'] = source['allow_merge_commit']
        payload['allow_rebase_merge'] = source['allow_rebase_merge']
        payload['delete_branch_on_merge'] = source['delete_branch_on_merge']
        p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
        if p.status_code == 201:
            print(f'Repository {reponame} created!')
    except:
        print(f"ERROR: Unable to create repository {reponame}.\n Status Code: {p.status_code} : {p.text}")

def get_org_repos(org):
    query_url = f"https://{settings.source_api_url}/orgs/{org}/repos"
    params = { 'type': 'all', 'per_page': 100, 'page': 1 }
    p = requests.get(query_url, headers=settings.source_headers, params=params, verify=False)
    if p.status_code == 200:
        repos = json.loads(p.text)
        file = open("repofile.txt", "a+")
        for repo in repos:
            file.write(f"{repo['name']}\n")
        file.close()
        while 'next' in p.links.keys():
            p = requests.get(p.links['next']['url'], headers=settings.source_headers)
            if p.status_code == 200:
                try: 
                    file = open("repofile.txt", "a+")
                    repos = json.loads(p.text) 
                    for repo in repos:
                        file.write(f"{repo['name']}\n")
                except:
                    print("ERROR: Unable to write to file.")
            else:
                print(f"ERROR: {p.status_code} : {p.text}")
        else:
            file.close()
    else:
        print(f"ERROR: {p.status_code} : {p.text}")

def get_source_repo_info(org, repo):
    headers = settings.source_headers
    headers['Accept'] = 'application/vnd.github.nebula-preview+json'
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}"
    r = requests.get(query_url, headers=headers)
    if r.status_code == 200:
        resp = json.loads(r.text)
        return resp
    elif r.status_code == 403:
        print(f"Access to {org}/{repo} is forbidden.")
    else:
        print(f"Unable to find repo {org}/{repo}")
    


# Check if org exists
def get_org(orgname):
    org_name = orgname
    try:
        r = requests.get(f"{settings.base_url}/orgs/{org_name}", headers=settings.headers)
        if r.status_code != 200:
            print(f"Organization {org_name} doesn't exist, please create and try again!")
        else:
            return r
    except ValueError as e: 
        print(f"ERROR: {e.message}")

def remove_writeprotect(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def cleanup(repo):
    shutil.rmtree(f"{repo}.git", onerror=remove_writeprotect)



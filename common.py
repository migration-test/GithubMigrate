# Common utilities for Migrate Program

import requests, os, sys, json, time, random, time, subprocess
import settings
from datetime import timedelta
from pprint import pprint

# Check for API request rate 
def get_rate_reset():
    r = requests.get(f"{settings.target_url}/rate_limit", headers=settings.headers)
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
def create_repo(org, repo):
    reponame = repo
    orgname = org
    query_url = f"https://{settings.target_url}/orgs/{orgname}/repos"
    try:
        payload = {}
        payload['name'] = f'{reponame}'
        payload['org'] = f'{orgname}'
        p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers)
        if p.status_code == 201:
            print(f'Repository {reponame} created!')
    except:
        print(f"ERROR: Unable to create repository {reponame}.\n Status Code: {p.status_code} : {p.text}")



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


def cleanup(repo):
    subprocess.run('rm -rf ./' + repo + '.git')



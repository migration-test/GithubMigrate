# Common utilities for Migrate Program

import requests, os, sys, json, time, random, time
import settings
from datetime import timedelta
from pprint import pprint

# Check for API request rate 
def get_rate_reset():
    r = requests.get("{settings.base_url}/rate_limit", headers=settings.headers)
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
    try:
        file = open("{filename}", 'r')
        repos = file.readlines()
    except ValueError as e:
        print("Cannot open file {filename}")
    return repos 

# Create repo in target
def create_repo(org, repo):
    reponame = repo
    orgname = org
    query_url = "{settings.base_url}/orgs/{orgname}/repos"
    try:
        r = requests.get("{settings.base_url}/repos/{orgname}/{reponame}", headers=settings.headers)
        if r.status_code == 200:
            return r
        elif r.status_code == 403:
            print(f"Repo already exists however we do not have access to it!")
        else:
            try:  
                p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.headers)
                if p.status_code == 201:
                    print(f'Repository {reponame} created!')
            except ValueError as e:
                print(f"ERROR: Unable to create repository {reponame}.\n Message: {e.message}")
    except ValueError as e:
        print(f"Something went wrong! Here is what the message is: {e.message}")


# Check if org exists
def get_org(orgname):
    org_name = orgname
    try:
        r = requests.get("{settings.base_url}/orgs/{org_name}", headers=settings.headers)
        if r.status_code != 200:
            print(f"Organization {org_name} doesn't exist, please create and try again!")
        else:
            return r
    except ValueError as e: 
        print(f"ERROR: {e.message}")
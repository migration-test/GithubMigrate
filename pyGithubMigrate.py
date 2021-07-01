import requests
import os
import sys
import json
import time
import random
import time
from datetime import timedelta
from pprint import pprint

sourceuser = sys.argv[1]
sourcetoken = sys.argv[2]
targetuser = sys.argv[3]
targettoken = sys.argv[4]
orgname = sys.argv[5]
orgname2 = sys.argv[6]
reponame = ["pbr"]
rate = ""

params = {}
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'python',
    'Authorization': f'token {sourcetoken}'
    }

def get_rate_reset():
    r = requests.get("https://api.github.com/rate_limit", headers=headers)
    rate = json.loads(r.text)
    if rate["resources"]["core"]["remaining"] >= 2:
        print(f'{rate["resources"]["core"]["remaining"]} API calls until I have to take a break.')
        return rate 
    else:
        reset_time = rate["resources"]["core"]["reset"] - time.time()
        print(f'Waiting for rate API rate limit to reset... Sleeping for {reset_time} seconds.')
        time.sleep(reset_time)
        

# Get All Issues from source
for repo in reponame: 
    query_url = f"https://api.github.com/repos/{orgname}/{repo}/issues"
    params = {}
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'python',
        'Authorization': f'token {sourcetoken}'
        }
    r = requests.get(query_url, headers=headers, params=params)
    issues = json.loads(r.text)
    get_rate_reset()


for issue in issues:
    try:
        json_object = issue
        print (f"JSON is valid, creating issue: ", issue["id"])
        query_url = f"https://api.github.com/repos/{orgname2}/{repo}/issues"
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'python',
            'Authorization': f'token {sourcetoken}'
            }
        payload = {
            "title": issue["title"],
            "body": issue["body"],
        }
        with open("payload.json", "w") as write_payload:
            json.dump(payload, write_payload, indent=2, sort_keys=False)
            write_payload.close()
        p = requests.request("POST", query_url, data=json.dumps(payload), headers=headers)
        get_rate_reset()
        if p.status_code == 201:
            print('Successfully created Issue ID: ', issue["id"])
            time.sleep(random.randrage(1, 5))
        elif p.status_code == 403:
            print(f"Github told us to slow down, so I am taking a breath!") 
            time.sleep(random.randrange(10, 60))
        else:
            print(f"Could not create Issue ID: ", issue["id"])
            #print(f"Response: {p.status_code}\nMessage: {p.content}")
            print(p.status_code)
            print(p.headers)
    except ValueError as e:
        print ("Is valid json? false")


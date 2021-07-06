import os, sys, requests, json, time, random
import settings 
import common


rate = ""
params = {}


# Get All Issues from source
def get_issues(org, repo):
    query_url = f"https://{settings.source_url}/repos/{org}/{repo}/issues"
    params = {}
    r = requests.get(query_url, headers=settings.source_headers, params=params)
    issues = json.loads(r.text)
    return issues 


def create_issue(org, repo, issue):
    query_url = f"https://{settings.target_url}/repos/{org}/{repo}/issues"
    payload = {
        "title": issue["title"],
        "body": issue["body"],
    }
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers)
    return p 

def migrate_issues(org, repo, issues):
    for issue in issues:
        try:
            json_object = issue
            print (f"Creating issue: {issue['id']} in {org}/{repo}.")
            p = create_issue(org, repo, issue)
            if p.status_code == 201:
                print(f"Successfully created Issue ID: {issue['id']} in {org}/{repo}.")
                time.sleep(random.randrange(1, 5))
            elif p.status_code == 403:
                print(f"Github told us to slow down, so I am taking a breath!") 
                time.sleep(random.randrange(10, 60))
            else:
                print(f"Could not create Issue ID: {issue['id']} in {org}/{repo} - Gave status code {p.status_code}")
        except ValueError as e:
            print ("Is valid json? false")


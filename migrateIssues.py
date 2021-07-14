import os, sys, requests, json, time, random, migratePulls
import settings 
import common
import urllib3
urllib3.disable_warnings()


rate = ""
params = {}


# Get All Issues from source
def get_issues(org, repo):
    query_url = f"https://{settings.source_url}/repos/{org}/{repo}/issues"
    params = {'state': 'all', 'filter': 'all', 'direction': 'asc', 'per_page': 100, 'page': 1}
    r = requests.get(query_url, headers=settings.source_headers, params=params, verify=False)
    issues = json.loads(r.text)
    while 'next' in r.links.keys():
        r = requests.get(r.links['next']['url'], settings.source_headers, verify=False)
        issues.append(json.loads(r.text))
    return issues 


def create_issue(org, repo, issue):
    query_url = f"https://{settings.target_url}/repos/{org}/{repo}/issues"
    payload = {
        "title": issue["title"],
        "body": issue["body"],
    }
    print(f"Creating issue {issue['number']}")
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    return p 

def update_issue(org, repo, issue, num):
    query_url = f"https://{settings.target_url}/repos/{org}/{repo}/issues/{num}"
    payload = {
        "state": issue["state"],
        "labels": issue["labels"]
    }
    p = requests.request("PATCH", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    return p 

def get_comments(org, repo, issue):
    num = issue['number']
    query_url = f"https://{settings.source_url}/repos/{org}/{repo}/issues/{num}/comments"
    params = {
        'per_page': 100, 'page': 1
    }    
    p = requests.get(query_url, headers=settings.source_headers, params=params, verify=False)
    c = json.loads(p.text)
    while 'next' in p.links.keys():
        p = requests.get(p.links['next']['url'], headers=settings.source_headers, verify=False)
        c.append(json.loads(p.text))
    return c

def migrate_comments(org, repo, comment, num):
    query_url = f"https://{settings.target_url}/repos/{org}/{repo}/issues/{num}/comments"
    payload = {
        "body": comment["body"]
    }
    print(query_url)
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    return p

def migrate_issues(org, repo, issues):
    for issue in issues:
        try:
            json_object = issue
            print (f"Creating issue: {issue['number']} in {org}/{repo}.")
            if 'pull_request' in issue:
                pull = issue['number']
                pr = migratePulls.get_pull(settings.sourceorg, repo, pull)
                issue["base"] = pr["base"]
                issue["head"] = pr["head"]
                issue["merged_at"] = pr["merged_at"]
                b = migratePulls.create_branch(org, repo, issue)
                if b.status_code == 201:
                    print("Base branch created!")
                else:
                    print(f"Branch could not be created: {b.status_code} : {b.text}")
                h = migratePulls.create_head_branch(org, repo, issue)
                if h.status_code == 201:
                    print("Head branch created!")
                else:
                    print(f"Head branch could not be created: {h.status_code} : {h.text}")
                p = migratePulls.create_pulls(org, repo, issue)
                if p.status_code == 201:
                    print("Pull created!")
                    pp = p.json()
                else: 
                    print(f"Unable to create pull: {p.status_code} : {p.text}")
            else:
                p = create_issue(org, repo, issue)
                pp = p.json()
            if p.status_code == 201:
                print(f"Successfully created Issue ID: {pp['number']} in {org}/{repo}.")
                if 'pull_request' in issue:
                    print(f"Updating PR {pp['number']}")
                    num = pp['number']
                    migratePulls.update_pulls(org, repo, issue, num)
                    comments = get_comments(settings.sourceorg, repo, issue)
                    for comment in comments:
                        c = migrate_comments(org, repo, comment, num)
                        if c.status_code == 201:
                            print("Comment Created")
                        else:
                            print(f"{c.status_code} : {c.text}") 
                else:
                    time.sleep(2)
                    num = pp['number']
                    u = update_issue(org, repo, issue, num)
                    comments = get_comments(settings.sourceorg, repo, issue)
                    for comment in comments:
                        c = migrate_comments(org, repo, comment, num)
                        if c.status_code == 201:
                            print("Comment Created")
                        else:
                            print(f"{c.status_code} : {c.text}") 
                    if u.status_code == 200:
                        print(f"Updated Issue: {pp['number']}")
                    else:
                        print(f"Could not update issue: {issue['number']} - Status Code: {u.status_code} - {u.text}")
                time.sleep(random.randrange(1, 5))
            elif p.status_code == 403:
                print(f"Github told us to slow down, so I am taking a breath!") 
                time.sleep(random.randrange(10, 60))
            else:
                print(f"Could not create Issue ID: {issue['number']} in {org}/{repo} - Gave status code {p.status_code} - {p.text}")
        except ValueError as e:
            print ("Is valid json? false")


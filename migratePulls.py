# Migrate pulls 

import settings, requests, json, time, random, urllib3
urllib3.disable_warnings()


def get_pull(org, repo, pull):
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}/pulls/{pull}"
    params = {}
    print(f"Getting PR number {pull} from {query_url}")
    r = requests.get(query_url, headers=settings.source_headers, params=params, verify=False)
    pull = json.loads(r.text)
    return pull 

def create_branch(org, repo, pull):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/pr{pull['number']}base",
        "sha": f"{pull['base']['sha']}"
    }
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    return p 

def create_head_branch(org, repo, pull):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/pr{pull['number']}head",
        "sha": f"{pull['head']['sha']}"
    }
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    return p 

def delete_branch(org, repo, pull):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs"
    head_payload = {
        "ref": f"refs/heads/pr{pull['number']}head"
    }
    base_payload = {
        "ref": f"refs/heads/pr{pull['number']}base"
    }
    h = requests.delete(query_url, data=json.dumps(head_payload), headers=settings.target_headers, verify=False)
    if h.status_code == 200: 
        print(f"Head branch for PR{pull['number']} deleted!")
    else: 
        print(f"Unable to remove head branch for PR{pull['number']}, you will need to delete manually.\n{h.status_code} : {h.text}")
    b = requests.delete(query_url, data=json.dumps(base_payload), headers=settings.target_headers, verify=False)
    if b.status_code == 200: 
        print(f"Base branch for PR{pull['number']} deleted!")
    else: 
        print(f"Unable to remove base branch for PR{pull['number']}, you will need to delete manually.\n{b.status_code} : {b.text}")
    return
    


def create_pulls(org, repo, pull):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/pulls"  
    payload = {
        "title": pull["title"],
        "body": pull["body"],
        "head": "",
        "base": f"pr{pull['number']}base",
        "maintainer_can_modify": True 
    }

    if pull["base"]["sha"] == pull["head"]["sha"]:
        payload["head"] = 'refs/heads/master'
    else:
        payload["head"] = f"pr{pull['number']}head"
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    pp = p.json()
    print(f"Created pull {pp['number']}")
    return p 

def update_pulls(org, repo, pull, num):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/pulls/{num}"  
    payload = {
        "state": pull["state"],
    }
    p = requests.request("PATCH", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=False)
    return p 

""" 
TODO: Deprecated, will remove
def migrate_pulls(org, repo, pulls):
    for pr in pulls:
        try:
            json_object = pr
            print (f"Creating PR: {pr['id']} in {org}/{repo}.")
            create_branch(org, repo, pr)
            create_head_branch(org, repo, pr)
            p = create_pulls(org, repo, pr)
            if p.status_code == 201:
                print(f"Successfully created Issue ID: {pr['id']} in {org}/{repo}.")
                time.sleep(random.randrange(1, 5))
            elif p.status_code == 403:
                print(f"Github told us to slow down, so I am taking a breath!") 
                time.sleep(random.randrange(10, 60))
            else:
                print(f"Could not create Issue ID: {pr['id']} in {org}/{repo} - Gave status code {p.status_code} {p.text}")
        except ValueError as e:
            print ("Is valid json? false") """
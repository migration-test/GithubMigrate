# Migrate pulls 

from common import debug_mode
import settings, requests, json, time, random



def get_pull(org, repo, pull):
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}/pulls/{pull}"
    params = {}
    print(f"Getting PR number {pull} from {query_url}")
    r = requests.get(query_url, headers=settings.source_headers, params=params, verify=settings.cafile)
    pull = json.loads(r.text)
    if settings.debug:
        debug_mode(r.url, r.headers, r.text)
    return pull 

def create_branch(org, repo, pull):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/pr{pull['number']}base",
        "sha": f"{pull['base']['sha']}"
    }
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=settings.cafile)
    if settings.debug:
        debug_mode(p.url, p.headers, p.text)
    return p 

def create_head_branch(org, repo, pull):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/pr{pull['number']}head",
        "sha": f"{pull['head']['sha']}"
    }
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=settings.cafile)
    if settings.debug:
        debug_mode(p.url, p.headers, p.text)
    return p 

def delete_branch(org, repo, pull):
    head_query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs/heads/pr{pull['number']}head"
    base_query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/git/refs/heads/pr{pull['number']}base"
    h = requests.delete(head_query_url, headers=settings.target_headers, verify=settings.cafile)

    if h.status_code == 204: 
        print(f"Head branch for PR{pull['number']} deleted!")
    else: 
        print(f"Unable to remove head branch for PR{pull['number']}, you will need to delete manually.\n{h.status_code} : {h.text}")
    b = requests.delete(base_query_url, headers=settings.target_headers, verify=settings.cafile)
    if b.status_code == 204: 
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
    p = requests.request("POST", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=settings.cafile)
    pp = p.json()
    print(f"Created pull {pp['number']}")
    if settings.debug:
        debug_mode(p.url, p.headers, p.text)
    return p 

def update_pulls(org, repo, pull, num):
    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/pulls/{num}"  
    payload = {
        "state": pull["state"],
    }
    p = requests.request("PATCH", query_url, data=json.dumps(payload), headers=settings.target_headers, verify=settings.cafile)
    if settings.debug:
        debug_mode(p.url, p.headers, p.text)
    return p 


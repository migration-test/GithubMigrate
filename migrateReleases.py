import settings, requests, json

def get_releases(org, repo):
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}/releases"
    params = {
        'per_page': 100, 'page': 1
    } 
    p = requests.request("GET", query_url, headers=settings.source_headers, params=params)
    if p.status_code == 200:
        resp = json.loads(p.text)
        while 'next' in p.links.keys():
            p = requests.request("GET", resp['next']['url'], headers=settings.source_headers)
            resp.append(json.loads(p.text))
    else: 
        print(f"Error getting release. {p.status_code} : {p.text} : {p.url}")
    return resp

def create_release(org, repo, rel):
    payload = {}
    payload["tag_name"] = rel["tag_name"]
    payload["target_commitish"] = rel["target_commitish"]
    payload["name"] = rel["name"]
    payload["body"] = rel["body"]
    payload["draft"] = rel["draft"]
    payload["prerelease"] = rel["prerelease"]

    query_url = f"https://{settings.target_api_url}/repos/{org}/{repo}/releases"
    p = requests.request("POST", query_url, headers=settings.target_headers, data=json.dumps(payload))
    if p.status_code == 201: 
        output = json.loads(p.text)
        print(f"Release {output['name']} created!")
    else: 
        print(f"Unable to create release {rel['name']}.\nStatus Code: {p.status_code} Message: {p.text}")

def migrate_releases(org, repo):
    rels = get_releases(org, repo)
    if bool(rels) == False:
        print("No releases to migrate!")
    else: 
        for rel in rels:
            create_release(settings.targetorg, repo, rel)
            
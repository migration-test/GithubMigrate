import settings, requests, json

def get_releases(org, repo):
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}/releases"
    r = requests.get(query_url, headers=settings.source_headers)
    if r.status_code == 200:
        resp = json.loads(r.text)
        return resp
    else: 
        print(f"Error getting release. {r.status_code} : {r.text}")

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
    if len(rels) ==0:
        print("No releases to migrate!")
    else: 
        for rel in rels:
            create_release(org, repo, rel)
            
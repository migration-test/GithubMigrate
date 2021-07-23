import settings, requests, json, mimetypes, sys
from pathlib import Path 
filepath = Path(f"{Path.cwd()}/tmp/releases/assets/")


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
    return output

def get_assets(org, repo, rel):
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}/releases/{rel['id']}/assets"
    p = requests.request("GET", query_url, headers=settings.source_headers)
    if p.status_code == 200:
        resp = json.loads(p.text)
        while 'next' in p.links.keys():
            p = requests.request("GET", resp['next']['url'], headers=settings.source_headers)
            resp.append(json.loads(p.text))
    else:
        print(f"Error getting assets. {p.status_code} : {p.text} : {p.url}")
    return resp

def check_path(path):
    if not Path.exists(path):
        Path.mkdir(path, parents=True, exist_ok=True)

def get_asset(org, repo, asset):
    query_url = f"https://{settings.source_api_url}/repos/{org}/{repo}/releases/assets/{asset['id']}"
    headers = settings.source_headers
    headers['Accept'] = 'application/octet-stream'
    save_to = f"{filepath}{asset['name']}"
    with open(save_to, 'wb') as f:
        p = requests.request("GET", query_url, headers=settings.source_headers, stream=True, allow_redirects=True)
        if p.status_code == 200 or p.status_code == 302:
            print(f"Downloading {filepath}{asset['name']} from {p.url}")
            total_length = p.headers.get('content-length')
            if total_length is None:
                f.write(p.content)
            else:
                dl = 0
                total_length = int(total_length)
                chunk_length = total_length // 100 
                for chunk in p.iter_content(chunk_size=int(chunk_length)):
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(50 * dl / total_length)
                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {done}%")
                    sys.stdout.flush()
        else:
            print(f"Error getting asset. {p.status_code} : {p.text} : {p.url}")
    return p
    

def upload_asset(rel, asset):
    mimetype = mimetypes.guess_type(asset['name'])[0]
    if mimetype == None:
        mimetype = 'application/octet-stream'
    header = settings.target_headers
    header['Content-Type'] = mimetype
    params = {
        'name': asset['name']
    }
    data = open(f"{filepath}{asset['name']}", 'rb').read()

    resp = requests.request("POST", rel['upload_url'], headers=header, params=params, data=data)
    if resp.status_code == 201:
        print(f"{asset['name']} uploaded!")
    else:
        print(f"Error uploading {asset['name']}.\nStatus Code: {resp.status_code} Message: {resp.text}")

def migrate_assets(repo, rel, targetrel):
    assets = get_assets(settings.sourceorg, repo, rel)
    if bool(assets) == False:
        print("No assets to migrate!")
    else: 
        for asset in assets:
            get_asset(settings.sourceorg, repo, asset)
            upload_asset(targetrel, asset)


def migrate_releases(repo):
    check_path(filepath)
    rels = get_releases(settings.sourceorg, repo)
    if bool(rels) == False:
        print("No releases to migrate!")
    else: 
        for rel in rels:
            targetrel = create_release(settings.targetorg, repo, rel)
            migrate_assets(repo, rel, targetrel)

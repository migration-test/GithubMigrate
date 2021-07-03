# Global settings

def init():
    global headers
    headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'python',
    'Authorization': f'token {sourcetoken}'
    }
    global base_url
    base_url = "https://api.github.com"
    
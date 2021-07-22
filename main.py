# main.py Main entrypoint for migration

import settings, common, argparse, migrateRepo, migrateIssues, migratePulls, time, random, json, requests, subprocess, os
from pathlib import Path 

os.environ['REQUESTS_CA_BUNDLE'] = 'ca-bundle.crt'

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description="Migrate repositories in Github."
    )
    parser.add_argument(
        "--generaterepofile",
        action='store_true',
        help="Generates repofile.txt with list of repos to migrate"
    )
    parser.add_argument(
        "--migrate",
        action='store_true',
        help="This executes the repo migration."   
    )
    parser.add_argument(
        "--behindthescenes",
        action='store_true',
        help=argparse.SUPPRESS,
        default=False, 
        required=False
    )
    parser.add_argument(
        "--sourcepat",
        help="Private Access Token from Source",
        required=True
    )
    parser.add_argument(
        "--targetpat",
        help="Private Access Token from Target",
        required=True
    )
    parser.add_argument(
        "--sourceuser",
        help="Username from source",
        required=True
    )
    parser.add_argument(
        "--sourceorg",
        help="Source Organization name",
        required=True
    )
    parser.add_argument(
        "--targetuser",
        help="Username from target",
        required=True
    )
    parser.add_argument(
        "--targetorg",
        help="Target Organization name",
        required=True
    )
    parser.add_argument(
        "--file",
        help="File containing reponames",
        required=False
    )
    parser.add_argument(
        "--ryesiamsure",
        help=argparse.SUPPRESS,
        required=False,
        action='store_true',
        default=False
    )
    parser.add_argument(
        "--debug",
        help="Debug mode",
        required=False,
        action='store_true',
        default=False
    )
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    settings.sourcetoken = args.sourcepat
    settings.targettoken = args.targetpat
    settings.sourceuser = args.sourceuser
    settings.targetuser = args.targetuser
    settings.targetorg = args.targetorg
    settings.sourceorg = args.sourceorg
    settings.debug = args.debug
    settings.target_api_url = "api.github.com"
    settings.source_api_url = "github.build.ge.com/api/v3"
    #settings.source_api_url = "api.github.com"
    settings.source_instance_url = "github.build.ge.com"
    settings.target_instance_url = "github.com"
    settings.source_headers = {
    'Authorization': f'token {settings.sourcetoken}'
    }
    settings.target_headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {settings.targettoken}'
    }

    if args.generaterepofile: 
        common.get_org_repos(settings.sourceorg)
    if args.file:
        settings.repofile = args.file
    else:
        settings.repofile = "repofile.txt"

    if args.migrate:
        reponame = common.get_repos(settings.repofile)
        for repo in reponame: 
            repo = repo.rstrip()
            migrateRepo.cloneSource(settings.sourceorg, repo, settings.sourceuser, settings.sourcetoken)
            migrateRepo.rewriteRefs(repo)
            migratePulls.create_branch
            migrateRepo.pushTarget(settings.targetorg, repo, settings.targetuser, settings.targettoken)
            issues = migrateIssues.get_issues(settings.sourceorg, repo)
            migrateIssues.migrate_issues(settings.targetorg, repo, issues)
            common.cleanup(repo)
    if args.behindthescenes:
        d = requests.get(f"https://{settings.target_api_url}/repos/Capgemini-test-import/GithubMigrate", headers=settings.target_headers, verify=settings.cafile)
        print(f"{d.status_code} : {d.text}") 
    if args.ryesiamsure:
        reponame = common.get_repos(settings.repofile)
        for repo in reponame:
            repo = repo.rstrip()
            d = migrateRepo.delete_repo(settings.targetorg, repo)
            if d.status_code == 204:
                print(f"Deleted repo {repo} on target!")
            elif d.status_code == 404:
                print(f"Repository {repo} does not exist!")
            else: 
                print(f"Error, unable to delete {repo}.\n Code: {d.status_code} : {d.text}\n Headers:\n{d.headers}")
main()
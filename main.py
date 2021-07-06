# main.py Main entrypoint for migration

import settings, common, argparse, migrateRepo, migrateIssues, time, random


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description="Migrate repositories in Github."
    )
    parser.add_argument(
        "--repo",
        action='store_true',
        help="This executes the repo migration."   
    )
    parser.add_argument(
        "--issues",
        action='store_true',
        help="This executes issue migration"
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
        required=True
    )
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    settings.sourcetoken = args.sourcepat
    settings.targettoken = args.targetpat
    settings.sourceuser = args.sourceuser
    settings.targetuser = args.targetuser
    settings.repofile = args.file
    settings.targetorg = args.targetorg
    settings.sourceorg = args.sourceorg
    settings.target_url = "api.github.com"
    #settings.source_url = "github.build.ge.com"
    settings.source_url = "api.github.com"
    settings.source_repo_url = "github.com"
    settings.target_repo_url = "github.com"
    settings.source_headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'python',
    'Authorization': f'token {settings.sourcetoken}'
    }
    settings.target_headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'python',
    'Authorization': f'token {settings.targettoken}'
    }


    if args.repo:
        reponame = common.get_repos(settings.repofile)
        for repo in reponame: 
            migrateRepo.cloneSource(settings.sourceorg, repo, settings.sourceuser, settings.sourcetoken)
            migrateRepo.rewriteRefs(repo)
            migrateRepo.pushTarget(settings.targetorg, repo, settings.targetuser, settings.targettoken)
    if args.issues:
        reponame = common.get_repos(settings.repofile)
        for repo in reponame: 
            issues = migrateIssues.get_issues(settings.sourceorg, repo)
            migrateIssues.migrate_issues(settings.targetorg, repo, issues)

main()
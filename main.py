# main.py Main entrypoint for migration

import settings, common, argparse, migrateRepo, migrateIssues, migratePulls, time, random, json
import pprint 

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
        "--debug",
        action='store_true',
        help="Debugging"
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
    settings.target_url = "api.github.com"
    settings.source_url = "github.build.ge.com/api/v3"
    settings.source_url = "api.github.com"
    #settings.source_repo_url = "github.build.ge.com"
    settings.target_repo_url = "github.com"
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
    if args.debug:
        reponame = common.get_repos(settings.repofile)
        for repo in reponame:
            repo = repo.rstrip()
            data = migrateIssues.get_issues(settings.sourceorg, repo)
            #with open('debug.json', 'w', encoding='utf-8') as f:
            #    json.dump(data, f, ensure_ascii=False, indent=2)




main()
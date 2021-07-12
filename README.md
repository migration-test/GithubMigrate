# GithubMigrate

GithubMigrate can be used to migrate from Github Enterprise to Github Cloud or between organizations within the same github instance, or between two github enterprise instances when access to the Github migration tool is not available. 

## Pre-requisits

- [ ] Python 3.6.x
- [ ] User account in both target and source Github's
- [ ] Organization created & Configurated in target Github (This step will go away in future release)
- [ ] Private access tokens for each Github account (See [Create a Private Access Token](#create-a-private-access-token))
- [ ] Install python modules (See [Install python modules](#install-python-modules))
- [ ] Generate repofile with list of repo's to be migrated (See [Generate Repo File](#generate-repo-file))

### Create a private access token

1. Log into Github Account
1. Go to your github profile settings by clicking on user account icon in top right corner
1. Click on **Developer Settings** 
1. Click on **Personal access tokens**
1. Click on **Generate new token**
1. Enter your password
1. Add a name for the token in the **Note** box
1. Make sure a checkmark is in every box under **Select scopes**
1. Click **Generate Token**
1. Copy token from green box, save it somewhere you will not be able to retrieve it again

### Install Python Modules
*Note: This step will go away in a future release*

To install the required python modules execute the following command from inside the GithubMigrate directory.

`pip install -f .\requirements.txt`

## Generate Repo File
To generate a list of repo's for an organization prior to running a migration, run the command for the migration like this. 
`python .\main.py --sourcepat <Source Personal Access Token> --sourceuser <Source Username> --sourceorg <Source Org> --targetpat <Target Personal Access Token> --targetuser <Target Username> --targetorg <Target Organization Name> --file <Path to list of repo's> --generaterepofile`

Example: `python .\main.py --sourcepat a5453d243b2e6fd9fc3fasdfawerf879aa --sourceuser 501649102 --sourceorg FooOrg --targetpat ghp_FAV4R33zocb3RkRJOLXzasdfNasdfdxrf --targetuser oscarthegrouch --targetorg BarOrg --generaterepofile`

This will generate a file at .\repofile.txt - review this file and remove any repo's you do not want migrated. 

## Execute Migration

Once all of your information has been collected to execute the migration the command looks like this.

`python .\main.py --sourcepat <Source Personal Access Token> --sourceuser <Source Username> --sourceorg <Source Org> --targetpat <Target Personal Access Token> --targetuser <Target Username> --targetorg <Target Organization Name> --file <Path to list of repo's> --repo --issues`

Example: `python .\main.py --sourcepat a5453d243b2e6fd9fc3fasdfawerf879aa --sourceuser 501649102 --sourceorg FooOrg --targetpat ghp_FAV4R33zocb3RkRJOLXzasdfNasdfdxrf --targetuser oscarthegrouch --targetorg BarOrg --file repofile.txt --repo --issues`

This will execute a migration on all repositories within the organization along with all issues or pull requests in an organization. 



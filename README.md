# GithubMigrate

GithubMigrate can be used to migrate from Github Enterprise to Github Cloud or between organizations within the same github instance, or between two github enterprise instances when access to the Github migration tool is not available. 

## Pre-requisits

- [ ] Python 3.6.x
- [ ] User account in both target and source Github's
- [ ] Organization created & Configurated in target Github (This step will go away in future release)
- [ ] Personal access token for source GE Github account (See [Create a Personal Access Tokens](#create-a-personal-access-tokens))
- [ ] Personal access token for target Normal Github account (See [Create a Personal Access Tokens](#create-a-personal-access-tokens))
- [ ] Install python modules (See [Install python modules](#install-python-modules))
- [ ] Generate repofile with list of repo's to be migrated (See [Generate Repo File](#generate-repo-file))

### Install Python Modules
*Note: This step will go away in a future release*

To install the required python modules execute the following command from inside the GithubMigrate directory.

`pip install -f .\requirements.txt`


# How to Use
This migration tool migrates repositories using personal access tokens from a source GitHub instance to another. In this case from the self hosted GE instance of GitHub (source) to the normal Microsoft hosted GitHub (target).

There are 3 steps:
1. Create tokens for both systems.
2. Generate a list of repositories to be migrated, for a particular GitHub Org.
3. Migrate the repositories from the source org to the target org. 

### Create a personal access tokens
You will need to generate access tokens for both the GE GitHub and normal Github. Repeat the process below for each system.

1. Login to your [Github](https://github.com) account or [GE GitHub](https://github.build.ge.com) account.
1. In the top right, click on your profile icon, and click **Settings**.
1. In the left navigation, click on **Developer Settings** 
1. Click on **Personal access tokens**
1. Click on **Generate new token**
    > If needed, confirm you password.
1. In the **Note** field enter a description like `BH Migration`.
    > This is just a description to identify the token usage.
1. Under **Select scopes**, make sure all items are checked.
    > Warning: If something is not checked, the migration will be partial.  
    > Note: This token will only be used by yourself and the tool.
1. Click **Generate Token**. The page will refresh and display the token in a green box.
1. **Save the token** from the green box somewhere safe. It cannot be retrieved again.
    > If lost, just delete this token and generate a new one.

If creating the token for Normal GitHub, continue with MFA authorization. GE GitHub does not need this.
1. Next to the newly generated token, click on **Enable SSO**. It will expand to show your github organizations. 
1. Find the organization(s) you need to migrate and click **Authorize**. Follow the usual Baker Hughes authorization process.




## Generate List of Repositories
1. Ensure all information is available from the prerequisites.
1. Run the below command to generate a list of repo's for a given organization in the source GitHub instance. This will generate the file `.\repofile.txt`

    `python .\main.py --sourcepat <Source Personal Access Token> --sourceuser <Source Username> --sourceorg <Source Org> --targetpat <Target Personal Access Token> --targetuser <Target Username> --targetorg <Target Organization Name> --generaterepofile`

    Example: `python .\main.py --sourcepat a5453d243b2e6fd9fc3fasdfawerf879aa --sourceuser 501649102 --sourceorg FooOrg --targetpat ghp_FAV4R33zocb3RkRJOLXzasdfNasdfdxrf --targetuser oscarthegrouch --targetorg BarOrg --generaterepofile`

 1. Review `.\repofile.txt` and remove any repositories you do not want migrated. 

## Migrate the Repositories
Given the generated list, content is copied from the source GitHub instance to the target instance. This includes: repository, branches, pull requests, and issues.
It does not include: repository settings or the wiki

1. Ensure all information is available from the prerequisites.
1. Ensure that a `repofile.txt` file has been created.
1. Run the below command to start migration. Status updates will be returned via the console window.

    `python .\main.py --sourcepat <Source Personal Access Token> --sourceuser <Source Username> --sourceorg <Source Org> --targetpat <Target Personal Access Token> --targetuser <Target Username> --targetorg <Target Organization Name> --migrate`

    Example: `python .\main.py --sourcepat a5453d243b2e6fd9fc3fasdfawerf879aa --sourceuser 501649102 --sourceorg FooOrg --targetpat ghp_FAV4R33zocb3RkRJOLXzasdfNasdfdxrf --targetuser oscarthegrouch --targetorg BarOrg --migrate`

    > Tip: Run in smaller batches so manual verification can be performed by splitting your repofile into smaller chunks and specifying with the --file command for each file.

    `python .\main.py --sourcepat <Source Personal Access Token> --sourceuser <Source Username> --sourceorg <Source Org> --targetpat <Target Personal Access Token> --targetuser <Target Username> --targetorg <Target Organization Name> --file <path to repo file> --migrate`

    Example: `python .\main.py --sourcepat a5453d243b2e6fd9fc3fasdfawerf879aa --sourceuser 501649102 --sourceorg FooOrg --targetpat ghp_FAV4R33zocb3RkRJOLXzasdfNasdfdxrf --targetuser oscarthegrouch --targetorg BarOrg --file repofile1.txt --migrate`
    
## Known Limitations
* References to issues numbers may change. Github will not let us force the issue #
* Images and attachments to comments/issues cannot be migrated
* Releases are not currently migrated this will be resolved with (See [Issue 9](https://github.com/Capgemini-test-import/GithubMigrate/issues/9))
* Wiki does not currently transfer automatically (See [Issue 7](https://github.com/Capgemini-test-import/GithubMigrate/issues/7))
* Links to GE Github will not be automatically updated

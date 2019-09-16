import fileinput
import os
import random
import sys
import subprocess
import time
from github import Github


def run_command(full_command):
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = proc.communicate()
    print(output)
    if proc.returncode != 0:
        sys.exit(1)
    return b''.join(output).strip().decode()  # only save stdout into output, ignore stderr

# def pr_merge(github_token):
#     g = Github(github_token)


def main():

    # pipeline = os.getenv('PIPELINE')
    branch = '-b {}'.format(os.getenv('BRANCH'))
    github_token = os.getenv('GITHUB_TOKEN')

    # Configure git

    output = run_command('git config --global user.email "cfsalesdemo@gmail.com"')
    print(output)

    output = run_command('git config --global user.name "Freshbot"')
    print(output)

    # codefresh_command = 'codefresh run'
    
    # output = run_command(' '.join([codefresh_command, pipeline, branch]))
    # print(output)

    places = [
        'Seattle',
        'New York',
        'Austin',
        'Chicago',
        'Denver',
        'San Francisco',
        'Boston',
        'Miami',
        'New Orleans',
        'Portland'
    ]
    place = random.choice(places)
    code_friendly_place = place.replace(' ', '-').lower()
    resorts = [
        'Lego Land',
        'Disney Land',
        'Disney World',
        'Six Flags',
        'Universal',
        'Hershey Park',
        'Cedar Point',
        'Kings Island',
        'Epcot'
    ]
    resort = random.choice(resorts)
    code_friendly_resort = resort.replace(' ', '-').lower()

    # Clean directory

    output = run_command('rm -rf /codefresh/volume/example-voting-app')
    print(output)

    # Clone repository

    output = run_command('git clone https://salesdemocf:{}@github.com/cfsalesdemo/example-voting-app.git /codefresh/volume/example-voting-app'.format(github_token))
    print(output)

    # Change working directory

    os.chdir('/codefresh/volume/example-voting-app')

    # Clean remote branches

    try:
        output = run_command('git branch -r | grep origin/ | grep -v \'master$\' | grep -v HEAD| cut -d/ -f2 | while read line; do git push origin :$line; done;')
        print(output)
    except:
        pass

    try:
        output = run_command('git branch | grep -v "master" | xargs git branch -D')
        print(output)
    except:
        pass

    # Create branch

    branch = '{}-or-{}'.format(code_friendly_place, code_friendly_resort)
   
    output = run_command('git checkout -b {}'.format(branch))
    print(output)

    # Update Tests

    for line in fileinput.input(['tests/selenium/test_app.py'], inplace=True):
        if line.strip().startswith('option_a = '):
            line = '    option_a = "{}"\n'.format(place)
        sys.stdout.write(line)

    for line in fileinput.input(['tests/selenium/test_app.py'], inplace=True):
        if line.strip().startswith('option_b = '):
            line = '    option_b = "{}"\n'.format(resort)
        sys.stdout.write(line)

    # Update Vote

    for line in fileinput.input(['vote/app.py'], inplace=True):
        if line.strip().startswith('option_a = '):
            line = 'option_a = os.getenv(\'OPTION_A\', "{}")\n'.format(place)
        sys.stdout.write(line)

    for line in fileinput.input(['vote/app.py'], inplace=True):
        if line.strip().startswith('option_b = '):
            line = 'option_b = os.getenv(\'OPTION_B\', "{}")\n'.format(resort)
        sys.stdout.write(line)

    # Create commit
    output = run_command('git commit -am "update for {}"'.format(branch))
    print(output)

    # Push commit

    output = run_command('git push --set-upstream origin {}'.format(branch))
    print(output)

    # Sleep

    time.sleep(30)

    # PyGitHub Auth

    g = Github(github_token)

    # Set repo

    repo = g.get_repo('cfsalesdemo/example-voting-app')

    # Create pull request

    create_pull_request = repo.create_pull(title='Pull Request from Freshbot', head=branch, base='master', body='Automated Pull Request', maintainer_can_modify=True)

    # get_pull_request_build_id

    pull_request = repo.get_pull(create_pull_request.number)

    merge_pull_request = None
    while merge_pull_request is None:
        try:
            print('Waiting 30 seconds for Pull Request builds')
            time.sleep(30)
            merge_pull_request = pull_request.merge(commit_title='Freshbot Demo Automation', commit_message='Committed by Codefresh Freshbot', merge_method='merge')
        except:
            pass

    # create_release

if __name__ == "__main__":
    main()
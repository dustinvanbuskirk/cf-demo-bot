import os
import sys
import subprocess
import random
import fileinput
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

    # codefresh_command = 'codefresh run'
    
    # output = run_command(' '.join([codefresh_command, pipeline, branch]))
    # print(output)

    places = [
        'Seattle',
        'New York',
        'Austin',
        'Chicago',
        'Denver'
    ]
    place = random.choice(places)
    code_friendly_place = place.replace(' ', '-').lower()
    resorts = [
        'Lego Land',
        'Disney Land',
        'Disney World',
        'Six Flags',
        'Universal'
    ]
    resort = random.choice(resorts)
    code_friendly_resort = resort.replace(' ', '-').lower()

    # Configure git

    output = run_command('git config --global user.email "cfsalesdemo@gmail.com"')
    print(output)

    # Checkout master and pull

    output = run_command('git checkout master')
    print(output)

    output = run_command('git pull')
    print(output)

    # Create branch

    branch = '{}-or-{}'.format(code_friendly_place, code_friendly_resort)
   
    output = run_command('git checkout -b {}'.format(branch))
    print(output)

    # Update Tests

    for line in fileinput.input(['tests/selenium/test_app.py'], inplace=True):
        if line.strip().startswith('option_a = '):
            line = 'option_a = "{}"\n'.format(place)
        sys.stdout.write(line)

    for line in fileinput.input(['tests/selenium/test_app.py'], inplace=True):
        if line.strip().startswith('option_b = '):
            line = 'option_b = "{}"\n'.format(resort)
        sys.stdout.write(line)

    # Update Vote

    for line in fileinput.input(['vote/app.py'], inplace=True):
        if line.strip().startswith('option_a = '):
            line = 'option_a = os.getenv(\'OPTION_A\', "{}"\n)'.format(place)
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

    # Create pull request

    # push_commit

    # create_pull_request

    # get_pull_request_build_id

    # wait_for_build_completion

    # merge_pull_request

    # create_release

    # get_release_build_id

    # wait_for_build_completion

    # trigger_new_deployment


if __name__ == "__main__":
    main()
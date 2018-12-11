import os
import sys
import subprocess
import random
from github import Github


def run_command(full_command):
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = proc.communicate()
    print(output)
    if proc.returncode != 0:
        sys.exit(1)
    return b''.join(output).strip().decode()  # only save stdout into output, ignore stderr

def pr_merge(github_token):
    g = Github(github_token)


def main():

    pipeline = os.getenv('PIPELINE')
    branch = '-b {}'.format(os.getenv('BRANCH'))

    codefresh_command = 'codefresh run'
    
    output = run_command(' '.join([codefresh_command, pipeline, branch]))
    print(output)

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

    # Create branch
    run_command = 'git checkout -b {}-or-{}'.format(code_friendly_place, code_friendly_resort)

    # Update Vote A
    update_vote_a

    # Update Vote B
    update_vote_b

    create_commit



    push_commit

    create_pull_request

    get_pull_request_build_id

    wait_for_build_completion

    merge_pull_request

    create_release

    get_release_build_id

    wait_for_build_completion

    trigger_new_deployment


if __name__ == "__main__":
    main()
import os
import sys
import subprocess


def run_command(full_command):
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = proc.communicate()
    print(output)
    if proc.returncode != 0:
        sys.exit(1)
    return b''.join(output).strip().decode()  # only save stdout into output, ignore stderr

def main():

    pipeline = os.getenv('PIPELINE')

    codefresh_command = 'codefresh run'
    
    output = run_command(' '.join([codefresh_command, pipeline]))
    print(output)


if __name__ == "__main__":
    main()
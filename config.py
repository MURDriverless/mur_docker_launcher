#!/usr/bin/python3
import subprocess
import os
import argparse
import sys

from string import Template

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

parser = argparse.ArgumentParser(description='mdock configurator script')
parser.add_argument('-i', '--interactive', action='store_true',
                    help='Enable interactive mode for configuration')

cli_args = parser.parse_args()

print("""
  __  __ _    _ _____    _____             _             
 |  \/  | |  | |  __ \  |  __ \           | |            
 | \  / | |  | | |__) | | |  | | ___   ___| | _____ _ __ 
 | |\/| | |  | |  _  /  | |  | |/ _ \ / __| |/ / _ \ '__|
 | |  | | |__| | | \ \  | |__| | (_) | (__|   <  __/ |   
 |_|  |_|\____/|_|  \_\ |_____/ \___/ \___|_|\_\___|_|   
                                                         
""")

print("---")
print("{:40}".format("Checking for CUDA GPU"), end = '')
CUDA = subprocess.call("nvidia-smi", stdout=subprocess.DEVNULL) == 0

docker_args = {}
docker_args["X11_FLAG"] = "-v /tmp/.X11-unix/:/tmp/.X11-unix/:ro -e DISPLAY=$(echo $DISPLAY)"
docker_args["AUTOMOUNT_FLAG"] = "-v $(pwd):/workspace"
docker_args["VSCODEINT_FLAG"] = "-v ~/.vscode_mur_docker:/root/.vscode-server"
docker_args["PORTFORWARD_FLAG"] = "-p 11311:11311"
docker_args["USBBUS_FLAG"] = "--device=/dev/bus"
docker_args["CONTAINER_NAME"] = "mur_dev"
docker_args["IMAGE_NAME"] = "murauto/mur_dev_stack"
docker_args["EXTRA_FLAGS"] = ""

docker_args_status = {}
docker_args_status["X11_FLAG"] = True
docker_args_status["AUTOMOUNT_FLAG"] = True
docker_args_status["VSCODEINT_FLAG"] = True
docker_args_status["PORTFORWARD_FLAG"] = True
docker_args_status["USBBUS_FLAG"] = True

if (CUDA):
    print("FOUND")
    docker_args["GPU_FLAG"] = "--gpus=all"
else:
    print("NOT FOUND")
    print("No CUDA compatible GPU, or missing Nvidia drivers")
    docker_args["GPU_FLAG"] = "--device=/dev/dri/card0"

print('---\n')

if cli_args.interactive:
    docker_args_status["X11_FLAG"] = query_yes_no("Forward X11 for GUI?")
    docker_args_status["AUTOMOUNT_FLAG"] = query_yes_no("Automount host $(pwd) to container /workspace?")
    docker_args_status["VSCODEINT_FLAG"] = query_yes_no("Cache vscode-server extensions?")
    docker_args_status["PORTFORWARD_FLAG"] = query_yes_no("Port forward roscore (11311)?")
    docker_args_status["USBBUS_FLAG"] = query_yes_no("Expose USB devices?")

    print("Container name? [{}] ".format(docker_args["CONTAINER_NAME"]), end='')
    res = input()
    if len(res) > 0:
        docker_args["CONTAINER_NAME"] = res

    print("Docker image name? [{}]".format(docker_args["IMAGE_NAME"]), end='')
    res = input()
    if len(res) > 0:
        docker_args["IMAGE_NAME"] = res

    print("Extra flags?")
    res = input()
    if len(res) > 0:
        docker_args["EXTRA_FLAGS"] = res

    print('---\n')

print("{:40}{}".format("CUDA Enabled", CUDA))
print("{:40}{}".format("Foward X11 for GUI", docker_args_status["X11_FLAG"]))
print("{:40}{}".format("Automount $(pwd) to /workspace", docker_args_status["AUTOMOUNT_FLAG"]))
print("{:40}{}".format("Cache vscode-server extensions", docker_args_status["VSCODEINT_FLAG"]))
print("{:40}{}".format("Port forward roscore (11311)", docker_args_status["PORTFORWARD_FLAG"]))
print("{:40}{}".format("Expose USB devices", docker_args_status["USBBUS_FLAG"]))
print("{:40}{}".format("Container name", docker_args["CONTAINER_NAME"]))
print("{:40}{}".format("Image name", docker_args["IMAGE_NAME"]))
print("{:40}{}".format("Extra flags", docker_args["EXTRA_FLAGS"]))

with open('mdock.template', 'r') as templateFile:
    src = Template(templateFile.read())
    result = src.safe_substitute(docker_args)

with open('mdock', 'w') as output:
    output.write(result)

print("---\n")
print("Configured mdock, run `sudo make install` to install wrapper")
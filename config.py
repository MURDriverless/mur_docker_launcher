#!/usr/bin/python3
import subprocess
import os

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

docker_args = []

if (CUDA):
    print("FOUND")
    docker_args.append(("--gpus=all", ))
else:
    print("NOT FOUND")
    print("No CUDA compatible GPU, or missing Nvidia drivers")
    docker_args.append(("--device=/dev/dri/card0", ))

print('---\n')

print("{:40}{}".format("Foward X11 for GUI", "TRUE"))
docker_args.append(("-v", "/tmp/.X11-unix/:/tmp/.X11-unix/:ro"))
docker_args.append(("-e", "DISPLAY=$(echo $DISPLAY)"))

print("{:40}{}".format("Automount $(pwd) to /workspace", "TRUE"))
docker_args.append(("-v", "$(pwd):/workspace"))

print("{:40}{}".format("Cache vscode-server", "TRUE"))
docker_args.append(("-v", "~/.vscode_mur_docker:/root/.vscode-server"))

print("{:40}{}".format("Port forward roscore (11311)", "TRUE"))
docker_args.append(("-p", "11311:11311"))

print("{:40}{}".format("Expose usb devices", "TRUE"))
docker_args.append(("--device=/dev/bus", ))

print("{:40}{}".format("Container name", "mur_dev"))
docker_args.append(("--name=mur_dev", ))

docker_args.append(("-itd", ))
docker_args.append(("--rm", ))
docker_args.append(("murauto/mur_dev_stack", ))

with open("mdock", "w") as output:
    output.write("#!/bin/bash\n")
    output.write("docker run \\\n    ")
    output.write(" \\\n    ".join([" ".join(x) for x in docker_args]))
    output.write("\n\n")
    output.write(
    "containerId=$(docker ps -l -q)\n"
    "xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`\n"
    "docker attach $containerId\n"
    )

print("---\n")
print("Configured mdock, run `sudo make install` to install wrapper")
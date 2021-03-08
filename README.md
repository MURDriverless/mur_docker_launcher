# mur_docker_launcher
A shell script wrapper for `mur_docker`

Run an interactive terminal instance with automounted `$pwd` for `mur_docker`.

To create a new terminal instance of the docker container,
`docker exec -it {container_name} bash`
## Features
 - Auto detects CUDA capable GPU
 - Foward X11 for GUI applications
   - Safer `xhost` permissions
 - Automounting `$(pwd)` to `/workspace` in container
 - Cachcing `vscode-server` install
 - Port forwarding `roscore` port
 - Expose usb devices to container
 - Custom container name

## Usage
Run,
```
python3 ./config.py
```
or with `-i` flag for interactive mode,
```
python3 ./config.py -i
```
To generate mdock, then install with
```
sudo make install
```

## TODO
- [x] Move install to /usr/local/sbin, with `sudo`
- [x] Actually make cli config options
    - cli flag to enable text based configurator
- [ ] More configurations

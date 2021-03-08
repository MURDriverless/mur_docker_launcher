# mur_docker_launcher
A shell script wrapper for `mur_docker`

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
To generate mdock, then install with
```
sudo make install
```

## TODO
- [x] Move install to /usr/local/sbin, with `sudo`
- [ ] Actually make cli config options
- [ ] More configurations

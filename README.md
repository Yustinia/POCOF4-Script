# HyperOS Porting Script

This is a porting script that should be used in union with the DNA app. The goal of this script is to automate the process of manually modifying files/folders/props

## Features

- [x] Add prop lines for fixes

- [x] Add a downloader for the fixes

- [x] User specify folder names for the script

- [ ] Add modding capabilities

## Prerequisites

- DNA application — For unpacking and repacking roms
- Termux — For running the script
- Python — For the script to run
- Root Access — Requires access at `/data`
- Python Libraries
    - shutil
    - subprocess
    - Path

## Installation / Preparation

1. Use `git clone` to download the repository

```bash
git clone https://github.com/Yustinia/POCOF4-Script.git
```

2. Give execution permissions to the shell scripts using Termux

```bash
chmod +x downloader.sh
chmod +x linefixes.sh
```

3. Do a first run of `main.py` and choose "2" to prepare the fixes

4. Place the following inside `/data/DNA`. Create if absent

    - downloader.sh
    - linefixes.sh
    - main.py
    - hosfix

4. Download `python` via Termux using either commands

```bash
apt install python # if pkg manager is apt
pacman -S python # if pkg manager is pacman
```

## Usage

1. Run the python script with

```bash
python3 main.py
```

2. Start with porting by entering "1"

3. Wait until it finishes

## Disclaimer

**USE AT YOUR OWN RISK!** This script requires and modifies the `/data` directory and can potentially:

- Brick your device
- Cause data loss

Always create a reliable backup before proceeding

## License

This *small* project is licensed under the MIT License

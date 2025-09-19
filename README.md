# HyperOS Porting Script

This is a porting script that should be used in union with the DNA app. The goal of this script is to automate the process of manually modifying files/folders/props

## Features

- [x] Add prop lines for fixes

- [x] Add a downloader for the fixes

- [x] User specify folder names for the script

- [ ] Add modding capabilities

- [ ] Extend porting capability to HyperOS 2.0, 2.1, and 2.2

## Prerequisites

- DNA application — For unpacking and repacking roms
- Termux — For running the script
- Python — For the script to run
- Rooted Device — Requires access at `/data`
- Python Libraries
    - shutil
    - subprocess
    - Path

## Installation / Preparation

1. Use `git clone` to clone the repo

```bash
git clone https://github.com/Yustinia/POCOF4-Script.git
```

2. Give execution permissions to the shell scripts using Termux

```bash
chmod +x downloader.sh
chmod +x linefixes.sh
```

3. Do a first run of `main.py` and choose "2" to download the fixes

4. Move/Copy the following inside `/data/DNA`. Create if absent

    - linefixes.sh
    - main.py
    - hosfix/

5. Download the following packages in Termux (apt or pacman)

    - python
    - aria2
    - unzip
    - sudo

## Usage

1. Using Termux, `cd /data/DNA`

> To list files, use `sudo ls -latr`

2. Run the python script with

```bash
python3 main.py
```

3. Start with porting by entering "1"

4. Provide the exact folder name — ensure correct folders

5. Wait until it completes

6. Enter "3" to exit

## Disclaimer

**USE AT YOUR OWN RISK!** This script requires and modifies the `/data` directory and can potentially:

- Brick your device
- Cause data loss

Always create a reliable backup before proceeding. You have been warned

## License

This *small* project is licensed under the **MIT License**

# HyperOS Porting Script

This is a porting script that should be used in union with the DNA app. The goal of this script is to automate the process of manually modifying files/folders/props

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Disclaimer](#disclaimer)
- [Credits](#credits)
- [License](#license)

## Features

- [x] Add prop lines for fixes

- [x] Add a downloader for the fixes

- [x] User specify folder names for the script

- [ ] Add modding capabilities
    
    - APK File Replacement
    - 144hz capability
    - System Optimizations
    - Device prop spoofing

- [ ] Extend porting capability to HyperOS 2.0, 2.1, and 2.2

## Prerequisites

- [DNA Application](https://t.me/OrcaCloud) — For unpacking and repacking roms
- [Termux](https://f-droid.org/packages/com.termux/) — For running the script
- Python — For the script to run
- Rooted Device — Requires access at `/data`
- Python Libraries
    - shutil
    - subprocess
    - Path

## Installation

1. Use `git clone` to clone the repo

```bash
git clone https://github.com/Yustinia/POCOF4-Script.git
```

2. Give execution permissions to the shell scripts using Termux

```bash
chmod +x downloader.sh
chmod +x linefixes.sh
```

3. Download the following packages in Termux (apt or pacman)

    - python — To run the script
    - aria2 — To download the fixes
    - unzip — To unzip the archive
    - sudo — For unzip to work

```bash
pacman -S --needed python aria2 unzip sudo # This is for pacman
```

4. Do a first run using `sudo python main.py` and choose "2" to download the fixes

5. Move/Copy the following into `/data/DNA` using your preferred file manager or do it CLI-style. Create if absent

    - linefixes.sh
    - main.py
    - hosfix/

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

## Credits

Credits to olzhas0986 and the POCOF4 community for the help!

## License

This *small* project is licensed under the **[MIT License](https://github.com/Yustinia/POCOF4-Script/blob/main/LICENSE)**

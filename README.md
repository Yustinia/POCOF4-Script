# POCOF4 / Redmi K40S Porting Script

This is a porting script used in union with the DNA app. The goal of this script is to automate the process of manually modifying files/folders/props.

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

- [ ] Extend porting capability to HyperOS 2.0, 2.1, and 2.2

## Prerequisites

- [DNA Application](https://t.me/OrcaCloud) — For unpacking and repacking roms
- [Termux](https://f-droid.org/packages/com.termux/) — For running the script
- Rooted Device — Requires access at `/data` and for DNA
- Python Libraries Used:
    - shutil
    - subprocess
    - Path

## Installation

1. Download the following packages in Termux (apt or pacman).

    - git — To clone the repo
    - python — To run the script
    - aria2 — To download the fixes
    - unzip — To unzip the archive
    - sudo — For unzip to work

```bash
pacman -S --needed git python aria2 unzip sudo # This is for pacman
```

2. Use `git clone` to clone the repo to anywhere on your device.

```bash
git clone https://github.com/Yustinia/POCOF4-Script.git
```

3. Give execution permissions to the shell scripts using Termux.

```bash
chmod +x downloader.sh
chmod +x linefixes.sh
```

4. Do a first run using `sudo python main.py` and download the fixes.

5. Move/Copy the following into `/data/DNA` using your preferred file manager or do it CLI-style. Create if absent.

    - linefixes.sh
    - checkpaths.py
    - portingprocess.py
    - main.py
    - hosfix/

```bash
cd POCOF4-Script/
mv -fv linefixes.sh checkpaths.py portingprocess.py main.py hosfix/ /data/DNA
```

## Usage

1. Using Termux, `cd /data/DNA`.

> To list files, use `sudo ls -latr`

2. Run the python script with.

```bash
sudo python main.py
```

3. Provide the folder name being asked.

4. Choose [1] to start the porting process.

5. Wait until it completes.

6. Exit the tool.

## Disclaimer

**USE AT YOUR OWN RISK!** This script requires access at `/data/DNA`, while it only accesses that specific directory, it might potentially have the following:

- Brick your device
- Cause data loss

Always create a reliable backup before proceeding. You have been warned.

## Credits

Credits to olzhas0986 and the POCOF4 / K40S community!

## License

This *small* project is licensed under the **[MIT License](https://github.com/Yustinia/POCOF4-Script/blob/main/LICENSE)**.

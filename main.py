# set libraries

from pathlib import Path
import subprocess
import shutil

# set device global paths
dna_dir = Path("/data/DNA")
hosfix = Path("/data/DNA/hosfix")
mods_dir = Path("/data/DNA/mods")


def mod_display():
    opts = [
        "[1] Start",
        "[2] Quit",
    ]

    print()
    for line in opts:
        print(line)
    print()


def mk_mod_dirs():
    req_dirs = ["product", "system", "system_ext", "vendor"]

    if not mods_dir.exists():
        mods_dir.mkdir(parents=True, exist_ok=True)

    for dir in req_dirs:
        mod_path = mods_dir / dir
        if not mod_path.exists():
            mod_path.mkdir(parents=True, exist_ok=True)


def should_start_mod(do_start):
    if do_start in [1, 2]:
        return do_start
    return None


def start_mods(port_path):
    if not port_path:
        return "Port path not defined yet. Define them at option [1]"

    for item in mods_dir.iterdir():
        dest = port_path / item.name
        shutil.copytree(item, dest, dirs_exist_ok=True)

    return "Finished modding"


# === download essential files === #


def download_essen():
    print("Downloading Fixes...")
    script_path = Path.cwd() / "downloader.sh"
    subprocess.run(script_path, check=True)


# === check whether folder exists === #


def validate_fd_exists(folder_name) -> Path | None:
    fd_path = dna_dir / folder_name

    if Path(fd_path).exists():
        return fd_path
    return None


def check_exists():
    ent_f4_fd = input("Enter the F4 folder name: ").strip()
    ent_port_fd = input("Enter the PORT folder name: ").strip()

    f4_path = validate_fd_exists(ent_f4_fd)
    port_path = validate_fd_exists(ent_port_fd)

    missing_dirs = []

    if not f4_path:
        missing_dirs.append(ent_f4_fd)
    if not port_path:
        missing_dirs.append(ent_port_fd)

    if missing_dirs:
        print("Missing:", ", ".join(missing_dirs))

    return f4_path, port_path


# === start porting process === #


def do_port(f4_path, port_path):
    # f4_path, port_path = check_exists()

    # If folders not found
    if not (f4_path and port_path):
        return None

    # set file directories to prepare for copy
    # f4 source folders
    f4_src = (
        Path(f"{f4_path}/product/etc/device_features/munch.xml"),
        Path(f"{f4_path}/product/etc/displayconfig/"),
        Path(f"{f4_path}/product/etc/permissions/"),
        Path(f"{f4_path}/product/overlay/AospFrameworkResOverlay.apk"),
        Path(f"{f4_path}/product/overlay/DevicesAndroidOverlay.apk"),
        Path(f"{f4_path}/product/overlay/DevicesOverlay.apk"),
        Path(f"{f4_path}/product/overlay/MiuiFrameworkResOverlay.apk"),
        Path(f"{f4_path}/system_ext/apex/"),
    )

    # fixes source folders
    fix_src = (
        Path(f"{hosfix}/product/app/"),
        Path(f"{hosfix}/product/priv-app/"),
        Path(f"{hosfix}/product/etc/permissions/"),
        Path(f"{hosfix}/product/overlay/AospFrameworkResOverlay.apk"),
        Path(f"{hosfix}/product/overlay/DevicesOverlay.apk"),
        Path(f"{hosfix}/system/system/app/"),
        Path(f"{hosfix}/system/system/priv-app/"),
        Path(f"{hosfix}/system/system/lib/"),
        Path(f"{hosfix}/system/system/lib64/"),
        Path(f"{hosfix}/vendor/lib/"),
        Path(f"{hosfix}/vendor/lib64/"),
    )

    # copy to these folders f4 -> port
    out_port = (
        Path(f"{port_path}/product/etc/device_features/"),
        Path(f"{port_path}/product/etc/displayconfig/"),
        Path(f"{port_path}/product/etc/permissions/"),
        Path(f"{port_path}/product/overlay/"),
        Path(f"{port_path}/product/overlay/"),
        Path(f"{port_path}/product/overlay/"),
        Path(f"{port_path}/product/overlay/"),
        Path(f"{port_path}/system_ext/apex/"),
    )

    # copy the these folders fixes -> f4/port
    out_fixes = (
        Path(f"{port_path}/product/app/"),
        Path(f"{port_path}/product/priv-app/"),
        Path(f"{port_path}/product/etc/permissions/"),
        Path(f"{port_path}/product/overlay/"),
        Path(f"{port_path}/product/overlay/"),
        Path(f"{port_path}/system/system/app/"),
        Path(f"{port_path}/system/system/priv-app/"),
        Path(f"{port_path}/system/system/"),
        Path(f"{port_path}/system/system/"),
        Path(f"{f4_path}/vendor/"),
        Path(f"{f4_path}/vendor/"),
    )

    for src, dest in zip(f4_src, out_port):
        if src.is_file():
            shutil.copy2(src, dest)
        elif src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)

    for src, dest in zip(fix_src, out_fixes):
        if src.is_file():
            shutil.copy2(src, dest)
        elif src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)

    # fix lines on buildprop
    subprocess.run(Path.cwd() / "linefixes.sh", check=True)

    return True


# === display main menu options


def disp_opts():
    opts = [
        "[1] Define Path",
        "[2] Start Port",
        "[3] Modding",
        "[4] Download Fixes",
        "[5] Exit",
    ]

    print()
    for ln in opts:
        print(ln)
    print()


def get_choice(choice):
    if choice in ["1", "2", "3", "4", "5"]:
        return choice
    return None


# === main execution === #


def main():
    f4_path, port_path = None, None
    while True:
        # display menu
        disp_opts()

        # get choice
        ent_choice = input("> ").strip()
        choice = get_choice(ent_choice)

        if choice == "1":
            f4_path, port_path = check_exists()

        elif choice == "2":
            if (
                not f4_path
                or not f4_path.exists()
                or not port_path
                or not port_path.exists()
            ):
                print("Unable to process. Please define the paths with [1]")
                continue

            do_port(f4_path, port_path)
            print("Porting Fixes Done!")

        elif choice == "3":
            mod_display()  # display options
            mk_mod_dirs()  # create directories first

            do_start = int(input("Do you want to start modding: "))
            choice = should_start_mod(do_start)

            if choice == 1:
                print(start_mods(port_path))

        elif choice == "4":
            download_essen()

        elif choice == "5":
            print("Thank you for using the script!")
            break


if __name__ == "__main__":
    main()

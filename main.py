# set libraries
from pathlib import Path
import subprocess
import shutil

# set device global paths
dna_dir = Path("/data/DNA")
hosfix = Path("/data/DNA/hosfix")


# downloads fixes
def download_essen():
    print("Downloading Fixes...")
    script_path = Path.cwd() / "downloader.sh"
    subprocess.run(script_path, check=True)


# checks whether the unpacked folders exists, else None
def validate_fd_exists(folder_name):
    fd_path = dna_dir / folder_name

    if Path(fd_path).exists():
        return fd_path
    return None


# existence
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


# start porting
def do_port():
    f4_path, port_path = check_exists()

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


# display options
def disp_opts():
    opts = [
        "[1] Start Port",
        "[2] Download Fixes",
        "[3] Exit",
    ]

    print()
    for ln in opts:
        print(ln)
    print()


# get choice
def get_choice(choice):
    if choice in ["1", "2", "3"]:
        return choice
    return None


# final process
def main():
    while True:
        # display menu
        disp_opts()

        # get choice
        ent_choice = input("> ").strip()
        choice = get_choice(ent_choice)

        if choice == "1":
            result = do_port()

            if not result:
                print("Unable to proceed")

            else:
                print("Porting Fixes Done!")

        elif choice == "2":
            download_essen()

        elif choice == "3":
            print("Thank you for using the script!")
            break

        else:
            print(f"Invalid: '{choice}'")


if __name__ == "__main__":
    main()

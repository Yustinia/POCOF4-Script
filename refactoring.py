# libraries
from pathlib import Path
import subprocess
import shutil

# gloal paths
dna_dir = Path("/data/DNA")
hosfix = Path("/data/DNA/hosfix")
mods_dir = Path("/data/DNA/mods")


# === download essential port fixes === #


def download_fixes() -> None:
    print("Downloading fixes...")
    download_script_path = Path.cwd() / "downloader.sh"
    subprocess.run(download_script_path, check=True)


# === verify if the folders does exist === #


def return_dir(folder_name) -> Path | None:
    folder_path = dna_dir / folder_name

    if Path(folder_path).exists():
        return folder_path
    return None


def check_dir_exists(
    user_defined_pocof4, user_defined_port
):  # checks the directories if they exist
    poco_f4_path = return_dir(user_defined_pocof4)
    port_path = return_dir(user_defined_port)

    missing_dir = []
    if not poco_f4_path:
        missing_dir.append(user_defined_pocof4)
    if not port_path:
        missing_dir.append(user_defined_port)

    return poco_f4_path, port_path, missing_dir


# === porting process === #


def start_porting(pocof4_path, port_path):
    if not pocof4_path and not port_path:
        return None

    # set file directories to prepare for copy
    # f4 source folders
    f4_src = (
        Path(f"{pocof4_path}/product/etc/device_features/munch.xml"),
        Path(f"{pocof4_path}/product/etc/displayconfig/"),
        Path(f"{pocof4_path}/product/etc/permissions/"),
        Path(f"{pocof4_path}/product/overlay/AospFrameworkResOverlay.apk"),
        Path(f"{pocof4_path}/product/overlay/DevicesAndroidOverlay.apk"),
        Path(f"{pocof4_path}/product/overlay/DevicesOverlay.apk"),
        Path(f"{pocof4_path}/product/overlay/MiuiFrameworkResOverlay.apk"),
        Path(f"{pocof4_path}/system_ext/apex/"),
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
        Path(f"{pocof4_path}/vendor/"),
        Path(f"{pocof4_path}/vendor/"),
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


# === menu options === #


def display_options() -> None:
    opts = [
        "[1] Start Port",
        "[2] Modding",
        "[3] Download Fixes",
        "[4] Exit",
    ]

    print()
    for ln in opts:
        print(ln)
    print()


def get_choice_options(choice) -> int | None:
    if choice in [1, 2, 3, 4]:
        return choice
    return None


def main():
    while True:
        set_pocof4_path = input("Enter folder name of F4: ").strip()
        set_port_path = input("Enter folder name of PORT: ").strip()

        set_pocof4_path, set_port_path, missing_dir = check_dir_exists(
            set_pocof4_path, set_port_path
        )

        if missing_dir:
            print("Missing: ", ", ".join(missing_dir))
            continue

        print(f"F4: {set_pocof4_path}, PORT: {set_port_path}")
        break

    while True:
        display_options()  # display possible options
        try:
            menu_choice = int(input("Enter choice: "))
            menu_choice = get_choice_options(menu_choice)

            if menu_choice == 1:  # porting process here
                porting_result = start_porting(set_pocof4_path, set_port_path)

                if not porting_result:
                    print("Unable to port")
                    continue

                print("Successfully finished porting")

            elif menu_choice == 2:  # modding starts here
                pass

            elif menu_choice == 3:  # downloading fixes here
                download_fixes()

            elif menu_choice == 4:
                print("Thank you for using the script!")
                break

            elif not menu_choice:
                print("Invalid: Enter choice from 1/2/3/4")

        except ValueError:
            print("Invalid: Enter a number")


if __name__ == "__main__":
    main()

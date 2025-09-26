from pathlib import Path
from portingprocess import start_porting
import shutil
import subprocess

# GLOBAL PATHS
DNA_DIR = Path("/data/DNA")
HOSFIX_DIR = Path("/data/DNA/hosfix")
SHELL_SCRIPTS = Path("/data/DNA/shell-scripts")


def download_fixes():
    if not HOSFIX_DIR.exists():
        try:
            subprocess.run(SHELL_SCRIPTS / "downloader.sh", check=True)
            return True, f"{HOSFIX_DIR} has been created"
        except subprocess.CalledProcessError as e:
            return False, f"Failed: {e}"
    return True, f"{HOSFIX_DIR} already exists"


def check_dir_exists(poco_f4: str, port: str):
    poco_f4_dir = DNA_DIR / poco_f4
    port_dir = DNA_DIR / port

    missing_dir = []
    if not poco_f4_dir.exists():
        missing_dir.append(poco_f4_dir.name)
    if not port_dir.exists():
        missing_dir.append(port_dir.name)

    return poco_f4_dir, port_dir, missing_dir


def menu_disp_opts(set_dirs: bool):
    opts = [
        "[1] Set Folders",
        "[2] Download Fixes",
    ]

    if set_dirs:
        opts.append("[3] Start Port")

    opts.append("[4] Quit")

    print()
    for ln in opts:
        print(ln)
    print()


def main():
    is_set_dirs = False
    f4_folder, port_folder = None, None
    menu_choose_opt = [1, 2, 4]

    while True:
        menu_disp_opts(is_set_dirs)
        if is_set_dirs:
            menu_choose_opt = [1, 2, 3, 4]
        try:
            do_choice = int(input("Enter choice: "))
            if do_choice not in menu_choose_opt:
                print("Invalid: Not an option")
                continue
        except ValueError:
            print("Invalid: Must be a number")
            continue

        if do_choice == 1:  # ensure folders are there
            f4_folder = input("Enter the F4 folder name: ").strip()
            port_folder = input("Enter the PORT folder name: ").strip()

            f4_folder, port_folder, missing_fds = check_dir_exists(
                f4_folder, port_folder
            )

            if missing_fds:
                print("Missing:", ", ".join(missing_fds))
            else:
                is_set_dirs = True

        elif do_choice == 2:  # download fixes
            ph, msg = download_fixes()
            print(msg)

        elif do_choice == 3:
            print("Start Porting...")
            result = start_porting(f4_folder, port_folder)
            if result:
                print("Successful!")
            else:
                print("Failed")

        elif do_choice == 4:
            print("Thank you for using the tool!")
            break


if __name__ == "__main__":
    main()

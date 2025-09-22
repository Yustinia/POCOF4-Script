# libraries
from checkpaths import *
from portingprocess import start_porting
from pathlib import Path
import subprocess
import shutil

# gloal paths
dna_dir = Path("/data/DNA")
hosfix = Path("/data/DNA/hosfix")
mods_dir = Path("/data/DNA/mods")


# === download essential port fixes === #


def download_fixes() -> None:
    download_script_path = Path.cwd() / "downloader.sh"
    subprocess.run(download_script_path, check=True)


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


# === main execution === #


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
                print("Downloading fixes...")
                download_fixes()
                print("Fixes downloaded!")

            elif menu_choice == 4:
                print("Thank you for using the script!")
                break

            elif not menu_choice:
                print("Invalid: Enter choice from 1/2/3/4")

        except ValueError:
            print("Invalid: Enter a number")


if __name__ == "__main__":
    main()

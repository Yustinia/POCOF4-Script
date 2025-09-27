# from portingprocess import start_porting
# from pathlib import Path
# import shutil
# import subprocess
from HOSPorter import Porter


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
    porter = Porter(None, None)
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

            # f4_folder, port_folder, missing_fds = check_dir_exists(
            #     f4_folder, port_folder
            # )

            f4_folder, port_folder, missing_fds = porter.check_dir_exists(
                f4_folder, port_folder
            )

            if missing_fds:
                print("Missing:", ", ".join(missing_fds))
            else:
                is_set_dirs = True
                porter = Porter(f4_folder, port_folder)

        elif do_choice == 2:  # download fixes
            ph, msg = porter.download_fixes()
            print(msg)

        elif do_choice == 3:
            print("Start Porting...")

            # result = start_porting(f4_folder, port_folder)

            result = porter.start_porting()
            if result:
                print("Successful!")
            else:
                print("Failed")

        elif do_choice == 4:
            print("Thank you for using the tool!")
            break


if __name__ == "__main__":
    main()

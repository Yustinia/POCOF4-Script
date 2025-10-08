from HOSPorterv2 import Porter

porter = Porter("munch", "port")


def menu_disp_opts():
    opts = [
        "[0] Quit",
        "[1] Set Folders",
        "[2] Download Fixes",
        "[3] Start Port",
    ]

    print()
    for ln in opts:
        print(ln)
    print()


def handle_define_dirs():
    f4dir = input("Enter F4: ").strip()
    port_dir = input("Enter PORT: ").strip()

    porter = Porter(f4dir, port_dir)

    result = porter.check_operation_dir_exists(f4dir, port_dir)

    return porter, result


def handle_download():
    try:
        porter.download_fixes()
    except (FileNotFoundError, PermissionError) as e:
        print(e)


def handle_port_start():
    porter, _ = handle_define_dirs()

    try:
        porter.start_porting()
    except PermissionError as e:
        print(e)


def main():
    is_set_dirs = False
    do_option = 0
    # instantiate porter class later

    while True:
        menu_disp_opts()

        try:
            do_option = int(input("Enter option: "))
        except ValueError as e:
            print("Invalid:", e)
            continue

        match (do_option):
            case 0:
                print("Exiting...")
                break

            case 1:
                _, result = handle_define_dirs()

                if result:
                    print("Missing:", ", ".join(result))
                else:
                    is_set_dirs = True

            case 2:
                handle_download()

            case 3:
                if not is_set_dirs:
                    print("Invalid: Did not set folders")
                else:
                    handle_port_start()

            case _:
                print("Invalid: Not an option")


main()

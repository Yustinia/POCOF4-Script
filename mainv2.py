from HOSPorterv2 import Porter


def menu_disp_opts():
    opts = [
        "[1] Set Folders",
        "[2] Download Fixes",
        "[3] Start Port",
        "[4] Quit",
    ]

    print()
    for ln in opts:
        print(ln)
    print()


def define_operation_dirs():
    f4dir = input("Enter F4: ").strip()
    port_dir = input("Enter PORT: ").strip()

    porter = Porter(f4dir, port_dir)

    check_result = porter.check_operation_dir_exists(f4dir, port_dir)

    return porter, check_result


def main():
    is_set_dirs = False
    do_option = 0
    porter = Porter("munch", "port")
    # instantiate porter class later

    while True:
        menu_disp_opts()

        try:
            do_option = int(input("Enter option: "))
        except ValueError as e:
            print("Invalid:", e)
            continue

        match (do_option):
            case 1:
                porter, result = define_operation_dirs()

                if result:
                    print("Missing:", ", ".join(result))

            case 2:
                try:
                    porter.download_fixes()
                except (FileNotFoundError, PermissionError) as e:
                    print(e)


main()

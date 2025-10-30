from hoscopyfix import HOSCopyFixes
from hosport import HOSPort
from hosmodder import HOSModder
from unpacker import SuperUnpacker


def show_all_opts() -> None:  # display
    options = [
        "[0] Exit",
        "[1] Start Port",
        "[2] Add Mods",
        "[3] Extract Super",
    ]

    print()
    for line in options:
        print(line)
    print()


def check_if_valid_choice(choice: int):  # input
    if choice in [int(i) for i in range(4)]:
        return choice
    raise ValueError(f"Invalid: '{choice}' got")


def main():
    show_all_opts()

    while True:
        get_choice = None
        try:
            get_choice = int(input("Enter choice: "))
            get_choice = check_if_valid_choice(get_choice)
        except ValueError as e:
            print(e)
            continue
        break

    if get_choice == 0:
        print("Exiting...")
        return

    match get_choice:
        case 1:
            processed_prod = processed_sys = processed_vendor = None

            hosporter = HOSPort()
            hosfixer = HOSCopyFixes()
            print("Start Porting...")

            try:
                hosporter.copy_f4_to_port()
            except ValueError as e:
                print(e)

            hosporter.fix_props()

            try:
                processed_prod = hosfixer.fix_product()
                processed_sys = hosfixer.fix_system()
                processed_vendor = hosfixer.fix_vendor()
            except ValueError as e:
                print(e)

            processed = [
                processed_prod,
                processed_sys,
                processed_vendor,
            ]

            for line in processed:
                print("Processed:", line)

        case 2:
            processed_mods = []

            hosmodding = HOSModder()

            try:
                processed_mods = hosmodding.copy_mods()
            except ValueError as e:
                print(e)

            for line in processed_mods:
                print(line)

        case 3:
            unpacker = SuperUnpacker()
            results = unpacker.ext_super()

            for line in results:
                print(line)


if __name__ == "__main__":
    main()

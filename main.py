from hoscopyfix import HOSCopyFixes
from hosport import HOSPort
from hosmodder import HOSModder


def show_all_opts() -> None:  # display
    options = [
        "[Q] Exit",
        "[1] Start Port",
        "[2] Add Mods",
    ]

    print()
    for line in options:
        print(line)
    print()


def check_if_valid_choice(choice: str):  # input
    if choice.upper() in [str(i) for i in range(3)] + ["Q"]:
        return choice.upper()
    raise ValueError(f"Invalid '{choice}' got")


def main():
    show_all_opts()

    while True:
        get_choice = None
        try:
            get_choice = input("Enter choice: ").strip()
            get_choice = check_if_valid_choice(get_choice)
        except ValueError as e:
            print(e)
            continue
        break

    if get_choice == "Q":
        print("Exiting...")
        return

    match get_choice:
        case "1":
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

        case "2":
            processed_mods = []

            hosmodding = HOSModder()

            try:
                processed_mods = hosmodding.copy_mods()
            except ValueError as e:
                print(e)

            for line in processed_mods:
                print(line)


if __name__ == "__main__":
    main()

from pathlib import Path

dna_dir = Path("/data/DNA")


# Return directories if they exist
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

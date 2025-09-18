# set libraries
from pathlib import Path

# set global paths
dna_dir = Path("/data/DNA")
hosfix = Path("/data/DNA/hosfix")


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

    missing_dirs = []

    if not validate_fd_exists(ent_f4_fd):
        missing_dirs.append("F4")
    if not validate_fd_exists(ent_port_fd):
        missing_dirs.append("PORT")

    if missing_dirs:
        print("Missing:", ", ".join(missing_dirs))
        return False
    return True

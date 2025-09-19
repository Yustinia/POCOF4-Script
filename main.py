# set libraries
from pathlib import Path
import subprocess
import shutil

# set device global paths
dna_dir = Path("/data/DNA")
hosfix = Path("/data/DNA/hosfix")


# downloads fixes
def download_essen():
    print("Downloading Fixes...")
    subprocess.run(Path.cwd() / "downloader.sh", check=True)


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

    f4_path = validate_fd_exists(ent_f4_fd)
    port_path = validate_fd_exists(ent_port_fd)

    missing_dirs = []

    if not f4_path:
        missing_dirs.append("F4")
    if not port_path:
        missing_dirs.append("PORT")

    if missing_dirs:
        print("Missing:", ", ".join(missing_dirs))
        return False
    return f4_path, port_path


# start porting
def do_port():
    valid_res = check_exists()

    # If folders not found
    if not valid_res:
        return

    f4_path, port_path = valid_res

    # set file directories to prepare for copy
    # f4 source folders
    f4_src = (
        Path(f"{f4_path}/product/etc/device_features/munch.xml"),
        Path(f"{f4_path}/product/etc/displayconfig/"),
        Path(f"{f4_path}/product/etc/permissions/"),
        Path(f"{f4_path}/product/overlay/AospFrameworkResOverlay.apk"),
        Path(f"{f4_path}/product/overlay/DevicesAndroidOverlay.apk"),
        Path(f"{f4_path}/product/overlay/DevicesOverlay.apk"),
        Path(f"{f4_path}/product/overlay/MiuiFrameworkResOverlay.apk"),
        Path(f"{f4_path}/system_ext/apex/"),
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
        Path(f"{f4_path}/vendor/"),
        Path(f"{f4_path}/vendor/"),
    )

    for src, dest in zip(f4_src, out_port):
        if src.is_file():
            shutil.copy2(src, dest)
        elif src.is_dir():
            shutil.copytree(src, dest)

    for src, dest in zip(fix_src, out_fixes):
        if src.is_file():
            shutil.copy2(src, dest)
        elif src.is_dir():
            shutil.copytree(src, dest)

    # fix lines on buildprop
    subprocess.run(Path.cwd() / "linefixes.sh", check=True)


do_port()

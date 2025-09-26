from pathlib import Path
import shutil
import subprocess

HOSFIX_DIR = Path("/data/DNA/hosfix")
SHELL_SCRIPTS = Path("/data/DNA/shell-scripts")


# start porting process
def start_porting(pocof4_path, port_path):
    # set file directories to prepare for copy
    # f4 source folders
    f4_src = (
        Path(f"{pocof4_path}/product/etc/device_features/munch.xml"),
        Path(f"{pocof4_path}/product/etc/displayconfig/"),
        Path(f"{pocof4_path}/product/etc/permissions/"),
        Path(f"{pocof4_path}/product/overlay/AospFrameworkResOverlay.apk"),
        Path(f"{pocof4_path}/product/overlay/DevicesAndroidOverlay.apk"),
        Path(f"{pocof4_path}/product/overlay/DevicesOverlay.apk"),
        Path(f"{pocof4_path}/product/overlay/MiuiFrameworkResOverlay.apk"),
        Path(f"{pocof4_path}/system_ext/apex/"),
    )

    # fixes source folders
    fix_src = (
        Path(f"{HOSFIX_DIR}/product/app/"),
        Path(f"{HOSFIX_DIR}/product/priv-app/"),
        Path(f"{HOSFIX_DIR}/product/etc/permissions/"),
        Path(f"{HOSFIX_DIR}/product/overlay/AospFrameworkResOverlay.apk"),
        Path(f"{HOSFIX_DIR}/product/overlay/DevicesOverlay.apk"),
        Path(f"{HOSFIX_DIR}/system/system/app/"),
        Path(f"{HOSFIX_DIR}/system/system/priv-app/"),
        Path(f"{HOSFIX_DIR}/system/system/lib/"),
        Path(f"{HOSFIX_DIR}/system/system/lib64/"),
        Path(f"{HOSFIX_DIR}/vendor/lib/"),
        Path(f"{HOSFIX_DIR}/vendor/lib64/"),
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
        Path(f"{pocof4_path}/vendor/"),
        Path(f"{pocof4_path}/vendor/"),
    )

    for src, dest in zip(f4_src, out_port):
        if src.is_file():
            shutil.copy2(src, dest)
        elif src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)

    for src, dest in zip(fix_src, out_fixes):
        if src.is_file():
            shutil.copy2(src, dest)
        elif src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)

    # fix lines on buildprop
    subprocess.run(SHELL_SCRIPTS / "linefixes.sh", check=True)

    return True

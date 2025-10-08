from pathlib import Path
import os
import shutil
import subprocess


class Porter:
    def __init__(self, f4dir: str, portdir: str) -> None:
        self.DNA_DIR = Path("/data/DNA")
        self.HOSFIX_DIR = Path("/data/DNA/hosfix")
        self.SHELL_SCRIPTS = Path("/data/DNA/shell-scripts")

        self.f4dir = f4dir
        self.portdir = portdir

    def download_fixes(self):
        downloader_script = self.SHELL_SCRIPTS / "downloader.sh"

        if not self.HOSFIX_DIR.exists():
            raise FileNotFoundError("Missing:", self.HOSFIX_DIR)

        if not os.access(downloader_script, os.X_OK):
            raise PermissionError(
                f"{downloader_script.name} is not executable. Use `chmod +x` to fix it."
            )

        subprocess.run([str(downloader_script)], check=True)

    def check_operation_dir_exists(self, f4dir, portdir):
        self.f4dir = self.DNA_DIR / f4dir
        self.portdir = self.DNA_DIR / portdir

        missing_dirs = []

        if not self.f4dir.exists():
            missing_dirs.append(self.f4dir.name)
        if not self.portdir.exists():
            missing_dirs.append(self.portdir.name)

        return missing_dirs

    def start_porting(self):
        linefix_script = self.SHELL_SCRIPTS / "linefixes.sh"

        if not os.access(linefix_script, os.X_OK):
            raise PermissionError(
                f"{linefix_script.name} is not executable. Use `chmod +x` to fix it"
            )

        # set file directories to prepare for copy
        # f4 source folders
        f4_src = (
            Path(f"{self.f4dir}/product/etc/device_features/munch.xml"),
            Path(f"{self.f4dir}/product/etc/displayconfig/"),
            Path(f"{self.f4dir}/product/etc/permissions/"),
            Path(f"{self.f4dir}/product/overlay/AospFrameworkResOverlay.apk"),
            Path(f"{self.f4dir}/product/overlay/DevicesAndroidOverlay.apk"),
            Path(f"{self.f4dir}/product/overlay/DevicesOverlay.apk"),
            Path(f"{self.f4dir}/product/overlay/MiuiFrameworkResOverlay.apk"),
            Path(f"{self.f4dir}/system_ext/apex/"),
        )

        # fixes source folders
        fix_src = (
            Path(f"{self.HOSFIX_DIR}/product/app/"),
            Path(f"{self.HOSFIX_DIR}/product/priv-app/"),
            Path(f"{self.HOSFIX_DIR}/product/etc/permissions/"),
            Path(f"{self.HOSFIX_DIR}/product/overlay/AospFrameworkResOverlay.apk"),
            # Path(f"{self.HOSFIX_DIR}/product/overlay/DevicesOverlay.apk"),
            Path(f"{self.HOSFIX_DIR}/system/system/app/"),
            Path(f"{self.HOSFIX_DIR}/system/system/priv-app/"),
            Path(f"{self.HOSFIX_DIR}/system/system/lib/"),
            Path(f"{self.HOSFIX_DIR}/system/system/lib64/"),
            Path(f"{self.HOSFIX_DIR}/vendor/lib/"),
            Path(f"{self.HOSFIX_DIR}/vendor/lib64/"),
        )

        # copy to these folders f4 -> port
        out_port = (
            Path(f"{self.portdir}/product/etc/device_features/"),
            Path(f"{self.portdir}/product/etc/displayconfig/"),
            Path(f"{self.portdir}/product/etc/permissions/"),
            Path(f"{self.portdir}/product/overlay/"),
            Path(f"{self.portdir}/product/overlay/"),
            Path(f"{self.portdir}/product/overlay/"),
            Path(f"{self.portdir}/product/overlay/"),
            Path(f"{self.portdir}/system_ext/apex/"),
        )

        # copy the these folders fixes -> f4/port
        out_fixes = (
            Path(f"{self.portdir}/product/app/"),
            Path(f"{self.portdir}/product/priv-app/"),
            Path(f"{self.portdir}/product/etc/permissions/"),
            Path(f"{self.portdir}/product/overlay/"),
            # Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.portdir}/system/system/app/"),
            Path(f"{self.portdir}/system/system/priv-app/"),
            Path(f"{self.portdir}/system/system/"),
            Path(f"{self.portdir}/system/system/"),
            Path(f"{self.f4dir}/vendor/"),
            Path(f"{self.f4dir}/vendor/"),
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
        subprocess.run([str(linefix_script)], check=True)

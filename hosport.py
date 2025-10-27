from pathlib import Path
import shutil
import subprocess

F4PATH = Path.cwd() / "POCOF4"
PORTPATH = Path.cwd() / "PORT"
HOSFIX = Path.cwd() / "HOSFix"


class HOSPort:
    def __init__(self) -> None:
        self.f4_path = F4PATH
        self.port_path = PORTPATH

    def copy_f4_to_port(self) -> None:
        path_map = {
            f"{self.f4_path}/product/etc/device_features/munch.xml": f"{self.port_path}/product/etc/device_features/",
            f"{self.f4_path}/product/etc/displayconfig/": f"{self.port_path}/product/etc/displayconfig/",
            f"{self.f4_path}/product/etc/permissions/": f"{self.port_path}/product/etc/permissions/",
            f"{self.f4_path}/product/overlay/AospFrameworkResOverlay.apk": f"{self.port_path}/product/overlay/",
            f"{self.f4_path}/product/overlay/DevicesAndroidOverlay.apk": f"{self.port_path}/product/overlay/",
            f"{self.f4_path}/product/overlay/DevicesOverlay.apk": f"{self.port_path}/product/overlay/",
            f"{self.f4_path}/product/overlay/MiuiFrameworkResOverlay.apk": f"{self.port_path}/product/overlay/",
            f"{self.f4_path}/system_ext/apex/": f"{self.port_path}/system_ext/apex/",
        }

        for src, dest in path_map.items():
            src_path = Path(src)
            dest_path = Path(dest)

            if not src_path.exists():
                raise ValueError(f"Cannot proceed '{src_path.name}' is missing")

            if src_path.is_file():
                shutil.copy2(src_path, dest_path)
            else:
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

    def fix_props(self) -> None:
        propfx_path = Path.cwd() / "scripts" / "linefix.sh"
        subprocess.run(str(propfx_path), check=True, shell=True)

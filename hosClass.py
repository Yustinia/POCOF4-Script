from pathlib import Path
import shutil
import subprocess

F4PATH = Path.cwd() / "POCOF4"
PORTPATH = Path.cwd() / "PORT"
HOSFIX = Path.cwd() / "HOSFix"
MODSPATH = Path.cwd() / "MODS"


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


class HOSModder:
    def __init__(self) -> None:
        self.port_path = PORTPATH
        self.mods = MODSPATH

    def copy_mods(self) -> list[str]:
        directories = ["product", "system", "system_ext"]

        for base_path in [self.mods, self.port_path]:
            missing = [path for path in directories if not (base_path / path).exists()]

            # capture early missing files
            if missing:
                raise ValueError(f"Aborted: '{missing}' not found at '{base_path}'")

        processed = []
        for folder in directories:
            mod_base = self.mods / folder
            dest = self.port_path / folder

            shutil.copytree(mod_base, dest, dirs_exist_ok=True)
            processed.append(f"'{mod_base}' -> '{dest}'")

        return processed


class HOSCopyFixes:
    def __init__(self) -> None:
        self.f4_path = F4PATH
        self.port_path = PORTPATH
        self.hosfix = HOSFIX

    def _copy_dirs(self, src_dest: dict[str, Path], tar_dest: Path) -> list[str]:
        if not tar_dest.exists():
            raise ValueError(f"'{tar_dest}' does not exist")

        processed = []
        for path in src_dest.values():
            shutil.copytree(path, tar_dest / path.name, dirs_exist_ok=True)
            processed.append(f"'{path}' copied to '{tar_dest/path.name}'")

        return processed

    def fix_product(self) -> list[str]:
        prod_paths = {
            "prod_app": self.hosfix / "product" / "app",
            "prod_overlay": self.hosfix / "product" / "overlay",
            "prod_perms": self.hosfix / "product" / "permissions",
            "prod_privapp": self.hosfix / "product" / "priv-app",
        }

        return self._copy_dirs(prod_paths, self.port_path / "product")

    def fix_system(self) -> list[str]:
        system_paths = {
            "sys_app": self.hosfix / "system" / "app",
            "sys_lib": self.hosfix / "system" / "lib",
            "sys_lib64": self.hosfix / "system" / "lib64",
            "sys_privapp": self.hosfix / "system" / "priv-app",
        }

        return self._copy_dirs(system_paths, self.port_path / "system")

    def fix_vendor(self) -> list[str]:
        vendor_paths = {
            "ven_lib": self.hosfix / "vendor" / "lib",
            "ven_lib64": self.hosfix / "vendor" / "lib64",
        }

        return self._copy_dirs(vendor_paths, self.f4_path / "vendor")

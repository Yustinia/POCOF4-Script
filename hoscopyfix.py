from pathlib import Path
import shutil

F4PATH = Path.cwd() / "POCOF4"
PORTPATH = Path.cwd() / "PORT"
HOSFIX = Path.cwd() / "HOSFix"


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

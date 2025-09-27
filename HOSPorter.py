from pathlib import Path
import shutil
import subprocess


class Porter:
    DNA_DIR = Path("/data/DNA")
    HOSFIX_DIR = Path("/data/DNA/hosfix")
    SHELL_SCRIPTS = Path("/data/DNA/shell-scripts")

    def __init__(self, f4_dir, port_dir) -> None:
        self.f4_dir = f4_dir
        self.port_dir = port_dir

    @classmethod
    def download_fixes(cls):
        if not cls.HOSFIX_DIR.exists():
            try:
                subprocess.run([str(cls.SHELL_SCRIPTS / "downloader.sh")], check=True)
                return True, f"{cls.HOSFIX_DIR} has been created"
            except subprocess.CalledProcessError as e:
                return False, f"Failed: {e}"
        return True, f"{cls.HOSFIX_DIR} already exists"

    def check_dir_exists(self, poco_f4: str, port: str):
        poco_f4_dir = self.DNA_DIR / poco_f4
        port_dir = self.DNA_DIR / port

        missing_dir = []
        if not poco_f4_dir.exists():
            missing_dir.append(poco_f4_dir.name)
        if not port_dir.exists():
            missing_dir.append(port_dir.name)

        return poco_f4_dir, port_dir, missing_dir

    def start_porting(self):
        # set file directories to prepare for copy
        # f4 source folders
        f4_src = (
            Path(f"{self.f4_dir}/product/etc/device_features/munch.xml"),
            Path(f"{self.f4_dir}/product/etc/displayconfig/"),
            Path(f"{self.f4_dir}/product/etc/permissions/"),
            Path(f"{self.f4_dir}/product/overlay/AospFrameworkResOverlay.apk"),
            Path(f"{self.f4_dir}/product/overlay/DevicesAndroidOverlay.apk"),
            Path(f"{self.f4_dir}/product/overlay/DevicesOverlay.apk"),
            Path(f"{self.f4_dir}/product/overlay/MiuiFrameworkResOverlay.apk"),
            Path(f"{self.f4_dir}/system_ext/apex/"),
        )

        # fixes source folders
        fix_src = (
            Path(f"{self.HOSFIX_DIR}/product/app/"),
            Path(f"{self.HOSFIX_DIR}/product/priv-app/"),
            Path(f"{self.HOSFIX_DIR}/product/etc/permissions/"),
            Path(f"{self.HOSFIX_DIR}/product/overlay/AospFrameworkResOverlay.apk"),
            Path(f"{self.HOSFIX_DIR}/product/overlay/DevicesOverlay.apk"),
            Path(f"{self.HOSFIX_DIR}/system/system/app/"),
            Path(f"{self.HOSFIX_DIR}/system/system/priv-app/"),
            Path(f"{self.HOSFIX_DIR}/system/system/lib/"),
            Path(f"{self.HOSFIX_DIR}/system/system/lib64/"),
            Path(f"{self.HOSFIX_DIR}/vendor/lib/"),
            Path(f"{self.HOSFIX_DIR}/vendor/lib64/"),
        )

        # copy to these folders f4 -> port
        out_port = (
            Path(f"{self.port_dir}/product/etc/device_features/"),
            Path(f"{self.port_dir}/product/etc/displayconfig/"),
            Path(f"{self.port_dir}/product/etc/permissions/"),
            Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.port_dir}/system_ext/apex/"),
        )

        # copy the these folders fixes -> f4/port
        out_fixes = (
            Path(f"{self.port_dir}/product/app/"),
            Path(f"{self.port_dir}/product/priv-app/"),
            Path(f"{self.port_dir}/product/etc/permissions/"),
            Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.port_dir}/product/overlay/"),
            Path(f"{self.port_dir}/system/system/app/"),
            Path(f"{self.port_dir}/system/system/priv-app/"),
            Path(f"{self.port_dir}/system/system/"),
            Path(f"{self.port_dir}/system/system/"),
            Path(f"{self.f4_dir}/vendor/"),
            Path(f"{self.f4_dir}/vendor/"),
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
        subprocess.run([str(self.SHELL_SCRIPTS / "linefixes.sh")], check=True)

        return True


class Modder:
    DNA_DIR = Path("/data/DNA")
    HOSFIX_DIR = Path("/data/DNA/hosfix")
    SHELL_SCRIPTS = Path("/data/DNA/shell-scripts")

    def __init__(self, f4_dir, port_dir) -> None:
        self.f4_dir = f4_dir
        self.port_dir = port_dir

    def full_rw_fstab(self):
        # needs f4 vendor and delete port mi_ext/init file
        f4_fstab_file = self.DNA_DIR / self.f4_dir / "vendor" / "etc" / "fstab.qcom"
        port_mi_ext = self.DNA_DIR / self.port_dir / "mi_ext" / "etc" / "init"

        for item in port_mi_ext.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def high_rr(self):
        # needs f4 vendor and modify munch.xml
        f4_buildprop = self.DNA_DIR / self.f4_dir / "vendor" / "build.prop"
        f4_defaultprop = self.DNA_DIR / self.f4_dir / "vendor" / "default.prop"
        f4_munchxml = (
            self.DNA_DIR
            / self.port_dir
            / "product"
            / "etc"
            / "device_features"
            / "munch.xml"
        )

    def eliminate_data_app(self):
        # moves all data_apps to priv_app
        port_data_app = self.DNA_DIR / self.port_dir / "product" / "data-app"
        port_priv_app = self.DNA_DIR / self.port_dir / "product" / "priv-app"

        for item in port_data_app.iterdir():
            shutil.move(str(item), port_priv_app)

from pathlib import Path
import shutil
import subprocess

F4_SUPER_PATH = Path.cwd() / "POCOF4" / "super.img"
PORT_SUPER_PATH = Path.cwd() / "PORT" / "super.img"


class SuperUnpacker:
    def __init__(
        self,
        super_f4: Path = F4_SUPER_PATH,
        super_port: Path = PORT_SUPER_PATH,
    ) -> None:

        self.super_f4_path = super_f4
        self.super_port_path = super_port

        self.base_super_f4 = [
            "unsuper",
            str(super_f4),
            str(super_f4.parent),
            "-p",
            "product_a",
            "vendor_a",
            "system_ext_a",
            "--jobs=8",
        ]
        self.base_super_port = [
            "unsuper",
            str(super_port),
            str(super_port.parent),
            "-p",
            "product_a",
            "system_ext_a",
            "system_a",
            "mi_ext_a",
            "--jobs=8",
        ]

    def ext_super(self) -> dict[str, bool]:
        extracted = {
            "F4": False,
            "PORT": False,
        }

        if F4_SUPER_PATH.exists():
            subprocess.run(self.base_super_f4, check=True)
            extracted["F4"] = True

        if PORT_SUPER_PATH.exists():
            subprocess.run(self.base_super_port, check=True)
            extracted["PORT"] = True

        return extracted

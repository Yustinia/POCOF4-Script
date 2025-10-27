from pathlib import Path
import shutil

PORTPATH = Path.cwd() / "PORT"
MODSPATH = Path.cwd() / "MODS"


class HOSModder:
    def __init__(self) -> None:
        self.port_path = PORTPATH
        self.mods = MODSPATH

    def copy_mods(self) -> list[str]:
        directories = ["product", "system", "system_ext"]

        for base_path in [self.mods, self.port_path]:
            missing = [path for path in directories if not (base_path / path).exists()]

            if missing:
                raise ValueError(f"Aborted: '{missing}' not found at '{base_path}'")

        processed = []
        for folder in directories:
            mod_base = self.mods / folder
            dest = self.port_path / folder

            shutil.copytree(mod_base, dest, dirs_exist_ok=True)
            processed.append(f"'{mod_base}' -> '{dest}'")

        return processed

import shutil
import os
import sys


class Colors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    reset = '\033[0m'

    def success(self, msg, end="\n"):
        print(f"[{self.green}+{self.reset}] {msg}", end=end)

    def error(self, msg, end="\n"):
        print(f"[{self.red}-{self.reset}] {msg}", end=end)

    def info(self, msg, end="\n"):
        print(f"[{self.yellow}?{self.reset}] {msg}", end=end)


class Modder:
    def __init__(self):
        self.c = Colors()
        print(f"{self.c.green}--- FNAF Security Breach Mod Installer ---{self.c.reset}")
        print(f"Discord: {self.c.blue}https://discord.gg/nQfqAUw8TJ{self.c.reset}")
        print("")

        self.find_fnaf_files()

    def find_fnaf_files(self):
        # Default fnaf directory
        system = sys.platform
        game_dir = None

        if system == "win32":
            steam_directory = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Quarters\\fnaf9"
        else:
            steam_directory = "/home/user/.steam/steam/steamapps/common/Quarters/fnaf9"

        if not os.path.exists(steam_directory):
            self.c.error(f"Could not find Security Breach directory. Please enter it manually.")
            self.c.info(f"Example: {steam_directory}")
            self.c.info(f"Enter the directory: ", end="")
            game_dir = input()

            if not game_dir.endswith("fnaf9"):
                game_dir = os.path.join(game_dir, "fnaf9")

            if not os.path.exists(game_dir):
                self.c.error(f"Could not find Security Breach directory. Exiting...")
                exit()

        self.c.success(f"Found Security Breach directory at {game_dir}")
        paks_dir = os.path.join(game_dir, "Content", "Paks")

        # Now we need the directory of the mod files
        print("")
        self.c.info(f"Enter the directory of the mod files: ", end="")
        mod_dir = input()

        if not os.path.exists(mod_dir):
            self.c.error(f"Mod directory is either invalid or does not exist. Exiting...")
            exit()

        mod_files = [file for file in os.listdir(mod_dir) if file.endswith(".pak")]

        if len(mod_files) == 0:
            self.c.error(f"No mod files found. Exiting...")
            exit()

        print("Please select a mod file to install")
        for i, mod in enumerate(mod_files):
            print(f"[{self.c.blue}{i + 1}{self.c.reset}] {mod}")

        print(f"[{self.c.blue}{i + 2}{self.c.reset}] Install all mods")
        print(f"[{self.c.blue}{i + 3}{self.c.reset}] Exit")

        upper_bound = i + 3

        action = input(">> ")
        try:
            action = int(action)
        except ValueError:
            self.c.error(f"Invalid option. Exiting...")
            exit()

        if action > upper_bound or action < 1:
            self.c.error(f"Invalid option. Exiting...")
            exit()

        print("")

        if action == i + 2:
            # Install all mods
            for mod in mod_files:
                self.install_mod(mod, paks_dir, mod_dir)
        elif action == i + 3:
            # Exit
            exit()
        else:
            # Install one mod
            mod = mod_files[action - 1]
            mod = os.path.join(mod_dir, mod)
            self.install_mod(mod, paks_dir, mod_dir)

        print("Your mod has now been installed. If you run into an error while in the game, the mod is most likely outdated.")
        print("Enjoy!")

    def install_mod(self, mod, paks_dir, mod_dir):
        # Install the mod
        mod_name = os.path.basename(mod)
        mod_name_final = mod_name.replace(" ", "").replace(".pak", "_P.pak")

        self.c.info(f"Installing {mod_name}...")
        final_dest = os.path.join(paks_dir, mod_name)

        if os.path.exists(final_dest):
            self.c.info(f"{mod_name} already exists in the Paks directory.")
            exit()
        elif os.path.exists(os.path.join(paks_dir, mod_name_final)):
            self.c.info(f"{mod_name_final} already exists in the Paks directory.")
            return
        else:
            mod_path = os.path.join(mod_dir, mod)
            shutil.copy(mod_path, final_dest)

        # Rename file
        os.rename(final_dest, os.path.join(paks_dir, mod_name_final))
        print("")
        self.c.success(f"Successfully installed {mod_name_final}!")


if __name__ == "__main__":
    modder = Modder()

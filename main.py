import shutil
import os
import sys
import time
import subprocess
import colorama
import requests
import patoolib
from tqdm import tqdm


class Colors:
    def __init__(self):
        colorama.init()

    def success(self, msg, end="\n"):
        print(f"[{colorama.Fore.GREEN}+{colorama.Fore.RESET}] {msg}", end=end)

    def error(self, msg, end="\n"):
        print(f"[{colorama.Fore.RED}-{colorama.Fore.RESET}] {msg}", end=end)

    def info(self, msg, end="\n"):
        print(f"[{colorama.Fore.YELLOW}!{colorama.Fore.RESET}] {msg}", end=end)


class Patcher:
    def __init__(self):
        self.c = Colors()
        print(f"{colorama.Fore.GREEN}--- FNAF Security Breach Unverum Patcher ---{colorama.Fore.RESET}")
        print(f"Discord: {colorama.Fore.BLUE}https://discord.gg/nQfqAUw8TJ{colorama.Fore.RESET}")
        print("")

        self.main()

    def menu(self):
        print(f"[{colorama.Fore.BLUE}1{colorama.Fore.RESET}] Install + Patch Unverum")
        print(f"[{colorama.Fore.BLUE}2{colorama.Fore.RESET}] Patch Unverum")
        print(f"[{colorama.Fore.BLUE}3{colorama.Fore.RESET}] Install Unverum")
        print(f"[{colorama.Fore.BLUE}4{colorama.Fore.RESET}] Exit")

        action = input(">> ")

        try:
            action = int(action)
        except ValueError:
            self.c.error("Invalid input.")
            return self.menu()

        return action

    def main(self):
        system = sys.platform
        if not system == "win32":
            self.c.error("This program only works on Windows.")
            sys.exit(1)

        try:
            action = self.menu()

            if action == 1:
                # Install + Patch Unverum
                self.install_unverum_with_patch()
                self.c.success("Successfully installed and patched Unverum.")
            elif action == 2:
                # Patch Unverum
                self.patch_unverum()
                self.c.success("Successfully patched Unverum.")
            elif action == 3:
                # Install Unverum
                self.install_unverum()
                self.c.success("Successfully installed Unverum.")
            elif action == 4:
                # Exit
                sys.exit(0)
            else:
                self.c.error("Invalid menu option. Please select a valid option.")
        except Exception as e:
            self.c.error(f"An unexpected error occurred: {str(e)}")
            sys.exit(1)

        self.c.success("Done.")

    def install_unverum_with_patch(self):
        try:
            self.install_unverum()
            self.patch_unverum()
        except Exception as e:
            self.c.error(f"Error while installing and patching Unverum: {str(e)}")
            sys.exit(1)

    def install_unverum(self):
        try:
            self.c.info("Installing Unverum...")
            url = "https://gamebanana.com/dl/718209"
            file_name = "unverum_160.rar"

            t0 = time.time()
            resp = requests.get(url, stream=True)
            total = int(resp.headers.get("content-length", 0))
            with open(file_name, "wb") as file, tqdm(
                desc=file_name,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in resp.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            t1 = time.time()

            self.c.success(f"Downloaded Unverum in {round(t1 - t0, 2)} seconds.")

            t0 = time.time()
            self.c.info("Extracting Unverum...")
            time.sleep(1)
            try:
                self.extract_rar_archive(file_name, "unverum")
            except Exception as e:
                # Directory doesnt exist
                os.mkdir("unverum")
                self.extract_rar_archive(file_name, "unverum")
            t1 = time.time()

            self.c.success(f"Extracted Unverum in {round(t1 - t0, 2)} seconds.")
            os.remove(file_name)
            self.c.success("Done.")
        except Exception as e:
            self.c.error(f"Error while installing Unverum: {str(e)}")
            sys.exit(1)

    def extract_rar_archive(self, archive_file, target_folder):
        try:
            patoolib.extract_archive(archive_file, outdir=target_folder)
        except Exception as e:
            self.c.error(f"Error while extracting archive: {str(e)}")
            sys.exit(1)

    def patch_unverum(self):
        # Check if .NET 5.0 Runtime is installed
        try:
            if shutil.which("dotnet"):
                self.c.success(".NET 5.0 Runtime is already installed.")
                return

            self.c.info("Patching Unverum...")
            self.c.info("Download .NET 5.0 Runtime...")

            url = f"https://download.visualstudio.microsoft.com/download/pr/14ccbee3-e812-4068-af47-1631444310d1/3b8da657b99d28f1ae754294c9a8f426/dotnet-sdk-5.0.408-win-x64.exe"
            file_name = "dotnet-sdk-5.0.408-win-x64.exe"
            install_command = [file_name, "/install", "/quiet", "/norestart"]

            t1 = time.time()
            resp = requests.get(url, stream=True)
            total = int(resp.headers.get("content-length", 0))
            with open(file_name, "wb") as file, tqdm(
                desc=file_name,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in resp.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            t2 = time.time()

            self.c.success(f"Downloaded .NET 5.0 Runtime in {round(t2 - t1, 2)} seconds.")
            self.c.info("Installing .NET 5.0 Runtime...")

            t1 = time.time()
            subprocess.run(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            os.remove(file_name)

            t2 = time.time()

            self.c.success(f"Installed .NET 5.0 Runtime in {round(t2 - t1, 2)} seconds.")
        except Exception as e:
            self.c.error(f"Error while patching Unverum: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    Patcher()

    input("Press enter to exit...")

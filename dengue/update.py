#!/usr/bin/env python3
from requests import get
from json import loads
from sys import executable, exc_info
from subprocess import Popen
from os import name as os_name


def remove_old_exe():
    executable_path = executable
    print(f"Removing old in {executable_path}")

    batch_script = f"""
    @echo off
    timeout /t 5 /nobreak >nul
    del "{executable_path}" >nul 2>nul
    del "%~f0"
    """

    batch_file = executable_path + ".bat"
    try:
        with open(batch_file, "w") as file:
            file.write(batch_script)
    except:
        print(f"Failed to write batch file {batch_file}")
        print(exc_info()[1])
    try:
        Popen([batch_file])
    except:
        print(f"Failed to execute batch file {batch_file}")
        print(exc_info()[1])


def check_version(version):
    url = f"https://api.github.com/repos/ieremies/dengue/releases/latest"
    response = get(url)

    if response.status_code != 200:
        print("Falha em conferir atualização.")
        return None

    release_info = loads(response.text)

    latest_version = release_info["tag_name"]

    if latest_version != version:
        print(f"Nova versão disponível: {latest_version}")

        if os_name == "nt":  # windows
            remove_old_exe()

        return latest_version

    print("Seu aplicativo está atualizado.")
    return None

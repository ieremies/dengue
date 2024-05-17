#!/usr/bin/env python3
import requests
import json
import sys
import subprocess
import os


def remove_old_exe():
    executable_path = sys.executable

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
        subprocess.Popen([batch_file])
    except:
        ...


def check_version(version):
    url = f"https://api.github.com/repos/ieremies/dengue/releases/latest"
    response = requests.get(url)

    if response.status_code != 200:
        print("Falha em conferir atualização.")
        return None

    release_info = json.loads(response.text)

    latest_version = release_info["tag_name"]

    if latest_version != version:
        print(f"Nova versão disponível: {latest_version}")

        if os.name == "nt":  # windows
            remove_old_exe()

        return latest_version

    print("Seu aplicativo está atualizado.")
    return None

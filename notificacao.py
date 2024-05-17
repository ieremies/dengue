#!/usr/bin/env python3
from flask import Flask, request, render_template, send_file
from dengue.parse import parse
from dengue.write import writer
from dengue.update import check_version
from os import getpid
from psutil import process_iter
from webbrowser import open

app = Flask(__name__, template_folder="templates")

UPDATE_URL = "https://github.com/ieremies/dengue/releases/download/"
VERSION = "v1.1.6"
APP_NAME = "notificacao.exe"


def kill_others():
    current_pid = getpid()
    for process in process_iter(["pid", "name"]):
        if (process.info["name"].lower().endswith(APP_NAME.lower())) and (
            process.info["pid"] != current_pid
        ):
            print(
                f"Terminating process {process.info['name']} with PID {process.info['pid']}"
            )
            process.terminate()


@app.route("/", methods=["GET", "POST"])
def index():

    update = check_version(VERSION)
    if not update is None:
        return render_template(
            "update.html",
            download_url=UPDATE_URL + f"{update}/{APP_NAME}",
        )

    if request.method == "POST":
        text = request.form["text"]
        f = writer(parse(text)).save()
        return send_file(f, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    kill_others()
    open("http://127.0.0.1:5000")
    print(f"Running version {VERSION}...")
    app.run()

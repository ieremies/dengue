#!/usr/bin/env python3
from flask import (
    Flask,
    request,
    render_template,
    send_file,
    redirect,
    url_for,
    after_this_request,
)
from dengue.parse import parse, usuario
from dengue.write import writer
from dengue.update import check_version, kill_others
from webbrowser import open

app = Flask(__name__, template_folder="templates")

UPDATE_URL = "https://github.com/ieremies/dengue/releases/download/"
VERSION = "v1.1.7"
APP_NAME = "notificacao.exe"


@app.route("/form", methods=["POST"])
def submit_form():
    f = writer(usuario(**request.form)).save()
    return send_file(f, as_attachment=True)


@app.route("/form", methods=["GET"])
def form():
    user = request.args
    return render_template("form.html", usuario=user)


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
        d = parse(text).dict()
        return redirect(url_for("form", **d))

    return render_template("index.html")


if __name__ == "__main__":
    kill_others()
    open("http://127.0.0.1:5000")
    print(f"Running version {VERSION}...")
    app.run(debug=True)

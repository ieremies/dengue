#!/usr/bin/env python3
from flask import Flask, request, render_template, send_file
from dengue.parse import parse
from dengue.write import writer

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        f = writer(parse(text)).save()
        return send_file(f, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    # open url
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000")
    app.run()

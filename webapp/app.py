from flask import Flask, redirect, render_template, url_for

import cache
from dicom.wlmscpfs import clear_file_wl, write_file_wl
from util import generate_worklist

app = Flask(__name__)


@app.route("/")
def index():
    if cache.exists():
        worklists = cache.get_data()
    else:
        worklists = generate_worklist(50)
        cache.write_data(worklists)
        write_file_wl(worklists)

    return render_template("index.html", worklists=worklists)


@app.route("/reset")
def reset():
    clear_file_wl()
    cache.invalidate()
    return redirect(url_for("index"))


@app.errorhandler(Exception)
def error_handler(e):
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

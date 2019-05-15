from decouple import config
from flask import Flask, redirect, render_template, url_for

import cache
from dicom.wlmscpfs import remove_all_worklist, write_file_worklist
from util import generate_worklist

app = Flask(__name__)


@app.route("/")
def index():
    if cache.exists():
        worklists = cache.get_data()
    else:
        worklists = generate_worklist(50)
        cache.write_data(worklists)
        write_file_worklist(worklists)

    context = {
        "worklist_address": config("WORKLIST_ADDRESS"),
        "worklist_port": config("WORKLIST_PORT"),
        "calling_ae_title": config("CALLING_AE_TITLE"),
        "called_ae_title": config("CALLED_AE_TITLE"),
        "worklists": worklists,
    }
    return render_template("index.html", **context)


@app.route("/reset")
def reset():
    remove_all_worklist()
    cache.invalidate()
    return redirect(url_for("index"))


@app.errorhandler(Exception)
def error_handler(e):
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

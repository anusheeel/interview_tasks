from flask import Flask, render_template
import importlib
import os

app = Flask(__name__)


@app.route("/grid-power-analysis/", methods=["GET"])
def grid_power_analysis():
    script = importlib.import_module("test_sim")
    results = script.run()
    return render_template("results.html", results=results)


if __name__ == "__main__":
    app.run()

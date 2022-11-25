from flask import Flask, render_template
app = Flask(__name__)  # name est le nom du programme


@app.route("/")
def root():
    return render_template("root")

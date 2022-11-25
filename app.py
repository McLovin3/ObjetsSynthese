from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from MatriceLED import write

import packages.Freenove_DHT11 as DHT
app = Flask(__name__)
app.config['SECRET_KEY'] = "McLovin"


class MessageForm(FlaskForm):
    message = StringField("Message", [DataRequired()])
    submit = SubmitField("Envoyer le message", render_kw={
                         "class": "btn btn-secondary"})


temperature = 0
humidity = 0


def get_sensor_info():
    global temperature, humidity
    try:
        dht = DHT.DHT(4)

        verification = dht.readDHT11()
        if (verification is dht.DHTLIB_OK):
            temperature = dht.temperature
            humidity = dht.humidity
    except:
        temperature = humidity = "No sensor"


@ app.route("/", methods=["GET", "POST"])
def root():
    get_sensor_info()
    form = MessageForm()
    if form.validate_on_submit():
        message = form.message.data
        form.message.data = ""
        write(message)

    return render_template("root.html", form=form, temperature=temperature, humidity=humidity)

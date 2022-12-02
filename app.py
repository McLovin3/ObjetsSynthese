from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from gpiozero import DistanceSensor
from datetime import datetime
from MatriceLED import write
import cv2
import packages.Freenove_DHT11 as DHT

app = Flask(__name__)
app.config['SECRET_KEY'] = "McLovin"


class MessageForm(FlaskForm):
    message = StringField("Message", [DataRequired()])
    submit = SubmitField("Envoyer le message", render_kw={
                         "class": "btn btn-secondary"})


distance_sensor = DistanceSensor(echo=19, trigger=26)
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


image_path = ""


@app.route("/photo", methods=["POST"])
def photo():
    global image_path
    capture = cv2.VideoCapture(0)
    _, img = capture.read()
    image_path = "./static/" + datetime.now().strftime("%s") + ".jpg"
    cv2.imwrite(image_path, img)
    return redirect("/")


@ app.route("/", methods=["GET", "POST"])
def root():
    # If method is get
    get_sensor_info()

    form = MessageForm()
    if form.validate_on_submit():
        message = form.message.data
        form.message.data = ""
        write(message)

    return render_template("root.html",
                           form=form,
                           temperature=temperature,
                           humidity=humidity,
                           image_path=image_path,
                           time=str(datetime.now()).split(".")[0],
                           distance=int(distance_sensor.distance * 100))

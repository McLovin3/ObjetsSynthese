from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from model import predict_image
from gpiozero import DistanceSensor
from datetime import datetime
from MatriceLED import write
import sms_service
import cv2
import Freenove_DHT11 as DHT

app = Flask(__name__)
app.config['SECRET_KEY'] = "McLovin"


class MessageForm(FlaskForm):
    message = StringField("Message", [DataRequired()])
    submit = SubmitField("Envoyer le message", render_kw={
                         "class": "btn btn-secondary"})


distance_sensor = DistanceSensor(echo=19, trigger=26)
temperature = 0
humidity = 0
image_path = ""
sms_time = ""
prediction = "Aucune prédiction"


def send_sms(reason):
    global sms_time

    sms_time = str(datetime.now()).split(".")[0]
    sms_service.send_sms(reason, sms_time)


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
    global sms_time

    form = MessageForm()

    # Post
    if request.method == "POST" and form.validate_on_submit():
        message = form.message.data
        form.message.data = ""
        write(message)

    # S'occupe des capteurs
    get_sensor_info()
    distance = distance_sensor.distance
    if distance < 0.05:
        send_sms("Objet trop près")

    return render_template("index.html",
                           form=form,
                           temperature=temperature,
                           humidity=humidity,
                           sms_time=sms_time,
                           image_path=image_path,
                           prediction=prediction,
                           time=str(datetime.now()).split(".")[0],
                           distance=int(distance * 100))


@app.route("/photo", methods=["POST"])
def photo():
    global image_path, prediction, sms_time

    # Créer l'image
    capture = cv2.VideoCapture(0)
    _, img = capture.read()
    image_path = "./static/" + datetime.now().strftime("%s") + ".jpg"
    cv2.imwrite(image_path, img)

    # Prédiction
    prediction = predict_image(image_path).prediction
    if prediction == "Unmasked":
        send_sms("Visage non masqué")

    return redirect("/")

from flask import Flask, render_template
import packages.Freenove_DHT11 as DHT
app = Flask(__name__)

try:
    dht = DHT.DHT(4)

    verification = dht.readDHT11()
    if (verification is dht.DHTLIB_OK):
        temperature = dht.temperature
        humidity = dht.humidity
except:
    temperature = humidity = "No sensor"


@app.route("/")
def root():
    return render_template("root.html", humidity=humidity, temperature=temperature)

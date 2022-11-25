# le fichier Freenove_DHT11 est fourni sur Moodle
import packages.Freenove_DHT11 as DHT
dht = DHT.DHT(4)  # ATTENTION: vérifier ce que vous avez à la ligne 26 du

verification = dht.readDHT11()
if (verification is dht.DHTLIB_OK):
    print(dht.humidity, dht.temperature)
